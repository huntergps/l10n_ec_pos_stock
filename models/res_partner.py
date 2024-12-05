# my_module/models/res_partner.py
from odoo import models, api, fields, _
from odoo.exceptions import ValidationError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model_create_multi
    def create(self, vals):
        if 'vat' in vals and vals['vat']:
            self._check_vat_uniqueness(vals['vat'])
        return super(ResPartner, self).create(vals)

    def write(self, vals):
        if 'vat' in vals and vals['vat']:
            self._check_vat_uniqueness(vals['vat'])
        return super(ResPartner, self).write(vals)

    def copy(self, default=None):
        self.ensure_one()  # Ensure that only one record is being copied
        if self.vat:
            self._check_vat_uniqueness(self.vat)
        return super(ResPartner, self).copy(default)
