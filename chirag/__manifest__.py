# -*- coding: utf-8 -*-

{
    "name": "Sale Margin",
    "summary": "Calculation of sales margin based on product.",
    "version": "14.0.0.1",
    "category": "sale, invoice.",
	"description": """
		- Add Sales Margin in product
        - Calculation of sales margin in sales order line and invoice. 
        - Sales report based on sales person 
    """,
    "depends": [
        'sale_management','account'
    ],
    "data": [
        'views/product_view.xml',
        'views/sales_view.xml',
        'views/account_view.xml'
    ],
    "installable": True,
    'application': True,
}