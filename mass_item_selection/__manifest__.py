# -*- coding: utf-8 -*-
# © 2015 Elico Corp (www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Mass item selection',
    'version': "12.0.0.1",
    'depends': [
        'sale',
        'purchase',
        'stock',
        'account',
    ],
    'author': 'Elico Corp',
    'license': 'AGPL-3',
    'website': 'https://www.elico-corp.com',
    'data': [
        'wizard/mass_item_selection.xml',
        'wizard/mass_items_confirm.xml',
        'wizard/mass_items_quantities.xml',
        'views/mass_item_selection.xml',
        'views/quantity.xml',
    ],
    'installable': True,
    'application': False,
}
