# -*- coding: utf-8 -*-

from odoo import fields, api, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    sales_margin = fields.Float('Margin', digits='Product Price', default=0.0)
    sales_person_ids = fields.Many2many('res.users',string='Sales Person')
    

     #based on the product sales margin set in the invoice line
    @api.onchange('product_id')
    def _onchange_product_id(self):
        res = super(AccountMoveLine, self)._onchange_product_id()
        for line in self:
            line.sales_margin = line.product_id.sales_margin
        return res

    #for the one Invoice  if margin is set then based on that unit price is also change.    
    @api.onchange('sales_margin')
    def sales_margin_change(self):
        for margin in self:
            if self.product_id and self.sales_margin:
                self.price_unit = self.product_id.standard_price / self.sales_margin