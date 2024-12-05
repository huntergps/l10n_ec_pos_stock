# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _
import json
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_is_zero


class stock_quant(models.Model):
    _inherit = 'stock.move'

    @api.model_create_multi
    def create(self, vals_list):
        res = super(stock_quant, self).create(vals_list)
        notifications = []
        for rec in res:
            rec.product_id.sync_product()
        return res

    def write(self, vals):
        res = super(stock_quant, self).write(vals)
        notifications = []
        for rec in self:
            rec.product_id.sync_product()
        return res


class ProductProduct(models.Model):
    _inherit = 'product.product'

    quant_text = fields.Text('Cantidad', compute='_compute_avail_locations')



    @api.model
    def _load_pos_data_fields(self, config_id):
        fields_list = super()._load_pos_data_fields(config_id)
        fields_list += ['virtual_available','type','is_storable','qty_available', 'incoming_qty', 'outgoing_qty', 'quant_text', 'name']
        return fields_list

    @api.model_create_multi
    def create(self, vals_list):
        res = super(ProductProduct, self).create(values)
        notifications = []
        for rec in self:
            rec.sync_product()
        return res

    def write(self, values):
        res = super(ProductProduct, self).write(values)
        notifications = []
        for rec in self:
            rec.sync_product()
            return res

    @api.model
    def sync_product(self):
        notifications = []
        pos_configs = self.env['pos.config'].sudo().search([('pos_display_stock', '=', True)])
        for config in pos_configs:
            if config:
                prod_fields = self._load_pos_data_fields(config.id)
                config._notify('PRODUCT_MODIFIED', {
                'product.product': self.read(prod_fields, load=False)
                })
        return True

    def get_low_stock_products(self,low_stock):
        products=self.search([('is_storable', '=' , True),('available_in_pos', '=', True)]);
        product_list=[]
        for product in products:
            if product.qty_available <= low_stock:
                product_list.append(product.id)
        return product_list


    @api.depends('stock_quant_ids', 'stock_quant_ids.product_id', 'stock_quant_ids.location_id',
    'stock_quant_ids.quantity')
    def _compute_avail_locations(self):
        notifications = []
        for rec in self:
            final_data = {}
            rec.quant_text = json.dumps(final_data)
            if rec.is_storable:
                quants = self.env['stock.quant'].sudo().search(
                [('product_id', 'in', rec.ids), ('location_id.usage', '=', 'internal')])
                for quant in quants:
                    loc = quant.location_id.id
                    if loc in final_data:
                        last_qty = final_data[loc][0]
                        final_data[loc][0] = last_qty + quant.quantity
                    else:
                        final_data[loc] = [quant.quantity, 0, 0,quant.available_quantity]
                        rec.quant_text = json.dumps(final_data)
        return True
