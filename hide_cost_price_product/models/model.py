# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _


class ProductTemplate(models.Model):
    _inherit = "product.template"


    @api.model
    def fields_get(self, fields=None):
        fields_to_hide = ['standard_price']
        res = super(ProductTemplate, self).fields_get()
        for field in fields_to_hide:
            if self.env.user.has_group('hide_cost_price_product.hide_cost_price_custom')==False:
                res[field]['exportable'] = False
        return res
class Product(models.Model):
    _inherit = "product.product"


    @api.model
    def fields_get(self, fields=None):
        fields_to_hide = ['standard_price']
        res = super(Product, self).fields_get()
        for field in fields_to_hide:
            if self.env.user.has_group('hide_cost_price_product.hide_cost_price_custom')==False:
                res[field]['exportable'] = False
        return res