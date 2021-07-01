'''
Created on Jun 15, 2021

@author: OnurUgur
'''
from odoo import fields, models


class SaleReport(models.Model):
    _inherit = 'sale.report'

    sales_person_id = fields.Many2one('res.users','SalesPerson')
    sales_person_amount = fields.Float('Sales Person Per Amount')
    # getting query values with new model and addin it left join the get assignment
    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        fields['sales_person_id'] = ", per.user_id as sales_person_id"
        fields['sales_person_amount'] = ", l.per_person_subtotal AS sales_person_amount"
        
        groupby += ', per.user_id,l.per_person_subtotal'
        from_clause+='left join sale_order_line_person per on (l.id = per.sale_line_id)'
        return super(SaleReport, self)._query(with_clause, fields, groupby, from_clause)