# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime
from pprint import pprint

class biaya_registrasi(models.Model):
    _name = 'siswa_psb_ocb11.biaya_registrasi'

    name = fields.Char(string='Name', requred=True, default='New')
    tahunajaran_id = fields.Many2one('siswa_ocb11.tahunajaran', string="Tahun Ajaran", required=True)
    jenjang_id = fields.Many2one('siswa_ocb11.jenjang', string='Jenjang', required=True)
    tahunajaran_jenjang_id = fields.Many2one('siswa_ocb11.tahunajaran_jenjang', string='Tahun Ajaran - Jenjang', required=True)
    biaya_ta_jenjang_ids = fields.Many2many('siswa_keu_ocb11.biaya_ta_jenjang',relation='siswa_psb_ocb11_biaya_registrasi_rel', column1='biaya_registrasi_id',column2='biaya_ta_jenjang_id', string="Biaya")

    @api.onchange('tahunajaran_id')
    def onchange_tahun_ajaran(self):
        # get jenjang_id on this tahunjaran
        by_regs = self.env['siswa_psb_ocb11.biaya_registrasi'].search([
                            ('tahunajaran_id' ,'=', self.tahunajaran_id.id)
                        ])
        print('biaya registrasi')
        pprint(by_regs)
        ta_ids = []
        for by in by_regs:
            ta_ids.append(by.tahunajaran_jenjang_id.id)
        
        print('List tahun ajaran jenjang id')
        pprint(ta_ids)

        domain = {'tahunajaran_jenjang_id':[
                    ('tahunajaran_id','=',self.tahunajaran_id.id), 
                    ('id','not in', ta_ids), 
                    ]}

        return {'domain':domain, 'value':{'tahunajaran_jenjang_id':[]}}
    
    @api.onchange('tahunajaran_jenjang_id')
    def onchange_tahun_ajaran_jenjang(self):
        self.jenjang_id = self.tahunajaran_jenjang_id.jenjang_id
        domain = {'biaya_ta_jenjang_ids':[('tahunajaran_jenjang_id','=',self.tahunajaran_jenjang_id.id)]}
        return {'domain':domain, 'value':{'biaya_ta_jenjang_ids':[]}}

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            tahunajaran = self.env['siswa_ocb11.tahunajaran'].search([('id','=',vals['tahunajaran_id'])])
            jenjang = self.env['siswa_ocb11.jenjang'].search([('id','=',vals['jenjang_id'])])
            vals['name'] = tahunajaran[0].name + ' ' + jenjang[0].name

        result = super(biaya_registrasi, self).create(vals)
        return result
    
    
   