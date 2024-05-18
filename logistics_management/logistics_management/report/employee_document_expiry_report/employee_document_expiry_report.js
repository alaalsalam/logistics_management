// Copyright (c) 2024, Upscape Technologies and contributors
// For license information, please see license.txt

frappe.query_reports["Employee Document Expiry Report"] = {
	"filters": [

		{
			"fieldname": "employee",
			"label": __("Employee"),
			"fieldtype": "Link",
			"options": "Employee"
		},
		{
			"fieldname": "document_type",
			"label": __("Document Type"),
			"fieldtype": "Link",
			"options": "Document Type"

		},
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date"
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date"
		}

	]
};
