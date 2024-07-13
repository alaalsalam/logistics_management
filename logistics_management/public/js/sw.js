
self.addEventListener('notificationclick', event => {
    const notification = event.notification;
    clients.openWindow(notification.data.url)
    notification.close();
})

self.addEventListener('notificationclose', event => {
    console.log('closed' + event);
});