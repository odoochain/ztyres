from odoo import models, fields,_
import logging
import base64
from io import BytesIO
from odoo.exceptions import UserError
_logger = logging.getLogger(__name__)

try:
    import openpyxl
    _openpyxl_lib_imported = True

except ImportError:
    _openpyxl_lib_imported = False
    _logger.info(
        "The `openpyxl` Python module is not available. "
        "Phone number validation will be skipped. "
        "Try `pip3 install openpyxl` to install it."
    )
class ImportCustomerWizard(models.TransientModel):
    _name = "ztyres.pricelist_import_wizard"
    file = fields.Binary(string="File", required=True)
    pricelist_ids = fields.Many2many('product.pricelist', string='Lista de Precios destino',required=True)    
    options = fields.Selection(
        string='Opciones de carga de precios',
        selection=[('replace', 'Reemplazar precios si existen y crear nuevos precios si no existen.'), ('delete', 'Borrar todo y dejar los únicamente los precios cargados.')],        
        default='replace'        
    )
    

    def import_prices(self):
        try:
            if self.options == 'delete':
                self.pricelist_ids.ensure_one()
                self.pricelist_ids.item_ids.unlink()
            if _openpyxl_lib_imported:
                    
                wb = openpyxl.load_workbook(filename=BytesIO(base64.b64decode(self.file)), read_only=True)
                ws = wb.active
                records_modified = False
                for record in ws.iter_rows(min_row=2, max_row=None, min_col=None,max_col=None, values_only=True):
                   #TODO Usar filtered para mejorar el performance
                    product = self.pricelist_ids.item_ids.search([('pricelist_id','in',[self.pricelist_ids.id]),('product_tmpl_id','in',[int(record[0])])])
                    if product:
                        product.fixed_price = float(record[1])   
                        records_modified = True                  
                    else:    
                        self.pricelist_ids.item_ids.create({
                        "applied_on": "1_product",
                        "product_tmpl_id": int(record[0]),
                        "pricelist_id": self.pricelist_ids.id,
                        "compute_price": "fixed",
                        "fixed_price":float(record[1]) ,
                        })
                        records_modified = True
                if records_modified:
                    
                    return {
                        'name': _('Listas de Precios'),
                        'type': 'ir.actions.act_window',
                        'view_type': 'form',
                        'view_mode': 'form',
                        'res_model': 'product.pricelist',
                        'res_id': self.pricelist_ids.id                    
                    }                                                                  
                    # search if the price exist else create
        except:
            raise UserError(_('El archivo no es válido'))