from odoo import _, api, fields, models


class Manufacturer(models.Model):
    _name = 'product.manufacturer'
    _description = 'New Description'
    _sql_constraints = [
        ("name_uniq", "unique(name)", "El nombre debe ser único para marca.")
    ]    
    name = fields.Char(string='Nombre de marca')
    
