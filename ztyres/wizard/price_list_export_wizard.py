from odoo import _, api, fields, models
import pandas as pd 
import base64
import pandas as pd
import io
class PriceListExportWizard(models.TransientModel):
    _name = 'ztyres.pricelist_export_wizard'
    _description = 'Exportación de Precios'

    def _default_tax(self):
        return self.env['account.tax'].search([('id', 'in', [2])]).ids
    def _default_pricelist(self):
        return self.env['product.pricelist'].search([]).ids        
    pricelist_ids = fields.Many2many('product.pricelist', string='Lista de Precios',default=_default_pricelist,required=True)
    file_data = fields.Binary('File')
    only_on_hand = fields.Boolean(string='Solo productos en existencia',default=True)    
    # include_dot = fields.Boolean(string='Incluir DOT',default=False)
    tax_ids = fields.Many2many('account.tax', string='Impuestos',default=_default_tax)



    def get_low_price(self,product_tmpl_ids,pricelist_ids,order):
        limit = False
        if order:
            limit =1            
        pricelist_item = self.env['product.pricelist.item']
        pricelist_items = pricelist_item.search([('product_tmpl_id','in',product_tmpl_ids),('pricelist_id.active','in',[True]),('pricelist_id','in',pricelist_ids)],order=order,limit=limit)
        if len(pricelist_items)>1:
            print("Err")
        return pricelist_items

    def download_report(self):
        self.tax_ids.ensure_one()
        data = []
        
        not_defined = ''        
        for item in self:
            order = False
            pricelist_item = self.env['product.pricelist.item']
            pricelist_items_ids = pricelist_item.search([('pricelist_id.active','in',[True]),('pricelist_id','in',item.pricelist_ids.ids)]).mapped('product_tmpl_id').ids
            for tmpl_id in pricelist_items_ids:
                product_list = self.get_low_price([tmpl_id],item.pricelist_ids.ids,order)                
                record = {}
                for product in product_list:                    
                    if self.only_on_hand:
                        if product.product_tmpl_id.qty_available:
                            record.update(                                {   
                             '01 Código':product.product_tmpl_id.default_code or not_defined,                     
                             '02 Nombre' : product.product_tmpl_id.name or not_defined,
                             '03 Capas':product.product_tmpl_id.x_studio_capas or not_defined,
                             '04 Marca':product.product_tmpl_id.x_studio_marca or not_defined,
                             '05 Indice de Carga':product.product_tmpl_id.x_studio_indice_carga or not_defined,
                             '06 Uso':product.product_tmpl_id.x_studio_uso or not_defined,                                  
                             '07 Disponible':product.product_tmpl_id.qty_available or not_defined,
                             '08 '+product.pricelist_id.name : self.tax_ids.compute_all(product.fixed_price,self.env.company.currency_id,1.0,None,None,False,True)['total_included'] or not_defined,
                            #  '09 Dot' : product.product_tmpl_id.product_variant_id.dot_range or not_defined                              
                            })
                        # if self.include_dot:
                        #     record.update({'09 Dot' : product.product_tmpl_id.product_variant_id.dot_range or not_defined})
                            
                    else:                                                
                        record.update(                                {   
                             '01 Código':product.product_tmpl_id.default_code or not_defined,                     
                             '02 Nombre' : product.product_tmpl_id.name or not_defined,
                             '03 Capas':product.product_tmpl_id.x_studio_capas or not_defined,
                             '04 Marca':product.product_tmpl_id.x_studio_marca or not_defined,
                             '05 Indice de Carga':product.product_tmpl_id.x_studio_indice_carga or not_defined,
                             '06 Uso':product.product_tmpl_id.x_studio_uso or not_defined,                                  
                             '07 Disponible':product.product_tmpl_id.qty_available or not_defined,
                             '08 '+product.pricelist_id.name : self.tax_ids.compute_all(product.fixed_price,self.env.company.currency_id,1.0,None,None,False,True)['total_included'] or not_defined,
                            #  '09 Dot' : product.product_tmpl_id.product_variant_id.dot_range or not_defined
                            })
                        # if self.include_dot:
                        #     record.update({'09 Dot' : product.product_tmpl_id.product_variant_id.dot_range or not_defined})
                if record:
                    data.append(dict(sorted(record.items())))                        
                                        
        df = pd.DataFrame(data)
        fp = io.BytesIO()
        df.to_excel(fp,index=False)
        fp.seek(0)
        data = fp.read()
        fp.close()
        self.write({'file_data': base64.b64encode(data)})
        action = {
            'name': 'Lista de Precios',
            'type': 'ir.actions.act_url',
            'url': "/web/content/?model=ztyres.pricelist_export_wizard&id=" + str(self.id) + "&field=file_data&download=true&filename=Lista de Precios.xlsx",
            'target': 'self',
            }
        return action        
        #print(df)
            # pricelist_unique_items_ids = list(set(pricelist_items_ids))
            # print(pricelist_unique_items_ids)
        
    

    

