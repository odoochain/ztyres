# -*- coding: utf-8 -*-
from odoo import models, fields, api,_
from datetime import datetime

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    partner_credit_limit_used = fields.Monetary(related='partner_id.credt_limit_used', readonly=True)
    partner_credit_limit_available = fields.Monetary(related='partner_id.credt_limit_available', readonly=True)    
    show_partner_credit_alert = fields.Boolean(compute='_compute_show_partner_credit_alert')
    partner_credit_limit = fields.Float(related='partner_id.credit_limit', readonly=True)
    partner_credit_amount_overdue = fields.Monetary(related='partner_id.credit_amount_overdue', readonly=True)
    #month_promotion = fields.Selection([('01','Enero'),('02','Febrero'),('03','Marzo'),('04','Abril'),('05','Mayo'),('06','Junio'),('07','Julio'),('08','Agosto'),('09','Septiembre'),('10','Octubre'),('11', 'Noviembre'),('12','Diciembre')], string='Mes para promoción')
    sale_reason_cancel_id = fields.Many2many(comodel_name='ztyres.sale_reason_cancel', string='Motivo de Cancelación')
    payment_term_days = fields.Integer(compute='_compute_payment_term_days',string='Días de Crédito')
    APPROVE_STATES = [('draft', 'Gerente de Ventas'),('done', 'Crédito y Cobranza'),('confirm', 'Anticipado')]
    approve_state = fields.Selection(string='Estado de Aprobación', selection=APPROVE_STATES,track_visibility='onchange')    

    def sale_approve_state_draft(self):
        for record in self:
            record.approve_state = 'draft'

    def sale_approve_state_done(self):
        for record in self:
            record.approve_state = 'done'


    def sale_approve_state_confirm(self):
        for record in self:
            record.approve_state = 'confirm'


    def _compute_payment_term_days(self):
        for record in self:
            record.payment_term_days = record.payment_term_id.line_ids.days


    def _compute_show_partner_credit_alert(self):
        for order in self:
            order.show_partner_credit_alert = True

    def _action_cancel_delete_picking_ids(self):
        res = super(SaleOrder, self).action_cancel()
        for order in self:    
            for picking in order.picking_ids:
                if picking.state in ['cancel']:
                    picking.sudo().unlink()     
        return res

    @api.model
    def create(self, values):        
        currentMonth = str(datetime.now().month).zfill(2)
        values.update({'month_promotion':currentMonth})
        print(values)
        result = super().create(values)
        result.order_line.check_price_not_in_zero()
        return result
    
    
    def write(self, values):
        res = super().write(values)        
        if values.get("order_line") is not None:
            self.order_line.check_price_not_in_zero()
            if self.state == 'done':
                self.action_unlock()
            if self.state == 'draft':
                self.quotation_action_confirm()
                res = self._ztyres_check_account_status()
                if res:                
                    return res                          
            if self.state == 'sale':
                self.action_done()                  
        return res
    
    def action_confirm(self):
        for order in self:            
            res = order._ztyres_check_account_status()       
        return res or super(SaleOrder, self).action_confirm()


    def quotation_action_confirm(self):     
        # Validate sale policies again
        for order in self:            
            for picking in order.picking_ids:
                if picking.state not in ['done']:
                    picking.do_unreserve()
                    picking.action_cancel()
                    picking.sudo().unlink()

        self.order_line._ztyres_action_launch_stock_rule()

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
            if not (order.amount_total <= order.partner_credit_limit_available and 0.0 <=order.partner_credit_amount_overdue):
                return {
                    'type': 'ir.actions.act_window',
                    'name': 'Error en la Validación',
                    'res_model': 'ztyres.wizard_denied_confirm_sale',
                    'view_mode': 'form',                    
                    'target': 'new'
                } 
            elif  order.partner_credit_amount_overdue == 0.0 and self.approve_state == 'confirm' and self.payment_term_days == 0.0:
                return False    
            else:
                return False 

    # def update_prices(self):
    #     self.ensure_one()
    #     for line in self._get_update_prices_lines():
    #         line.product_uom_change()
    #         line.discount = 0  # Force 0 as discount for the cases when _onchange_discount directly returns
    #         line._onchange_discount()
    #     self.show_update_pricelist = False
    #     self.message_post(body=_("Product prices have been recomputed according to pricelist <b>%s<b> ", self.pricelist_id.display_name))            
    #     self.order_line.check_ztyres_sale_promotion()
    
    
    def action_cancel(self):
        
        # Add code here
        return {
            'type': 'ir.actions.act_window',
            'name': 'Motivo de Cancelación',
            'res_model': 'ztyres.cancel_reason',
            'view_mode': 'form',            
            'target': 'new',
            'context' : {'sale_id':self}
        }        
    




"""
orders = self.env['sale.order'].search([('state','in',['done'])])
for item in orders:
    item.with_context(tracking_disable=True).action_unlock()
"""