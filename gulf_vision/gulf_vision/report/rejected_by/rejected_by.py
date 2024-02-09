# Copyright (c) 2024, Abdul Basit Ali and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
    columns = get_columns()
    data = get_data_and_format()
    return columns, data


def get_data_and_format():
    data = []
    material_request = frappe.get_all(
        "Material Request",
        filters={
            "docstatus": 0,
            "owner": frappe.session.user,
            "rejected": 1,
            "workflow_state": "Rejected",
        },
        fields=[
            "name as document_name",
            "approval_stage as rejected_by",
            "owner as created_by",
            "workflow_state as workflow_state",
            "transaction_date as transaction_date",
        ],
        as_list=False,
    )
    purchase_order = frappe.get_all(
        "Purchase Order",
        filters={
            "docstatus": 0,
            "owner": frappe.session.user,
            "rejected": 1,
            "workflow_state": "Rejected",
        },
        fields=[
            "name as document_name",
            "approval_stage as rejected_by",
            "owner as created_by",
            "workflow_state as workflow_state",
            "transaction_date as transaction_date",
        ],
        as_list=False,
    )

    for approver in material_request + purchase_order:
        transition_dict = {
            "rejected_by": approver.get("rejected_by"),
            "created_by": approver.get("created_by"),
            "workflow_state": approver.get("workflow_state"),
            "transaction_date": approver.get("transaction_date"),
        }

        document_name = approver.get("document_name")
        if document_name.startswith("PUR"):
            transition_dict[
                "document_name"
            ] = '<a href ="/app/purchase-order/{0}">{0}</a>'.format(document_name)
            transition_dict["document_type"] = "Purchase Order"
        else:
            transition_dict[
                "document_name"
            ] = '<a href ="/app/material-request/{0}">{0}</a>'.format(document_name)
            transition_dict["document_type"] = "Material Request"

        data.append(transition_dict)

    return data


def get_columns():
    columns = [
        {
            "label": _("Document Type"),
            "fieldname": "document_type",
            "fieldtype": "Data",
            "width": 150,
        },
        {
            "label": _("Document"),
            "fieldname": "document_name",
            "fieldtype": "Data",
            "width": 150,
        },
        {
            "label": _("Rejected By"),
            "fieldname": "rejected_by",
            "fieldtype": "Link",
            "options": "User",
            "width": 180,
        },
        {
            "label": _("Created By"),
            "fieldname": "created_by",
            "fieldtype": "Link",
            "options": "User",
            "width": 180,
        },
        {
            "label": _("Workflow State"),
            "fieldname": "workflow_state",
            "fieldtype": "Link",
            "options": "Workflow State",
            "width": 180,
        },
        {
            "label": _("Date"),
            "fieldname": "transaction_date",
            "fieldtype": "date",
            "width": 180,
        },
    ]
    return columns
