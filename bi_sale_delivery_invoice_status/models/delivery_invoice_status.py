# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _

class inherit_sale(models.Model):
	_inherit = "sale.order"

	#is_partially_delivery = fields.Boolean(string="Partially Delivered")
	is_fully_delivery = fields.Boolean(string="Fully Delivered")
	is_repeated = fields.Boolean(string="Repeated")
	is_Delayed = fields.Date(Date="Delayed To")

