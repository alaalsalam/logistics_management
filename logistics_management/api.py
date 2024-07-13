import frappe
import json
import ast
from frappe.utils import today, date_diff
from datetime import datetime,date
from dateutil.relativedelta import relativedelta
import requests
import pytz
from hrms.hr.doctype.employee_checkin.employee_checkin import add_log_based_on_employee_field


def get_utc_time():
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

def update_last_checkin_sync(shift):
    doc= frappe.get_doc("Shift Type", shift)
    if doc:
        saudi_tz = pytz.timezone('Asia/Riyadh')
        saudi_time = datetime.now(saudi_tz)
        frappe.db.set_value("Shift Type", doc, "last_sync_of_checkin", saudi_time.strftime("%Y-%m-%d %H:%M:%S"))
@frappe.whitelist()
def claculate_expiry(expiry_date):
    try:
        if not expiry_date:
            return "N/A"

        # Check if expiry_date is already a date object
        if not isinstance(expiry_date, date):
            # If not, convert from string to date
            expiry_date = datetime.strptime(expiry_date, "%Y-%m-%d").date()

        current_date = datetime.today().date()
        delta = relativedelta(expiry_date, current_date)

        if delta.years > 0:
            return f"{delta.years} year(s), {delta.months} month(s)"
        elif delta.months > 0:
            return f"{delta.months} month(s), {delta.days} day(s)"
        else:
            return f"{delta.days} day(s)"
    except Exception as e:
        print(f"Error calculating expiry: {e}")
        return "Error"

@frappe.whitelist()
def process_checkin(Logdata):
    # data = [
    #     {
    #         "EmployeeCode": "KF1018",
    #         "LogDate": "2024-06-04 9:43:34",
    #         "SerialNumber": "CRJP232260403",
    #         "PunchDirection": "IN",
    #         "Temperature": 0.0,
    #         "TemperatureState": "Not Measured"
    #     },
    #     {
    #         "EmployeeCode": "KF1017",
    #         "LogDate": "2024-06-04 10:00:34",
    #         "SerialNumber": "CRJP232260403",
    #         "PunchDirection": "IN",
    #         "Temperature": 0.0,
    #         "TemperatureState": "Not Measured"
    #     },
    #     {
    #         "EmployeeCode": "KF1018",
    #         "LogDate": "2024-06-04 12:43:34",
    #         "SerialNumber": "CRJP232260403",
    #         "PunchDirection": "OUT",
    #         "Temperature": 0.0,
    #         "TemperatureState": "Not Measured"
    #     },
    #     {
    #         "EmployeeCode": "KF1017",
    #         "LogDate": "2024-06-04 01:00:34",
    #         "SerialNumber": "CRJP232260403",
    #         "PunchDirection": "OUT",
    #         "Temperature": 0.0,
    #         "TemperatureState": "Not Measured"
    #     },
        
    # ]

    for index,item in enumerate(Logdata):
        employee_code = item['EmployeeCode']
        timestamp_str = item['LogDate']
        device_id = item['SerialNumber']
        # log_type = item['PunchDirection']
        timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')

        employee = frappe.db.get_value('Employee', {'attendance_device_id': employee_code}, 'name')
        shift = frappe.db.get_value('Employee', {'attendance_device_id': employee_code}, 'default_shift')


        if not employee:
            frappe.log_error(f"Employee with attendance_device_id {employee_code} not found.", 'Checkin Error')
            continue

        checkin_exists = frappe.db.exists('Employee Checkin', {
            'employee': employee,
            'time': timestamp
        })

        if not checkin_exists:
            check_in = frappe.new_doc('Employee Checkin')
            check_in.employee = employee
            check_in.time = timestamp
            check_in.device_id = device_id
            # check_in.log_type = log_type
            check_in.insert()

        if index == len(Logdata)-1:
            update_last_checkin_sync(shift)

@frappe.whitelist()
def essl_attendance_log():

    api_key = frappe.db.get_single_value("Smart Office Settings", "api_key")
    url = frappe.db.get_single_value("Smart Office Settings", "url")
    port = frappe.db.get_single_value("Smart Office Settings", "port")

    from_date = today()
    to_date = today()

    essl_url = f"{url}:{port}/api/v2/webapi/getdevicelogs?APIKey={api_key}&fromdate={from_date}&todate={to_date}"

    payload = {}
    headers = {}

    response = requests.request("GET", url=essl_url, headers=headers, data=payload)
    process_checkin(Logdata=response.json())
    return response.json()

@frappe.whitelist()

def claculate_expiry(expiry_date):
    try:
        if not expiry_date:
            return "N/A"

        # Check if expiry_date is already a date object
        if not isinstance(expiry_date, date):
            # If not, convert from string to date
            expiry_date = datetime.strptime(expiry_date, "%Y-%m-%d").date()

        current_date = datetime.today().date()
        delta = relativedelta(expiry_date, current_date)

        if delta.years > 0:
            return f"{delta.years} year(s), {delta.months} month(s)"
        elif delta.months > 0:
            return f"{delta.months} month(s), {delta.days} day(s)"
        else:
            return f"{delta.days} day(s)"
    except Exception as e:
        print(f"Error calculating expiry: {e}")
        return "Error"

frappe.whitelist()
def update_expiry_for_employee():
    try:
        # Fetch all employees
        employees = frappe.get_all('Employee', fields=['name'])

        for employee in employees:
            employee_doc = frappe.get_doc('Employee', employee.name)
            for child in employee_doc.get('custom_document_table'):
                expiry_date = child.get('expiry_date')
                if expiry_date:
                    expiry_status = claculate_expiry(expiry_date)
                    child.db_set('time_to_expire', expiry_status)

        frappe.db.commit()
    except Exception as e:
        frappe.log_error(f"Error updating expiry for employee child table: {e}", "Update Expiry Cron Job")


@frappe.whitelist()

def review_email_notification(expense_claim,employee):

    expense_claim_doc = frappe.get_doc('Expense Claim', expense_claim)
    employee_doc = frappe.get_doc('Employee', employee)
    email = employee_doc.company_email or employee_doc.personal_email

    if not email:
        frappe.throw("Employee does not have an email address.")

    email_subject = "New Expense Claim Assigned"
    email_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <html>
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            .container {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333333;
            }}
            .header {{
                background-color: #004a99;
                color: white;
                padding: 10px;
                text-align: center;
            }}
            .content {{
                padding: 20px;
            }}
            .footer {{
                background-color: #f1f1f1;
                color: #777777;
                padding: 10px;
                text-align: center;
            }}
            .button {{
                background-color: #004a99;
                color: white;
                padding: 10px 20px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                border-radius: 5px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Expense Claim Assigned</h1>
            </div>
            <div class="content">
                <p>Dear {employee_doc.employee_name},</p>
                <p>You have been assigned a new expense claim.</p>
                <p>Please review and take the necessary action:</p>
                <a href="/app/expense-claim/{expense_claim}" class="button">View Expense Claim</a>
            </div>
            <div class="footer">
                <p>Thank you,</p>
                <p>KAAF Logistics</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Send the email
    frappe.sendmail(
        recipients=email,
        subject=email_subject,
        message=email_content
    )

    # if comment:
    #     # doc = frappe.get_doc('Expense Claim', expense_claim)
    #     expense_claim_doc.add_comment('Comment', comment)
    #     expense_claim_doc.save()
    #     frappe.db.commit()

        # print("done")
    return "Email Sent"



