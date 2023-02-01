from odoo import _, api, fields, models


class SalePromotions(models.Model):
    _name = 'ztyres.sale_promotion_line'
    _description = 'New Description'
    _rec_name = 'sale_promotion_id'

    sale_promotion_id = fields.Many2one('ztyres.sale_promotion')
    manufacturer_ids = fields.Many2many('product.manufacturer', string='Fabricante')
    product_tier_ids = fields.Many2many('product.tier', string='Tier')
    product_usage_ids = fields.Many2many('product.segment', string='Uso')
    discunt = fields.Float(string='% de Descuento')
    qty = fields.Float(string='Cantidad de Llantas')
    





