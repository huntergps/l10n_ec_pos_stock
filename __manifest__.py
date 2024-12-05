# -*- coding: utf-8 -*-
{
    "name": "Ecuadorian Stock Sync in POS",
    'version': '18.01',
    'summary': 'Customization module for Ecuadorian localization to Stock Sync in POS',
    "version": "18.0.0.0",
    "category": "Point of Sale",
    'maintainer': 'Elmer Salazar Arias',
    'website': 'http://www.galapagos.tech',
    'email': 'esalazargps@gmail.com',
    'license': 'LGPL-3',
    "depends": ['base', 'sale_management', 'stock', 'point_of_sale'],
    "data": [
        'views/custom_pos_config_view.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'l10n_ec_pos_stock/static/src/css/stock.css',

            'l10n_ec_pos_stock/static/src/app/generic_components/product_card/product_card.xml',
            'l10n_ec_pos_stock/static/src/app/generic_components/product_card/product_card.js',

            'l10n_ec_pos_stock/static/src/app/screens/product_screen/product_list/product_list.js',
            # 'l10n_ec_pos_stock/static/src/app/screens/product_screen/product_screen.xml',

            'l10n_ec_pos_stock/static/src/app/screens/product_screen/product_low_stock_screen/product_low_stock_screen.js',
            'l10n_ec_pos_stock/static/src/app/screens/product_screen/product_low_stock_screen/product_low_stock_screen.xml',

            'l10n_ec_pos_stock/static/src/app/screens/product_screen/product_low_stock_screen/low_stock_line/low_stock_line.js',
            'l10n_ec_pos_stock/static/src/app/screens/product_screen/product_low_stock_screen/low_stock_line/low_stock_line.xml',

            'l10n_ec_pos_stock/static/src/app/generic_components/order_widget/order_widget.js',
            'l10n_ec_pos_stock/static/src/app/generic_components/order_widget/order_widget.xml',

            'l10n_ec_pos_stock/static/src/app/navbar/navbar.js',
            'l10n_ec_pos_stock/static/src/app/navbar/navbar.xml',

            'l10n_ec_pos_stock/static/src/app/store/models.js',
        ],
    },
    "auto_install": False,
    "installable": True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
