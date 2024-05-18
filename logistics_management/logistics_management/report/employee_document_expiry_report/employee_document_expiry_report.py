# Copyright (c) 2024, Upscape Technologies and contributors
# For license information, please see license.txt

from frappe import _
import frappe
from datetime import datetime,date
from dateutil.relativedelta import relativedelta

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)

    return columns, data

def get_columns():
    return [
        _("Employee") + ":Link/Employee:120",
        _("Document Type") + "::150",
        _("Expiry Date") + ":Date:120",
        _("Unique ID") + ":Data:120",
        _("Time to Expire") + ":Data:200"
    ]

def get_data(filters):
    conditions = get_conditions(filters)
    # Include a join with the tabEmployee table to ensure that the document entries are linked to an existing employee.
    query = f"""
        SELECT
            dt.parent as employee, dt.document_type, dt.expiry_date, dt.uid as unique_id, dt.time_to_expire
        FROM
            `tabDocument Table` dt
        JOIN
            `tabEmployee` e ON dt.parent = e.name
        WHERE
            dt.docstatus < 2
            {conditions}
    """
    data = frappe.db.sql(query, filters, as_dict=1)

    return data

def get_conditions(filters):
    conditions = ""
    if filters.get("employee"):
        conditions += " AND parent = %(employee)s"
    if filters.get("document_type"):
        conditions += " AND document_type = %(document_type)s"
    if filters.get("from_date"):
        conditions += " AND expiry_date >= %(from_date)s"
    if filters.get("to_date"):
        conditions += " AND expiry_date <= %(to_date)s"

    return conditions