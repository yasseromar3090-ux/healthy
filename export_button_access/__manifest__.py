# -*- coding: utf-8 -*-
{
    'name': 'Export Button Access Control',
    'version': '12.0.1.0.0',
    'category': 'Tools',
    'summary': 'Control export button visibility with access groups',
    'description': """
Export Button Access Control
=============================
This module adds access control to the export button in list views.
Only users in the "Export Data" group can see and use the export functionality.
    """,
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'depends': ['base', 'web'],
    'data': [
        'security/export_security.xml',
        'views/assets.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
