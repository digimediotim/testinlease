# -*- coding: utf-8 -*-

from odoo import fields,api,models

class ProductTemplate(models.Model):
	_inherit = "product.template"

	sales_margin = fields.Float('Sales Margin', digits='Product Price', default=0.0)
	
	#set values for the cost price.  based on sales margin and standard price. 
	@api.onchange('sales_margin','standard_price')
	def onchange_list_price(self):
		if self.standard_price and self.sales_margin:
			self.list_price = self.standard_price / self.sales_margin


class ProductProduct(models.Model):
	_inherit = "product.product"

	sls_margin = fields.Float('Sales Margin', digits='Product Price', default=0.00)

	@api.depends('list_price', 'price_extra')
	@api.depends_context('uom')
	def _compute_product_lst_price(self):
		res = super(ProductProduct, self)._compute_product_lst_price()
		# set the value for sales margin from product.template to product.product. 
		for product in self:
			if product.sales_margin:
				product.sls_margin = product.sales_margin
		return res