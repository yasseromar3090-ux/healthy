# Copyright 2019 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Sales inv_balance Report',
    'summary': 'Add sale card report on Inventory Reporting.',
    'version': '12.0.1.0.0',
    'category': 'Warehouse',
    'website': 'https://github.com/OCA/stock-logistics-reporting',
    'author': 'Ecosoft,Odoo Community Association (OCA)',
    'license': 'AGPL-3',
    'depends': [
        'sale',

    ],
    'data': [

        'wizard/sale_inv_balance_report_wizard_view.xml',
    ],
    'installable': True,
}
