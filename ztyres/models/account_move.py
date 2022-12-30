# -*- coding: utf-8 -*-
from odoo import models, fields, api,_

class AccountMove(models.Model):
    _inherit = 'account.move'
    partner_credit_limit_used = fields.Monetary(related='partner_id.credt_limit_used', readonly=True)
    partner_credit_limit_available = fields.Monetary(related='partner_id.credt_limit_available', readonly=True)
    show_partner_credit_alert = fields.Boolean(compute='_compute_show_partner_credit_alert')
    partner_credit_limit = fields.Float(related='partner_id.credit_limit', readonly=True)
    partner_credit_amount_overdue = fields.Monetary(related='partner_id.credit_amount_overdue', readonly=True)
    
    
    def _compute_show_partner_credit_alert(self):
        for order in self:
            order.show_partner_credit_alert = True

    l10n_mx_edi_payment_policy = fields.Selection(string='Payment Policy',
        selection=[('PPD', 'PPD'), ('PUE', 'PUE')],
        compute='_compute_l10n_mx_edi_payment_policy', raise_if_not_found=False)


    @api.depends('move_type', 'invoice_date_due', 'invoice_date', 'invoice_payment_term_id', 'invoice_payment_term_id.line_ids')
    def _compute_l10n_mx_edi_payment_policy(self):     
        for move in self:
            if move.is_invoice(include_receipts=True) and move.invoice_date_due and move.invoice_date:
                if move.move_type == 'out_invoice':
                    # In CFDI 3.3 - rule 2.7.1.43 which establish that
                    # invoice payment term should be PPD as soon as the due date
                    # is after the last day of  the month (the month of the invoice date).
                    if move.invoice_date_due.month > move.invoice_date.month or \
                       move.invoice_date_due.year > move.invoice_date.year or \
                       len(move.invoice_payment_term_id.line_ids) > 1:  # to be able to force PPD
                        move.l10n_mx_edi_payment_policy = 'PPD'
                    else:
                        move.l10n_mx_edi_payment_policy = 'PPD'                
                else:
                    move.l10n_mx_edi_payment_policy = 'PPD'
            elif move.move_type == 'out_refund':
                move.l10n_mx_edi_payment_policy = 'PPD'
            else:
                move.l10n_mx_edi_payment_policy = 'PPD'