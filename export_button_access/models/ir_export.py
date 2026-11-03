# -*- coding: utf-8 -*-

from odoo import models, _
from odoo.exceptions import AccessError


class Base(models.AbstractModel):
    _inherit = 'base'

    def export_data(self, fields_to_export):
        """Override export_data to check for group access"""
        if not self.env.user.has_group('export_button_access.group_export_data'):
            raise AccessError(_('You do not have permission to export data. Please contact your administrator.'))
        return super(Base, self).export_data(fields_to_export)


class IrExport(models.Model):
    _inherit = 'ir.exports'

    def create(self, vals):
        """Check access when creating export templates"""
        if not self.env.user.has_group('export_button_access.group_export_data'):
            raise AccessError(_('You do not have permission to create export templates.'))
        return super(IrExport, self).create(vals)
