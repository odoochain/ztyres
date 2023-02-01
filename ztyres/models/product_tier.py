from odoo import _, api, fields, models


class Tier(models.Model):
    _name = 'product.tier'
    _description = 'New Description'
    _sql_constraints = [
        ("name_uniq", "unique(code)", "El código debe ser único para tier.")
    ]    
    active = fields.Boolean(default=True)
    name = fields.Char(string='Nombre')
    code = fields.Char(string='Código')