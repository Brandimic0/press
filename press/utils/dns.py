import frappe
from frappe.model.document import Document
from frappe.core.utils import find
from press.utils import log_error

import boto3


@frappe.whitelist()
def create_dns_record(doc, record_name=None):
	"""Check if site needs dns records and creates one."""
	domain = frappe.get_doc("Root Domain", doc.domain)
	is_standalone = frappe.get_value("Server", doc.server, "is_standalone")

	if is_standalone:
		_change_dns_record("UPSERT", domain, doc.server, record_name=record_name)
	else:
		proxy_server = frappe.get_value("Server", doc.server, "proxy_server")
		_change_dns_record("UPSERT", domain, proxy_server, record_name=record_name)


def _change_dns_record(
	method: str, domain: Document, proxy_server: str, record_name: str = None
):
	"""
	Change dns record of site

	method: CREATE | DELETE | UPSERT
	"""
	try:
		client = boto3.client(
			"route53",
			aws_access_key_id=domain.aws_access_key_id,
			aws_secret_access_key=domain.get_password("aws_secret_access_key"),
		)
		zones = client.list_hosted_zones_by_name()["HostedZones"]
		hosted_zone = find(reversed(zones), lambda x: domain.name.endswith(x["Name"][:-1]))[
			"Id"
		]
		client.change_resource_record_sets(
			ChangeBatch={
				"Changes": [
					{
						"Action": method,
						"ResourceRecordSet": {
							"Name": record_name,
							"Type": "CNAME",
							"TTL": 600,
							"ResourceRecords": [{"Value": proxy_server}],
						},
					}
				]
			},
			HostedZoneId=hosted_zone,
		)
	except Exception:
		log_error(
			"Route 53 Record Creation Error",
			domain=domain.name,
			site=record_name,
			proxy_server=proxy_server,
		)
