from odoo import models,fields ,api,_
from odoo.exceptions import UserError

class sale_order(models.Model):
    _inherit='sale.order'

    Sales_Channel= fields.Selection([ ('type1', 'Facebook'),('type2', 'TV'),('type3', 'TeleSales'),],'Type', default='type1')
