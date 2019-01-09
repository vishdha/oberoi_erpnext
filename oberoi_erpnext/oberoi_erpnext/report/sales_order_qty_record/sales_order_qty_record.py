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
        for x in xrange(1,10):
            print("entries", entries)
	for d in entries:
		data.append([
            d.transaction_date, d.name, d.item_name, d.qty, d.dn_qty, d.qty-d.dn_qty
        ])

	return columns, data

def get_columns(filters):
    return [
        _("Date") + ":Date:80",
        _("Sales Order") + ":Link/Sales Order:100",
        _("Portions") + ":Link/Item:100",
        _("Portions in order") + ":Data:100",
        _("Portions to dispatched") + ":Data:100",
        _("Portions balance to dispatch") + ":Int:200",
        _("Portions executed") + ":Link/:150",
        _("Portions balance to execute") + ":Link/:180"
        ]

def get_entries(filters):
    date_field = "transaction_date"
    conditions, values = get_conditions(filters, date_field)

    for x in xrange(1,10):
        print("sss", conditions, values)
    entries = frappe.db.sql("""
        select
            so.%s, so.name, soi.item_name, soi.qty, dni.qty AS dn_qty
        from
            `tabSales Order` so INNER JOIN `tabSales Order Item` soi
			ON soi.parent = so.name INNER JOIN `tabDelivery Note Item` dni 
            ON dni.against_sales_order=so.name
		where 
			so.company = '%s' AND so.docstatus= 1 AND dni.docstatus = 1

			%s order by transaction_date 
        """ %(date_field, filters['company'], conditions), tuple(values),
              as_dict=1)

    return entries

def get_conditions(filters, date_field):
    conditions = [""]
    values = []

 

    if filters.get("from_date"):
        conditions.append("so.{0}>=%s".format(date_field))
        values.append(filters["from_date"])

    if filters.get("to_date"):
        conditions.append("so.{0}<=%s".format(date_field))
        values.append(filters["to_date"])

    return "and ".join(conditions), values
