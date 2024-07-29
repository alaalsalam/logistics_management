import frappe
from frappe.utils import flt

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
		{"label": "Date", "fieldname": "date", "fieldtype": "Date", "width": 120},
        {"label": "Employee Name", "fieldname": "employee_name", "fieldtype": "Data", "width": 150},
        {"label": "Branch", "fieldname": "branch", "fieldtype": "Data", "width": 150},
        {"label": "Approval Status", "fieldname": "approval_status", "fieldtype": "Data", "width": 120},
		{"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 120},
        {"label": "Total Sanctioned Amount", "fieldname": "total_sanctioned_amount", "fieldtype": "Currency", "width": 180},
        {"label": "Total Claimed Amount", "fieldname": "total_claimed_amount", "fieldtype": "Currency", "width": 180},
        {"label": "Total Amount Reimbursed", "fieldname": "total_amount_reimbursed", "fieldtype": "Currency", "width": 180},
		# {"label": "Project", "fieldname": "project", "fieldtype": "Data", "width": 120},
        
    ]

def get_data(filters):
    conditions, values = get_conditions(filters)
    
    query = """
        SELECT
			ec.posting_date AS date,
            e.employee_name,
            e.branch,
            ec.approval_status,
            ec.status,
            ec.total_sanctioned_amount,
            ec.total_claimed_amount,
            ec.total_amount_reimbursed,
			ec.project
            
        FROM 
            `tabExpense Claim` ec
        JOIN 
            `tabEmployee` e ON ec.employee = e.name
        WHERE 
            ec.docstatus = 1
            {conditions}
        ORDER BY 
            ec.posting_date DESC
    """.format(conditions=conditions)
    
    data = frappe.db.sql(query, values, as_dict=1)
    return data

def get_conditions(filters):
    conditions = []
    values = {}

    if filters.get("status"):
        conditions.append("AND ec.status = %(status)s")
        values["status"] = filters.get("status")
    if filters.get("approval_status"):
        conditions.append("AND ec.approval_status = %(approval_status)s")
        values["approval_status"] = filters.get("approval_status")
    if filters.get("employee"):
        conditions.append("AND ec.employee = %(employee)s")
        values["employee"] = filters.get("employee")
    if filters.get("from_date") and filters.get("to_date"):
        conditions.append("AND ec.posting_date BETWEEN %(from_date)s AND %(to_date)s")
        values["from_date"] = filters.get("from_date")
        values["to_date"] = filters.get("to_date")
    if filters.get("expense_claim_type"):
        conditions.append("AND EXISTS (SELECT 1 FROM `tabExpense Claim Detail` ecd WHERE ecd.parent = ec.name AND ecd.expense_type = %(expense_claim_type)s)")
        values["expense_claim_type"] = filters.get("expense_claim_type")
    if filters.get("branch"):
        conditions.append("AND e.branch = %(branch)s")
        values["branch"] = filters.get("branch")
    if filters.get("company"):
        conditions.append("AND e.company = %(company)s")
        values["company"] = filters.get("company")

    return " ".join(conditions), values
