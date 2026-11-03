# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.exceptions import UserError

class Move(models.Model):
    _inherit = 'account.move'
    team_id = fields.Many2one('crm.team', string='Sales Team',compute='_calc_team_id',store=False)
    source_doc = fields.Char('Source Document',compute='_calc_team_id',store=False)

    @api.depends('state')
    def _calc_team_id(self):
        for rec in self:
            invoice=self.env['account.invoice'].search([('move_id','=',rec.id)],limit=1)
            if invoice:
                rec.team_id=invoice.team_id
                rec.source_doc=invoice.origin
            else:
                rec.team_id=False
                rec.source_doc =False
                stock = self.env['stock.picking'].search([('name', '=', rec.ref)], limit=1)
                if stock:
                    sale = self.env['sale.order'].search([('name', '=', stock.origin)], limit=1)
                    if sale:
                        rec.team_id = sale.team_id
                        rec.source_doc = sale.name
                    else:
                        po = self.env['purchase.order'].search([('name', '=', stock.origin)], limit=1)
                        rec.team_id = False
                        rec.source_doc = po.name

                else:
                    rec.team_id = False
                    rec.source_doc = False


class Sale(models.Model):
    _inherit = 'sale.order'


    def _finalize_invoices(self, invoices, references):
        """
        Invoked after creating invoices at the end of action_invoice_create.
        :param invoices: {group_key: invoice}
        :param references: {invoice: order}
        """
        for invoice in invoices.values():
            invoice.compute_taxes()
            # if not invoice.invoice_line_ids:
            #     raise UserError(_(
            #         'There is no invoiceable line. If a product has a Delivered quantities invoicing policy, please make sure that a quantity has been delivered.'))
            # If invoice is negative, do a refund invoice instead
            if invoice.amount_total < 0:
                invoice.type = 'out_refund'
                for line in invoice.invoice_line_ids:
                    line.quantity = -line.quantity
            # Use additional field helper function (for account extensions)
            for line in invoice.invoice_line_ids:
                line._set_additional_fields(invoice)
            # Necessary to force computation of taxes and cash rounding. In account_invoice, they are triggered
            # by onchanges, which are not triggered when doing a create.
            invoice.compute_taxes()
            invoice._onchange_cash_rounding()
            invoice.message_post_with_view('mail.message_origin_link',
                values={'self': invoice, 'origin': references[invoice]},
                subtype_id=self.env.ref('mail.mt_note').id)






