# -*- coding: utf-8 -*-

from odoo import fields, models

class SaleReport(models.Model):
    _inherit = 'sale.report'

    sales_person = fields.Many2one('res.users', 'Sales Person(s)', readonly=True)
    sale_line_id = fields.Many2one('sale.order.line', 'Sales Line', readonly=True)
    contribution_price = fields.Float(string='Total Exc. VAT (Salesperson)', readonly=True)

    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        fields['sale_line_id'] = ', spc.sale_line_id'
        fields['contribution_price'] = ', l.contribution_price'
        fields['sales_person'] = ', spc.user_id as sales_person'

        from_clause += ' right join sales_person_contribution spc on (spc.sale_line_id = l.id)'
        groupby += ', spc.sale_line_id,spc.user_id,l.contribution_price'

        return super(SaleReport, self)._query(with_clause, fields, groupby, from_clause)
