# -*- coding: utf-8 -*-
# Part of Kiran Infosoft. See LICENSE file for full copyright and licensing details.

from odoo import api, models


class FloorwiseSummary(models.AbstractModel):
    _name = 'report.ki_floor_wise_sales.pos_floor_wise_summary_tmpl'

    @api.model
    def _get_report_values(self, docids, data=None):
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_id'))

        date_start = docs.start_date
        date_stop = docs.end_date
        floor_ids = docs.floor_ids

        pos_order_obj = self.env['pos.order']

        domain = [
                ('date_order', '>=' , date_start),
                ('date_order', '<=' , date_stop),
            ]

        if floor_ids:
            domain.append(('table_id.floor_id', 'in', floor_ids.ids))

        pos_order_ids = pos_order_obj.search(domain)

        floor_categ_wise_dict = {}

        for order in pos_order_ids:
            
            if order.table_id.floor_id not in floor_categ_wise_dict:
                floor_categ_wise_dict[order.table_id.floor_id] = {}
            
            for line in order.lines:
                floor_key = floor_categ_wise_dict[order.table_id.floor_id]
                if line.product_id not in floor_key:
                    amt = {
                        'amount_untaxed': line.price_subtotal,
                        'amount_taxed': line.price_subtotal_incl - line.price_subtotal,
                        'amount_total': line.price_subtotal_incl,
                        'qty': line.qty
                    }
                    floor_key[line.product_id] = amt
                else:
                    product_key = floor_key[line.product_id]
                    amount_untaxed = product_key['amount_untaxed']
                    amount_taxed = product_key['amount_taxed']
                    amount_total = product_key['amount_total']
                    qty = product_key['qty']
                    amt = {
                        'amount_untaxed': amount_untaxed + line.price_subtotal,
                        'amount_taxed': amount_taxed + (
                            line.price_subtotal_incl - line.price_subtotal
                        ),
                        'amount_total': amount_total + line.price_subtotal_incl,
                        'qty': line.qty + qty
                    }
                    product_key = amt

        docargs = {
            'doc_ids': self.ids,
            'doc_model': self.model,
            'docs': docs,
            'floor_categ_wise_dict':floor_categ_wise_dict,
        }
        return docargs
