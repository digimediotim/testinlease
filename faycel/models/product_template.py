# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

class ProductProduct(models.Model):
    _inherit = 'product.product'

    sales_margin = fields.Float(
        'Sales Margin', default=1.0,
        digits='Product Price',
        help="Price at which the product is sold to customers.")
