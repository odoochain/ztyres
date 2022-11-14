from odoo import _, api, fields, models


class DeniedConfirmSale(models.TransientModel):
    _name = 'ztyres.wizard_denied_confirm_sale'
    _description = 'DeniedConfirmSale'