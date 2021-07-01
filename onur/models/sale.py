'''
Created on Jun 14, 2021

@author: OnurUgur
'''


from odoo import models,fields,api,_




class SaleOrderLinePerson(models.Model):
    _name ="sale.order.line.person"
    
    
    sale_line_id = fields.Many2one('sale.order.line','Sale Line')
    user_id = fields.Many2one('res.users',"Sales Person")
    
    
    def name_get(self):
        """This model needs be calculate the sale.report cannot get relation over m2m fields. """
        result = []
        for line in self:
            name = line.user_id.name
            result.append((line.id, name))
        return result


class SaleOrderLine(models.Model):
    _inherit='sale.order.line'
    
    
    sales_margin = fields.Float('Sales Margin',digits="Sales Margin")
    standard_price = fields.Monetary("Cost")
    
    sales_person_ids = fields.One2many('sale.order.line.person','sale_line_id',string="Sales Persons")
    m2m_sales_person_ids =fields.Many2many('res.users',string='Sales Persons',)
    per_person_subtotal = fields.Float('Personal Subtotal',compute="_compute_per_person_subtotal",store=True)
    
    
    @api.depends('price_subtotal','sales_person_ids')
    def _compute_per_person_subtotal(self):
        """ to calculate person s to total sale of with lines"""
        for line in self:
            if line.price_subtotal and line.sales_person_ids:
                line.per_person_subtotal=line.price_subtotal/len(line.sales_person_ids)
            else:
                line.per_person_subtotal=line.price_subtotal
    
    
    
    
    
    
    @api.onchange('product_id')
    def product_id_change(self):
        """changing product id will get the cost 
        there is a module that sales_margin but i can not say it as assignment that module is here('sales_margin')."""
        if not self.product_id:
            return
        res =super(SaleOrderLine,self).product_id_change()
        self.update({'sales_margin':self.product_id.product_tmpl_id.sales_margin,
                     'standard_price':self.product_id.product_tmpl_id.standard_price})
        return res
    
    def write(self,values):
        """can be used compute inverse model but i prefer write function changes sales margin and price unit 
        if you enter both price unit and sales margin its not going chgange with calculations"""
        for line in self:
            if values.get('sales_margin') and not values.get('price_unit'):
                margin=values.get('sales_margin')
                values.update({'price_unit':line.product_id.standard_price*margin,
                               'standard_price':line.product_id.standard_price})
            if values.get('price_unit') and not values.get('sales_margin'):
                price_unit=values.get('price_unit')
                values.update({'sales_margin':price_unit/line.product_id.standard_price,
                               'standard_price':line.product_id.standard_price})
            if values.get('m2m_sales_person_ids'):
                line.sales_person_ids.unlink()
                for saleperson in values.get('m2m_sales_person_ids')[0][2]:
                    self.env['sale.order.line.person'].create({'user_id':saleperson,
                                                               'sale_line_id':line.id})
        return super(SaleOrderLine,self).write(values)
    
    def _prepare_invoice_line(self, **optional_values):
        """when creating invoice orderlines values is set here"""
        res = super(SaleOrderLine,self)._prepare_invoice_line(**optional_values)
        if self.sales_margin:
            res['sales_margin']=self.sales_margin
        if self.sales_person_ids:    
            res['sales_person_ids']=[(6,0,self.sales_person_ids.mapped('user_id').ids)]
        return res
    
