# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _
from pprint import pprint
from datetime import datetime, date
import math


class distribusi_siswa(models.Model):
    _name = 'siswa_psb_ocb11.distribusi_siswa'

    state = fields.Selection([('draft', 'Draft'), ('done', 'Done')], string='State', required=True, default='draft')
    name = fields.Char('Name', default='0')
    tahunajaran_id = fields.Many2one('siswa_ocb11.tahunajaran', string="Tahun Ajaran", default=lambda self: self.env['siswa_ocb11.tahunajaran'].search([('active','=',True)]), required=True)
    calon_siswa_ids = fields.Many2many('siswa_psb_ocb11.calon_siswa',relation='siswa_psb_ocb11_distribusi_calon_siswa_rel', column1='distribusi_id',column2='calon_siswa_id', string="Calon Siswa")
    jenjang_id = fields.Many2one('siswa_ocb11.jenjang', string='Jenjang', required=True)
    rombel_ids = fields.Many2many('siswa_ocb11.rombel',relation='siswa_psb_ocb11_distribusi_rombel_rel', column1='distribusi_id',column2='rombel_id', string="Rombongan Belajar", required=True)
    is_manual = fields.Boolean('Manual Distribution', required=True, default=False)
    is_distributed = fields.Boolean('Is Distributed', required=True, default=False)

    def action_reset(self):
        # reset rombels on calon_siswa_ids
        for cs in self.calon_siswa_ids:
            # Update Siswa
            # cs.rombel_id = None
            # cs.is_distributed = False
            self.env['siswa_psb_ocb11.calon_siswa'].search([('id', '=', cs.id)]).write({
                'rombel_id' : None,
                'is_distributed' : False
            })
            # get siswa
            siswa = self.env['res.partner'].search([('calon_siswa_id','=',cs.id)])
            # delete from rombel_siswa            
            self.env['siswa_ocb11.rombel_siswa'].search([('siswa_id','=',siswa.id),('tahunajaran_id','=',self.tahunajaran_id.id)]).unlink()
            # # delete from siswa
            # if not cs.is_siswa_lama:
            #     self.env['res.partner'].search([('calon_siswa_id','=',cs.id)]).unlink()

        # # reset is_distributed to false
        self.is_distributed = False
        self.state = 'draft'

    def action_auto_distribute(self):
        #distribute to rombel
        print('inside looping rombel')
        jk = ['l','p']
        for x in jk:
            print('inside loop jenis kelamin')
            if x == 'l':
                cs_filtered = self.calon_siswa_ids.filtered(lambda x: x.jenis_kelamin == 'laki')
            else:
                cs_filtered = self.calon_siswa_ids.filtered(lambda x: x.jenis_kelamin == 'perempuan')

            for rb in self.rombel_ids:
                cap = math.ceil(len(cs_filtered)/len(self.rombel_ids))
                for cs in cs_filtered:
                    if not cs.rombel_id:
                        if cap > 0:
                            cap -= 1
                            cs.rombel_id = rb.id
    
    def action_confirm_distribute(self):
        # # register siswa
        for cs in self.calon_siswa_ids:
            id_siswa = cs.registered_siswa_id.id
            if cs.is_siswa_lama:
                id_siswa = cs.siswa_id.id

            self.env['res.partner'].search([('id','=',id_siswa)]).write({
                    'rombels' : [(0, 0,  { 'rombel_id' : cs.rombel_id.id, 'tahunajaran_id' : cs.tahunajaran_id.id })],
                    'active_rombel_id' : cs.rombel_id.id,
                })
        
            # update calon_siswa
            cs.is_distributed = True
            
        # update state dsitributed
        self.is_distributed = True
        self.state = 'done'

        # compute rombel_dashboard
        rb_dashboards = self.env['siswa_ocb11.rombel_dashboard'].search([('rombel_id','ilike','%')])
        for rb_dash in rb_dashboards:
            rb_dash.lets_compute_jumlah_siswa()
       
    # def action_manual_distribute(self):
    #     # print('manual distribute')
    #     # node =  eview.xpath("//field[@name='calon_siswa_ids']/tree/field[@name='rombel_id']")
    #     # if login_user_dpt_id:
    #     user_filter =  "[('jenjang_id', '='," + self.jenjang_id.id + " )]"
    #     this.calon_siswa_ids.rombel_id.set('domain',user_filter)

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
        calon_siswas = self.env['siswa_psb_ocb11.calon_siswa'] \
                        .search(['&','&','&',('tahunajaran_id','=',result.tahunajaran_id.id),
                                        ('jenjang_id','=',result.jenjang_id.id),
                                        ('is_distributed','=',False),
                                        ('state','=','reg'),
                                ])
        reg_cs = []
        for cs in calon_siswas:
            print(cs.name)
            self.env['siswa_psb_ocb11.distribusi_siswa'].search([('id','=',result.id)]).write({
                'calon_siswa_ids' : [(4,cs.id)]
            })
        return result
    
    @api.multi
    def unlink(self):
        # clear rombel_id yang telah di set
        for cs in self.calon_siswa_ids:
            cs.rombel_id = None
            
        if self.state == 'done':
            # raise Warning(_("You can not delete Done state data"))
            raise exceptions.except_orm(_('Warning'), _('You can not delete Done state data'))
        return super(distribusi_siswa, self).unlink()