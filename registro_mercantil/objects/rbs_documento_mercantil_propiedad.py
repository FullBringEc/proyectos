# -*- coding: utf-8 -*-
#!/usr/bin/env python
from dateutil import parser
from openerp import models, fields, api, _
from openerp.osv import osv



class rbs_documento_mercantil_propiedad(models.Model):
	_name ="rbs.documento.mercantil.propiedad"
	_description = "Documento de la Propiedad"
	#name= field.Char('Nombre')
	
	anio_id = fields.Many2one('rbs.archivo.anio', string ='Año',required = True)
	libro_id = fields.Many2one('rbs.archivo.libro', string ='Libro' ,required = True)
	tomo_id = fields.Many2one("rbs.archivo.tomo", string ='Tomo', required = True)

	persona_id = fields.Many2one('rbs.persona', string ='Compareciente(n)')
	
	persona_nombres = fields.Char(string = 'Nombres del Compareciente')
	persona_apellidos = fields.Char(string = 'Apellidos del Compareciente')
	persona_cedula = fields.Char(string = 'Cedula del Compareciente')
	tipo_compareciente_id = fields.Many2one('rbs.tipo.compareciente.a', string ='Tipo de Compareciente')
	persona_razonSocial = fields.Char(string = 'Razon Social del Compareciente')

	tipo_contrato_id = fields.Many2one('rbs.tipo.contrato', string ='Tipo de Contrato', required = True)
	numero_inscripcion = fields.Char(string = 'Numero de Inscripcion' , required = True)
	fecha_inscripcion = fields.Datetime(string = 'Fecha de Inscripcion' )
	clave_catastral = fields.Char(string = 'Clave Catastral' )
	tipo_bien_id = fields.Many2one('rbs.tipo.bien', string ='Tipo de Bien', required = True)
	
	
	provincia_nombre_id = fields.Many2one('rbs.provincia', string ='Provincia', required = True)
	zona_nombre_id = fields.Many2one('rbs.zona', string ='Zona', required = True)
	superficie_bien = fields.Char(string = 'Superficie del bien')
	orientacio_lindero = fields.Char(string = 'Orientacion del lindero', default='NORTE/SUR/ESTE/OESTE', required = True)
	descripcion_lindero = fields.Text(string = 'Descripcion del lindero', default='NORTE:    SUR:    ESTE:   OESTE:', required = True)
	parroquia_nombre = fields.Selection([
            ('SAN VICENTE','SAN VICENTE'),
            ('CANOA','CANOA'),
        ],string ='Nombre de la Parroquia')
	notaria_juzgado_entidad = fields.Char(string ='Nombre Notaria o juzgado')
	
	canton_nombre_id = fields.Many2one('rbs.canton', string ='Canton del Bien', required = True)

	cuantia_valor = fields.Char(string ='Valor del bien' )

	cuantia_unidad = fields.Selection([
            ('SUCRE','SUCRE'),
            ('DOLAR','DOLAR'),
        ],string ='Unidad de la cuantia' )
	identificacion_unica = fields.Char(string = 'Identificador Unico Sistema Remoto',compute='_compute_upper',store = True) 
	juicio_numero = fields.Integer(string ='Numero del juicio')
	estado_inscripcion_id = fields.Many2one('rbs.estado.inscripcion', string ='Estado de la Inscripcion', required = True)
	ubicacion_dato_id = fields.Many2one('rbs.ubicacion.dato', string ='Ubicacion del Dato', required = True)

	modificacion_fuente = fields.Datetime(string = 'Fecha de la modificacion de la fuente' )
	canton_notaria_id = fields.Many2one('rbs.canton', string ='Canton de la Notaria', required = True)


	escritura_fecha = fields.Datetime(string = 'Fecha de la Escritura')
	#filedata = fields.Binary('Archivo',filters='*.pdf')
	#filename = fields.Char('Nombre de archivo', default="Archivo.pdf")
	filedata_id = fields.Many2one('rbs.archivo.pdf')
	filedata = fields.Binary(related='filedata_id.filedata',filters='*.pdf')
	esPesado = fields.Boolean(related='filedata_id.esPesado',string = '¿Es Pesado?')
	rutaFTP = fields.Char(related='filedata_id.rutaFTP', string = 'Escriba la ruta del Archivo')

	def _getUltimoAnio(self, cr, uid, context=None):
		acta_id = self.pool.get("rbs.documento.mercantil.propiedad").search(cr, uid,  [], limit=1, order='id desc')
		anio = self.pool.get("rbs.documento.mercantil.propiedad").browse(cr,uid,acta_id,context = None).anio_id.id
		return anio
	def _getUltimoLibro(self, cr, uid, context=None):
		acta_id = self.pool.get("rbs.documento.mercantil.propiedad").search(cr, uid,  [], limit=1, order='id desc')
		libro = self.pool.get("rbs.documento.mercantil.propiedad").browse(cr,uid,acta_id,context = None).libro_id.id
		return libro
	def _getUltimoTomo(self, cr, uid, context=None):
		acta_id = self.pool.get("rbs.documento.mercantil.propiedad").search(cr, uid,  [], limit=1, order='id desc')
		tomo = self.pool.get("rbs.documento.mercantil.propiedad").browse(cr,uid,acta_id,context = None).tomo_id.id
		return tomo

	def _create_pdf(self, cr, uid, context=None):
		return self.pool.get("rbs.archivo.pdf").create(cr, uid,{},context=None)

	_defaults = {
		'anio_id': _getUltimoAnio,
		'libro_id': _getUltimoLibro,
		'tomo_id' : _getUltimoTomo,
		'filedata_id' : _create_pdf,
	}
	_rec_name='numero_inscripcion'

	def open_ui(self, cr, uid, ids, context=None):
		data = self.browse(cr, uid, ids[0], context=context)
		context = dict(context or {})
		#context['active_id'] = data.ids[0]
		return {
			'type' : 'ir.actions.act_url',
			'url':   '/web_tiff_widget/web/?binary='+str(ids[0])+'&tipo=propiedad',
			'target': 'current',
		}

	@api.depends('ubicacion_dato_id','persona_cedula','numero_inscripcion')
	def _compute_upper(self):
		for rec in self:
			try:
				rec.identificacion_unica = '02'+rec.ubicacion_dato_id.name+rec.persona_cedula+rec.numero_inscripcion
			except:
				pass
	def codigoascii(self, text):
		return unicode(text).encode('utf-8')

	def onchange_persona_id(self, cr, uid, ids, persona_id,context=None):
		persona_id = self.pool.get('rbs.persona').search(cr, uid, [('id','=',persona_id),])
		persona = self.pool.get('rbs.persona').browse(cr,uid,persona_id,context = None)
		result = {}
		
		#try:
			
		       			
		if persona:
			#raise osv.except_osv('Esto es un Mesaje!',establecimiento)
			#try:
			if persona.persona_nombres:
				result['persona_nombres'] = self.codigoascii(persona.persona_nombres)
				
			#except:
			#	pass
			
			try:
				if persona.persona_apellidos:
					result['persona_apellidos'] = self.codigoascii(persona.persona_apellidos)

			except: 
				pass
			try:
				if persona.name:
					result['persona_cedula'] = str(persona.name) 
			except: 
				pass
			
			try:
				if persona.persona_razonSocial:
					result['persona_razonSocial'] = self.codigoascii(persona.persona_razonSocial) 
			except: 
				pass
		#except:
		#	pass
		
		return { 'value':result, }
	def on_change_anio_id(self, cr, uid, ids,anio_id,context=None):
		result = {}		
		if(self._getUltimoAnio(cr, uid, context=None) != anio_id):
			result['libro_id'] = 0;
		return { 'value':result, }
	def on_change_libro_id(self, cr, uid, ids,libro_id,context=None):
		result = {}		
		if(self._getUltimoLibro(cr, uid, context=None) != libro_id):
			result['tomo_id'] = 0;
		return { 'value':result, }


	def onchange_inscripcion(self, cr, uid, ids, inscripcion_num,libro_id,context=None):
		propiedad_id = self.pool.get('rbs.documento.mercantil.propiedad').search(cr, uid, [('numero_inscripcion','=',inscripcion_num),('libro_id','=',libro_id)])
		propiedad = self.pool.get('rbs.documento.mercantil.propiedad').browse(cr,uid,propiedad_id,context = None)
		result = {}

		
		try:
			
		       			
			if propiedad:
				propiedad = propiedad[0]
				#raise osv.except_osv('Esto es un Mesaje!',establecimiento)
				try:
					if propiedad.notaria_juzgado_entidad:
						result['notaria_juzgado_entidad'] = self.codigoascii(propiedad.notaria_juzgado_entidad)
					
				except:
					pass
				
				try:
					if propiedad.fecha_inscripcion:
						result['fecha_inscripcion'] = str(propiedad.fecha_inscripcion)
					
				except:
					pass

				try:
					if propiedad.tomo_id:
						result['tomo_id'] = propiedad.tomo_id.id

				except: 
					pass

				try:
					if propiedad.anio_id:
						result['anio_id'] = propiedad.anio_id.id
				except:
					pass
				
				try:
					if propiedad.libro_id:
						result['libro_id'] = propiedad.libro_id.id
				except:
					pass
					
				try:
					if propiedad.tipo_contrato_id:
						result['tipo_contrato_id'] = propiedad.tipo_contrato_id.id

				except: 
					pass

				try:
					if propiedad.clave_catastral:
						result['clave_catastral'] = self.codigoascii(propiedad.clave_catastral)
					
				except:
					pass

				try:
					if propiedad.tipo_bien_id:
						result['tipo_bien_id'] = propiedad.tipo_bien_id.id

				except: 
					pass
				try:
					if propiedad.provincia_nombre_id:
						result['provincia_nombre_id'] = propiedad.provincia_nombre_id.id

				except: 
					pass
				try:
					if propiedad.zona_nombre_id:
						result['zona_nombre_id'] = propiedad.zona_nombre_id.id

				except: 
					pass

				try:
					if propiedad.superficie_bien:
						result['superficie_bien'] = self.codigoascii(propiedad.superficie_bien)
					
				except:
					pass

				try:
					if propiedad.orientacio_lindero:
						result['orientacio_lindero'] = self.codigoascii(propiedad.orientacio_lindero)
					
				except:
					pass

				try:
					if propiedad.descripcion_lindero:
						result['descripcion_lindero'] = self.codigoascii(propiedad.descripcion_lindero)
					
				except:
					pass

				try:
					if propiedad.parroquia_nombre:
						result['parroquia_nombre'] = self.codigoascii(propiedad.parroquia_nombre)
					
				except:
					pass

				try:
					if propiedad.canton_nombre_id:
						result['canton_nombre_id'] = propiedad.canton_nombre_id.id

				except: 
					pass
				try:
					if propiedad.cuantia_valor:
						result['cuantia_valor'] = self.codigoascii(propiedad.cuantia_valor)
					
				except:
					pass

				try:
					if propiedad.cuantia_unidad:
						result['cuantia_unidad'] = self.codigoascii(propiedad.cuantia_unidad)
					
				except:
					pass

				try:
					if propiedad.juicio_numero:
						result['juicio_numero'] = self.codigoascii(propiedad.juicio_numero)
					
				except:
					pass
				try:
					if propiedad.estado_inscripcion_id:
						result['estado_inscripcion_id'] = propiedad.estado_inscripcion_id.id

				except: 
					pass

				try:
					if propiedad.ubicacion_dato_id:
						result['ubicacion_dato_id'] = propiedad.ubicacion_dato_id.id

				except: 
					pass

				try:
					if propiedad.modificacion_fuente:
						result['modificacion_fuente'] = self.codigoascii(propiedad.modificacion_fuente)
					
				except:
					pass
				try:
					if propiedad.canton_notaria_id:
						result['canton_notaria_id'] = propiedad.canton_notaria_id.id

				except: 
					pass
				try:
					if propiedad.escritura_fecha:
						result['escritura_fecha'] = str(propiedad.escritura_fecha)
					
				except:
					pass

				try:
					if propiedad.filedata_id:
						result['filedata_id'] = propiedad.filedata_id.id

				except: 
					pass
			if not propiedad:
				result['filedata_id'] = self._create_pdf(cr, uid, context=None)

				
				
		except:
			pass
		
		return { 'value':result, }



class rbs_provincia(models.Model):
	_name = 'rbs.provincia'
	_description = "Nombre de la provincia"
		
	name = fields.Char(string = 'Nombre de la provincia')


class rbs_zona(models.Model):
	_name = 'rbs.zona'
	_description = "Nombre de la zona"
	
	name = fields.Char(string = 'Nombre de la zona')
