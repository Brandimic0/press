# -*- coding: utf-8 -*-
# Copyright (c) 2020, Frappe and contributors
# For license information, please see license.txt


# import frappe
from frappe.model.document import Document


class ModuleSetupGuide(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		enabled: DF.Check
		industry: DF.Literal[
			"",
			"Manufacturing",
			"Distribution",
			"Retail",
			"Services",
			"Education",
			"Healthcare",
			"Non Profit",
			"Other",
		]
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		setup_guide: DF.Attach | None
	# end: auto-generated types

	pass
