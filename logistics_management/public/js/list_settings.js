frappe.listview_settings['Employee Checkin'] = {
    onload: function (listview) {
        listview.page.add_menu_item(__('Update Checkinss'), function () {
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
