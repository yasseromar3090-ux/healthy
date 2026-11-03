# -*- coding: utf-8 -*-

from odoo import models, api, _
from odoo.exceptions import AccessError


class Base(models.AbstractModel):
    _inherit = 'base'

    @api.multi
    def export_data(self, fields_to_export, raw_data=False):
        """Override export_data to check access"""
        if not self.env.user.has_group('hide_export_button.group_show_export_button'):
            raise AccessError(_('You do not have permission to export data.'))
        return super(Base, self).export_data(fields_to_export, raw_data)
