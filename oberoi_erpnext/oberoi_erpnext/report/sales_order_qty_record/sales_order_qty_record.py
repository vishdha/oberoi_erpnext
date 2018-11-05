# Copyright (c) 2013, Vishal Dhayagude and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import msgprint, _

def execute(filters=None):
	if not filters: filters = {}

	columns = get_columns(filters)
	entries = get_entries(filters)
	data = []

	for d in entries:
		data.append([
            d.transaction_date, d.name, d.qty
        ])

	return columns, data

def get_columns(filters):
    return [
        _("Date") + ":Date:80",
        _("Sales Order") + ":Link/Sales Order:100",
        _("Portions in order") + ":Link/:150",
        _("Portions executed") + ":Link/:150",
        _("Portions balance to execute") + ":Link/:180",
		_("Portions to dispatched") + ":Link/:180",
        _("Portions balance to dispatch") + ":Int:200"
        ]

def get_entries(filters):
    date_field = "transaction_date"
    conditions, values = get_conditions(filters, date_field)
    entries = frappe.db.sql("""
        select
            vt.%s, vt.name, soi.qty
        from
            `tabSales Order` vt INNER JOIN `tabSales Order Item` soi
			ON soi.parent = vt.name
		where 
			vt.company = '%s'

			%s order by transaction_date 
        """ %(date_field, filters['company'], conditions), tuple(values),
              as_dict=1)

    return entries


def get_conditions(filters, date_field):
    conditions = [""]
    values = []

 

    if filters.get("from_date"):
        conditions.append("vt.{0}>=%s".format(date_field))
        values.append(filters["from_date"])

    if filters.get("to_date"):
        conditions.append("vt.{0}<=%s".format(date_field))
        values.append(filters["to_date"])

    return "and ".join(conditions), values
