# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from pprint import pprint
from datetime import datetime, date


class distribusi_siswa(models.Model):
    _name = 'siswa_psb_ocb11.distribusi_siswa'

    name = fields.Char('Name', default='0')
    tahunajaran_id = fields.Many2one('siswa_ocb11.tahunajaran', string="Tahun Ajaran", default=lambda self: self.env['siswa_ocb11.tahunajaran'].search([('active','=',True)]), required=True)
    calon_siswa_ids = fields.Many2many('siswa_psb_ocb11.calon_siswa',relation='siswa_psb_ocb11_distribusi_calon_siswa_rel', column1='distribusi_id',column2='calon_siswa_id', string="Calon Siswa")
    jenjang_id = fields.Many2one('siswa_ocb11.jenjang', string='Jenjang', required=True)
    rombel_ids = fields.Many2many('siswa_ocb11.rombel',relation='siswa_psb_ocb11_distribusi_rombel_rel', column1='distribusi_id',column2='rombel_id', string="Rombongan Belajar", required=True)

    @api.onchange('jenjang_id')
    def onchange_jenjang(self):
        domain = {'rombel_ids':[('jenjang_id','=',self.jenjang_id.id)]}
        return {'domain':domain, 'value':{'rombel_ids':[]}}
    
    @api.model
    def create(self, vals):
        vals['name'] = 'Distribusi Siswa'
        result = super(distribusi_siswa, self).create(vals)
        # # update name
        # self.write({
        #     'name' : 'Distribusi Siswa ' + result.jenjang_id.name + ' '  + result.tahunajaran_id.name
        # })
        # add calon siswa
        calon_siswas = self.env['siswa_psb_ocb11.calon_siswa'].search(['&','&',('tahunajaran_id','=',result.tahunajaran_id.id),('jenjang_id','=',result.jenjang_id.id),('is_distributed','=',False)])
        reg_cs = []
        for cs in calon_siswas:
            print(cs.name)
            self.env['siswa_psb_ocb11.distribusi_siswa'].search([('id','=',result.id)]).write({
                'calon_siswa_ids' : [(4,cs.id)]
            })
        return result
    
    # @api.onchange('tahunajaran_id')
    # def onchange_jenjang(self):
    #     jenjang_ids = []
    #     distribusi = self.env['siswa_psb_ocb11.distribusi_siswa'].search([('tahunajaran_id','=',self.id)])
    #     for i in distribusi:
    #         jenjang_ids.append 
    #     domain = {'rombel_ids':[('jenjang_id','=',self.jenjang_id.id)]}
    #     return {'domain':domain, 'value':{'rombel_ids':[]}}