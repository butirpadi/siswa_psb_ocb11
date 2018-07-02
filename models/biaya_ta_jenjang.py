# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from pprint import pprint
from datetime import datetime, date
import calendar

class biaya_ta_jenjang(models.Model):
    _inherit = 'siswa_keu_ocb11.biaya_ta_jenjang'

    is_bulanan = fields.Boolean('Is Bulanan',related='biaya_id.is_bulanan')
    bulan = fields.Selection([(1, 'Januari'), 
                            (2, 'Februari'),
                            (3, 'Maret'),
                            (4, 'April'),
                            (5, 'Mei'),
                            (6, 'Juni'),
                            (7, 'Juli'),
                            (8, 'Agustus'),
                            (9, 'September'),
                            (10, 'Oktober'),
                            (11, 'November'),
                            (12, 'Desember'),
                            ], string='Bulan')
    