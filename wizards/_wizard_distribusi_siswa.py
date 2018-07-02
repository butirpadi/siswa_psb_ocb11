from odoo import models, fields, api
from pprint import pprint

class distribusi_siswa(models.TransientModel):
    _name = 'siswa_psb_ocb11.wizard_distribusi_siswa'

    name = fields.Char('Name', default='0')
    tahunajaran_id = fields.Many2one('siswa_ocb11.tahunajaran', string="Tahun Ajaran", default=lambda self: self.env['siswa_ocb11.tahunajaran'].search([('active','=',True)]), required=True)
    calon_siswa_ids = fields.Many2many('siswa_psb_ocb11.calon_siswa',relation='siswa_psb_ocb11_wizard_dist_calon_siswa_rel', column1='distribusi_id',column2='calon_siswa_id', string="Calon Siswa")
    jenjang_id = fields.Many2one('siswa_ocb11.jenjang', string='Jenjang', required=True)
    rombel_ids = fields.Many2many('siswa_ocb11.rombel',relation='siswa_psb_ocb11_wizard_dist_rombel_rel', column1='distribusi_id',column2='rombel_id', string="Rombongan Belajar", required=True)

    @api.onchange('jenjang_id')
    def onchange_jenjang(self):
        domain = {'rombel_ids':[('jenjang_id','=',self.jenjang_id.id)]}
        return {'domain':domain, 'value':{'rombel_ids':[]}}

    @api.multi 
    def action_save(self):
        self.ensure_one()
        # update name
        self.write({
            'name' : 'Distribusi Siswa'
        })
        # add calon siswa
        calon_siswas = self.env['siswa_psb_ocb11.calon_siswa'].search(['&','&','&',
                                                    ('tahunajaran_id','=',self.tahunajaran_id.id),
                                                    ('jenjang_id','=',self.jenjang_id.id),
                                                    ('state','=','reg'),
                                                    ('is_distributed','=',False)
                                                    ])
        reg_cs = []
        for cs in calon_siswas:
            self.write({
                'calon_siswa_ids' : [(4,cs.id)]
            })
        # filter rombel
        
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'siswa_psb_ocb11.wizard_distribusi_siswa',
            'target': 'current',
            'res_id': self.id,
            # 'domain' : [('wizard_stock_on_hand_id','=',self.id)],
            # 'context' : {'search_default_group_location_id':1,'search_default_group_product_id':1},
            # 'context' : ctx,
            'type': 'ir.actions.act_window'
        }

    def action_confirm(self):
        print('action confirm')
        for rb in self.rombel_ids:
            rb_kapasitas = rb.kapasitas
            for cs in self.calon_siswa_ids:
                if rb_kapasitas > 0:
                    if not cs.rombel_id:
                        cs.rombel_id = rb.id
                        rb_kapasitas -= 1
                        # insert into res_partner
                        self.env['res.partner'].create({
                            'is_customer' : 1,
                            'name' : cs.nama_calon, 
                            'calon_siswa_id' : cs.id, 
                            'street' : cs.street,
                            'street2' : cs.street2,
                            'zip' : cs.zip,
                            'city' : cs.city,
                            'state_id' : cs.state_id.id,
                            'country_id' : cs.country_id.id,
                            'phone' : cs.phone,
                            'mobile' : cs.mobile,
                            'tanggal_registrasi' : cs.tanggal_registrasi,
                            'tahunajaran_id' : cs.tahunajaran_id.id,
                            'nis' : cs.nis,
                            'panggilan' : cs.panggilan,
                            'jenis_kelamin' : cs.jenis_kelamin,
                            'tanggal_lahir' : cs.tanggal_lahir,
                            'tempat_lahir' : cs.tempat_lahir, 
                            'alamat' : cs.alamat,
                            'telp' : cs.telp,
                            'ayah' : cs.ayah,
                            'pekerjaan_ayah_id' : cs.pekerjaan_ayah_id.id,
                            'telp_ayah' : cs.telp_ayah,
                            'ibu' : cs.ibu,
                            'pekerjaan_ibu_id' : cs.pekerjaan_ibu_id.id,
                            'telp_ibu' : cs.telp_ibu,
                            'rombels' : [(0, 0,  { 'rombel_id' : cs.rombel_id.id, 'tahunajaran_id' : cs.tahunajaran_id.id })],
                            'active_rombel_id' : cs.rombel_id.id,
                            'is_siswa' : True,
                            'anak_ke' : cs.anak_ke,
                            'dari_bersaudara' : cs.dari_bersaudara
                        })
                        # update calon_siswa
                        cs.is_distributed = True
                else:
                    break
    
    def action_reset(self):
        for cs in self.calon_siswa_ids:
            cs.rombel_id = None
            cs.is_distributed = False
            
