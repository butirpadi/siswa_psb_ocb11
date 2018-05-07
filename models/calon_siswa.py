# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from pprint import pprint
from datetime import datetime, date

class calon_siswa(models.Model):
    _name = 'siswa_psb_ocb11.calon_siswa'

    state = fields.Selection([('draft', 'Draft'), ('reg', 'Registered')], string='State', required=True, default='draft')
    tahunajaran_id = fields.Many2one('siswa_ocb11.tahunajaran', string='Tahun Ajaran', required=True, default=lambda self: self.env['siswa_ocb11.tahunajaran'].search([('active','=',True)]))
    name = fields.Char('Nama', required=True)
    reg_number = fields.Char('Nomor Registrasi', required=True, default='New')
    street = fields.Char()
    street2 = fields.Char()
    zip = fields.Char()
    city = fields.Char()
    state_id = fields.Many2one("res.country.state", string='State')
    country_id = fields.Many2one('res.country', string='Country')
    phone = fields.Char()
    mobile = fields.Char()
    # formulir_id = fields.Many2one('siswa_psb_ocb11.formulir', string='Nomor Formulir', required=True, domain=[('is_registered', '=', False)], ondelete="restrict")
    # nama_calon = fields.Char('Nama Calon', related='formulir_id.nama_calon')
    
    jenjang_id = fields.Many2one('siswa_ocb11.jenjang', string='Jenjang')
    # formulir_tahunajaran_id = fields.Many2one('siswa_ocb11.tahunajaran', string='Tahun Diterima', related='formulir_id.tahunajaran_id')
    tanggal_registrasi = fields.Date('Tanggal Registrasi', required=True, default=datetime.today())
    tahunajaran_id = fields.Many2one('siswa_ocb11.tahunajaran', string='Tahun Diterima')
    induk = fields.Char(string='Internal Reference', required=False, copy=False, readonly=True, default="New")
    nis = fields.Char(string="NIS", required=False)
    panggilan = fields.Char(string="Panggilan")
    jenis_kelamin = fields.Selection([('laki', 'Laki-laki'), ('perempuan', 'Perempuan')], string='Jenis Kelamin', required=False)
    tanggal_lahir = fields.Date(string='Tanggal Lahir', required=False)
    tempat_lahir = fields.Char(string='Tempat Lahir', required=False)
    alamat = fields.Char(string='Alamat')
    telp = fields.Char(string='Telp')
    ayah = fields.Char(string='Ayah')
    pekerjaan_ayah_id = fields.Many2one('siswa_ocb11.pekerjaan', string='Pekerjaan Ayah')
    telp_ayah = fields.Char(string='Telp. Ayah')
    ibu = fields.Char(string='Ibu')
    pekerjaan_ibu_id = fields.Many2one('siswa_ocb11.pekerjaan', string='Pekerjaan Ibu')
    telp_ibu = fields.Char(string='Telp. Ibu')
    rombels = fields.One2many('siswa_ocb11.rombel_siswa', inverse_name='siswa_id' , string='Detail Rombongan Belajar')
    active_rombel_id = fields.Many2one('siswa_ocb11.rombel', string='Rombongan Belajar', compute='_compute_rombel', store=True)
    is_siswa = fields.Boolean(default=False)
    mutasi = fields.Boolean(string='Mutasi', default=False)
    lulus = fields.Boolean(string='Lulus', default=False)
    non_aktif_selection = fields.Selection([('mutasi', 'Mutasi'), ('lulus', 'Lulus'), ('meninggal', 'Meninggal Dunia')], string='Keterangan')
    tanggal_non_aktif = fields.Date('Tanggal Non Aktif')
    anak_ke = fields.Float('Anak ke')
    dari_bersaudara = fields.Float('Dari Bersaudara')
    usia = fields.Float('Usia', compute="_compute_usia")
    is_distributed = fields.Boolean('is distributed', default=False)
    rombel_id = fields.Many2one('siswa_ocb11.rombel',string='Rombongan Belajar')


    # @api.multi
    # def unlink(self):
    #     print('Formulir ID : '  + str(self.formulir_id.id))
    #     # set formulir to unregistered
    #     self.env['siswa_psb_ocb11.formulir'].search([('id', '=', self.formulir_id.id)]).update({
    #         'is_registered' : False
    #     })
    #     res = super(calon_siswa, self).unlink()
    #     return res

    @api.model
    def create(self, vals):
        if vals.get('reg_number', _('New')) == _('New'):
            if 'company_id' in vals:
                vals['reg_number'] = self.env['ir.sequence'].with_context(force_company=vals['company_id']).next_by_code('reg.no.siswa.psb.ocb11') or _('New')
            else:
                vals['reg_number'] = self.env['ir.sequence'].next_by_code('reg.no.siswa.psb.ocb11') or _('New')

        result = super(calon_siswa, self).create(vals)
        # # set formulit to registered 
        # self.env['siswa_psb_ocb11.formulir'].search([('id', '=', result.formulir_id.id)]).update({
        #     'is_registered' : True
        # })
        return result

    # @api.depends('formulir_id')
    # def _compute_name(self):
    #     for rec in self:
    #         # self.ensure_one()
    #         rec.name = rec.formulir_id.name
    #         rec.tahunajaran_id = rec.formulir_tahunajaran_id
    #         rec.jenjang_id = rec.formulir_id.jenjang_id.id
            

    @api.depends('tanggal_lahir')
    def _compute_usia(self):
        for rec in self:
            print(type(rec.tanggal_lahir))
            today = date.today()
            usia =  today.year - rec.year - ((today.month, today.day) < (rec.month, rec.day))
            print(usia)
            # if rec.tanggal_lahir:
            #     print(rec.tanggal_lahir.strftime('%Y/%m/%d'))
        # for rec in self:
        #     if rec.tanggal_lahir:
        #         born = date(rec.tanggal_lahir)
        #         today = date.today()
        #         usia = today.year - born.year - int((today.month, today.day) < (born.month, born.day))
        #         # print('Usia : ' + str(usia))
    