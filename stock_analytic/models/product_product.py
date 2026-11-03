# Copyright (C) 2020 Brahoo
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models,fields


class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.model
    def _anglo_saxon_sale_move_lines(self, name, product, uom, qty, price_unit,
                                     currency=False, amount_currency=False,
                                     fiscal_position=False,
                                     account_analytic=False,
                                     analytic_tags=False):
        res = super()._anglo_saxon_sale_move_lines(
            name,
            product,
            uom,
            qty,
            price_unit,
            currency=currency,
            amount_currency=amount_currency,
            fiscal_position=fiscal_position,
            account_analytic=account_analytic,
            analytic_tags=analytic_tags,
        )
        if res:
            res[0]['account_analytic_id'] = \
                account_analytic and account_analytic.id
            res[0]['analytic_tag_ids'] = \
                analytic_tags and analytic_tags.ids and \
                [(6, 0, analytic_tags.ids)] or False
        return res
class ProductCategory(models.Model):
    _inherit = "product.category"
    analytic_account_id = fields.Many2one(
        string='Analytic Account',
        comodel_name='account.analytic.account',
    )
class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    analytic_account_id = fields.Many2one(
        string='Analytic Account',
        comodel_name='account.analytic.account',compute='_calc_analytic_account_id',store=True,readonly=False
    )

    @api.multi
    def _prepare_invoice_line(self, qty):
        res = super()._prepare_invoice_line(qty)
        if self.analytic_account_id:
            res['account_analytic_id']=self.analytic_account_id.id
        return res

    @api.depends('product_id')
    def _calc_analytic_account_id(self):
        for rec in self:
            if rec.product_id.categ_id.analytic_account_id:
                rec.analytic_account_id=rec.product_id.categ_id.analytic_account_id.id
            else:
                rec.analytic_account_id =False

class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    @api.depends('product_id')
    @api.onchange('product_id')
    def _calc_analytic_account_id(self):
        for rec in self:
            if rec.product_id.categ_id.analytic_account_id:
                rec.account_analytic_id = rec.product_id.categ_id.analytic_account_id.id
            else:
                rec.account_analytic_id = False
class AccuntMoveLine(models.Model):
    _inherit = "account.move.line"

    def _prepare_invoice_line_from_po_line(self, line):
        res=super()._prepare_invoice_line_from_po_line(line)
        if line.analytic_account_id:
            res['account_analytic_id']=line.analytic_account_id.id
        return res
