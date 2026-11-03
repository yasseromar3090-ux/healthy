# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.exceptions import UserError

class Move(models.Model):
    _inherit = 'account.move'
    sale_team_id = fields.Many2one('crm.team', string='Sales Team',compute='_calc_team_id',store=True)
    source_doc = fields.Char('Source Document',compute='_calc_team_id',store=True)

    @api.depends('state')
    def _calc_team_id(self):
        for rec in self:
            invoice=self.env['account.invoice'].search([('move_id','=',rec.id)],limit=1)
            if invoice:
                rec.sale_team_id=invoice.team_id
                rec.source_doc=invoice.origin
            else:
                rec.sale_team_id=False
                rec.source_doc =False
                stock = self.env['stock.picking'].search([('name', '=', rec.ref)], limit=1)
                if stock:
                    sale = self.env['sale.order'].search([('name', '=', stock.origin)], limit=1)
                    if sale:
                        rec.sale_team_id = sale.team_id
                        rec.source_doc = sale.name
                    else:
                        po = self.env['purchase.order'].search([('name', '=', stock.origin)], limit=1)
                        rec.sale_team_id = False
                        rec.source_doc = po.name

                else:
                    rec.sale_team_id = False
                    rec.source_doc = False
class MoveLine(models.Model):
    _inherit = 'account.move.line'
    sale_team_id = fields.Many2one('crm.team', string='Sales Team',related='move_id.sale_team_id',store=True)
    source_doc = fields.Char('Source Document',related='move_id.source_doc',store=True)





class AccountInvoiceReport(models.Model):
    _inherit = 'account.invoice.report'
    origin = fields.Char(string='Source Document')
    call_center_id = fields.Many2one(
        comodel_name='res.users',
        string='موظف الكول سنتر',
        required=False)

    def _sub_select(self):
        return super(AccountInvoiceReport, self)._sub_select() + ",ai.origin as origin,ai.create_uid as call_center_id"

    def _select(self):
        return super(AccountInvoiceReport, self)._select() + ",sub.origin as origin,sub.call_center_id as call_center_id"

class SaleReport(models.Model):
    _inherit = "sale.report"

    call_center_id = fields.Many2one(
        comodel_name='res.users',
        string='موظف الكول سنتر',
        required=False)

    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        fields['call_center_id'] = ", s.create_uid as call_center_id"
        return super(SaleReport, self)._query(with_clause, fields, groupby, from_clause)
