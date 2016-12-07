#!/usr/bin/env python
# -*- coding: utf-8 -*-

from openerp import models, fields, api, _
from openerp.osv import osv
from opcua import Client
from opcua import ua
class StockTransferDetails(osv.osv):
	_inherit = 'stock.transfer_details'
	se_transfiere = fields.Boolean(string = '¿Se quiere despachar por OPC?', default=True)

	@api.one
	def do_detailed_transfer(self):
		mostrar = ''
		opc_es_liquido = False
		opc_itemBooleanoDeInicioDeProceso = ''
		opc_itemStringCantidadDeLiquido = ''
		cantidad_de_liquido = 0
		if self.se_transfiere == True:
			
			
			for lstits in [self.item_ids, self.packop_ids]:
				for prod in lstits:
					opc_es_liquido  					= 	prod.sourceloc_id.stock_opc_es_liquido 
					opc_itemBooleanoDeInicioDeProceso 	= 	prod.sourceloc_id.plc_ids[0].plc_itemBooleanoDeInicioDeProceso
					opc_itemStringCantidadDeLiquido 	= 	prod.sourceloc_id.plc_ids[0].plc_itemStringCantidadDeLiquido
					cantidad_de_liquido 				= 	prod.quantity
			#raise osv.except_osv('Esto es un Mesaje!',opc_itemBooleanoDeInicioDeProceso + " "+opc_itemStringCantidadDeLiquido+" "+str(cantidad_de_liquido))
			if opc_es_liquido != True or (opc_itemBooleanoDeInicioDeProceso == '' or opc_itemBooleanoDeInicioDeProceso == False ) or (opc_itemStringCantidadDeLiquido == '' or opc_itemStringCantidadDeLiquido == False) :
				raise osv.except_osv('Esto es un Mesaje!',"Hay un error en la cofiguracion de datos del OPC en la ubicacion "+prod.sourceloc_id.name)
			else:
				#ns=2;s=Demo.Static.Scalar.Boolean
				#ns=2;s=Demo.Static.Scalar.Double
				
				#raise osv.except_osv('Esto es un Meadssaje!',)+'  '+opc_itemBooleanoDeInicioDeProceso+'  '+opc_itemStringCantidadDeLiquido)
				client = Client(str(self.env['rbs.opc.config.settings'].get_opc_ip()))
				client.connect()

				
				#raise osv.except_osv('prueba boolean',)
				node_inicio = client.get_node(str(opc_itemBooleanoDeInicioDeProceso))
				node_liguido = client.get_node(str(opc_itemStringCantidadDeLiquido))
				if node_inicio.get_value()==False:
					node_inicio.set_value(True)
					node_liguido.set_value(ua.Variant(cantidad_de_liquido, ua.VariantType.Double))
					raise osv.except_osv('prueba boolean',"paso"+' '+str(cantidad_de_liquido))	
				else:
					raise osv.except_osv('prueba boolean',"no paso"+' '+str(cantidad_de_liquido))		
				client.disconnect()
				
				'''opc = OpenOPC.open_client('192.168.1.115')
					v = opc.servers()[3]
					opc.connect(v)


					#se le indica la cantidad de liquido que se va a tranferir
					opc.write((opc_itemStringCantidadDeLiquido, cantidad_de_liquido))
					#se le indica al OPC que inicia la Transferencia
					opc.write((opc_itemBooleanoDeInicioDeProceso, True))
					opc.close()
				'''

			super(StockTransferDetails, self).do_detailed_transfer()
		else:
			super(StockTransferDetails, self).do_detailed_transfer()