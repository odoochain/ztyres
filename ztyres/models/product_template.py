# -*- coding: utf-8 -*-
from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    manufacturer_id = fields.Many2one('product.manufacturer', string='Fabricante')
    product_tier_id = fields.Many2one('product.tier', string='Tier')
    product_usage_id = fields.Many2one('product.segment', string='Uso')


    