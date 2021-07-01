'''
Created on Jun 14, 2021

@author: Onurugur
'''


from odoo import models,fields,api



class ProductTemplate(models.Model):
    _inherit='product.template'
    
    
    
    sales_margin = fields.Float('Sales Margin',digits="Sales Margin")
    
    @api.onchange('sales_margin')
    def _onchange_sales_margin_standard_price(self):
        """ i think calculation must be this format given format that cost /margin =list price cause
        the list price is smaller than cost."""
        if self.sales_margin:
            self.list_price =  self.standard_price*self.sales_margin