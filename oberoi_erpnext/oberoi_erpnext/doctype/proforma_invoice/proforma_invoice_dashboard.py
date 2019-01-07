from frappe import _

def get_data():
	return {
		'fieldname': 'proforma_invoice',
		'non_standard_fieldnames': {
			'Delivery Note': 'agianst_proforma_invoice',
			'Journal Entry': 'reference_name',
			'Payment Entry': 'reference_name',
			'Payment Request': 'reference_name',
			'Subscription': 'reference_document',
		},
		'internal_links': {
			'Sales Order': ['items', 'prevdoc_docname']
		},
		'transactions': [
			{
				'label': _('Fulfillment'),
				'items': ['Sales Order','Sales Invoice','Delivery Note']
			}
		]
	}