# -*- coding: utf-8 -*-
from odoo import models, fields, api,_

class StockProductionLotWeek(models.Model):
    _name = 'stock.production.lot.week'
    _rec_name = 'week'
    week = fields.Char(string='Semana',size=2)
    @api.model
    def create(self, values):
        # CODE HERE
        res = super(StockProductionLotWeek, self).create(values)    
        return res