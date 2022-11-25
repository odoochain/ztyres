# -*- coding: utf-8 -*-
from odoo import models, fields,api, _
from odoo.tools import  float_compare
from odoo.exceptions import UserError
class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'    

    dot_range = fields.Char(related='product_id.dot_range')
    # amount_discount = fields.Float(compute='check_ztyres_sale_promotion',string='Ahorro',store=True)
    # price_with_discount = fields.Float(compute='check_ztyres_sale_promotion',string='Precio con descuento',store=True)    
    # promotion_applied = fields.Many2many('ztyres.sale_promotion_line', string='Promoción aplicada')
    
    

    
    def check_price_not_in_zero(self):
        for record in self:
            if record.price_unit == 0 or record.price_unit < 1:
                raise UserError('No puede continuar con productos con precio $0   %s documento origen %s'%(record.name,record.order_id.name))

    # @api.depends('product_id','product_uom_qty','order_id.month_promotion')
    # def check_ztyres_sale_promotion(self):
    #     promotion = self.env['ztyres.sale_promotion'].search([])
    #     for record in self:
    #         for promo in promotion:
    #             for rec in  promo.sale_promotion_lines:
    #                 discount_amount = (rec.discunt*record.price_unit) * record.product_uom_qty
    #                 discounted_price = ((record.price_unit * record.product_uom_qty)-discount_amount) 
    #                 if  record.product_id.manufacturer_id.id in rec.manufacturer_ids.ids and record.product_uom_qty >= rec.qty:
    #                     record.amount_discount = discount_amount
    #                     record.price_with_discount = discounted_price
    #                     record.promotion_applied = [(4,rec.id)]
    #                     break
    #                 elif record.product_id.product_tier_id.id in rec.product_tier_ids.ids and record.product_uom_qty >= rec.qty:
    #                     record.amount_discount = discount_amount
    #                     record.price_with_discount = discounted_price
    #                     record.promotion_applied = [(4,rec.id)]
    #                     break
    #                 elif record.product_id.product_usage_id.id in rec.product_usage_ids.ids and record.product_uom_qty >= rec.qty:
    #                     record.amount_discount = discount_amount
    #                     record.price_with_discount = discounted_price
    #                     record.promotion_applied = [(4,rec.id)]
    #                     break
    #                 else:                        
    #                     record.amount_discount = 0
    #                     record.price_with_discount = 0                        
    #                     record.promotion_applied = False





    



    def _ztyres_action_launch_stock_rule(self, previous_product_uom_qty=False):
       
        """
        Launch procurement group run method with required/custom fields genrated by a
        sale order line. procurement group will launch '_run_pull', '_run_buy' or '_run_manufacture'
        depending on the sale order line product rule.
        """
        precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
        procurements = []
        for line in self:
            line = line.with_company(line.company_id)
            if not line.product_id.type in ('consu','product'):
                continue
            qty = line._get_qty_procurement(previous_product_uom_qty)
            if float_compare(qty, line.product_uom_qty, precision_digits=precision) >= 0:
                continue

            group_id = line._get_procurement_group()
            if not group_id:
                group_id = self.env['procurement.group'].create(line._prepare_procurement_group_vals())
                line.order_id.procurement_group_id = group_id
            else:
                # In case the procurement group is already created and the order was
                # cancelled, we need to update certain values of the group.
                updated_vals = {}
                if group_id.partner_id != line.order_id.partner_shipping_id:
                    updated_vals.update({'partner_id': line.order_id.partner_shipping_id.id})
                if group_id.move_type != line.order_id.picking_policy:
                    updated_vals.update({'move_type': line.order_id.picking_policy})
                if updated_vals:
                    group_id.write(updated_vals)

            values = line._prepare_procurement_values(group_id=group_id)
            product_qty = line.product_uom_qty - qty

            line_uom = line.product_uom
            quant_uom = line.product_id.uom_id
            product_qty, procurement_uom = line_uom._adjust_uom_quantities(product_qty, quant_uom)
            procurements.append(self.env['procurement.group'].Procurement(
                line.product_id, product_qty, procurement_uom,
                line.order_id.partner_shipping_id.property_stock_customer,
                line.name, line.order_id.name, line.order_id.company_id, values))
        if procurements:
            self.env['procurement.group'].run(procurements)
        return True
