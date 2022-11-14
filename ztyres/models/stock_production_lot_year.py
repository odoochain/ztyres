# -*- coding: utf-8 -*-
from odoo import models, fields, api,_

class StockProductionLotYear(models.Model):
    _name = 'stock.production.lot.year'
    _rec_name = 'year'
    year = fields.Char(string='Año',size=4)
    short_code = fields.Char(string='Año dos últimos digitos',size=2)

    @api.model
    def create(self, values):
        # CODE HERE
        res = super(StockProductionLotYear, self).create(values)
        return res