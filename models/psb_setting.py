from ast import literal_eval

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # use_biaya_registrasi_manager = fields.Boolean('Enable Biaya Registrasi', default=False)
    module_siswa_psb_biaya_registrasi_manager_ocb11 = fields.Boolean()

    