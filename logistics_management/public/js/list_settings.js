frappe.listview_settings['Employee Checkin'] = {
    onload: function (listview) {
        console.log("hello")
        listview.page.add_menu_item(__('Update Checkinsss'), function () {
            frappe.call({
                method: "logistics_management.api.essl_attendance_log",
                callback: function (response) {
                    if (response.message) {
                        frappe.msgprint(__('Checkins updated successfully'));
                    }
                }
            });
        });
    }
};
