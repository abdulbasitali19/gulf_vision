import frappe 
import json
from frappe.utils import today
from frappe.custom.doctype.property_setter.property_setter import make_property_setter


def updated_only_by_owner(doc, method=None):
    if frappe.session.user == doc.owner and doc.rejected == 1:
        doc.remarks_for_rejection = " "
        doc.rejected = 0
        doc.save(ignore_permissions = True)
        frappe.db.commit()



@frappe.whitelist()
def purchase_order_approved(doc):
    purchase_order = frappe.get_doc("Purchase Order",doc)
    cost_center = frappe.get_doc("Cost Center",purchase_order.cost_center)
    document_approval_workflow = frappe.get_doc("Documents Approval Workflow",{"document":"Purchase Order"})
    if len(purchase_order.transition_table) == 0 and document_approval_workflow.approver_1 and document_approval_workflow.approver_1 == 'Project Admin':
        project_admin = cost_center.project_admin
        if frappe.session.user == project_admin:
            purchase_order.append("transition_table", {
                    "role": "Project Admin",
                    "approved": 1,
                    "approving_date": today(),
                    "user": frappe.session.user,
                    "transition_detail": "Purchase approved by Project Admin"
                })
            purchase_order.approval_stage = cost_center.store_keeper
            purchase_order.docstatus = 0
            purchase_order.workflow_state = 'Draft'
            purchase_order.save()
            return True
        else:
           frappe.throw("Document Should Be Approved By Project Admin")

        
    elif len(purchase_order.transition_table) == 1 and document_approval_workflow.approver_2 and document_approval_workflow.approver_2 == 'Store Keeper':
        store_keeper = cost_center.store_keeper
        if frappe.session.user == store_keeper:
            purchase_order.append("transition_table", {
                    "role": "Store Keeper",
                    "approved": 1,
                    "approving_date": today(),
                    "user": frappe.session.user,
                    "transition_detail": "Purchase Order approved by Store Keeper "
                })
            purchase_order.approval_stage = cost_center.management
            purchase_order.docstatus = 0
            purchase_order.workflow_state = 'Draft'
            purchase_order.save()
            return True
        else:
            frappe.throw("Document Should Be Approved By Store keeper")
    

    elif len(purchase_order.transition_table) == 2 and document_approval_workflow.approver_3 and document_approval_workflow.approver_3 == 'Management':
        management = cost_center.management
        if frappe.session.user == management:
            purchase_order.append("transition_table", {
                    "role": "Management",
                    "approved": 1,
                    "approving_date": today(),
                    "user": frappe.session.user,
                    "transition_detail": "Purchase Order approved by Management"
                })
            purchase_order.approval_stage = cost_center.pm_name
            purchase_order.docstatus = 0
            purchase_order.workflow_state = 'Draft'
            purchase_order.save()
            return True
        else:
            frappe.throw("Document Should Be Approved By Management")
    
    elif len(purchase_order.transition_table) == 3 and document_approval_workflow.approver_4 and document_approval_workflow.approver_4 == 'PM':
        project_manager = cost_center.pm_name
        if frappe.session.user == project_manager:
            purchase_order.append("transition_table", {
                    "role": "Management",
                    "approved": 1,
                    "approving_date": today(),
                    "user": frappe.session.user,
                    "transition_detail": "Purchase Order approved by Project Manager "
                })
            purchase_order.approval_stage = " "
            purchase_order.submit()
            return True
        else:
            frappe.throw("Document Should Be Approved By Project Manager")
    else:
        if len(purchase_order.transition_table) == 0 and frappe.session.user !="Administrator" : 
            frappe.throw("Document  Must be approved by Project Admin")
        elif len(purchase_order.transition_table) == 1 :
            frappe.throw("Document Must be approved by Store Keeper")
        elif len(purchase_order.transition_table) == 2:
            frappe.throw("Document Must be approved by Management")
        else:
            frappe.throw("Document Must be Submit by Project Manager")




@frappe.whitelist()
def purchase_order_reject(doc):
    purchase_order = frappe.get_doc("Purchase Order", doc)
    cost_center = frappe.get_doc("Cost Center", purchase_order.cost_center)
    document_approval_workflow = frappe.get_doc("Documents Approval Workflow", {"document": "Purchase Order"})

    # make_property_setter( "Purchase Order", "rejected", "mandatory", 1,"check", validate_fields_for_doctype=False)


    if len(purchase_order.transition_table) == 0:
        if document_approval_workflow.approver_1 == 'Project Admin':
            project_admin = cost_center.project_admin
            if frappe.session.user == project_admin:
                purchase_order.transition_table = []
                purchase_order.workflow_state = 'Rejected'
                return True
            else:
                throw("Document Should Be Rejected By Project Admin")

    elif len(purchase_order.transition_table) == 1:
        if document_approval_workflow.approver_2 == 'Store Keeper':
            store_keeper = cost_center.store_keeper
            if frappe.session.user == store_keeper:
                purchase_order.transition_table = []
                purchase_order.workflow_state = 'Rejected'
                # purchase_order.save()
                return True
            else:
                throw("Document Should Be Rejected By Shopkeeper")

    elif len(purchase_order.transition_table) == 2:
        if document_approval_workflow.approver_3 == 'Management':
            management = cost_center.management
            if frappe.session.user == management:
                purchase_order.transition_table = []
                purchase_order.workflow_state = 'Rejected'
                # purchase_order.save()
                return True
            else:
                throw("Document Should Be Rejected By Shopkeeper")

    elif len(purchase_order.transition_table) == 3:
        if document_approval_workflow.approver_4 == 'PM':
            project_manager = cost_center.pm_name
            if frappe.session.user == project_manager:
                purchase_order.transition_table = []
                purchase_order.workflow_state = 'Rejected'
                # purchase_order.save()
                return True
            else:
                throw("Document Should Be Rejected By Project Manager")

    else:
        if len(purchase_order.transition_table) == 0 and session.user != "Administrator":
            throw("Document Must be rejected by Project Admin")
        elif len(purchase_order.transition_table) == 1:
            throw("Document Must be rejected by Store Keeper")
        elif len(purchase_order.transition_table) == 2:
            throw("Document Must be rejected by Management")
        else:
            throw("Document Must be Rejected by Project Manager")











