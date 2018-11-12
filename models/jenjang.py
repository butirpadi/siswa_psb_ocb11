# -*- coding: utf-8 -*-

from odoo import models, fields, api
from pprint import pprint


class jenjang(models.Model):
    _inherit = 'siswa_ocb11.jenjang'
    
    @api.model
    def create(self, vals):        
        result = super(jenjang, self).create(vals)
        
        print('--------------------------------------------------------------------------')
        print('Auto generating biaya registrasi for Jenjang : ' + result.name)
        print('--------------------------------------------------------------------------')
        # auto generate biaya_registrasi on jenjang create
        tahunajaran_ids = self.env['siswa_ocb11.tahunajaran'].search([('id','ilike','%'),
                                                                      ('active','ilike','%')])
        for ta in tahunajaran_ids:
            # get biaya_registrasi with jenjang
            biaya_registrasi_id = self.env['siswa_psb_ocb11.biaya_registrasi'].search([('tahunajaran_id', '=', ta.id), ('jenjang_id', '=', result.id)])
            pprint(biaya_registrasi_id)
            if not biaya_registrasi_id:
                new_biaya_registrasi = self.env['siswa_psb_ocb11.biaya_registrasi'].create({
                        'tahunajaran_id' : ta.id,
                        'jenjang_id' : result.id
                    })
                new_biaya_registrasi.recompute_biaya_ta_jenjang()
        
        return result    
