import frappe


def set_transitions_roles(doc):
    if doc.cost_center:
        email = frappe.db.get_value("User",frappe.session.user,'email' )
        cost_center = frappe.get_doc("Cost Center", cost_center)
        if cost_center.store_keeper == email:
            doc.append("transition_table",{
                "role" : "Shop Keeper",
                "approved" : 1,
                "user" : email
                "transition_detail": "Purchase Order approved by Shop Keeper"
            })
    else:
        frappe.throw("please select the cost center")

