# -*- coding: utf-8 -*-

from odoo import models, fields, api

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





