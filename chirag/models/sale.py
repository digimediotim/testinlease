# -*- coding: utf-8 -*-

from odoo import fields, api, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    sales_margin = fields.Float('Margin', digits='Product Price', default=0.0)
    sales_person_ids = fields.Many2many('res.users',string='Sales Person')

    #based on the product sales margin set in the sales order line
    @api.onchange('product_id')
    def product_id_change(self):
        self.sales_margin = 0.0
        res = super(SaleOrderLine, self).product_id_change()
        if self.product_id.sales_margin:
            self.price_unit = self.product_id.lst_price
            self.sales_margin = self.product_id.sales_margin
        return res


    @api.onchange('product_uom', 'product_uom_qty')
    def product_uom_change(self):
        res = super(SaleOrderLine, self).product_uom_change()
        if self.product_id.sales_margin:
            self.price_unit = self.product_id.lst_price
        return res

    #for the one sales order if margin is set then based on that unit price is also change. 
    @api.onchange('sales_margin')
    def sales_margin_change(self):
        for margin in self:
            if self.product_id and self.sales_margin:
                self.price_unit = self.product_id.standard_price / self.sales_margin

    #auto set sales margin and sales person in the invoice invoices are created as 'Regular invoice'
    def _prepare_invoice_line(self, **optional_values):
        res = super(SaleOrderLine, self)._prepare_invoice_line(**optional_values)
        res.update({'sales_margin': self.sales_margin,
                    'sales_person_ids':[(6,0,self.sales_person_ids.ids)]})
        return res
