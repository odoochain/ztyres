from odoo import _, api, fields, models

class ModelName(models.TransientModel):
    _name = 'ztyres.update_pricelist_confirm_import'
    _description = 'ztyres.update_pricelist_confirm_import'

    def action_done(self):
        self.env['ztyres.wizard_update_pricelist'].search([]).update_pricelist()    
