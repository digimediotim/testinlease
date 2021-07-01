# -*- coding: utf-8 -*-
from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)

class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    sales_margin = fields.Float(
        string='Margin',
        digits=(16, 2),
        states={'draft': [('readonly', False)]},
        help='The sales margin amount')
    cost_price = fields.Float(
        string='Cost', compute="_compute_cost_price",
        digits='Product Price', store=True, readonly=False,
        )
    sales_users_ids = fields.Many2many(
        'res.users',
        string='Salespersons',
        store=True,
        readonly=True
        )
    contribution_price = fields.Float(
        string='Turnover Exc. Tax',
        store=True, readonly=False,
        compute='_compute_contribution_price',
        )

    def _copy_data_extend_business_fields(self, values):
        # OVERRIDE to copy the 'user_ids' field as well.
        super(AccountMoveLine, self)._copy_data_extend_business_fields(values)
        values['sales_users_ids'] = [(6, None, self.sales_users_ids.ids)]

    @api.depends('sales_users_ids', 'price_subtotal')
    def _compute_contribution_price(self):
        for val in self:
            if len(val.sales_users_ids) > 0 and val.price_subtotal > 0:
                val.contribution_price = val.price_subtotal / len(val.sales_users_ids)

    @api.depends('product_id', 'company_id', 'currency_id', 'product_uom_id')
    def _compute_cost_price(self):
        for line in self:
            if not line.product_id:
                line.cost_price = 0.0
                continue
            line = line.with_company(line.company_id)
            product = line.product_id
            product_cost = product.standard_price
            if not product_cost:
                line.cost_price = 0.0
                continue
            from_currency = product.cost_currency_id
            to_currency = line.currency_id or line.move_id.currency_id
            if line.product_uom_id and line.product_uom_id != product.uom_id:
                product_cost = product.uom_id._compute_price(
                    product_cost,
                    line.product_uom_id,
                )
            line.cost_price = from_currency._convert(
                from_amount=product_cost,
                to_currency=to_currency,
                company=line.company_id or self.env.company,
                date=line.move_id.invoice_date or fields.Date.today(),
                round=False,
            ) if to_currency and product_cost else product_cost

    @api.onchange('product_id')
    def _onchange_product_id(self):
        result = super(AccountMoveLine, self)._onchange_product_id()
        self.update({'sales_margin': self.product_id.sales_margin})
        return result

    @api.onchange('sales_margin')
    def onchange_sales_margin(self):
        if self.cost_price > 0 and self.sales_margin > 0:
            self.update({'price_unit': self.cost_price / self.sales_margin})

    @api.onchange('price_unit')
    def onchange_price_unit(self):
        if self.cost_price > 0 and self.price_unit:
            self.update({'sales_margin': self.cost_price / self.price_unit})


class AccountMove(models.Model):
    _inherit = "account.move"

    total_sales_margin = fields.Float("Margin", compute='_compute_sales_margin', store=True)

    @api.depends('invoice_line_ids.sales_margin', 'amount_untaxed')
    def _compute_sales_margin(self):
        self.total_sales_margin = sum(self.invoice_line_ids.mapped('sales_margin'))
