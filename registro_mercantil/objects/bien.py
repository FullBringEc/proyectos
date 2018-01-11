# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
from openerp.osv import osv

class rbs_bien(models.Model):
	_name = 'rbs.bien'
	_description = u"Bien"

	documento_propiedad_id = fields.Many2one('rbs.documento.propiedad',"Documento de propiedad")
	documento_mercantil_id = fields.Many2one('rbs.documento.mercantil',"Documento mercantil")
	numero_predial = fields.Char(string = 'Numero Predial')
	# name = fields.Char(string = 'Clave Catastral')
	clave_catastral = fields.Char(string = 'Clave Catastral' )
	descripcion_bien= fields.Char(string ='Descripcion del Bien')
	descripcion_lindero = fields.Text(string = 'Descripcion del lindero', default='NORTE:    SUR:    ESTE:   OESTE:')
	

	provincia_id = fields.Many2one('rbs.provincia', string ='Provincia')
	canton_id = fields.Many2one('rbs.canton', string ='Canton del Inmueble')
	parroquia_id = fields.Many2one('rbs.parroquia',string ='Parroquia Inmueble')
	zona_id = fields.Many2one('rbs.zona', string ='Zona')
	
	ubicacion_geografica = fields.Selection([
            ('NORTE','NORTE'),
            ('SUR','SUR'),
            ('ESTE','ESTE'),
            ('OESTE','OESTE'),
            ('SUROESTE','SUROESTE'),
            ('SURESTE','SURESTE'),
            ('NOROESTE','NOROESTE'),
            ('NORESTE','NORESTE'),
        ],string = 'Ubicacion Geografica', default='NORTE')
	superficie_area_numero = fields.Integer(string = 'Superficie o Area')
	superficie_area_letras = fields.Char(string = 'Superficie o Area')
	es_propiedad_horizontal = fields.Boolean(String = 'Propiedad Horizontal')
	parte_char_ids = fields.Many2many('rbs.parte.char',string='Partes')

	alicuota_ids = fields.One2many('rbs.alicuota','bien_id',"Alicuota")






	tipo_bien_id = fields.Many2one('rbs.tipo.bien', "Tipo de bien")
	chasis = fields.Char(string = 'Chasis/Serie' )
	motor = fields.Char(string = 'Motor' )
	marca = fields.Char(string = 'Marca' )
	modelo = fields.Char(string = 'Modelo' )
	anio_fabricacion = fields.Many2one('rbs.anio',string = 'Año de Fabricacion' )
	placa = fields.Char(string = 'Placa' )
	color = fields.Char(string = 'Color' )
	numero_provisional = fields.Char(string = 'Numero Provisional' )
	
	def name_get(self):
		res = []
		for record in self:
			numero_predial = record.numero_predial
			clave_catastral = record.clave_catastral
			# pais = record.pais_id.name
			tit = "%s/%s" % (numero_predial,clave_catastral)
			res.append((record.id, tit))
		return res

	@api.onchange('numero_predial','clave_catastral')
	def onchange_numero_predial(self):
		parte_char_ids_num = []
		for parte_char in self.documento_propiedad_id.parte_char_ids:
			parte_char_ids_num.append(parte_char.id)
		self.parte_char_ids = [(6,0,parte_char_ids_num)]
		# raise osv.except_osv('Esto es un Mesaje!',)
	# cuantia_valor = fields.Char(string ='Valor del bien' )
	# cuantia_unidad = fields.Selection([
 #            ('SUCRE','SUCRE'),
 #            ('DOLAR','DOLAR'),
 #        ],string ='Unidad Monetaria' )


class rbs_tipo_bien(models.Model):
	_name = 'rbs.tipo.bien'
	_description = u"Tipo de bien"
	name = fields.Char("Descripción")

