# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime

class formulir(models.Model):
    _name = 'siswa_psb_ocb11.formulir'

    name = fields.Char(string='Nomor Form', requred=True, default='New')
    is_registered = fields.Boolean('is registered', default=False)
    nama_calon = fields.Char('Nama', requred=True)
    tahunajaran_id = fields.Many2one('siswa_ocb11.tahunajaran', string='Tahun Ajaran', required=True, default=lambda x: x.env['siswa_ocb11.tahunajaran'].search([('active','=',True)]))
    tanggal = fields.Date('Tanggal', required=True, default=datetime.today())
    harga = fields.Float('Harga', required=True, default=0)
    # jenjang = fields.Selection([(1, 'PG'), (2, 'TK A'), (3, 'TK B')], string='Jenjang', required=True, default=1)
    jenjang_id = fields.Many2one('siswa_ocb11.jenjang', string='Jenjang', required=True)
    terbilang = fields.Char('Terbilang')
    satuan = ['', 'satu', 'dua', 'tiga', 'empat', 'lima', 'enam', 'tujuh',
          'delapan', 'sembilan', 'sepuluh', 'sebelas']
          
    def generate_terbilang(self, n):
        if n >= 0 and n <= 11:
            hasil = [self.satuan[int(n)]]
        elif n >= 12 and n <= 19:
            hasil = self.generate_terbilang(n % 10) + ['belas']
        elif n >= 20 and n <= 99:
            hasil = self.generate_terbilang(n / 10) + ['puluh'] + self.generate_terbilang(n % 10)
        elif n >= 100 and n <= 199:
            hasil = ['seratus'] + self.generate_terbilang(n - 100)
        elif n >= 200 and n <= 999:
            hasil = self.generate_terbilang(n / 100) + ['ratus'] + self.generate_terbilang(n % 100)
        elif n >= 1000 and n <= 1999:
            hasil = ['seribu'] + self.generate_terbilang(n - 1000)
        elif n >= 2000 and n <= 999999:
            hasil = self.generate_terbilang(n / 1000) + ['ribu'] + self.generate_terbilang(n % 1000)
        elif n >= 1000000 and n <= 999999999:
            hasil = self.generate_terbilang(n / 1000000) + ['juta'] + self.generate_terbilang(n % 1000000)
        else:
            hasil = self.generate_terbilang(n / 1000000000) + ['milyar'] + self.generate_terbilang(n % 100000000)
        return hasil

    @api.depends('harga')
    def _compute_terbilang(self):
        if self.harga == 0:
            self.terbilang = 'nol'
        else:
            t = self.generate_terbilang(self.harga)
            while '' in t:
                t.remove('')
            self.terbilang = ' '.join(t)

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            if 'company_id' in vals:
                vals['name'] = self.env['ir.sequence'].with_context(force_company=vals['company_id']).next_by_code('formulir.siswa.psb.ocb11') or _('New')
            else:
                vals['name'] = self.env['ir.sequence'].next_by_code('formulir.siswa.psb.ocb11') or _('New')
        
        if vals['harga'] == 0:
            vals['terbilang'] = 'nol'
        else:
            t = self.generate_terbilang(vals['harga'])
            while '' in t:
                t.remove('')
            vals['terbilang'] = ' '.join(t)
        

        result = super(formulir, self).create(vals)
        return result
    
    def action_print(self):
        return self.env.ref('siswa_psb_ocb11.report_formulir_action').report_action(self)
    
    def action_print_kwitansi(self):
        return self.env.ref('siswa_psb_ocb11.report_kwitansi_formulir_action').report_action(self)
