# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.tools import float_round



class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    reward_id = fields.Many2one('loyalty.reward', string="Loyalty Reward")







class SaleOrder(models.Model):
    _inherit = 'sale.order'

    loyalty_points = fields.Float(string="Loyalty Points Earned", compute="_compute_loyalty_points", store=True)

    @api.depends('order_line.product_id', 'order_line.price_subtotal')
    def _compute_loyalty_points(self):
        for order in self:
            # Fetch any active loyalty program
            loyalty_program = self.env['loyalty.program'].search([], limit=1)

            if not loyalty_program:
                order.loyalty_points = 0
                continue

            points = 0
            for line in order.order_line:
                points += (line.price_subtotal * loyalty_program.pp_currency)
                points += (line.product_uom_qty * loyalty_program.pp_product)

                for rule in loyalty_program.rule_ids:
                    if rule.rule_type == 'product' and rule.product_id == line.product_id:
                        points += (line.product_uom_qty * rule.pp_product)
                        points += (line.price_subtotal * rule.pp_currency)

                    if rule.rule_type == 'category' and rule.category_id in line.product_id.categ_id.parent_path:
                        points += (line.product_uom_qty * rule.pp_product)
                        points += (line.price_subtotal * rule.pp_currency)

            order.loyalty_points = round(points, int(loyalty_program.rounding))

    def action_confirm(self):
        """ Overrides the confirm method to apply loyalty rewards. """
        res = super(SaleOrder, self).action_confirm()

        for order in self:
            if not order.partner_id:
                continue

            # Find an active loyalty program
            loyalty_program = self.env['loyalty.program'].search([], limit=1)
            if not loyalty_program:
                continue

            # Fetch applicable rewards
            available_rewards = self.env['loyalty.reward'].search([
                ('loyalty_program_id', '=', loyalty_program.id),
                ('minimum_points', '<=', order.partner_id.loyalty_points)
            ], order='minimum_points desc')  # Prioritize highest-value rewards

            if available_rewards:
                best_reward = available_rewards[0]  # Pick the highest-ranked reward
                order.apply_loyalty_reward(best_reward)

            # Ensure loyalty points never go negative
            order.partner_id.loyalty_points = max(0, order.partner_id.loyalty_points + order.loyalty_points)

        return res

    def apply_loyalty_reward(self, reward):
        """ Applies a selected loyalty reward automatically. """
        if not self.partner_id or self.partner_id.loyalty_points < reward.point_cost:
            return

        if reward.reward_type == 'gift':
            self.order_line.create({
                'order_id': self.id,
                'product_id': reward.gift_product_id.id,
                'product_uom_qty': 1,
                'price_unit': 0,
                'reward_id': reward.id,
            })

        elif reward.reward_type == 'discount':
            discount_amount = self.amount_total * (reward.discount / 100)
            discount_product = reward.discount_product_id

            self.order_line.create({
                'order_id': self.id,
                'product_id': discount_product.id,
                'product_uom_qty': 1,
                'price_unit': -discount_amount,
                'reward_id': reward.id,
            })

        elif reward.reward_type == 'resale':
            resale_product = reward.point_product_id
            if resale_product.list_price > 0:
                resale_qty = min(self.partner_id.loyalty_points / resale_product.list_price, self.amount_total / resale_product.list_price)

                self.order_line.create({
                    'order_id': self.id,
                    'product_id': resale_product.id,
                    'product_uom_qty': -resale_qty,
                    'reward_id': reward.id,
                })

        # Deduct used points, ensuring they don't go negative
        self.partner_id.loyalty_points = max(0, self.partner_id.loyalty_points - reward.point_cost)
