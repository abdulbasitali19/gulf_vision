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
            "document_currently_updated_by": frappe.session.user,
            "rejected": 0,
            "workflow_state": "Approved",
        },
        fields=[
            "name as document_name",
            "document_currently_updated_by as approved_by",
            "owner as created_by",
            "workflow_state as workflow_state",
            "transaction_date as transaction_date",
        ],
        as_list=False,
    )

    purchase_order = frappe.get_all(
        "Purchase Order",
        filters={
            "documnet_currently_update_by": frappe.session.user,
            "rejected": 0,
            "workflow_state": "Approved",
        },
        fields=[
            "name as document_name",
            "documnet_currently_update_by as approved_by",
            "owner as created_by",
            "workflow_state as workflow_state",
            "transaction_date as transaction_date",
        ],
        as_list=False,
    )

    for approver in material_request + purchase_order:
        transition_dict = {
            "approved_by": approver.get("approved_by"),
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
            "label": _("Document Type"),
            "fieldname": "document_name",
            "fieldtype": "Link",
            "options": "Doctype",
            "width": 150,
        },
        {
            "label": _("Approved By"),
            "fieldname": "approved_by",
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
