# -*- coding: utf-8 -*-
from odoo import models, fields

class Product(models.Model):
    _inherit = 'product.product'

    dot_range = fields.Char(compute='_compute_dot_range', string='DOT')

    def _compute_dot_range(self):
        product_lot = self.env['stock.lot']
        for record in self:
            record.dot_range = 'N/A'
            lots = product_lot.search([('product_id','in',[record.id])]).mapped('name')
            if lots:
                try:
                    arr_dict = []
                    for item in lots:                    
                        if len(item)==4:
                            arr_dict.append((int(item[-2:]),int(item[:2])))
                        elif len(item)==3:
                            arr_dict.append((int(item[-2:]),int(item[:1])))
                    sorted_list_year_month = sorted(arr_dict)
                    max_dot = str(sorted_list_year_month[-1][1])+str(sorted_list_year_month[-1][0])
                    min_dot = str(sorted_list_year_month[0][1])+str(sorted_list_year_month[0][0])
                    if max_dot == min_dot:
                        record.dot_range = '%s'%(max_dot)
                    else:
                        record.dot_range = '%s-%s'%(min_dot,max_dot)
                except Exception as e:
                    print('Error de DOT en producto')
                    record.dot_range = 'N/A'
            else:
                record.dot_range = 'N/A'
