# -*- coding: utf-8 -*-
from odoo.exceptions import UserError
from odoo import models, fields, api,_

class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'
    week = fields.Many2one('stock.production.lot.week', string='Semana')
    year = fields.Many2one('stock.production.lot.year', string='Año')

    @api.model
    def create(self, values):
        print(values)
        if not values['week'] or not values['year']:
            raise UserError('Debe ingresar un valor para Año y Semana')
        name = self.week.browse(values['week']).week+self.year.browse(values['year']).short_code
        values.update({'name':name})
        res = super(StockProductionLot, self).create(values)
        return res
    
    
    def write(self, values):
        name = ''
        if 'week'in values.keys() and 'year'in values.keys():
            name = self.week.browse(values['week']).week+self.year.browse(values['year']).short_code
            values.update({'name':name})
            return super(StockProductionLot, self).write(values)
        if 'week'in values.keys():
            name = name+self.week.browse(values['week']).week+self.year.short_code or ''
        if 'year'in values.keys():
            name = name+self.week.week+self.year.browse(values['year']).short_code        
        values.update({'name':name})
        return super(StockProductionLot, self).write(values)