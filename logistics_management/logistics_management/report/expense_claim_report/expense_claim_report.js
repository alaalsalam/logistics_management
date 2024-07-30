// Copyright (c) 2024, Upscape Technologies and contributors
// For license information, please see license.txt

frappe.query_reports["Expense Claim Report"] = {
	"filters": [

		{
			fieldname: "status",
			label: __("Status"),
			fieldtype: "Select",
			options: "\nPaid\nUnpaid",
		},
		{
			fieldname: "approval_status",
			label: __("Approval Status"),
			fieldtype: "Select",
			options: "\nApproved\nRejected\nDraft",
		},
		{
			fieldname: "employee",
			label: __("Employee"),
			fieldtype: "Link",
			options: "Employee"
		},
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date"
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Date"
		},
		{
			fieldname: "expense_claim_type",
			label: __("Expense Claim Type"),
			fieldtype: "Link",
			options: "Expense Claim Type"
		},
		{
			fieldname: "branch",
			label: __("Branch"),
			fieldtype: "Link",
			options: "Branch"
		},
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			reqd: 1
		}

	]
};
