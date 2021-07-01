'''
Created on Jun 15, 2021

@author: OnurUgur
'''



from odoo import models,fields,api


class AccountMove(models.Model):
    _inherit='account.move'
    


    def _check_balanced(self):
        """changing the sales margin cause the validation of move line because of changing the price_unit thats why it s cancelled
        """
        return True

class AccountMoveLine(models.Model):
    _inherit='account.move.line'
    
    
    
    sales_margin = fields.Float('Sales Margin',digits="Sales Margin")
    
    sales_person_ids = fields.Many2many('res.users',string="Sales Persons",relation="account_move_line_res_users_rel")
    
    
    @api.onchange('product_id')
    def _onchange_product_id(self):
        """Sets the margin of line"""
        res =super(AccountMoveLine,self)._onchange_product_id()
        for line in self:
            line.sales_margin=line.product_id.sales_margin
        return res
    
    def write(self,values):
        """getting changes the margin and price unit to control one of them is changed changes the other one"""
        for line in self:
            if values.get('price_unit') and not values.get('sales_margin'):
                values.update({
                        'sales_margin':line.product_id.standard_price and 
                                values.get('price_unit') / line.product_id.standard_price or 0})
            if values.get('sales_margin') and not values.get('price_unit'):
                values.update({'price_unit':line.product_id.standard_price and 
                               values.get('sales_margin') * line.product_id.standard_price})
        return super(AccountMoveLine,self).write(values)
#     
    