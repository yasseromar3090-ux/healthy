# Copyright (C) 2020 Brahoo
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models,fields
import re
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class User(models.Model):
    _inherit = "res.users"
    analytic_account_id = fields.Many2one(
        string='Analytic Account',
        comodel_name='account.analytic.account',
    )
class Partner(models.Model):
    _inherit = "res.partner"

    @api.model
    def create(self, values):
        res=super(Partner, self).create(values)
        if not res.country_id and res.customer:
            raise ValidationError("Country Required")
        if not res.mobile and res.customer:
            raise ValidationError("Mobile Required")
        return res




    @api.constrains('phone', 'mobile')
    def _check_phone_mobile_format(self):
        phone_pattern = re.compile(r'^\+\d{11,15}$')  
        for record in self:
            if record.phone and not phone_pattern.match(record.phone):
                raise ValidationError("Phone must be in the format: +20xxxxxxxxx.")
            if record.mobile and not phone_pattern.match(record.mobile):
                raise ValidationError("Mobile must be in the format: +20xxxxxxxxx.")


class Sale(models.Model):
    _inherit = "sale.order"
    analytic_account_id = fields.Many2one('account.analytic.account', 'Analytic Account', readonly=False,
                                          states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
                                          help="The analytic account related to a sales order.", copy=False,
                                          oldname='project_id',related='user_id.analytic_account_id',store=True)


class SaleOrderReport(models.AbstractModel):
    _name = 'report.user_analytic.report_sales_order_template'
    _description = 'Sales Order Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['sale.order'].browse(docids)
        total=0
        grouped_products_lst=[]
        for doc in docs:
            product_quantities = {}
            for line in doc.order_line:
                if line.product_id not in product_quantities:
                    product_quantities[line.product_id] = 0
                product_quantities[line.product_id] += line.product_uom_qty

            # Create a list of grouped products with quantities
            for product, qty in product_quantities.items():
                total+=qty
                grouped_products_lst.append({'product_id': product.name, 'quantity': qty} )
        print("grouped_products_lst",docs[0])


        return {
            'doc_ids': docids,
            'doc_model': 'sale.order',
            'total': total,
            'docs': docs,
            'user_id': docs[0].user_id.name,
            'date_order': docs[0].date_order.strftime('%A'),
            'date_order2': docs[0].date_order.strftime('%d/%m/%Y'),
            'grouped_products_lst':grouped_products_lst,
        }
class StockReport(models.AbstractModel):
    _name = 'report.user_analytic.report_stock_order_template'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['stock.picking'].browse(docids)
        total=0
        grouped_products_lst=[]
        for doc in docs:
            product_quantities = {}
            for line in doc.move_ids_without_package:
                if line.product_id not in product_quantities:
                    product_quantities[line.product_id] = 0
                product_quantities[line.product_id] += line.quantity_done

            # Create a list of grouped products with quantities
            for product, qty in product_quantities.items():
                total+=qty
                grouped_products_lst.append({'product_id': product.name, 'quantity': qty} )
        print("grouped_products_lst",docs[0])


        return {
            'doc_ids': docids,
            'doc_model': 'stock.picking',
            'total': total,
            'docs': docs,
            'user_id': docs[0].x_user_id.name,
            'date_order': docs[0].scheduled_date.strftime('%A'),
            'date_order2': docs[0].scheduled_date.strftime('%d/%m/%Y'),
            'grouped_products_lst':grouped_products_lst,
        }