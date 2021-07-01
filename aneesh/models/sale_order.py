# -*- coding: utf-8 -*-
from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    sales_margin = fields.Float(
        string='Margin',
        digits=(16, 2),
        states={'draft': [('readonly', False)]},
        help='The sales margin amount')

    cost_price = fields.Float(
        string='Cost', compute="_compute_cost_price",
        digits='Product Price', store=True, readonly=True,
        )

    sales_person_ids = fields.Many2many(
        'res.users',
         string='Salespersons',
        store=True,
        required=True,
        )

    contribution_price = fields.Float(
        string='Turnover Exc. Tax',
        store=True, readonly=True,
        compute='_compute_contribution_price',
        )

    @api.depends('sales_person_ids', 'price_subtotal')
    def _compute_contribution_price(self):
        # calculate the contribution price price
        for val in self:
            if len(val.sales_person_ids) > 0 and val.price_subtotal > 0:
                val.contribution_price = val.price_subtotal / len(val.sales_person_ids)

    @api.depends('product_id', 'company_id', 'currency_id', 'product_uom')
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
            to_currency = line.currency_id or line.order_id.currency_id
            if line.product_uom and line.product_uom != product.uom_id:
                product_cost = product.uom_id._compute_price(
                    product_cost,
                    line.product_uom,
                )
            line.cost_price = from_currency._convert(
                from_amount=product_cost,
                to_currency=to_currency,
                company=line.company_id or self.env.company,
                date=line.order_id.date_order or fields.Date.today(),
                round=False,
            ) if to_currency and product_cost else product_cost

    @api.onchange('product_id')
    def product_id_change(self):
        result = super(SaleOrderLine, self).product_id_change()
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

    def _prepare_invoice_line(self, **optional_values):
        res = super(SaleOrderLine, self)._prepare_invoice_line()
        res['cost_price'] = self.cost_price
        res['sales_users_ids'] = self.sales_person_ids.ids
        res['sales_margin'] = self.sales_margin
        return res


class SaleOrder(models.Model):
    _inherit = "sale.order"

    total_sales_margin = fields.Float("Sales Margin", compute='_compute_sales_margin', store=True)

    @api.depends('order_line.sales_margin', 'amount_untaxed')
    def _compute_sales_margin(self):
        self.total_sales_margin = sum(self.order_line.mapped('sales_margin'))

    sales_person_contribution = fields.One2many(
        'sales.person.contribution',
        'sale_id',
        compute='compute_sales_person_contribution',
        string='Contribution Lines',
        states={'draft': [('readonly', False)]},
        store=True,
        copy=False)

    @api.depends('order_line', 'order_line.sales_person_ids')
    def compute_sales_person_contribution(self):
        subline = []
        self.update({'sales_person_contribution': [(6, 0, [])]})
        for line_id in self.order_line:
            no_of_person = len(line_id.sales_person_ids)
            for user in line_id.sales_person_ids:
                check = [user_list for user_list in subline if
                         user_list.get('sale_line_id') == line_id.id and user_list.get('user_id') == user.id]
                if not check:
                    subline.append({
                        'sale_id': self.id,
                        'name': line_id.name,
                        'user_id': user.id,
                        'user_name': user.name,
                        'amount': line_id.price_subtotal / no_of_person,
                        'product_id': line_id.product_id.id,
                        'sale_line_id': line_id.id,
                    })
        line = [(0, 0, l) for l in subline]
        self.sales_person_contribution = line


class SalesPersonContribution(models.Model):
    _name = "sales.person.contribution"
    _description = "Sales Person Contribution"

    sale_id = fields.Many2one('sale.order', string='Sales', ondelete='cascade', index=True)
    sale_line_id = fields.Many2one('sale.order.line', string='Sale Line')
    name = fields.Char(string='Description', required=True)
    product_id = fields.Many2one('product.product', string='Product', required=True)
    user_id = fields.Many2one('res.users', string='Sales User')
    user_name = fields.Char(string='Sales Person')
    amount = fields.Monetary('Turnover Exc. Tax')
    company_id = fields.Many2one('res.company', string='Company', related='sale_id.company_id', store=True,
                                 readonly=True)
    currency_id = fields.Many2one('res.currency', related='sale_id.currency_id', store=True, readonly=True)
