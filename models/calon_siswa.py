# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _
from pprint import pprint
from datetime import datetime, date
import calendar

class calon_siswa(models.Model):
    _name = 'siswa_psb_ocb11.calon_siswa'

    state = fields.Selection([('draft', 'Draft'), ('reg', 'Registered')], string='State', required=True, default='draft')
    is_siswa_lama = fields.Boolean('Siswa Lama', default=False)
    siswa_id = fields.Many2one('res.partner', string="Data Siswa Lama")
    no_induk = fields.Char('No. Induk', related="siswa_id.induk")
    registered_siswa_id = fields.Many2one('res.partner', string="Registered Siswa")
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
    jenjang_id = fields.Many2one('siswa_ocb11.jenjang', string='Jenjang', required=True)
    tanggal_registrasi = fields.Date('Tanggal Registrasi', required=True, default=datetime.today())
    tahunajaran_id = fields.Many2one('siswa_ocb11.tahunajaran', string='Tahun Diterima')
    induk = fields.Char(string='Internal Reference', required=False, copy=False, readonly=True, default="New")
    nis = fields.Char(string="NIS", required=False)
    panggilan = fields.Char(string="Panggilan")
    jenis_kelamin = fields.Selection([('laki', 'Laki-laki'), ('perempuan', 'Perempuan')], string='Jenis Kelamin', required=True)
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
    anak_ke = fields.Integer('Anak ke')
    dari_bersaudara = fields.Integer('Dari Bersaudara')
    usia = fields.Float('Usia', compute="_compute_usia")
    is_distributed = fields.Boolean('is distributed', default=False)
    rombel_id = fields.Many2one('siswa_ocb11.rombel',string='Rombongan Belajar', domain="[('jenjang_id','=',jenjang_id)]")
    payment_lines = fields.One2many('siswa_psb_ocb11.calon_siswa_biaya', 
                    inverse_name='calon_siswa_id', 
                    string='Pembayaran')
    biaya_optional_ids = fields.Many2many('siswa_keu_ocb11.biaya',
                        relation='siswa_psb_ocb11_biaya_optional_calon_siswa_rel', 
                        column1='calon_siswa_id', column2='biaya_id', 
                        string="Biaya Opsional", ondelete="cascade")
    total = fields.Float('Total Bayar')
    terbilang = fields.Char('Terbilang')
    satuan = ['', 'satu', 'dua', 'tiga', 'empat', 'lima', 'enam', 'tujuh',
          'delapan', 'sembilan', 'sepuluh', 'sebelas']
    bayar_tunai = fields.Float('Bayar Tunai', default=0)

    def calculate_bayar_tunai(self):
        tunai = self.bayar_tunai
        for pay in self.payment_lines:
            if tunai > 0 :
                if tunai > pay.harga :
                    pay.dibayar = pay.harga
                    tunai -= pay.harga
                else:
                    pay.dibayar = tunai
                    tunai = 0
            else:
                # jika tunai tidak mencukupi maka hapus saja payment nya
                # pay.unlink()
                # ralat jika tunai tidak mencukupi makan set bayar = 0 
                pay.dibayar = 0

    @api.onchange('is_siswa_lama')
    def onchange_is_siswa_lama(self):
        print('onchange is siswa lama')
        # domain = {'siswa_id':[('tahunajaran_id','!=',self.tahunajaran_id.id),('is_siswa','=',True)]}
        domain = {'siswa_id':[('is_siswa','=',True)]}
        return {'domain':domain, 'value':{'siswa_id':[]}}    
    
    @api.onchange('siswa_id')
    def onchange_siswa_id(self):
        # get prev tahunajaran
        prev_ta = self.env['siswa_ocb11.tahunajaran'].search([
            ('sort_order', '=', self.tahunajaran_id.sort_order - 1)
        ])

        # get rombel siswa
        rombel_siswa = self.env['siswa_ocb11.rombel_siswa'].search([
            ('tahunajaran_id', '=', prev_ta.id),
            ('siswa_id', '=', self.siswa_id.id),
        ]).rombel_id

        # filter jenjang 
        domain = {'jenjang_id':[('order','>',rombel_siswa.jenjang_id.order )]}
        return {'domain':domain, 'value':{'jenjang_id':[]}} 

        # set data siswa
    # @api.onchange('siswa_id')
    # def siswa_id_onchange(self):
        self.name = self.siswa_id.name
        self.panggilan = self.siswa_id.panggilan
        self.nis = self.siswa_id.nis
        self.jenis_kelamin = self.siswa_id.jenis_kelamin
        self.tempat_lahir = self.siswa_id.tempat_lahir
        self.tanggal_lahir = self.siswa_id.tanggal_lahir
        self.anak_ke = self.siswa_id.dari_bersaudara
        self.street = self.siswa_id.street
        self.street2 = self.siswa_id.street2
        self.city = self.siswa_id.city
        self.state_id = self.siswa_id.state_id
        self.zip = self.siswa_id.zip
        self.country_id = self.siswa_id.country_id
        self.phone = self.siswa_id.phone
        self.mobile = self.siswa_id.mobile
        self.ayah = self.siswa_id.ayah
        self.pekerjaan_ayah_id = self.siswa_id.pekerjaan_ayah_id
        self.telp_ayah = self.siswa_id.telp_ayah
        self.ibu = self.siswa_id.ibu
        self.pekerjaan_ibu_id = self.siswa_id.pekerjaan_ibu_id
        self.telp_ibu = self.siswa_id.telp_ibu
    
    # @api.onchange('jenjan_id')
    # def onchange_jenjang_id(self): # set filter rombel_id
    #     domain = {'rombel_id':[('jenjang_id','=',self.jenjang_id)]}
    #     return {'domain':domain, 'value':{'rombel_id':[]}} 

    def get_current_jenjang_id(self):
        return self.jenjang_id

    @api.model
    def create(self, vals):
        if vals.get('reg_number', _('New')) == _('New'):
            if 'company_id' in vals:
                vals['reg_number'] = self.env['ir.sequence'].with_context(force_company=vals['company_id']).next_by_code('reg.no.siswa.psb.ocb11') or _('New')
            else:
                vals['reg_number'] = self.env['ir.sequence'].next_by_code('reg.no.siswa.psb.ocb11') or _('New')

        result = super(calon_siswa, self).create(vals)
        return result
    
    def action_confirm(self):
        # check pembayaran is set or not
        if len(self.payment_lines) > 0:
            # register siswa to res.partner
            if self.is_siswa_lama:
                # update siswa lama
                self.env['res.partner'].search([('id','=',self.siswa_id.id)]).write({
                    # 'rombels' : [(0, 0,  { 'rombel_id' : self.rombel_id.id, 'tahunajaran_id' : self.tahunajaran_id.id })],
                    # 'active_rombel_id' : self.rombel_id.id,
                    'is_siswa_lama' : True,
                    'calon_siswa_id' : self.id, 
                })
            else:
                # insert into res_partner
                new_siswa = self.env['res.partner'].create({
                    'is_customer' : 1,
                    'name' : self.name, 
                    'calon_siswa_id' : self.id, 
                    'street' : self.street,
                    'street2' : self.street2,
                    'zip' : self.zip,
                    'city' : self.city,
                    'state_id' : self.state_id.id,
                    'country_id' : self.country_id.id,
                    'phone' : self.phone,
                    'mobile' : self.mobile,
                    'tanggal_registrasi' : self.tanggal_registrasi,
                    'tahunajaran_id' : self.tahunajaran_id.id,
                    'nis' : self.nis,
                    'panggilan' : self.panggilan,
                    'jenis_kelamin' : self.jenis_kelamin,
                    'tanggal_lahir' : self.tanggal_lahir,
                    'tempat_lahir' : self.tempat_lahir, 
                    'alamat' : self.alamat,
                    'telp' : self.telp,
                    'ayah' : self.ayah,
                    'pekerjaan_ayah_id' : self.pekerjaan_ayah_id.id,
                    'telp_ayah' : self.telp_ayah,
                    'ibu' : self.ibu,
                    'pekerjaan_ibu_id' : self.pekerjaan_ibu_id.id,
                    'telp_ibu' : self.telp_ibu,
                    # 'rombels' : [(0, 0,  { 'rombel_id' : self.rombel_id.id, 'tahunajaran_id' : self.tahunajaran_id.id })],
                    # 'active_rombel_id' : self.rombel_id.id,
                    'is_siswa' : True,
                    'anak_ke' : self.anak_ke,
                    'dari_bersaudara' : self.dari_bersaudara
                })
                # self.siswa_id = new_siswa.id 
                self.registered_siswa_id = new_siswa.id
                # self.siswa_id = new_siswa.id

            # update state
            self.state = 'reg'

            # assign siswa biaya
            # get tahunajaran_jenjang
            ta_jenjang = self.env['siswa_ocb11.tahunajaran_jenjang'].search([('tahunajaran_id', '=', self.tahunajaran_id.id),
            ('jenjang_id', '=', self.jenjang_id.id)
            ])
            
            # assign biaya to siswa
            total_biaya = 0.0
            if self.is_siswa_lama:
                id_siswa = self.siswa_id.id 
            else:
                id_siswa = new_siswa.id

            for by in ta_jenjang.biayas:

                # cek biaya apakah is_optional dan apakah di pilih dalam payment_lines
                by_found = False
                if by.biaya_id.is_optional:
                    for by_in_pay in self.payment_lines:
                        if by.biaya_id.id == by_in_pay.biaya_id.id:
                            by_found = True
                    if not by_found:
                        continue
                        
                if self.is_siswa_lama and by.biaya_id.is_siswa_baru_only:
                    print('skip')
                    continue
                else:
                    print('JENJANG ID : ' + str(self.jenjang_id.id))
                    if by.biaya_id.is_bulanan:
                        for bulan_index in range(1,13):
                            harga = by.harga
                            
                            if by.is_different_by_gender:
                                if self.jenis_kelamin == 'perempuan':
                                    harga = by.harga_alt

                            self.env['siswa_keu_ocb11.siswa_biaya'].create({
                                'name' : by.biaya_id.name + ' ' + calendar.month_name[bulan_index],
                                'siswa_id' : id_siswa,
                                'tahunajaran_id' : self.tahunajaran_id.id,
                                'biaya_id' : by.biaya_id.id,
                                'bulan' : bulan_index,
                                'harga' : harga,
                                'amount_due' : harga,
                                'jenjang_id' : self.jenjang_id.id
                            })
                            total_biaya += harga
                    else:
                        harga = by.harga
                        
                        if by.is_different_by_gender:
                            if self.jenis_kelamin == 'perempuan':
                                harga = by.harga_alt

                        self.env['siswa_keu_ocb11.siswa_biaya'].create({
                            'name' : by.biaya_id.name,
                            'siswa_id' : id_siswa,
                            'tahunajaran_id' : self.tahunajaran_id.id,
                            'biaya_id' : by.biaya_id.id,
                            'harga' : harga,
                            'amount_due' : harga,
                            'jenjang_id' : self.jenjang_id.id
                        })
                        total_biaya += harga
                        
            # set total_biaya dan amount_due
            # total_biaya = sum(by.harga for by in self.biayas)
            print('ID SISWA : ' + str(id_siswa))
            res_partner_siswa = self.env['res.partner'].search([('id','=',id_siswa)])
            self.env['res.partner'].search([('id','=',id_siswa)]).write({
                'total_biaya' : total_biaya,
                'amount_due_biaya' : res_partner_siswa.amount_due_biaya + total_biaya,
            })         

            # add pembayaran
            pembayaran = self.env['siswa_keu_ocb11.pembayaran'].create({
                'tanggal' : self.tanggal_registrasi ,
                'tahunajaran_id' : self.tahunajaran_id.id,
                'siswa_id' : id_siswa,
            })

            # reset pembayaran_lines
            pembayaran.pembayaran_lines.unlink()
            pembayaran.total = 0

            total_bayar = 0.0
            for pay in self.payment_lines:

                print('Payment Lines : ')
                print('harga : ' + str(pay.harga))
                print('dibayar : ' + str(pay.dibayar))
                print('biaya_id : ' + str(pay.biaya_id.id))


                # get siswa_biaya
                if pay.dibayar > 0: # jangan dimasukkan ke pembayaran untuk yang nilai dibayarnya = 0
                    if pay.biaya_id:
                        if pay.biaya_id.is_bulanan:
                            pay_biaya_id = self.env['siswa_keu_ocb11.siswa_biaya'].search([
                                        ('siswa_id','=',id_siswa),
                                        ('tahunajaran_id','=',self.tahunajaran_id.id),
                                        ('biaya_id','=',pay.biaya_id.id),
                                        ('tahunajaran_id','=',self.tahunajaran_id.id),
                                        ('bulan','=',pay.bulan),
                                        ]).id
                        else:
                            pay_biaya_id = self.env['siswa_keu_ocb11.siswa_biaya'].search([
                                        ('siswa_id','=',id_siswa),
                                        ('tahunajaran_id','=',self.tahunajaran_id.id),
                                        ('biaya_id','=',pay.biaya_id.id),
                                        ('tahunajaran_id','=',self.tahunajaran_id.id),
                                        ]).id
                        
                        pembayaran.pembayaran_lines =  [(0, 0,  { 
                                                'biaya_id' : pay_biaya_id, 
                                                'bayar' : pay.dibayar 
                                                })]
                        total_bayar += pay.dibayar
                
                print('pay_biaya_id : ' + str(pay_biaya_id))
                print('-------------------')

            # raise exceptions.except_orm(_('Warning'), _('TEST ERROR'))

            # confirm pembayaran 
            pembayaran.action_confirm()

            # set terbilang
            if total_bayar == 0:
                self.terbilang = 'nol'
            else:
                t = self.terbilang_(total_bayar)
                while '' in t:
                    t.remove('')
                self.terbilang = ' '.join(t) 
            
            self.terbilang += ' Rupiah'
            # set total
            self.total = total_bayar

            # raise exceptions.except_orm(_('Warning'), _('You can not delete Done state data'))
        else:
            raise exceptions.except_orm(_('Warning'), _('Can not confirm this registration, complete payment first!'))
    
    def terbilang_(self, n):
        if n >= 0 and n <= 11:
            hasil = [self.satuan[int(n)]]
        elif n >= 12 and n <= 19:
            hasil = self.terbilang_(n % 10) + ['belas']
        elif n >= 20 and n <= 99:
            hasil = self.terbilang_(n / 10) + ['puluh'] + self.terbilang_(n % 10)
        elif n >= 100 and n <= 199:
            hasil = ['seratus'] + self.terbilang_(n - 100)
        elif n >= 200 and n <= 999:
            hasil = self.terbilang_(n / 100) + ['ratus'] + self.terbilang_(n % 100)
        elif n >= 1000 and n <= 1999:
            hasil = ['seribu'] + self.terbilang_(n - 1000)
        elif n >= 2000 and n <= 999999:
            hasil = self.terbilang_(n / 1000) + ['ribu'] + self.terbilang_(n % 1000)
        elif n >= 1000000 and n <= 999999999:
            hasil = self.terbilang_(n / 1000000) + ['juta'] + self.terbilang_(n % 1000000)
        else:
            hasil = self.terbilang_(n / 1000000000) + ['milyar'] + self.terbilang_(n % 100000000)
        return hasil

    
    def action_print_kwitansi(self):
        # return self.env.ref('siswa_psb_ocb11.report_kwitansi_registrasi_action').report_action(self)
        return self.env.ref('siswa_psb_ocb11.report_bukti_pembayaran_registrasi_action').report_action(self)

    def action_reset(self):
        # reset confirmed calon siswa
        id_siswa = self.registered_siswa_id.id
        if self.is_siswa_lama:
            id_siswa = self.siswa_id.id
        
        # remove pembayaran
        pembayaran = self.env['siswa_keu_ocb11.pembayaran'].search([
                                ('siswa_id','=',id_siswa),
                                ('tahunajaran_id','=',self.tahunajaran_id.id)
                            ])

        if pembayaran:
            for pb in pembayaran:
                if pb.state == 'paid':
                    pb.action_cancel()
                pb.unlink()
                print('Pembayaran Deleted')
        # --------------------------------        
        
        # remove tabungan siswa
        print('Delete Data Tabungan : ')
        tabungan = self.env['siswa_tab_ocb11.tabungan'].search([
                                ('siswa_id','=',id_siswa)
                            ])
        pprint(tabungan)
        for tab in tabungan:
            if tab.state == 'post':
                tab.action_cancel()
            tab.unlink()

        # remove siswa biaya
        siswa_biaya = self.env['siswa_keu_ocb11.siswa_biaya'].search([('siswa_id','=',id_siswa)])
        siswa_biaya.unlink()
        print('Siswa Deleted')

        # remove res_partner
        if not self.is_siswa_lama:
            self.env['res.partner'].search([('id','=',id_siswa)]).unlink()

        # update calon_siswa state
        self.state = 'draft'

        # Recompute Tagihan Siswa Dashboard/ Keuangan Dashboard
        dash_keuangan_id = self.env['ir.model.data'].search([('name','=','default_dashboard_pembayaran')]).res_id
        dash_keuangan = self.env['siswa_keu_ocb11.keuangan_dashboard'].search([('id','=',dash_keuangan_id)])
        for dash in dash_keuangan:
            dash.compute_keuangan()  
        print('Recompute Keuangan Dashboard done')

        # raise exceptions.except_orm(_('Warning'), _('Reset Succesfull'))
        
    # def generate_pembayaran(self):
    #     # clear data sebelumnya
    #     self.payment_lines.unlink()

    #     # get biaya registrasi
    #     biaya_registrasi_ids = self.env['siswa_psb_ocb11.biaya_registrasi'].search([
    #         ('tahunajaran_id', '=', self.tahunajaran_id.id),
    #         ('jenjang_id', '=', self.jenjang_id.id),
    #     ])

    #     for by in biaya_registrasi_ids[0].biaya_ta_jenjang_ids:
    #         harga = by.harga
    #         if by.biaya_id.is_different_by_gender and self.jenis_kelamin == 'perempuan':
    #                 harga = by.harga_alt
    #         self.payment_lines =  [(0, 0,  { 
    #                                 'biaya_id' : by.biaya_id.id, 
    #                                 'bulan' : by.bulan,
    #                                 'harga' : harga,
    #                                 'dibayar' : harga,
    #                                 })]

    @api.multi
    def write(self, vals):
        pprint(vals)

        result = super(calon_siswa, self).write(vals)       
        
        return result

    def generate_pembayaran_default(self):
        print('inside generate pembayaran default')
        # clear data sebelumnya
        self.payment_lines.unlink()
        # clear biaya optional
        self.biaya_optional_ids.unlink()
        # clear bayar tuna
        self.bayar_tunai = 0

        # get biaya registrasi
        ta_jenjang = self.env['siswa_ocb11.tahunajaran_jenjang'].search([
            ('tahunajaran_id', '=', self.tahunajaran_id.id),
            ('jenjang_id', '=', self.jenjang_id.id),
        ])
        biaya_registrasi_ids = self.env['siswa_keu_ocb11.biaya_ta_jenjang'].search([
            ('tahunajaran_jenjang_id', '=', ta_jenjang.id)
        ])

        # for by in biaya_registrasi_ids[0].biaya_ta_jenjang_ids:
        for by in biaya_registrasi_ids:
            if not by.biaya_id.is_optional:
                harga = by.harga
                
                if by.biaya_id.is_different_by_gender and self.jenis_kelamin == 'perempuan':
                        harga = by.harga_alt
                
                bulan = by.bulan
                if by.is_bulanan:
                    bulan = 7

                self.payment_lines =  [(0, 0,  { 
                                        'biaya_id' : by.biaya_id.id, 
                                        'bulan' : bulan,
                                        'harga' : harga,
                                        'dibayar' : harga,
                                        })]

    def generate_biaya_optional(self):
        for by in self.biaya_optional_ids:
            # get biaya registrasi
            ta_jenjang = self.env['siswa_ocb11.tahunajaran_jenjang'].search([
                ('tahunajaran_id', '=', self.tahunajaran_id.id),
                ('jenjang_id', '=', self.jenjang_id.id),
            ])
            biaya_registrasi_id = self.env['siswa_keu_ocb11.biaya_ta_jenjang'].search([
                ('tahunajaran_jenjang_id', '=', ta_jenjang.id),
                ('biaya_id', '=', by.id),
            ])

            harga = biaya_registrasi_id.harga
                
            if biaya_registrasi_id.biaya_id.is_different_by_gender and self.jenis_kelamin == 'perempuan':
                    harga = biaya_registrasi_id.harga_alt

            bulan = biaya_registrasi_id.bulan
            
            if biaya_registrasi_id.is_bulanan:
                bulan = 7

            # loop untuk mencari di payment_lines apakah biaya ini telah tersedia
            is_found = False
            for byPay in self.payment_lines:
                if byPay.biaya_id.id == by.id :
                    is_found = True
                    break

            if not is_found:
                newid = self.env['siswa_psb_ocb11.calon_siswa_biaya'].create({
                    'calon_siswa_id' : self.id,
                    'biaya_id' : by.id, 
                    'bulan' : bulan,
                    'harga' : harga,
                    'dibayar' : harga,
                })

                # after generate to payment_lines, clear the biaya_optional_ids
                self.biaya_optional_ids =  [[6, False, []]]
    
    # @api.onchange('payment_lines')
    # def payment_lines_onchange(self):
    #     print('onchange on payment_lines_onchange')
    #     added_biaya_optional_ids = []
    #     for by in self.payment_lines:
    #         if by.biaya_id.is_optional:
    #             added_biaya_optional_ids.append(by.id)

    #     domain = {'biaya_optional_ids':[('id','not in',added_biaya_optional_ids)]}
    #     return {'domain':domain, 'value':{'biaya_optional_ids':[]}}    

    # def filter_rombel_id(self):
    #     domain = {'rombel_id':[('jenjang_id','=',self.jenjang_id)]}
    #     self.rombel_id =  {'domain':domain, 'value':{'rombel_id':[]}} 



