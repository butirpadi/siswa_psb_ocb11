# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _
from pprint import pprint
from datetime import datetime, date
import math

class calon_siswa_biaya(models.Model):
    _name = 'siswa_psb_ocb11.calon_siswa_biaya'

    calon_siswa_id = fields.Many2one('siswa_psb_ocb11.calon_siswa', string="Calon Siswa")
    # is_siswa_lama = fields.Boolean(string='is Siswa Lama',related="calon_siswa_id.is_siswa_lama", store=True)
    biaya_id = fields.Many2one('siswa_keu_ocb11.biaya', string="Biaya")
    is_bulanan = fields.Boolean(string='Bulanan',related="biaya_id.is_bulanan")
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
    harga = fields.Float('Harga', compute="_compute_harga", store=True)
    dibayar = fields.Float('Dibayar', required=True, default=0)

    # @api.onchange('is_siswa_lama')
    # def onchange_is_siswa_lama(self):
    #     domain = {'biaya_id':[('is_siswa_baru_only','=',False)]}
    #     return {'domain':domain, 'value':{'biaya_id':[]}}    

    @api.depends('biaya_id')
    def _compute_harga(self):
        
        # get default harga
        #### Get tahunajaran and jenjang
        for rec in self:
            tahunajaran_id = rec.calon_siswa_id.tahunajaran_id
            jenjang_id = rec.calon_siswa_id.jenjang_id
            biaya_ta_jenjang = self.env['siswa_ocb11.tahunajaran_jenjang'].search([('tahunajaran_id','=',tahunajaran_id.id),('jenjang_id','=',jenjang_id.id)]).biayas
            for by in biaya_ta_jenjang:
                if by.biaya_id.id == rec.biaya_id.id :
                    rec.harga = by.harga
                    if by.biaya_id.is_different_by_gender:
                        if rec.calon_siswa_id.jenis_kelamin == 'perempuan':
                            rec.harga = by.harga_alt
                            print('Harga Alternatif : ' + str(rec.harga))
                    # if by.biaya_id.is_bulanan:
                    rec.dibayar = rec.harga
                    print('Harga : ' + str(rec.dibayar))
                    