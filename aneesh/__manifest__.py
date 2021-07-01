# -*- coding: utf-8 -*-
{
    'name': 'Sales Margin in Product / Sales Orders / Invoice',
    'version':'1.0',
    'category': 'Sales/Sales',
    'author':'Aneesh AV',
    'description': """
This module adds the 'Margin' on Product / Sales Orders / Invoice.
    """,
    'depends':['sale_management','account'],
    'demo':['data/sale_margin_demo.xml'],
    'data':[
            'security/ir.model.access.csv',
            'views/product_view.xml',
            'views/sales_view.xml',
            'views/invoice_view.xml',
            'report/sale_report_view.xml'
        ],
}
