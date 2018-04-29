# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from pprint import pprint
from datetime import datetime, date


class calon_siswa(models.Model):
    _inherit = 'res.partner'

    is_calon = fields.Boolean(default=False)