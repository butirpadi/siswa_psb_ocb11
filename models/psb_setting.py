from ast import literal_eval

from flectra import api, fields, models
from pprint import pprint 


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # use_biaya_registrasi_manager = fields.Boolean('Enable Biaya Registrasi', default=False)
#     module_siswa_psb_biaya_registrasi_manager_ocb11 = fields.Boolean()
    module_siswa_psb_manager_ocb11 = fields.Boolean()
    
    @api.multi
    def write(self, vals):
        print('enable new module')
        pprint(vals)
        result = super(ResConfigSettings, self).write(vals)       
        
        return result

     