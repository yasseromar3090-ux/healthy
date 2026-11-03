# -*- coding: utf-8 -*-
# Part of Kiran Infosoft. See LICENSE file for full copyright and licensing details.

from datetime import datetime
from dateutil import relativedelta
from odoo import models, fields, api, _


class pos_floor_wise_report_wizard(models.TransientModel):
    _name = 'pos.floor.wise.report.wizard'

    start_date = fields.Date(
        string="Start Date",
        required=True,
        default=str(
            datetime.now() + relativedelta.relativedelta(day=1)
        )[:10]
    )
    end_date = fields.Date(
        string="End Date",
        required=True,
        default=str(
            datetime.now() + relativedelta.relativedelta(
                day=1, days=-1, months=+1
            )
        )[:10]
    )
    pos_id = fields.Many2one(
        'pos.config',
        string="Point Of Sale",
        required=True
    )
    floor_ids = fields.Many2many(
        'restaurant.floor',
        string='Floors',
        required=True
    )

    @api.multi
    def action_print_report(self):
        data = {}
        data.update({'form': self.read([])[0]})
        return self.env.ref(
            'ki_floor_wise_sales.action_pos_floor_wise_summary'
        ).report_action(self, data=data)
