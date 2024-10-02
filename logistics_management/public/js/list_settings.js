frappe.listview_settings['Employee Checkin'] = {
    onload: function (listview) {
        console.log("Listview loaded for Employee Checkin");

        if (listview.page) {
            // Button to update checkins
            listview.page.add_menu_item(__('Update Checkin'), function () {
                console.log("Update Checkin button clicked");

                frappe.show_progress(__('Updating Checkins'), 0, 100, 'Please wait...');

                frappe.call({
                    method: "logistics_management.api.essl_attendance_log",
                    callback: function (response) {
                        if (response.message) {
                            frappe.show_progress(__('Updating Checkins'), 100, 100, 'Completed');
                            frappe.msgprint(__('Checkins updated successfully'));

                            setTimeout(() => {
                                frappe.hide_progress();
                            }, 1000);
                        } else {
                            frappe.hide_progress();
                            frappe.msgprint(__('Failed to update checkins'));
                        }
                    },
                    error: function (error) {
                        frappe.hide_progress();
                        frappe.msgprint(__('Error updating checkins'));
                        console.error("Error during update:", error);
                    }
                });
            });

            // Button to fetch missing employee data (branch and company)
            listview.page.add_menu_item(__('Fetch Missing Employee Data'), function () {
                console.log("Fetching missing employee data...");

                // Enqueue a background job for fetching missing data
                frappe.call({
                    method: "logistics_management.api.fetch_missing_employee_data",
                    args: {
                        doctype: 'Employee Checkin'  // You can pass any necessary arguments here
                    },
                    callback: function (response) {
                        frappe.msgprint(__('Missing employee data fetch initiated successfully.'));
                    },
                    error: function (error) {
                        frappe.msgprint(__('Error initiating missing data fetch'));
                        console.error("Error initiating fetch:", error);
                    }
                });
            });
        } else {
            console.error("Page object not found, cannot add menu item");
        }
    }
};
