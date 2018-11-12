# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from pprint import pprint


class siswa_biaya_ta_jenjang_on_calon_siswa_rel(models.Model):
    _name = 'siswa_biaya_ta_jenjang_on_calon_siswa_rel'
    
    biaya_ta_jenjang_id = fields.Many2one('siswa_keu_ocb11.biaya_ta_jenjang', string="Biaya TA Jenjang")
    calon_siswa_id = fields.Many2one('siswa_psb_ocb11.calon_siswa', string="Calon Siswa")
    
    biaya_id = fields.Many2one('siswa_keu_ocb11.biaya', string='Biaya', related="biaya_ta_jenjang_id.biaya_id")
    harga = fields.Float('Harga')
    qty = fields.Integer('Qty', default=1)
    potongan_harga = fields.Float('Potongan', default=0.0)
    jumlah_harga = fields.Float('Jumlah', default=0.0)
    
    @api.onchange('potongan_harga')
    def potongan_harga_onchange(self):
        self.jumlah_harga = (self.harga * self.qty) - (self.qty * self.potongan_harga)
    
    @api.multi
    def write(self, vals):
        if 'potongan_harga' in vals:
            vals['jumlah_harga'] = (self.qty * self.harga) - (self.qty * vals['potongan_harga'])
        
        return super(siswa_biaya_ta_jenjang_on_calon_siswa_rel, self).write(vals) 