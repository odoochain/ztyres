import pandas as pd 
from xmlrpc import client as xmlrpc_client
from decouple import config

import requests
requests.packages.urllib3.disable_warnings()
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'

"""
Modified Files


_get_csf_tables /home/isscjrmpacheco/.local/lib/python3.10/site-packages/pandas/io/html.py
read_csf "read_csf", /home/isscjrmpacheco/.local/lib/python3.10/site-packages/pandas/__init__.py
/home/isscjrmpacheco/.local/lib/python3.10/site-packages/pandas/io/api.py
from pandas.io.html import read_csf
pip install python-decouple
"""


def get_data_csf(url):
    rfc = url.split('_')[1]
    page = requests.get(url, verify=False)
    html = page.content.decode("utf-8")
    all_tables = pd.read_csf(html)
    vals = {}
    for table in all_tables:
        for st_1 in table:        
            if len(st_1) == 2:
                if st_1[0] and st_1[1]:
                    vals.update({st_1[0]:st_1[1]})
    name = vals.get('Denominación o Razón Social:') or '%s %s %s'%(vals.get('Nombre:') or "",vals.get('Apellido Materno:') or "",vals.get('Apellido Paterno:') or "")
    odoo_vals ={        
        'name': name,
        'street':vals.get('Nombre de la vialidad:'),
        'street_number':vals.get('Número exterior:') or False,
        'street_number2':vals.get('Número interior:') or False,
        'state_id':vals.get('Entidad Federativa:'),
        'city_id':vals.get('Municipio o delegación:'),
        'zip':vals.get('CP:'),
        'country_id':156,
        'vat':rfc,
        'l10n_mx_edi_fiscal_regime':vals.get('Régimen:')
    }
    return odoo_vals


# url = "https://siat.sat.gob.mx/app/qr/faces/pages/mobile/validadorqr.jsf?D1=10&D2=1&D3=14040812593_CVR140214T41"

# print(get_data_csf(url))





    


