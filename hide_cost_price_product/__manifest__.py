# -*- coding: utf-8 -*-
{
    'name': "Hide Cost Price Product",
    'summary': """Hide Cost Price For Product In Tree And Form View Odoo""",

    'description': """
       hide cost price in odoo product with group named Show Cost Price, hide cost price in variant, hide cost price in product template
    """,
    'category': 'Product',
    'version': '0.1',
    'license': 'LGPL-3',
    'depends': ['base', 'purchase','product','stock'],
    'data': [
        'security/group_view.xml',
        'views/views.xml',
    ],

}
