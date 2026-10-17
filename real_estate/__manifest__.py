{
    'name': 'Real Estate',
    'version': '1.1',
    'description': 'Learning odoo',
    'author': 'Mohamed Reyad',
    'depends': ['base','sale','mail','contacts'
                ],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'view/base_menu_view.xml',
        'view/property_view.xml',
        'view/owner_view.xml',
        'view/tag_view.xml',
        'view/sale_order_inherit.xml',
        'view/res_partner_view.xml',
        'reports/property_report.xml',
        'view/property_history_view.xml',
        'wizard/change_state.xml',

    ],
    'assets': {
        'web.assets_backend': ['real_estate/static/src/css/porperty.css', ],
       # 'web.report.assets_common': ['app_one/static/src/css/fonts_report.css', ],
    },

    'application': True,
}
