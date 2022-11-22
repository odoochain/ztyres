from odoo import _, api, fields, models


class Usage(models.Model):
    _name = 'product.segment'
    _description = 'New Description'
    _sql_constraints = [
        ("name_uniq", "unique(code)", "El código debe ser único para uso.")
    ]   
    active = fields.Boolean(default=True)
    name = fields.Char(string='Nombre')
    code = fields.Char(string='Código')