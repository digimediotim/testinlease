# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    sales_margin = fields.Float('Sales Margin', required=True, digits='Product Price', default=1.0)
    standard_price = fields.Float('Cost', required=True, digits='Product Price', default=1.0)
    sales_persons = fields.One2many('res.users', 'invoice_id', string="Sales Persons")


    @api.onchange('product_id')
    def _onchange_product_id(self):
        domain = super(AccountMoveLine, self)._onchange_product_id()
        if self.product_id:
            self.sales_margin = self.product_id.sales_margin
            self.standard_price = self.product_id.standard_price
            self.price_unit = self.sales_margin * self.standard_price
        return domain

    def _get_computed_price_unit(self):
        return self.standard_price * self.sales_margin

    @api.onchange('sales_margin', 'standard_price', 'sales_persons')
    def _onchange_sale_margin(self):
        self.price_unit = self.standard_price * self.sales_margin

    @api.onchange('product_uom_id')
    def _onchange_uom_id(self):
        self.price_unit = self.standard_price * self.sales_margin

    def _get_price_total_and_subtotal(self, price_unit=None, quantity=None, discount=None, currency=None, product=None,
                                      partner=None, taxes=None, move_type=None):
        self.ensure_one()
        return self._get_price_total_and_subtotal_model(
            price_unit=self.sales_margin * self.standard_price,
            quantity=quantity or self.quantity,
            discount=discount or self.discount,
            currency=currency or self.currency_id,
            product=product or self.product_id,
            partner=partner or self.partner_id,
            taxes=taxes or self.tax_ids,
            move_type=move_type or self.move_id.move_type,
        )


class ResUsers(models.Model):
    _inherit = "res.users"

    invoice_id = fields.Many2one('account.move.line', string='Invoice', ondelete='cascade')
