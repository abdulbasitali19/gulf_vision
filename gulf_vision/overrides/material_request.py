import frappe
from frappe.utils import today


def Validating_approver(doc, method=None):
    email = frappe.db.get_value("User",frappe.session.user,'email' )
    if email == doc.approved_by_project_manager:
        # doc.approver_role = frappe.get_roles(frappe.session.user)
        doc.approver_role = 'Project Manager'
        doc.approver_address = frappe.db.get_value("Contact", email, 'address' )
        doc.date_and_time = today()
        doc.docstatus = 1
    else:
        doc.docstatus = 0
        frappe.msgprint("For Submit the Document Approval Required By {0}".format(doc.approved_by_project_manager))