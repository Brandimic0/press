# -*- coding: utf-8 -*-
# Copyright (c) 2021, Frappe and contributors
# For license information, please see license.txt

import frappe
from press.utils import get_current_team


@frappe.whitelist()
def get_apps():
	"""Return list of apps developed by the current team"""
	team = get_current_team()
	apps = frappe.get_all(
		"Marketplace App",
		fields=["name", "title", "image", "app", "status", "description"],
		filters={"team": team},
	)

	return apps


@frappe.whitelist()
def get_app(name):
	"""Return the `Marketplace App` document with name"""
	app = frappe.get_doc("Marketplace App", name)
	return app
