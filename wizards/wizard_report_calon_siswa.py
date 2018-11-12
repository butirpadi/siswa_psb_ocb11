from odoo import models, fields, api
from pprint import pprint

class wizard_report_calon_siswa(models.TransientModel):
    _name = 'siswa_psb_ocb11.wizard_report_calon_siswa'

    name = fields.Char('Name', default='0')
    tahunajaran_id = fields.Many2one('siswa_ocb11.tahunajaran', string="Tahun Ajaran", default=lambda self: self.env['siswa_ocb11.tahunajaran'].search([('active','=',True)]), required=True)
    jenjang_id = fields.Many2one('siswa_ocb11.jenjang', string='Jenjang')
    calon_siswa_ids = fields.Many2many('siswa_psb_ocb11.calon_siswa',relation='siswa_psb_ocb11_wizard_report_calon_siswa_rel', column1='wizard_id',column2='calon_siswa_id', string="Calon Siswa")
    
    @api.multi 
    def action_save(self):
        self.ensure_one()
        # update name
        self.write({
            'name' : 'Data Calon Siswa'
        })
        # add calon siswa
        calon_siswas = self.env['siswa_psb_ocb11.calon_siswa'].search(['&','&',
                                                    ('tahunajaran_id','=',self.tahunajaran_id.id),
                                                    ('jenjang_id','=',self.jenjang_id.id),
                                                    ('state','=','reg'),
                                                    ])
        reg_cs = []
        for cs in calon_siswas:
            self.write({
                'calon_siswa_ids' : [(4,cs.id)]
            })

        # show wizard form view
        # return {
        #     'view_type': 'form',
        #     'view_mode': 'form',
        #     'res_model': 'siswa_psb_ocb11.wizard_report_calon_siswa',
        #     'target': 'current',
        #     'res_id': self.id,
        #     'type': 'ir.actions.act_window'
        # }

        # show html report
        return self.env.ref('siswa_psb_ocb11.report_calon_siswa_action').report_action(self)
    
    def action_print(self):
        return self.env.ref('siswa_psb_ocb11.report_calon_siswa_action').report_action(self)

    