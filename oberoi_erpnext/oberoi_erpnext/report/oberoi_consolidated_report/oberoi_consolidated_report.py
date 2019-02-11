# Copyright (c) 2013, Vishal Dhayagude and contributors
# For license information, please see license.txt

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
            d.posting_date, d.sales_order, d.proforma_invoice, d.proforma_invoice_amount, d.sales_invoice, d.sales_invoice_item, d.sales_invoice_out,  d.payment_entry, d.payment_amount
        ])

	return columns, data

def get_columns(filters):
    return [
        _("Date") + ":Date:80",
        _("Sales Order") + ":Link/Sales Order:100",
        _("Performa Invoice") + ":Link/Proforma Invoice:120",
        _("Performa Invoice Amount") + ":Int:150",
        _("Sales Invoice") + ":Link/Sales Invoice:100",
        _("Sales Invoice Amount") + ":Int:150",
        _("Sales Invoice Outstanding Amount") + ":Int:150",
        _("Payment Entry") + ":Link/Payment Entry:100",
        _("Payment Entry Amount") + "::180"
        ]

def get_entries(filters):
    date_field = "posting_date"
    conditions, values = get_conditions(filters, date_field)
    entries = frappe.db.sql("""
    	select DISTINCT SI.%s, PII.prevdoc_docname as sales_order, PI.name as proforma_invoice, PI.grand_total as proforma_invoice_amount, SII.parent as sales_invoice, SI.grand_total as sales_invoice_item,  SI.outstanding_amount as sales_invoice_out, PER.parent as payment_entry, PER.allocated_amount as payment_amount  
        from `tabProforma Invoice Item` as PII inner join `tabProforma Invoice` as PI 
        ON PII.parent = PI.name inner join `tabSales Invoice Item` as SII 
        ON SII.proforma_invoice= PI.name inner join `tabSales Invoice` as SI 
        ON SI.name=SII.parent inner join `tabPayment Entry Reference` as PER 
        ON SI.name=PER.reference_name
        where SI.company = '%s' AND SI.docstatus = 1
        %s
        """ %(date_field, filters['company'], conditions), tuple(values),
              as_dict=1)

    for x in xrange(1,10):
    	print("record", entries)
    return entries

def get_conditions(filters, date_field):
    conditions = [""]
    values = []

 

    if filters.get("from_date"):
        conditions.append("SI.{0}>=%s".format(date_field))
        values.append(filters["from_date"])

    if filters.get("to_date"):
        conditions.append("SI.{0}<=%s".format(date_field))
        values.append(filters["to_date"])

    return "and ".join(conditions), values
