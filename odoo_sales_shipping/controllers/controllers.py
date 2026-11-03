# -*- coding: utf-8 -*-
from odoo import http

# class OdooSalesShipping(http.Controller):
#     @http.route('/odoo_sales_shipping/odoo_sales_shipping/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/odoo_sales_shipping/odoo_sales_shipping/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('odoo_sales_shipping.listing', {
#             'root': '/odoo_sales_shipping/odoo_sales_shipping',
#             'objects': http.request.env['odoo_sales_shipping.odoo_sales_shipping'].search([]),
#         })

#     @http.route('/odoo_sales_shipping/odoo_sales_shipping/objects/<model("odoo_sales_shipping.odoo_sales_shipping"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('odoo_sales_shipping.object', {
#             'object': obj
#         })