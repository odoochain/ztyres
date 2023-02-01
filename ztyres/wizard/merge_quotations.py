# -*- coding: utf-8 -*-
from odoo import models,_,fields, api
from odoo.exceptions import UserError

class MergeQuotations(models.TransientModel):
    _name = 'ztyres.wizard_merge_quotations'
    
    def merge_quotations(self):
        sale = self.env['sale.order']
        sales = sale.search([('id','in',self._context['sale_ids']['active_ids'])])
        for sale in sales:
            if sale.state == 'done':
                sale.action_unlock()
                if sale.state == 'sale':
                    sale.action_done()
                    raise UserError('No es posible combinar documentos con estado Orden de Venta')
                
            elif sale.state == 'sale':
                raise UserError('No es posible combinar documentos con estado Orden de Venta')
            

        if not len(sales) >1:
            raise UserError('Solo se puede realizar la combinación de dos o mas cotizaciones.')
        picking_states = sales.picking_ids.mapped('state')
        if 'done' not in picking_states:
            for picking in sales.picking_ids:
                if picking.state in ['assigned']:
                    picking.do_unreserve()
                if picking.state in ['confirmed']:
                    picking.action_cancel()                    
                picking.sudo().unlink()
        else:
            raise UserError('No es posible combinar una cotización con movimientos de invetario validados.%s'%(sales.picking_ids.filtered(lambda r: r.state == "done").mapped('sale_id').mapped('name')))
            
        partner_id = sales.mapped('partner_id')
        
        sale_order_lines = sales.order_line
        if len(partner_id)>1:
            raise UserError('No se pueden combinar cotizaciones de clientes distintos. %s'%(partner_id.mapped('name')))
        new_sale = sale.create({'partner_id':partner_id.id})

        product_ids = sale_order_lines.mapped('product_id')
        grouped_vals_arr =[]
        for product in product_ids:
            vals = (0, 0,{'product_id':product.id,'product_uom_qty':sum(sale_order_lines.filtered(lambda r: r.product_id.id == product.id).mapped('product_uom_qty'))})
            grouped_vals_arr.append(vals)            
        new_sale.order_line = grouped_vals_arr        
        sales.order_line.sudo().unlink()
        sales.sudo().unlink()            
        return {
            'type': 'ir.actions.act_window',
            'name': 'Cotizacion',
            'res_model': 'sale.order',
            'view_mode': 'form',
            'target': 'current',
            'context' : {  },
            'res_id' : new_sale.id
        }




    def merge_quotations_to_sale(self):
        sale = self.env['sale.order']
        sales = sale.search([('id','in',self._context['sale_ids']['active_ids'])])
        for sale in sales:
            if sale.state == 'done':
                sale.action_unlock()
                if sale.state == 'sale':
                    sale.action_done()
                    raise UserError('No es posible combinar documentos con estado Orden de Venta')
                
            elif sale.state == 'sale':
                raise UserError('No es posible combinar documentos con estado Orden de Venta')
            

        if not len(sales) >1:
            raise UserError('Solo se puede realizar la combinación de dos o mas cotizaciones.')
        picking_states = sales.picking_ids.mapped('state')
        if 'done' not in picking_states:
            for picking in sales.picking_ids:
                if picking.state in ['assigned']:
                    picking.do_unreserve()
                if picking.state in ['confirmed']:
                    picking.action_cancel()                    
                picking.sudo().unlink()
        else:
            raise UserError('No es posible combinar una cotización con movimientos de invetario validados.%s'%(sales.picking_ids.filtered(lambda r: r.state == "done").mapped('sale_id').mapped('name')))
            
        partner_id = sales.mapped('partner_id')
        
        sale_order_lines = sales.order_line
        if len(partner_id)>1:
            raise UserError('No se pueden combinar cotizaciones de clientes distintos. %s'%(partner_id.mapped('name')))
        new_sale = sale.create({'partner_id':partner_id.id})

        product_ids = sale_order_lines.mapped('product_id')
        grouped_vals_arr =[]
        for product in product_ids:
            vals = (0, 0,{'product_id':product.id,'product_uom_qty':sum(sale_order_lines.filtered(lambda r: r.product_id.id == product.id).mapped('product_uom_qty'))})
            grouped_vals_arr.append(vals)            
        new_sale.order_line = grouped_vals_arr        
        sales.order_line.sudo().unlink()
        sales.sudo().unlink()         
        res = new_sale.action_confirm()  
        print(res) 
        return res or {
            'type': 'ir.actions.act_window',
            'name': 'Cotizacion',
            'res_model': 'sale.order',
            'view_mode': 'form',
            'target': 'current',
            'context' : {  },
            'res_id' : new_sale.id
        }

        

