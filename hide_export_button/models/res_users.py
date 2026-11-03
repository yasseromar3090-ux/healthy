# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.model
    def check_export_access(self):
        """Check if current user has export access"""
        return self.env.user.has_group('hide_export_button.group_show_export_button')
