

frappe.ui.form.on('Notification Log', {
    refresh: function(frm) {
        if (frm.doc.status === 'Open') {
            showDesktopNotification(frm.doc.subject, frm.doc.message);
        }
    }
});

function showDesktopNotification(title, message) {
    // Check if the browser supports notifications
    if ("Notification" in window) {
        // Check if notification permissions have already been granted
        if (Notification.permission === "granted") {
            // Show the notification
            new Notification(title, {
                body: message,
                icon: '/assets/custom_app/images/notification_icon.png' // Change the path to your notification icon
            });
        } else if (Notification.permission !== "denied") {
            // Request permission from the user
            Notification.requestPermission().then(function (permission) {
                // If the user grants permission, show the notification
                if (permission === "granted") {
                    new Notification(title, {
                        body: message,
                        icon: '/assets/custom_app/images/notification_icon.png'
                    });
                }
            });
        }
    }
}
