# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Sales Margin Custom',
    'version' : '1.1',
    'summary': 'Sales & Invoicing',
    'sequence': 10,
    'description': """
Sales & Invoicing
====================
This module add a custom information sale margin that provoke an update on the sale price base on Product cost.

    """,
    'category': 'Sales/Sales',
    'website': 'www.in-lease.com',
    'depends': ['sale', 'account'],
    'data': [
        'views/product_view.xml',
        'views/order_line.xml',
        'views/account_move_view.xml',
    ],
    'demo': [
    ],
    'qweb': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
