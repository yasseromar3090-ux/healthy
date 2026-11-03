# -*- coding: utf-8 -*-

from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit='sale.order'

    x_check_after_delivered = fields.Boolean(string='Check After Delivered')
    x_inventory_id = fields.Integer(string='inventory_id')
    country_id = fields.Many2one(comodel_name='res.country',string='Country',related='partner_id.country_id',store=True)
    state_id = fields.Many2one(comodel_name='res.country.state',string='State',related='partner_id.state_id',store=True)
    x_city = fields.Char(string='المحافظة',related='country_id.name',store=True)
    x_mobile = fields.Char(string='mobile',related='partner_id.mobile',store=True)
    x_street = fields.Char(string='Street',related='partner_id.street',store=True)
    x_street_city = fields.Char(string='المنطقة',related='state_id.name',store=True)
class StockPicking(models.Model):
    _inherit='stock.picking'

    x_street_2 = fields.Char(string='المنطقة',related='partner_id.street2',store=True)
    x_user_id = fields.Many2one(comodel_name='res.users',string='Salesman',related='sale_id.user_id',store=True)
