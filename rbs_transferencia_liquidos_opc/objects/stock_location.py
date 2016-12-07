#!/usr/bin/env python
# -*- coding: utf-8 -*-

from openerp import models, fields, api, _
from openerp.osv import osv

class rbs_relacion(osv.osv):
	_name = "rbs.relacion"
	_description = "rbs relacion"
	opc_conf_id = fields.Many2one('rbs.opc.config.settings', string='Invoice Reference',
        ondelete='restrict', index=True)
	rbs_plc_id = fields.Many2one('rbs.plc', string='PLC',
        ondelete='restrict', index=True)

	stock_location_id = fields.Many2one('stock.location', string='Ubicacion',
        ondelete='restrict', index=True)


class rbs_plc(osv.osv):
	_name ="rbs.plc"
	_description = "Plc Modelo"
	
	name = fields.Char(string ='name')	
	plc_itemBooleanoDeInicioDeProceso = fields.Char(string = 'Item en el PLC para inicio de la transferencia')
	plc_itemStringCantidadDeLiquido = fields.Char(string = 'Item en el PLC para la cantidad a transferir')


	ubicacion_ids = fields.Many2many(
        comodel_name='stock.location',
        inverse_name='plc_ids',
        string='Ubicaciones',
        relation='rbs_relacion',
    )

	_defaults = {    
    }
class stock_location(osv.osv):
	_inherit = "stock.location"
	stock_opc_es_liquido = fields.Boolean(string = '¿Es Liquido despachado por OPC?')
	plc_ids = fields.Many2many(
        comodel_name='rbs.plc',
        inverse_name='ubicacion_ids',
        string='plcs',
        relation='rbs_relacion',
    )

	stock_opc_itemBooleanoDeInicioDeProceso = fields.Char(string = 'Item en el OPC para inicio de la transferencia')
	stock_opc_itemStringCantidadDeLiquido = fields.Char(string = 'Item en el OPC para la cantidad a transferir')

