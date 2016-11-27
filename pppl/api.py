
from __future__ import unicode_literals
import frappe
from frappe.utils import cint, flt, cstr, comma_or
from erpnext.setup.utils import get_company_currency
from frappe import _, throw
from frappe.model.mapper import get_mapped_doc



@frappe.whitelist()

def set_total_in_words(doc, method):
    from frappe.utils import money_in_words
    company_currency = get_company_currency(doc.company)

    disable_rounded_total = cint(frappe.db.get_value("Global Defaults", None, "disable_rounded_total"))

    if doc.meta.get_field("base_in_words"):
        doc.base_in_words = money_in_words(disable_rounded_total and
            abs(doc.base_grand_total) or abs(doc.base_rounded_total), company_currency)
    if doc.meta.get_field("in_words"):
        doc.in_words = money_in_words(disable_rounded_total and
          abs(doc.grand_total) or abs(doc.rounded_total), doc.currency)
    if doc.meta.get_field("amount_of_duty_in_words"):
        doc.amount_of_duty_in_words = money_in_words(disable_rounded_total and
            abs(doc.excise_amount) or abs(doc.excise_amount), doc.currency)
    if doc.meta.get_field("vat_in_words"):
        doc.vat_in_words = money_in_words(disable_rounded_total and
            abs(doc.vat_amount) or abs(doc.vat_amount), doc.currency)


@frappe.whitelist()
def make_purchase_receipt(source_name, target_doc=None):
	def update_item(obj, target, source_parent):
		target.qty = flt(obj.qty) 
		target.stock_qty = flt(obj.qty)
		target.amount = flt(obj.qty) * flt(obj.rate)
		target.base_amount = flt(obj.qty) * flt(obj.rate) 

	doc = get_mapped_doc("Sales Invoice", source_name,	{
		"Sales Invoice": {
			"doctype": "Purchase Receipt",
			"validation": {
				"docstatus": ["=", 1],
			}
		},
		"Sales Invoice Item": {
			"doctype": "Purchase Receipt Item",
			"field_map": {
				"name": "sales_invoice_item",
				"parent": "sales_invoice",
			},
			"postprocess": update_item,
			"condition": lambda doc: abs(doc.qty) > 0
		},
		"Purchase Taxes and Charges": {
			"doctype": "Purchase Taxes and Charges",
			"add_if_empty": True
		}
	}, target_doc, set_missing_values)

	return doc

def set_missing_values(source, target):
	target.ignore_pricing_rule = 1
	target.run_method("set_missing_values")
	target.run_method("calculate_taxes_and_totals")
