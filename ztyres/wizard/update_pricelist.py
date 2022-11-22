from odoo import _, api, fields, models

# -*- coding: utf-8 -*-
from odoo import models, fields, api

class UpdatePricelist(models.TransientModel):
    _name = 'ztyres.wizard_update_pricelist'
    pricelist_id = fields.Many2one('product.pricelist', string='Tarifa')
    product_id = fields.Many2one('product.template', string='Aplicado en')
    min_quantity = fields.Float(string='Cantidad min.')
    fixed_price = fields.Float(string='precio')
    date_start = fields.Date(string='Fecha de inicio')
    date_end = fields.Date(string='Fecha final')

    def update_pricelist(self):
        pricelist = self.env['product.pricelist']
        for record in self:
            current = pricelist.browse(record.pricelist_id.id)
            values = {                
                'product_id':record.product_id.id,
                'min_quantity':record.min_quantity,
                'fixed_price':record.fixed_price,
                'date_start':record.date_start,
                'date_end':record.date_end
            }
            current.item_ids = [(0, 0, values)]
            print(current)


