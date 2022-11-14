# -*- coding: utf-8 -*-
from odoo import models, fields, api,_

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    partner_credit_limit_used = fields.Monetary(related='partner_id.credt_limit_used', readonly=True)
    partner_credit_limit_available = fields.Monetary(related='partner_id.credt_limit_available', readonly=True)    
    show_partner_credit_alert = fields.Boolean(compute='_compute_show_partner_credit_alert')
    partner_credit_limit = fields.Float(related='partner_id.credit_limit', readonly=True)
    partner_credit_amount_overdue = fields.Monetary(related='partner_id.credit_amount_overdue', readonly=True)
    def _compute_show_partner_credit_alert(self):
        for order in self:
            order.show_partner_credit_alert = True

    def action_cancel(self):
        res = super(SaleOrder, self).action_cancel()
        for order in self:    
            for picking in order.picking_ids:
                if picking.state in ['cancel']:
                    picking.sudo().unlink()     
        return res

    @api.model
    def create(self, values):
        print(values)
        result = super().create(values)
        
        return result

    def action_confirm(self):
        for order in self:
            res = order._ztyres_check_account_status()        
        return res or super(SaleOrder, self).action_confirm()


    def quotation_action_confirm(self):     

        # Validate sale policies again

        for order in self:
            res = order._ztyres_check_account_status()
            if res:                
                return res
            for picking in order.picking_ids:
                if picking.state in ['cancel']:
                    picking.sudo().unlink()

        self.order_line._ztyres_action_launch_stock_rule()

        return {
            'value': {'other_id': 'arr_est'},
            'warning': {'title': "Aqui se realizan las validaciones"},
        }

    def _ztyres_account_status(self):
        unpaid_invoices = False
        balance_for_followup = False
        for order in self:
            unpaid_invoices = order.partner_id._ztyres_compute_unpaid_invoices()
            balance_for_followup = order.partner_id._ztyres_compute_for_followup() 
        print(unpaid_invoices,balance_for_followup)  
        return (unpaid_invoices,balance_for_followup)
    
    def _ztyres_check_account_status(self):
        for order in self:            
            if (order.partner_credit_limit_available <= order.amount_total and order.partner_credit_amount_overdue <=0):
                return {
                    'type': 'ir.actions.act_window',
                    'name': 'Error en la Validación',
                    'res_model': 'ztyres.wizard_denied_confirm_sale',
                    'view_mode': 'form',                    
                    'target': 'new'
                }     
            else:
                return False 