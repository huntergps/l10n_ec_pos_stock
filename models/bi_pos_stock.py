# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _
import json
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_is_zero


class pos_config(models.Model):
    _inherit = 'pos.config'

    pos_display_stock = fields.Boolean(string='Mostrar Stock en POS')
    pos_stock_type = fields.Selection(
        [('onhand', 'Cant. Disponible'),('available', 'Cant. Pronosticada')], default='onhand', string='Tipo de Stock', help='El vendedor puede mostrar diferentes tipos de stock en el punto de venta.')
    pos_allow_order = fields.Boolean(string='Permitir vender en POS cuando el producto está agotado')
    pos_deny_order = fields.Char(string='Denegar pedido POS cuando la cantidad del producto baje a')
    stock_position = fields.Selection([
        ('top_right', 'Arriba Derecha'),
        ('top_left', 'Arriba Izquierda'),
        ('bottom_right', 'Abajo Derecha'),
        ('bottom_left', 'Abajo Izquierda'),
        ],
        default='bottom_left', string='Posicion de Stock')

    show_stock_location = fields.Selection([
        ('all', 'Todo el almacén'),
        ('specific', 'Almacén de sesion actual'),
    ], string='Mostrar Stock de', default='all')

    stock_location_id = fields.Many2one(
        'stock.location', string='Ubicación de stock',
        domain=[('usage', '=', 'internal')])

    color_background = fields.Char(
        string='Color',)
    font_background = fields.Char(
        string='Color Fuente',)
    low_stock = fields.Float(
        string='Cantidad de Stock bajo',default=0.00)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    pos_pos_display_stock = fields.Boolean(
        related="pos_config_id.pos_display_stock", readonly=False)
    pos_pos_stock_type = fields.Selection(related="pos_config_id.pos_stock_type", readonly=False,
                                          string='Stock Type', help='Seller can display Different stock type in POS.')
    pos_pos_allow_order = fields.Boolean(
        string='Permitir vender cuando el producto está agotado', readonly=False, related="pos_config_id.pos_allow_order")
    pos_pos_deny_order = fields.Char(string='Deny POS Order When Product Qty is goes down to',
                                     readonly=False, related="pos_config_id.pos_deny_order")

    pos_show_stock_location = fields.Selection(
        string='Mostrar Stock de', readonly=False, related="pos_config_id.show_stock_location")

    pos_stock_location_id = fields.Many2one(
        'stock.location',
        string='Ubicacin de Stock',
        domain=[('usage', '=', 'internal')],
        related="pos_config_id.stock_location_id",
        readonly=False
    )
    pos_stock_position = fields.Selection(
        related="pos_config_id.stock_position", readonly=False, string='Posicion de Stock')
    pos_color_background = fields.Char(
        string='Background Color', readonly=False, related="pos_config_id.color_background")
    pos_font_background = fields.Char(
        string='Font Color', readonly=False, related="pos_config_id.font_background")
    pos_low_stock = fields.Float(
        string='Product Low Stock', readonly=False, related="pos_config_id.low_stock")


class PosOrder(models.Model):
    _inherit = 'pos.order'

    location_id = fields.Many2one(
        comodel_name='stock.location',
        related='config_id.stock_location_id',
        string="Ubicacion",
        store=True,
        readonly=True,
    )
