# -*- coding: utf-8 -*-
{
    'name': 'Hide Export Button',
    'version': '12.0.1.0.0',
    'category': 'Tools',
    'summary': 'Hide export button based on user group access',
    'description': """
Hide Export Button
==================
This module allows you to hide the export functionality from users.
Only users with the "Show Export Button" access right can see and use export features.

Features:
- Hide export button from list/tree views
- Control via access group
- Easy user management
    """,
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'depends': ['base', 'web'],
    'data': [
        'security/export_security.xml',
        'views/res_users_views.xml',
        'views/assets.xml',
    ],
    'qweb': [
        'static/src/xml/list_view.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
