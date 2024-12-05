# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import models, api




class PosSession(models.Model):
    _inherit = 'pos.session'

    def _load_pos_data_models(self, config_id):
        res = super()._load_pos_data_models(config_id)
        res.append('stock.location')
        return res


class StockLocation(models.Model):
    _inherit ='stock.location'

    @api.model
    def _load_pos_data_domain(self, data):
        return [('id', '=', self.id)]

    @api.model
    def _load_pos_data_fields(self):
        return [
           'id','name'
        ]

    def _load_pos_data(self, data):
        domain = []
        fields = self._load_pos_data_fields()
        data = self.search_read(domain, fields, load=False)
        return {
            'data': data,
            'fields': fields
        }
