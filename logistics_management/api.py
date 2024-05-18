import frappe
import json
import ast
from frappe.utils import today, date_diff
from datetime import datetime,date
from dateutil.relativedelta import relativedelta
import http.client
import xml.etree.ElementTree as ET


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

def essl_attendance_log():
    conn = http.client.HTTPSConnection("www.esslcloud.com")

