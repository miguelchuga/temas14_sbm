# -*- coding: utf-8 -*-
# This module and its content is copyright of Technaureus Info Solutions Pvt.Ltd.
# - © Technaureus Info Solutions Pvt. Ltd 2020. All rights reserved.


{
    'name': 'Theme Pet Online',
    'category': 'Theme/Ecommerce',
    'description': 'Website theme of Petonline..',
    'version': '14.0.0.5',
    'author': 'Technaureus Info Solutions Pvt. Ltd.',
    'website': 'https://www.technaureus.com',
    'sequence': 1,
    'price': 40,
    'currency': 'EUR',
    'license': 'Other proprietary',
    'live_test_url': 'https://themes.technaureus.com/web/database/selector',
    'depends': ['website_sale_wishlist'],
    'data': [
        'security/ir.model.access.csv',
        'views/h_f_petonline.xml',
        'views/homepage_petonline.xml',
        'views/views.xml'
    ],
    'images': [
        'static/description/banner.png',
        'static/description/theme_screenshot.jpg',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
