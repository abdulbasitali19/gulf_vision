frappe.ui.form.on('Purchase Order', {
    validate: function (frm) {
        frm.set_value("documnet_currently_update_by", frappe.session.user)
        frappe.db.get_value("Cost Center",frm.doc.cost_center,"project_admin", (r) => { 
            frm.set_value("approval_stage",r.project_admin)
        });
    },
    after_save:function(frm){
        if(frappe.session.user != 'Administrator' && frappe.session.user != frm.doc.approval_stage){
        $("button[data-label='Submit']").hide();
        $(".inner-group-button[data-label='Actions'] > button").hide();
        }
    },

    onload:function(frm){
        if(!frm.is_new() && frappe.session.user != 'Administrator' && frappe.session.user != frm.doc.approval_stage){
            $("button[data-label='Submit']").hide();
            $(".inner-group-button[data-label='Actions'] > button").hide();
            }

    },

    refresh: function (frm) {
        frm.add_custom_button(__('Approved'), function () {
            frappe.call({
                method : "gulf_vision.overrides.purchase_order.purchase_order_approved",
                args:{

                    doc : frm.doc.name
                },
                callback:function(res){
                    frappe.msgprint("method not found")

                }

            })
        }, __('Actions'));

        frm.add_custom_button(__('Reject'), function () {
            frappe.call({
                method : "gulf_vision.overrides.purchase_order.purchase_order_reject",
                args:{

                    purchase_order:frm.doc,

                },
                callback:function(res){

                }

            })

        }, __('Actions'));
    }

},

)
