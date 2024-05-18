
frappe.ui.form.on("Document Table", {

    download: function (frm, cdt, cdn) {
        console.log("helloe")
        let row = locals[cdt][cdn]
        let url = row.attach_file

        fetch(url)
            .then(response => response.blob())
            .then(blob => {
                const link = document.createElement('a')
                link.href = URL.createObjectURL(blob)

                const fileName = url.substring(url.lastIndexOf('/') + 1);
                link.download = fileName;
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
            })
            .catch(error => {
                frappe.msgprint("Error Downloading File", error)
            })

    },
    expiry_date: function (frm, cdt, cdn) {

        console.log(locals[cdt][cdn])
        let row = locals[cdt][cdn]
        let expiry_date = row.expiry_date

        frappe.call({
            method: "logistics_management.api.claculate_expiry",
            args: {
                expiry_date: expiry_date
            },
            callback: function (r) {

                console.log(r.message)

                frappe.model.set_value(cdt, cdn, "time_to_expire", r.message)
            }
        })
    }
})