# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.depends('standard_price', 'sales_margin')
    def _compute_list_price(self):
        # calculate the sale price based on cost and margin
        self.list_price = self.standard_price / self.sales_margin

    sales_margin = fields.Float(
        string='Sales Margin',
        digits=(16, 2),
        help='The sales margin amount')

    list_price = fields.Float(
        'Sales Price', default=1.0,
        digits='Product Price',
        compute='_compute_list_price',
        store=True,
        help="Price at which the product is sold to customers.")
