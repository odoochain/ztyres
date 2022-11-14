# -*- coding: utf-8 -*-
{
    'name': "ztyres",

    'summary': """
        Personalizaciones y modificaciones realizadas a Odoo Enterprise 14.0 para la empresa ZTYRES.""",

    'description': """
Guía de modificaciones.
==========================================================================

Se describe de manera breve la funcionalidad, modificación, permiso ó característica instalada.

Contactos:
----------------------------
    Permisos:
    1. Modificación de RFC y Empresa relacionada de Contactos.

    2. Modificación de Forma de Pago y Política de Pago en facturas.

    3. The last one is available from the Analytic Chart of Accounts. It gives
       the spreading, for the selected Analytic Accounts of Budgets.

    Make the lock date irreversible:

    * You cannot define stricter conditions on advisors than on users. Then, the lock date on advisor must be set before the lock date for users.
    * You cannot lock a period that is not finished yet. Then, the lock date for advisors must be set before the last day of the previous month.
    * The new lock date for advisors must be set after the previous lock date.
    """,

    'author': "José Roberto Mejía Pacheco",
    'website': "https://mx.linkedin.com/in/jrmpacheco",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Customizations',
    'version': '14.0.0.0',

    # any module necessary for this one to work correctly
    'depends': ['stock','contacts','base','sale','account','l10n_mx_edi'],

    # always loaded
    'data': [
        'data/stock.production.lot.week.csv',
        'data/stock.production.lot.year.csv',
        'security/security.xml',
        'security/ir.model.access.csv',
        # 'views/account_move.xml',
        'views/account_views.xml',
        # 'views/res_partner_views.xml',
        'views/sale_order_report.xml',
        'views/sale_views.xml',
        'views/stock_production_lot_views.xml',
        'wizard/denied_confirm_sale.xml',
        'wizard/merge_quotations.xml',
        # 'views/stock_picking_views.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
