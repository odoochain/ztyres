from odoo import _, api, fields, models


class SalePromotions(models.Model):
    _name = 'ztyres.sale_promotion'
    _description = 'New Description'
    active = fields.Boolean(default=True)
    name = fields.Char(string='Nombre')
    start_date = fields.Date(string='Fecha inicio')
    end_date = fields.Date(string='Fecha final')     
    sale_promotion_lines = fields.One2many('ztyres.sale_promotion_line', 'sale_promotion_id')
