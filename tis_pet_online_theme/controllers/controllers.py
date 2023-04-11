# -*- coding: utf-8 -*-
# This module and its content is copyright of Technaureus Info Solutions Pvt.Ltd.
# - © Technaureus Info Solutions Pvt. Ltd 2020. All rights reserved.


from odoo import http
from odoo.http import request
from openerp.addons.website_sale.controllers.main import WebsiteSale


class website_sale(WebsiteSale):

    @http.route(['/shop/cart/update/product'], type='http', auth="public", methods=['GET'], website=True)
    def cart_update_product(self, product_id, add_qty=1, set_qty=0, **kw):
        try:
            add_qty = float(add_qty)
        except ValueError:
            return None
        if add_qty <= 0.0:
            return None
        request.website.sale_get_order(force_create=1)._cart_update(product_id=int(product_id), add_qty=add_qty,
                                                                    set_qty=float(set_qty))
        if request.httprequest.headers and request.httprequest.headers.get('Referer'):
            return request.redirect(str(request.httprequest.headers.get('Referer')))
        return request.redirect('/shop')

    @http.route(['/shop/cart/update_json'], type='json', auth="public", methods=['POST'], website=True, csrf=False)
    def cart_update_json(self, product_id, line_id=None, add_qty=None, set_qty=None, display=True):
        res = super(website_sale, self).cart_update_json(
            product_id=product_id, line_id=None, add_qty=add_qty, set_qty=set_qty, display=display)
        order = request.website.sale_get_order()
        if order.order_line:
            amount = "{:0.2f}".format(order.amount_total)
            res['cart_amount'] = order.currency_id.symbol + ' ' + amount
        return res

    @http.route(['/shop/cart/update_option'], type='http', auth="public", methods=['POST'], website=True,
                multilang=False)
    def cart_options_update_json(self, product_id, add_qty=1, set_qty=0, goto_shop=None, lang=None, **kw):
        res = super(website_sale, self).cart_options_update_json(
            product_id, add_qty=1, set_qty=0, goto_shop=None, lang=None, **kw)
        res = {}
        order = request.website.sale_get_order()
        if order.order_line:
            amt = "{:0.2f}".format(order.amount_total)
            amount = order.currency_id.symbol + ' ' + amt
            res = '{"cart_quantity": "%s", "cart_amount": "%s"}' % (
                str(order.cart_quantity), amount)
        return res
