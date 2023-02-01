# -*- coding: utf-8 -*-
from odoo import models, fields, api,_




class ResPartner(models.Model):
    _inherit = 'res.partner'

    credt_limit_used = fields.Monetary(compute='_compute_credt_limit_used', string='Crédito Usado')
    credt_limit_available = fields.Monetary(compute='_compute_credt_limit_available', string='Crédito Disponible')
    credit_amount_overdue = fields.Monetary(compute='_compute_credt_limit_available', string='Saldo Vencido')
    credit_limit = fields.Float(string='Límite de Crédito',tracking=True)
    

    def _compute_credt_limit_used(self):
        for partner in self:
            
            partner.credt_limit_used =0
            partner.credit_amount_overdue = 0

    def _compute_credt_limit_available(self):
        for partner in self:
            partner.credt_limit_available = (partner.credit_limit-partner.credt_limit_used) if (partner.credit_limit-partner.credt_limit_used)>=1 else 0
            print(partner.credt_limit_available)
    
          

    def _ztyres_compute_unpaid_invoices(self):
        account_move = self.env['account.move']        
        unpaid_invoices = False
        for record in self:
            unpaid_invoices = account_move.search([
                ('company_id', '=', self.env.company.id),
                ('commercial_partner_id', '=', record.id),
                ('state', '=', 'posted'),
                ('payment_state', 'in', ('not_paid', 'partial')),
                ('move_type', 'in', account_move.get_sale_types())
            ]).filtered(lambda inv: not any(inv.line_ids.mapped('blocked')))
        sales_unpaid = unpaid_invoices.mapped('invoice_line_ids').mapped('sale_line_ids').mapped('order_id').mapped('name')
        return (unpaid_invoices,sales_unpaid)

    @api.onchange('parent_id')
    def onchange_parent_id(self):
        # return values in result, as this method is used by _fields_sync()
        if not self.parent_id:
            return
        result = {}
        partner = self._origin
        if partner.parent_id and partner.parent_id != self.parent_id:
            result['warning'] = {
                'title': _('Warning'),
                'message': _('Changing the company of a contact should only be done if it '
                             'was never correctly set. If an existing contact starts working for a new '
                             'company then a new contact should be created under that new '
                             'company. You can use the "Discard" button to abandon this change.')}
        return result