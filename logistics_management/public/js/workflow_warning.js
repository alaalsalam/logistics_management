frappe.ui.form.on('Expense Claim', {

    before_workflow_action: async function (frm) {
        let promise = new Promise((resolve, reject) => {
            frappe.dom.unfreeze()
            frappe.confirm(
                "Are you sure you want to continue?",
                () =>
                    resolve(),
                () =>
                    reject()
            )
        })

        await promise.catch(() => frappe.throw());
    },


    before_save: function (frm) {

        console.log(frm.doc.custom_review_employees)

        let reviewrs = frm.doc.custom_review_employees

        reviewrs.forEach(function (reviewer) {

            console.log(reviewer.comment)

            if (reviewer.email_sent == 0) {

                console.log("hello")

                frappe.call({
                    method: "logistics_management.api.review_email_notification",
                    args: {
                        doctype: frm.doc.doctype,
                        docname: frm.doc.name,
                        employee: reviewer.review_employee,
                        // comment: reviewer.comment ? reviewer.comment : ""
                    },
                    callback: function (r) {

                        if (reviewer.comment) {

                            frappe.call({
                                method: 'frappe.desk.form.utils.add_comment',
                                args: {
                                    reference_doctype: frm.doc.doctype,
                                    reference_name: frm.doc.name,
                                    content: reviewer.comment,
                                    comment_email: frappe.session.user,
                                    comment_by: frappe.session.user_fullname
                                },
                                callback: function (e) {
                                    frappe.model.set_value(reviewer.doctype, reviewer.name, "email_sent", 1);
                                    console.log("worked")

                                }
                            },
                            )

                        }
                    }
                });

            }


        })
    },
    after_workflow_action: function (frm) {
        let approval_status = frm.doc.approval_status
        let reason = frm.doc.custom_reason

        console.log(approval_status, "BS")

        if (approval_status === "Rejected") {
            console.log(approval_status)
            if (reason) {
                console.log(reason)

                frappe.call({
                    method: "logistics_management.api.rejection_email",
                    args: {
                        doctype: frm.doc.doctype,
                        docname: frm.doc.name,
                        status: approval_status,
                        employee: frm.doc.employee,
                        reason: reason
                    },
                    callback: function (r) {
                        console.log("helo");
                    }
                })

            }
        }
    }

});

frappe.ui.form.on('Employee Reviewer', {
    approval: function (frm, cdt, cdn) {
        let row = locals[cdt][cdn]

        console.log(row, "row")

        if (row.approval) {

            frappe.call({
                method: "logistics_management.api.status_email_notification",
                args: {
                    doctype: frm.doc.doctype,
                    docname: frm.doc.name,
                    employee: row.review_employee,
                    status: row.approval
                },
                callback: function (r) {
                    console.log("helo");
                }
            })
        }


    }

})
