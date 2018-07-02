# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from pprint import pprint
from datetime import datetime, date


class siswa(models.Model):
    _inherit = 'res.partner'

    calon_siswa_id = fields.Many2one('siswa_psb_ocb11.calon_siswa', string='Data Calon Siswa', ondelete="restrict")
    tanggal_registrasi = fields.Date('Tanggal Registrasi', required=True, default=datetime.today())