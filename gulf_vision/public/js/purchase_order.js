frappe.ui.form.on('Purchase Order', {
    setup: function(frm){
        frm.set_query("role", "transition_table", function(doc,cdt,cdn){
            let role_list = ["Project Manager", "Store Keeper","Project Admin", "Management"]
            for(let i = 0; i < role_list.length; i++ ){
                var role = locals[cdt][cdn]
                role.role = i

            }

        })
    }
})



