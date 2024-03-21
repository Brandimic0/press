# Copyright (c) 2023, Frappe and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class PressNotification(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		assistance_url: DF.Data | None
		document_name: DF.DynamicLink
		document_type: DF.Link
		is_actionable: DF.Check
		is_addressed: DF.Check
		message: DF.LongText | None
		read: DF.Check
		team: DF.Link
		title: DF.SmallText | None
		traceback: DF.Code | None
		type: DF.Literal[
			"Site Update",
			"Site Migrate",
			"Version Upgrade",
			"Bench Deploy",
			"Site Recovery",
			"Downtime/Performance",
		]
	# end: auto-generated types

	dashboard_fields = [
		"team",
		"document_type",
		"class",
		"type",
		"document_name",
		"is_actionable",
		"read",
		"is_addressed",
		"title",
		"message",
		"traceback",
		"assistance_url",
	]

	dashboard_actions = ["mark_as_addressed"]

	def after_insert(self):
		if frappe.local.dev_server:
			return

		if self.type == "Bench Deploy":
			group_name = frappe.db.get_value("Deploy Candidate", self.document_name, "group")
			rg_title = frappe.db.get_value("Release Group", group_name, "title")

			frappe.sendmail(
				recipients=[frappe.db.get_value("Team", self.team, "user")],
				subject=f"Bench Deploy Failed - {rg_title}",
				template="bench_deploy_failure",
				args={
					"message": self.message,
					"link": f"dashboard/benches/{group_name}/deploys/{self.document_name}",
				},
			)

	@frappe.whitelist()
	def mark_as_addressed(self):
		self.read = True
		self.is_addressed = True
		self.save()
		frappe.db.commit()


def create_new_notification(team, type, document_type, document_name, message):
	if not frappe.db.exists("Press Notification", {"document_name": document_name}):
		frappe.get_doc(
			{
				"doctype": "Press Notification",
				"team": team,
				"type": type,
				"document_type": document_type,
				"document_name": document_name or 0,
				"message": message,
			}
		).insert()
		frappe.publish_realtime("press_notification", {"team": team})
