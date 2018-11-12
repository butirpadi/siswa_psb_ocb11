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
    is_bulanan = fields.Boolean(string='Bulanan', related="biaya_id.is_bulanan")
    bulan = fields.Selection([(0, '-'),
                            (1, 'Januari'),
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
    dibayar = fields.Float('Dibayar', required=True, default=0.0)
    qty = fields.Integer('Qty', default=1)
    potongan_harga = fields.Float('Potongan', default=0.0)
    jumlah_harga_setelah_potongan = fields.Float('Jumlah Harga', compute="_compute_jumlah_harga_setelah_potongan", default=0.0, store=True)
    amount_due = fields.Float('Amount Due', compute="_compute_amount_due")
    
    @api.depends('dibayar')
    def _compute_amount_due(self):
        for rec in self:
            rec.amount_due = rec.harga - rec.potongan_harga - rec.dibayar
        
#     @api.onchange('potongan_harga')
#     def potongan_harga_change(self):
#         harga_setelah_potong = (self.harga) - (self.qty * self.potongan_harga)
#         self.jumlah_harga_setelah_potongan = harga_setelah_potong
#         self.dibayar = harga_setelah_potong
    
    @api.multi
    def write(self, vals):
        if 'potongan_harga' in vals:
            vals['jumlah_harga_setelah_potongan'] = (self.qty * self.harga) - (self.qty * vals['potongan_harga'])
            vals['dibayar'] = (self.qty * self.harga) - (self.qty * vals['potongan_harga'])
        
        return super(calon_siswa_biaya, self).write(vals) 

#     @api.depends('biaya_id')
#     def _compute_harga(self):
#         print('inside compute harga on calon_siswa_biaya')        
#         # get default harga
#         #### Get tahunajaran and jenjang
#         for rec in self:
#             tahunajaran_id = rec.calon_siswa_id.tahunajaran_id
#             jenjang_id = rec.calon_siswa_id.jenjang_id
#             biaya_ta_jenjang = self.env['siswa_ocb11.tahunajaran_jenjang'].search([('tahunajaran_id', '=', tahunajaran_id.id), ('jenjang_id', '=', jenjang_id.id)]).biayas
#             for by in biaya_ta_jenjang:
#                 if by.biaya_id.id == rec.biaya_id.id :
#                     rec.harga = by.harga
#                     if by.biaya_id.is_different_by_gender:
#                         if rec.calon_siswa_id.jenis_kelamin == 'perempuan':
#                             rec.harga = by.harga_alt
#                             print('Harga Alternatif : ' + str(rec.harga))
#                     # if by.biaya_id.is_bulanan:
#                     rec.dibayar = rec.harga
#                     print('Harga : ' + str(rec.dibayar))
    
    @api.depends('potongan_harga')
    def _compute_jumlah_harga_setelah_potongan(self):
        for rec in self:
            harga_setelah_potong = (rec.harga * rec.qty) - (rec.qty * rec.potongan_harga)
            rec.jumlah_harga_setelah_potongan = harga_setelah_potong
            rec.dibayar = harga_setelah_potong
#             print(harga_setelah_potong)

    # @api.onchange('is_siswa_lama')
    # def onchange_is_siswa_lama(self):
    #     domain = {'biaya_id':[('is_siswa_baru_only','=',False)]}
    #     return {'domain':domain, 'value':{'biaya_id':[]}}   
