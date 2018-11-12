from odoo import models, fields, api
from pprint import pprint

class wizard_report_distribusi_siswa(models.TransientModel):
    _name = 'siswa_psb_ocb11.wizard_report_distribusi_siswa'

    name = fields.Char('Name', default='0')
    tahunajaran_id = fields.Many2one('siswa_ocb11.tahunajaran', string="Tahun Ajaran", default=lambda self: self.env['siswa_ocb11.tahunajaran'].search([('active','=',True)]), required=True)
    rombel_id = fields.Many2one('siswa_ocb11.rombel', string='Rombongan Belajar')
    siswa_ids = fields.Many2many('res.partner',relation='siswa_psb_ocb11_wizard_report_distribusi_siswa_rel_new', column1='wizard_id',column2='siswa_id', string="Siswa")
    
    @api.multi 
    def action_save(self):
        self.ensure_one()
        # update name
        self.write({
            'name' : 'Data Calon Siswa'
        })
        # add calon siswa
        # calon_siswas = self.env['siswa_psb_ocb11.calon_siswa'].search(['&','&',
        #                                             ('tahunajaran_id','=',self.tahunajaran_id.id),
        #                                             ('jenjang_id','=',self.jenjang_id.id),
        #                                             ('state','=','reg'),
        #                                             ])
        calon_siswas = self.env['siswa_ocb11.rombel_siswa'].search([
                                                    ('tahunajaran_id','=',self.tahunajaran_id.id),
                                                    ('rombel_id','=',self.rombel_id.id),
                                                    ])
        reg_cs = []
        for cs in calon_siswas:
            self.write({
                'siswa_ids' : [(4,cs.siswa_id.id)]
            })

        # show html report
        return self.env.ref('siswa_psb_ocb11.report_distribusi_siswa_action').report_action(self)

        # # show wizard form view
        # return {
        #     'view_type': 'form',
        #     'view_mode': 'form',
        #     'res_model': 'siswa_psb_ocb11.wizard_report_distribusi_siswa',
        #     'target': 'current',
        #     'res_id': self.id,
        #     'type': 'ir.actions.act_window'
        # }

    def action_print(self):
        return self.env.ref('siswa_psb_ocb11.report_distribusi_siswa_action').report_action(self)
  