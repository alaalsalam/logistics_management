import frappe
from datetime import datetime

def notify():
    employee = frappe.db.get_list('Employee',fields=['name','personal_email','company_email','employee_name'])

    for i in employee:
        email = i.personal_email or i.company_email
        check_document_expiry(i.name,email)

def check_document_expiry(employee,email):
    
    documents = frappe.db.get_all(
        'Document Table',
        filters = {'parent':employee,'parenttype':'Employee'},
        fields = ['name','document_type','expiry_date','attach_file','time_to_expire']
    )

    for document in documents:
        if document.expiry_date:
            selected_date_obj = document.expiry_date
            days_left = document.time_to_expire
            current_date =  datetime.strptime(frappe.utils.nowdate(),'%Y-%m-%d').date() 
            seven_days = frappe.utils.add_days(current_date, 7)
            one_month = frappe.utils.add_months(current_date, 1)

            if selected_date_obj == seven_days:
                send_email_notification(employee,email,seven_days,days_left,document.document_type,document.attach_file)
            elif selected_date_obj == one_month:
                send_email_notification(employee,email,one_month,days_left,document.document_type,document.attach_file)
            elif selected_date_obj == current_date:
                send_email_notification(employee,email,current_date,days_left,document.document_type,document.attach_file)
            
def send_email_notification(employee, email, days, days_left, document_type, attachment):
    recipients = [email, 'fadilsiddique@gmail.com']
    message_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document Expiry Notification</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            color: #333333;
        }}
        .container {{
            padding: 20px;
            max-width: 600px;
            margin: auto;
            background: #f8f8f8;
            border: 1px solid #e7e7e7;
        }}
        .header {{
            background-color: #004a99;
            color: #ffffff;
            padding: 10px;
            text-align: center;
        }}
        .content {{
            padding: 20px;
            text-align: left;
        }}
        .footer {{
            font-size: 12px;
            color: #777777;
            text-align: center;
            padding: 20px;
        }}
    </style>
    </head>
    <body>
    <div class="container">
        <div class="header">
            <h2>{document_type} Expiry Reminder</h2>
        </div>
        <div class="content">
            <p>Dear {employee},</p>
            <p>This is a friendly reminder that your document <strong>{document_type}</strong> is set to expire on <strong>{days_left} days</strong>. We recommend reviewing and renewing it as soon as possible to ensure continuous service.</p>
            <p>If you have any questions or require assistance, please do not hesitate to contact our support team.</p>
            <p>Thank you for your attention to this matter.</p>
            <p>Best regards,</p>
            <p><strong>KAAF Logistics</strong></p>
        </div>
        <div class="footer">
            This is an automated message. Please do not reply directly to this email.
        </div>
    </div>
    </body>
    </html>
    """

    frappe.sendmail(
        recipients=recipients,
        subject=f"{document_type} Expiry In {days_left}",
        message=message_html,
        attachments=[{'file_url': attachment}]
    )

    
def notify_queue():
    frappe.enqueue(
        notify,
        queue="default"
    )