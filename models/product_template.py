# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.model_create_multi
    def create(self, vals_list):
        res = super(ProductTemplate, self).create(vals_list)
        # Llamar a sync_product para los productos creados a partir de este template
        for template in res:
            for product in template.product_variant_ids:
                print(product.name)
                product.sync_product()
        return res

    def write(self, vals):
        res = super(ProductTemplate, self).write(vals)
        # Llamar a sync_product para los productos asociados a este template
        for template in self:
            for product in template.product_variant_ids:
                print(product.name)                
                product.sync_product()
        return res
