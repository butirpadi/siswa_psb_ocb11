# -*- coding: utf-8 -*-

from odoo import models, fields, api
from pprint import pprint


class biaya_registrasi(models.Model):
    _name = 'siswa_psb_ocb11.biaya_registrasi'
 
    name = fields.Char('Name', default=lambda self: str(self.tahunajaran_id.name) + " " + str(self.jenjang_id.name))
    tahunajaran_id = fields.Many2one('siswa_ocb11.tahunajaran', string="Tahun Ajaran", required=True, ondelete="cascade")
    jenjang_id = fields.Many2one('siswa_ocb11.jenjang', string="Jenjang", required=True, ondelete="cascade")
    biaya_ta_jenjang_ids = fields.Many2many('siswa_keu_ocb11.biaya_ta_jenjang',
                                            relation='siswa_registrasi_biaya_ta_jenjang_rel',
                                            column1='biaya_registrasi_id',
                                            column2='biaya_ta_jenjang_id',
                                            string="Biaya")
    total_biaya = fields.Float('Total', default=0.0) 
    total_biaya_alt = fields.Float('Total (alt)', default=0.0)
    
    @api.multi
    def write(self, vals):
        
        pprint(vals)
        if 'biaya_ta_jenjang_ids' in vals:
            by_ta_jj_ids = vals['biaya_ta_jenjang_ids'][0][2]
            get_biaya_ta_jenjang_ids = self.env['siswa_keu_ocb11.biaya_ta_jenjang'].search([('id','in',by_ta_jj_ids)])
            
            total_biaya_val = 0
            total_biaya_alt_val = 0
                     
            for biaya in get_biaya_ta_jenjang_ids:
                total_biaya_val += biaya.harga
                total_biaya_alt_val += biaya.harga_alt
                     
            vals['total_biaya'] = total_biaya_val 
            vals['total_biaya_alt'] = total_biaya_alt_val 
            
#             print('ada perubahan')
#             data_vals = vals['biaya_ta_jenjang_ids'][0][2]
#             for data in data_vals:
#                 print(data)
        
#         # update total_biaya
#         print('Update total biaya')        
#         biaya_reg_id = self.env['siswa_psb_ocb11.biaya_registrasi'].search([('id', '=', self.id)])
        
#         for by_reg in biaya_reg_id:
#             if by_reg.biaya_ta_jenjang_ids:
#                 total_biaya_val = 0
#                 total_biaya_alt_val = 0
#                     
#                 for biaya in by_reg.biaya_ta_jenjang_ids:
#                     total_biaya_val += biaya.harga
#                     total_biaya_alt_val += biaya.harga_alt
#                     print(biaya.biaya_id.name)
#                     print(biaya.harga)
#                     print(biaya.harga_alt)
#                     print('------------------------------')
#                 
#                 print('Total Biaya : ' + str(total_biaya_val))
#                 print('Total Biaya : ' + str(total_biaya_alt_val))
#             
#                 vals['total_biaya'] = total_biaya_val 
#                 vals['total_biaya_alt'] = total_biaya_alt_val 
                    
        result = super(biaya_registrasi, self).write(vals)            
     
        return result 
    
    @api.model
    def create(self, vals):
        tahunajaran = self.env['siswa_ocb11.tahunajaran']
        jenjang = self.env['siswa_ocb11.jenjang']        
        
        vals['name'] = str(tahunajaran.search([('id', '=', vals['tahunajaran_id'])]).name) + " " + str(jenjang.search([('id', '=', vals['jenjang_id'])]).name)
        result = super(biaya_registrasi, self).create(vals)
        
        return result
    
    @api.onchange('tahunajaran_id')
    def pembayaran_id_onchange(self):
        return self.recompute_biaya_ta_jenjang()
    
    @api.onchange('jenjang_id')
    def jenjang_id_onchange(self):
        return self.recompute_biaya_ta_jenjang()
    
    def recompute_biaya_ta_jenjang(self):
        domain = {'biaya_ta_jenjang_ids':[('tahunajaran_id', '=', self.tahunajaran_id.id),
                                          ('jenjang_id', '=', self.jenjang_id.id) ]}
        return {'domain':domain, 'value':{'biaya_ta_jenjang_ids':[]}}
    
    def generate_biaya_registrasi(self):
        print('Generate Biaya Registrasi')
        get_biaya_ta_jenjang_ids = self.env['siswa_keu_ocb11.biaya_ta_jenjang'].search([
                                        ('tahunajaran_id', '=', self.tahunajaran_id.id),
                                        ('jenjang_id', '=', self.jenjang_id.id),
                                    ])
#         self.biaya_ta_jenjang_ids =  [(0, 0, get_biaya_ta_jenjang_ids )]
        biaya_ids = []
        for by in get_biaya_ta_jenjang_ids:
            biaya_ids.append(by.id)
        
        self.biaya_ta_jenjang_ids = [(6, 0, biaya_ids)]
    
    @api.model
    def generate_init_on_install(self):
        tahunajaran_ids = self.env['siswa_ocb11.tahunajaran'].search([('active', 'ilike', '%')])
        jenjang_ids = self.env['siswa_ocb11.jenjang'].search([('id', 'ilike', '%')])
        
        print('---------------------------------------')
        print('GENERATE INIT BIAYA REGISTRASI ON INSTALLING MODULE ')
        print('---------------------------------------')
        
        for ta in tahunajaran_ids:
            for jj in jenjang_ids:
#                 print(jj.name + '   ' + ta.name)
                biaya_registrasi_ids = self.env['siswa_psb_ocb11.biaya_registrasi'].search([
                                            ('tahunajaran_id', '=', ta.id),
                                            ('jenjang_id', '=', jj.id),
                                        ])
                if not biaya_registrasi_ids:
                    # create new data
                    new_biaya_registrasi = self.env['siswa_psb_ocb11.biaya_registrasi'].create({
                        'tahunajaran_id' : ta.id,
                        'jenjang_id' : jj.id
                    })
                    new_biaya_registrasi.recompute_biaya_ta_jenjang()


