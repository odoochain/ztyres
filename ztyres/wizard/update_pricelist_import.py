# -*- coding: utf-8 -*-
import base64

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.addons.base.models.res_bank import sanitize_account_number
import io
import logging
import tempfile
import binascii
from datetime import datetime

from odoo import models, fields, api, _
from datetime import datetime
from odoo.tools.mimetypes import guess_mimetype
from odoo.exceptions import Warning
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, pycompat

_logger = logging.getLogger(__name__)

import io, os
import base64
try:
    import xlrd
    try:
        from xlrd import xlsx
    except ImportError:
        xlsx = None
except ImportError:
    xlrd = xlsx = None

try:
    #import odf_ods_reader
    from . import odf_ods_reader
except ImportError:
    odf_ods_reader = None

try:
    import csv
except ImportError:
    _logger.debug('Cannot `import csv`.')

FILE_TYPE_DICT = {
    'text/csv': ('csv', True, None),
    'application/vnd.ms-excel': ('xls', xlrd, 'xlrd'),
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ('xlsx', xlsx, 'xlrd >= 0.8'),
    'application/vnd.oasis.opendocument.spreadsheet': ('ods', odf_ods_reader, 'odfpy')
}
EXTENSIONS = {
    '.' + ext: handler
    for mime, (ext, handler, req) in FILE_TYPE_DICT.items()
}

class ImportarDiasWizard(models.TransientModel):
    _name = 'ztyres.update_pricelist_import'
    _description = 'ImportarDiasWizard'
    
    import_file = fields.Binary("Importar",required=True)
    file_name = fields.Char("Nombre de file")
    
    
    def import_xls_file(self):
        def str_to_number(number_str):
            number = False
            try:
                number = float(number_str)
            except:
                pass
            return number
        self.ensure_one()
        if not self.import_file:
            raise Warning("Please select the file first.") 
        p, ext = os.path.splitext(self.file_name)
        if ext[1:] not in ['xls','xlsx']:
            raise Warning(_("Unsupported file format \"{}\", import only supports XLS, XLSX").format(self.file_name))       
        try:
            fp = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")
            fp.write(binascii.a2b_base64(self.import_file))
            fp.seek(0)
            values = {}
            workbook = xlrd.open_workbook(fp.name)
            sheet = workbook.sheet_by_index(0)
        except:
            raise UserError(_("Invalid file!"))
        vals_list = []
        for row_no in range(sheet.nrows):
            values = {}
            if row_no <= 0:
                fields = map(lambda row: row.value.encode('utf-8'), sheet.row(row_no))
            else:
                line = list(map(
                    lambda row: isinstance(row.value, bytes) and row.value.encode('utf-8') or str(
                        row.value), sheet.row(row_no)))
                print(line)
                values.update({
                    'pricelist_id': str_to_number(line[0]),
                    'product_id': str_to_number(line[1]),
                    'min_quantity': str_to_number(line[2]),
                    'fixed_price': str_to_number(line[3]),
                    'date_start': str_to_number(line[4]),
                    'date_end': str_to_number(line[5])
                })
                vals_list.append(values)
        new_recs = []
        try:
            for dict in vals_list:
                new_recs += self.env['ztyres.wizard_update_pricelist'].create(dict)
        except:
            raise UserError(_('Por favor verifique los valores de su archivo, o solicite ayuda al área de Sistemas :( '))
            
        if new_recs:            
            return {
                'name': _('Vista Previa'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'ztyres.wizard_update_pricelist'
            }
            
                 
