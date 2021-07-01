# -*- coding: utf-8 -*-
from odoo import fields, models

class SaleReport(models.Model):
    _inherit = "sale.report"

    res_users_id = fields.Many2one('res.users', 'Salesperson Line Wise', readonly=True)
    
    #added a sales person line wise group by. but not showing the actual amount. 
    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        fields['res_users_id'] = ", rsl.res_users_id as res_users_id"
        groupby += ', rsl.res_users_id'
        from_clause +=  ' left join res_users_sale_order_line_rel rsl on (rsl.sale_order_line_id=l.id)'
        return super(SaleReport, self)._query(with_clause, fields, groupby, from_clause)
