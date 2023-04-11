# -*- coding: utf-8 -*-
# This module and its content is copyright of Technaureus Info Solutions Pvt.Ltd.
# - © Technaureus Info Solutions Pvt. Ltd 2020. All rights reserved.


from odoo import models, fields, api, SUPERUSER_ID
from odoo.addons import decimal_precision as dp

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    website_price = fields.Float('Website price', compute='_website_price', digits=dp.get_precision('Product Price'))
    # website_public_price deprecated, directly use _get_combination_info instead
    website_public_price = fields.Float('Website public price', compute='_website_price', digits=dp.get_precision('Product Price'))
    # website_price_difference deprecated, directly use _get_combination_info instead
    website_price_difference = fields.Boolean('Website price difference', compute='_website_price')

    def _website_price(self):
        current_website = self.env['website'].get_current_website()
        for template in self.with_context(website_id=current_website.id):
            res = template._get_combination_info()
            template.website_price = res.get('price')
            template.website_public_price = res.get('list_price')
            template.website_price_difference = res.get('has_discounted_price')

class website(models.Model):
    _inherit = 'website'

    def get_categories(self):
        categories = self.env['product.public.category'].sudo().search([])
        return categories

    def get_homepage_category(self):
        categories = self.env['homepage.category'].sudo().search([], order='sequence')
        return categories.mapped('category_id')

    def get_homepage_sliders(self):
        sliders = self.env['homepage.slider'].sudo().search([], order='sequence')
        return sliders

    def get_homepage_half_banner(self):
        banners = self.env['homepage.half.banner'].sudo().search([])
        return banners

    def get_homepage_products(self):
        products = self.env['homepage.product'].sudo().search([], order='sequence')
        return products.mapped('product_tmpl_id')

    def get_homepage_full_banner(self):
        banners = self.env['homepage.full.banner'].sudo().search([])
        return banners


class HomepageCategory(models.Model):
    _name = 'homepage.category'
    _rec_name = 'category_id'
    _order = 'sequence'

    category_id = fields.Many2one('product.public.category', string='Category')
    sequence = fields.Integer('Sequence', default=10)


class HomepageSlider(models.Model):
    _name = 'homepage.slider'
    _order = 'sequence'

    name = fields.Char('Name')
    image = fields.Binary('Slider Image', help="Slider image size must be 1920px x 845px.")
    sequence = fields.Integer('Sequence', default=10)


class HomepageHalfBanner(models.Model):
    _name = 'homepage.half.banner'

    name = fields.Char('Name')
    heading = fields.Char('Heading')
    caption = fields.Char('Caption')
    image = fields.Binary('Banner Image', help='Banner must be 555px x 261px size.')


class HomepageProduct(models.Model):
    _name = 'homepage.product'
    _order = 'sequence'

    product_tmpl_id = fields.Many2one('product.template', string='Product')
    sequence = fields.Integer('Sequence', default=10)


class HomepageFullBanner(models.Model):
    _name = 'homepage.full.banner'

    name = fields.Char('Name')
    image = fields.Binary('Banner Image', help='Banner must be 776px x 175px size.')


class IrModuleModule(models.Model):
    _name = "ir.module.module"
    _description = 'Module'
    _inherit = _name

    @api.model
    def _theme_remove(self, website):
        if website.theme_id.name == "tis_pet_online_theme":
            # default homepage set when un-install theme pet online
            header = self.env['ir.ui.view'].sudo().search([('name', '=', 'Website Petonline Header')])
            header.unlink()
            footer = self.env['ir.ui.view'].sudo().search([('name', '=', 'Petonline Footer')])
            footer.unlink()
            footer_cpy = self.env['ir.ui.view'].sudo().search([('name', '=', 'Pet Online Shop Footer Copyright')])
            footer_cpy.unlink()
            home = self.env['ir.ui.view'].sudo().search([('name', '=', 'Pet Online Home')])
            home.unlink()
            env = api.Environment(self.env.cr, SUPERUSER_ID, {})
            default_website = env.ref('website.default_website', raise_if_not_found=False)
            default_homepage = env.ref('website.homepage_page', raise_if_not_found=False)
            default_website.homepage_id = default_homepage.id
        return super(IrModuleModule, self)._theme_remove(website)
