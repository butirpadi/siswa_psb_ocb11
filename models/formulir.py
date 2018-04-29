# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime

class formulir(models.Model):
    _name = 'siswa_psb_ocb11.formulir'

    name = fields.Char(string='Nomor Form', requred=True, default='New')
    nama_calon = fields.Char('Nama', requred=True,)
    tahunajaran_id = fields.Many2one('siswa_ocb11.tahunajaran', string='Tahun Ajaran', required=True, default=lambda x: x.env['siswa_ocb11.tahunajaran'].search([('active','=',True)]))
    tanggal = fields.Date('Tanggal', required=True, default=datetime.today())
    harga = fields.Float('Harga', required=True, default=0)
    jenjang = fields.Selection([(1, 'PG'), (2, 'TK A'), (3, 'TK B')], string='Jenjang', required=True, default=1)

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            if 'company_id' in vals:
                vals['name'] = self.env['ir.sequence'].with_context(force_company=vals['company_id']).next_by_code('formulir.siswa.psb.ocb11') or _('New')
            else:
                vals['name'] = self.env['ir.sequence'].next_by_code('formulir.siswa.psb.ocb11') or _('New')

        result = super(formulir, self).create(vals)
        return result
    
    def action_print(self):
        return self.env.ref('siswa_psb_ocb11.report_formulir_action').report_action(self)
