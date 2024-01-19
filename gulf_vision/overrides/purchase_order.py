import frappe 
import json


@frappe.whitelist()
def purchase_order_approved(doc):
    purchase_order = frappe.get_doc("Purchase Order",doc)
    cost_center = frappe.get_doc("Cost Center",purchase_order.cost_center)
    document_approval_workflow = frappe.get_doc("Documents Approval Workflow",{"document":"Purchase Order"})
    if len(purchase_order.transition_table) == 0 and document_approval_workflow.approver_1 and document_approval_workflow.approver_1 == 'Project Admin':
        project_admin = cost_center.project_admin
        if frappe.session.user == project_admin:
            doc.append("transition_table", {
                    "role": "Project Admin",
                    "approved": 1,
                    "user": frappe.session.user,
                    "transition_detail": "Purchase Order must be approved by Shopkeeper"
                })
            doc.approval_stage = "Next Approval By Store Keeper {0}".format(cost_center.store_keeper)
            doc.docstatus = 0
            doc.workflow_state = 'Draft'
        else:
           frappe.throw("Document Should Be Approved By Project Admin")

        
    elif len(purchase_order.transition_table) == 1 and document_approval_workflow.approver_2 and document_approval_workflow.approver_2 == 'Store Keeper':
        store_keeper = cost_center.store_keeper
        if frappe.session.user == store_keeper:
            doc.append("transition_table", {
                    "role": "Store Keeper",
                    "approved": 1,
                    "user": frappe.session.user,
                    "transition_detail": "Purchase Order approved by Store Keeper "
                })
            doc.approval_stage = "Next Approval By Management {0}".format(cost_center.management)
            doc.docstatus = 0
            doc.workflow_state = 'Draft'
        else:
            frappe.throw("Document Should Be Approved By Shopkeeper")
    

    elif len(purchase_order.transition_table) == 2 and document_approval_workflow.approver_3 and document_approval_workflow.approver_3 == 'Management':
        management = cost_center.management
        if frappe.session.user == management:
            doc.append("transition_table", {
                    "role": "Management",
                    "approved": 1,
                    "user": frappe.session.user,
                    "transition_detail": "Purchase Order approved by Store Keeper "
                })
            doc.approval_stage = "Next Approval By Project Manager {0}".format(cost_center.pm_name)
            doc.docstatus = 0
            doc.workflow_state = 'Draft'
        else:
            frappe.throw("Document Should Be Approved By Shopkeeper")
    
    elif len(purchase_order.transition_table) == 3 and document_approval_workflow.approver_4 and document_approval_workflow.approver_4 == 'Project Manager':
        project_manager = cost_center.pm_name
        if frappe.session.user == project_manager:
            doc.append("transition_table", {
                    "role": "Management",
                    "approved": 1,
                    "user": frappe.session.user,
                    "transition_detail": "Purchase Order approved by Project Manager "
                })
            doc.approval_stage = ""
            doc.submit()
        else:
            frappe.throw("Document Should Be Approved By Project Manager")
    else:
        if len(self.transition_table) == 0 and frappe.session.user !="Administrator" : 
            frappe.throw("Document  Must be approved by Project Admin")
        elif len(self.transition_table) == 1 :
            frappe.throw("Document Must be approved by Store Keeper")
        elif len(self.transition_table) == 2:
            frappe.throw("Document Must be approved by Management")
        else:
            frappe.throw("Document Must be Submit by Project Manager")



            
            
            
        











