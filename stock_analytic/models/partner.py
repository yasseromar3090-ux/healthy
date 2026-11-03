from odoo import api, fields, models
from odoo.exceptions import ValidationError


class Customer(models.Model):
    _inherit = 'res.partner'

    @api.constrains('mobile', 'phone')
    def check_mobile_phone(self):
        for record in self:
            if record.mobile:
                mobile_partners = self.env['res.partner'].search([
                    ('mobile', '=', record.mobile),
                    ('id', '!=', record.id)
                ])
                if mobile_partners:
                    raise ValidationError("Mobile Number already exists: {}".format(record.mobile))

                phone_partners = self.env['res.partner'].search([
                    ('phone', '=', record.mobile),
                    ('id', '!=', record.id)
                ])
                if phone_partners:
                    raise ValidationError("Mobile Number already exists: {}".format(record.mobile))

            if record.phone:
                phone_partners = self.env['res.partner'].search([
                    ('phone', '=', record.phone),
                    ('id', '!=', record.id)
                ])
                if phone_partners:
                    raise ValidationError("Phone Number already exists: {}".format(record.phone))

                mobile_partners = self.env['res.partner'].search([
                    ('mobile', '=', record.phone),
                    ('id', '!=', record.id)
                ])
                if mobile_partners:
                    raise ValidationError("Phone Number already exists: {}".format(record.phone))

