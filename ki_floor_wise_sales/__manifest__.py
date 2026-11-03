# -*- coding: utf-8 -*-
# Part of Kiran Infosoft. See LICENSE file for full copyright and licensing details.

{
    'name': "Floor wise Product Sales Report",
    'summary': """Floor wise Product Sales Report""",
    'description': """
Floor wise Product Sales Report
    """,
    'version': "1.0",
    'category': "Point of Sale",
    'author': "Kiran Infosoft",
    'website': "http://www.kiraninfosoft.com",
    'license': 'Other proprietary',
    'price': 0.0,
    'currency': "EUR",
    'images': ['static/description/logo.png'],
    "depends": [
        'pos_restaurant'
    ],
    "data": [
        'report/report_view.xml',
        'wizard/floorwise_report_wizard_view.xml',
    ],
    'application': False,
    'installable': True,
}
