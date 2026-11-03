# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.exceptions import UserError

class Move(models.Model):
    _inherit = 'account.move'
    team_id = fields.Many2one('crm.team', string='Sales Team',compute='_calc_team_id',store=True)

    @api.depends('state')
    def _calc_team_id(self):
        for rec in self:
            invoice=self.env['account.invoice'].search([('move_id','=',rec.id)],limit=1)
            if invoice:
                rec.team_id=invoice.team_id
            else:
                rec.team_id=False


class Sale(models.Model):
    _inherit = 'sale.order'


    def create_invs(self):
        inv_obj = self.env['account.invoice']
        inv_obj_line = self.env['account.invoice.line']
        inv_data = self._prepare_invoice()
        invoice = inv_obj.create(inv_data)
        for line in self.order_line:
            val=line.invoice_line_create_vals(invoice.id, line.product_uom_qty)
            inv_obj_line.create(val)










