# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    sales_margin = fields.Float('Sales Margin', required=True, digits='Product Price', default=1.0)
    standard_price = fields.Float('Cost', required=True, digits='Product Price', default=1.0)
    sales_persons = fields.One2many('res.users', 'sale_id', string="Sales Persons")

    @api.onchange('product_id')
    def product_id_change(self):
        domain = super(SaleOrderLine, self).product_id_change()
        if self.product_id:
            self.sales_margin = self.product_id.sales_margin
            self.standard_price = self.product_id.standard_price
            self.price_unit = self.sales_margin * self.standard_price
        return domain

    @api.onchange('sales_margin', 'standard_price')
    def sale_margin_change(self):
        if not self.product_uom or not self.product_id:
            self.price_unit = 0.0
            return
        if self.order_id.pricelist_id and self.order_id.partner_id:
            product = self.product_id.with_context(
                lang=self.order_id.partner_id.lang,
                partner=self.order_id.partner_id,
                quantity=self.product_uom_qty,
                date=self.order_id.date_order,
                pricelist=self.order_id.pricelist_id.id,
                uom=self.product_uom.id,
                fiscal_position=self.env.context.get('fiscal_position')
            )
            self.price_unit = self.env['account.tax']._fix_tax_included_price_company(self._get_display_price(product),
                                                                                      product.taxes_id, self.tax_id,
                                                                                      self.company_id)

    def _get_display_price(self, product):
        return self.sales_margin * self.standard_price


class ResUsers(models.Model):
    _inherit = "res.users"

    sale_id = fields.Many2one('sale.order.line', string='Sale', ondelete='cascade')
