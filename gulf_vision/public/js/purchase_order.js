frappe.ui.form.on('Purchase Order', {
    validate: function (frm) {
        frm.set_value("documnet_currently_update_by", frappe.session.user)
    },
    onload: function (frm) {
        if (!frm.is_new() && frappe.session.user != 'Administrator' && frappe.session.user != frm.doc.approval_stage) {
            $("button[data-label='Submit']").hide();
            $(".inner-group-button[data-label='Actions'] > button").hide();
        }
        if (!frm.is_new() && frappe.session.user != 'Administrator' && frappe.session.user == frm.doc.approval_stage) {
            $("button[data-label='Submit']").hide();
        }

        if (frm.doc.rejected == 1 && !frm.is_new() && frappe.session.user != "Administrator" && frappe.session.user == frm.doc.approval_stage) {
            $("button[data-label='Submit']").hide();
            $(".inner-group-button[data-label='Actions'] > button").hide();

        }
        if (frm.doc.rejected == 1 && !frm.is_new() && frappe.session.user != "Administrator" && frappe.session.user != frm.doc.approval_stage) {
            $("button[data-label='Submit']").hide();
            $(".inner-group-button[data-label='Actions'] > button").hide();

        }

        if (frm.doc.workflow_state) {
            if (frm.doc.workflow_state == "Rejected" && frm.doc.rejected == 1) {
                frm.set_intro(`Rejected By ${frm.doc.approval_stage}`, 'red')
            }

            if (frm.doc.workflow_state == "Approved") {
                frm.set_intro(`Approved By ${frm.doc.document_currently_updated_by}`, 'green')

            }
        }

    },


    refresh: function (frm) {
        frm.add_custom_button(__('Approved'), function () {
            frappe.call({
                method: "gulf_vision.overrides.purchase_order.purchase_order_approved",
                args: {

                    doc: frm.doc.name
                },
                callback: function (r) {
                    r = r.message
                    if (r == true) {
                        frm.reload_doc()
                        frappe.set_route('app/purchase-order')

                    }

                }

            })
        }, __('Actions'));

        frm.add_custom_button(__('Reject'), function () {
            frappe.call({
                method: "gulf_vision.overrides.purchase_order.purchase_order_reject",
                args: {

                    doc: frm.doc.name,


                },
                callback: function (r) {
                    r = r.message
                    if (r == true) {
                        debugger;
                        frappe.prompt({
                            title: 'Remarks',
                            label: 'Provide Valid reason for rejection',
                            fieldname: 'reject_remark',
                            fieldtype: 'Small Text'
                        }, (values) => {
                            frm.set_value("remarks_for_rejection", values.reject_remark)
                            frm.set_value("workflow_state", "rejected")
                            frm.set_value("rejected", 1)
                            frm.save();
                        })
                    }
                    // frappe.set_route('app/purchase-order')
                    
                }

            })

        }, __('Actions'));
    }

},

)
