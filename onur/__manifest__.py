# -*- coding: utf-8 -*-
{
    'name' : 'Sales Assignment',
    'description':"""
Sales Margin Data
    """,
    'version' : '1.0',
    'category': 'Sales',
    'depends' : ['account','sale'],
    "author": "Onur Ugur",
    'data': [
        'security/ir.model.access.csv',
        'views/product_template_views.xml',
        'views/sale_views.xml',
        'views/account_views.xml',
        'data/data.xml'
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
