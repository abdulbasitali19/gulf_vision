# Copyright (c) 2024, abdul basit ali and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import today, getdate
from frappe.model.document import Document

class LeaveSettlement(Document):
	def validate(self):
		self.calculate_days()


	def calculate_days(self):
		total_days = getdate(self.approved_leave_to) - getdate(self.approved_leave_from)
		self.total_days =  total_days.days