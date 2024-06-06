frappe.listview_settings['Employee Checkin'] = {
    onload: function(listview) {
        listview.page.add_menu_item(__('Update Checkins'), function() {
            frappe.call({
                method: "logistics_management.api.process_checkin",
                callback: function(response) {
                    if (response.message) {
                        frappe.msgprint(__('Checkins updated successfully'));
                    }
                }
            });
        });
    }
};
