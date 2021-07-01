# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class SaleReport(models.Model):
    _inherit = 'sale.report'


    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        from_clause += """
                    LEFT JOIN sale_order so ON (so.user_id in (
                SELECT id FROM res_users  as ru WHERE l.id = ru.sale_id and l.order_id= so.id
            ))
                """
        return super(SaleReport, self)._query(with_clause, fields, groupby, from_clause)
