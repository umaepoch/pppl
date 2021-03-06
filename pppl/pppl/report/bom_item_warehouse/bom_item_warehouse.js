// Copyright (c) 2016, Epoch and contributors
// For license information, please see license.txt

frappe.query_reports["BOM Item Warehouse"] = {
	"filters": [

	        {
                        "fieldname":"bom",
                        "label": __("BOM"),
                        "fieldtype": "Link",
                        "options": "BOM"                                            
                                               
                },
                
                {      "fieldname":"from_date",
                        "label": __("From Date"),
                        "fieldtype": "Date",
                        "width": "80",
                        "default": sys_defaults.year_start_date,
                },
                {
                        "fieldname":"to_date",
                        "label": __("To Date"),
                        "fieldtype": "Date",
                        "width": "80",
                        "default": frappe.datetime.get_today()
                },
                {
                        "fieldname":"warehouse",
                        "label": __("Warehouse"),
                        "fieldtype": "Link",
                        "options": "Warehouse"
                },
                {
                        "fieldname":"item_code",
                        "label": __("Item"),
                        "fieldtype": "Link",
                        "options": "Item"
                }
                                  
                
        ]
}

// $(function() {
//      $(wrapper).bind("show", function() {
//              frappe.query_report.load();
//      });
// });

