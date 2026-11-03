# -*- coding: utf-8 -*-

from odoo import models, fields, api



class usersalesteam(models.Model):
    _inherit = "res.users"
    sales_team=fields.Many2one('crm.team',string="Sales Team")

class SaleOrder(models.Model):
    _inherit = "sale.order"

    shipping_amount = fields.Float(string="Shipping Cost",required=True)
    discount_x=fields.Float("Total Discount",compute="_compute_discount_total",readonly=True)
    team_id=fields.Many2one('crm.team',related='user_id.sales_team')
    shipping_amount_total = fields.Monetary(store=True, readonly=True, compute='_amount_total_s', string=" Total After Shipping Cost")



    @api.depends('order_line.discount_x')
    def _compute_discount_total(self):
        for order in self:
            discount_x = 0.0
            for line in order.order_line:
                discount_x += line.discount_x

            order.update({
                'discount_x': discount_x,

            })



    @api.depends('shipping_amount','amount_total')
    def _amount_total_s(self):
        for rec in self:
            rec.shipping_amount_total = rec.shipping_amount + rec.amount_total


class SaleOrderline(models.Model):
    _inherit = "sale.order.line"

    discount_x = fields.Float(string=' Discount Amount')
    discount = fields.Float(string=' Discount')
    # dis=fields.Float('dis amount')

    @api.onchange('discount','discount_x')
    def change(self):
        for re in self:
            if re.discount:
                # re.dis=re.discount
                re.discount_x=round((re.price_unit*re.product_uom_qty)*(re.discount/100))
            elif re.discount_x:
                re.discount=((re.discount_x)/(re.price_unit*re.product_uom_qty))*100

    @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id')
    def _compute_amount(self):
        """
        Compute the amounts of the SO line.
        """
        for line in self:
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            taxes = line.tax_id.compute_all(price, line.order_id.currency_id, line.product_uom_qty,
                                            product=line.product_id, partner=line.order_id.partner_shipping_id)
            line.update({
                'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                'price_total': taxes['total_included'],
                'price_subtotal': round(taxes['total_excluded']),
            })


    # @api.onchange('discount_x')
    # def compute_dt(self):
    #     for ord in self:
    #         if ord.discount_x:
    #             ord.discount = ord.discount_x /ord.price_subtotal

            # if ord.discount:
            #     ord.discount_x = ord.price_subtotal*(ord.discount /100)








