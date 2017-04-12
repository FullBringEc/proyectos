# -*- coding: utf-8 -*-
#!/usr/bin/env python
from dateutil import parser
from openerp import models, fields, api, _
from openerp.osv import osv



class rbs_documento_mercantil_propiedad(models.Model):
	_name ="rbs.documento.mercantil.propiedad"
	_description = "Documento de la Propiedad"
	#name= field.Char('Nombre')

	# categoria Datos libro
	anio_id = fields.Many2one('rbs.archivo.anio', string ='Año',required = True)
	libro_id = fields.Many2one('rbs.archivo.libro', string ='Nombre Acto/Contrato' ,required = True)
	reg_acto_contrato = fields.Char (string='Registra Acto/Contrato', required = True)
	tipo_contrato_id = fields.Many2one('rbs.tipo.contrato', string ='Tipo de Acto/Contrato', required = True)
	tipo_libro = fields.Char (string='Tipo Libro', required = True)
	tomo_id = fields.Many2one("rbs.archivo.tomo", string ='Tomo', required = True)
	foleo_desde = fields.Char(string='Desde', required = True)
	foleo_hasta = fields.Char (string='Hasta', required = True)
	repertorio = fields.Char (string='Repertorio', required = True)
	fecha_repertorio = fields.Datetime (string='Fecha Repertorio')
	numero_inscripcion = fields.Char(string = 'Numero de Inscripcion' , required = True)
	fecha_inscripcion = fields.Datetime(string = 'Fecha de Inscripcion' )
	identificacion_unica = fields.Char(string = 'Identificador Unico Sistema Remoto',compute='_compute_upper',store = True)
	#Fin categoria

	# categoria datos Persona/entidad
	tipo_persona_id = fields.Many2one('rbs.persona', string ='Tipo de Persona')
	persona_razonSocial = fields.Char(string = 'Razon Social')
	persona_id = fields.Many2one('rbs.persona', string ='Compareciente(n)')
	persona_nombres = fields.Char(string = 'Nombres del Compareciente')
	persona_apellidos = fields.Char(string = 'Apellidos del Compareciente')
	persona_tipo_interviniente_id = fields.Many2one('rbs.tipo.interviniente.a', string ='Tipo de Interviniente')
	persona_calidad_compareciente = fields.Char(string = 'Calidad Compareciente')
	persona_tipo_documento = fields.Char(string = 'Tipo Documento')
	persona_cedula = fields.Char(string = 'Cedula del Compareciente')
	persona_estado_civil = fields.Char(string = 'Estado Civil')
	persona_nombres_conyuge = fields.Char(string = 'Nombres de Conyuge')
	persona_apellidos_conyuge = fields.Char(string = 'Apellidos de Conyuge')
	persona_cedula_conyuge = fields.Char(string = 'Cedula del Conyuge')
	persona_separacion_bienes = fields.Char(string = 'Separacion de Bienes')
	#Fin categoria

	#Categoria Datos del Bien
	clave_catastral_id = fields.Many2one('rbs.clavecatastral')

	numero_predial = fields.Char(string = 'Numero Predial')
	clave_catastral = fields.Char(string = 'Clave Catastral' )
	descripcion_bien_id= fields.Many2one('rbs.tipo.bien', string ='Descripcion Bien', required = True)
	provincia_nombre_id = fields.Many2one('rbs.provincia', string ='Provincia', required = True)
	zona_nombre_id = fields.Many2one('rbs.zona', string ='Zona', required = True)
	superficie_bien = fields.Char(string = 'Superficie o Area')
	ubicacion_geografica = fields.Char(string = 'Ubicacion Geografica', default='NORTE/SUR/ESTE/OESTE', required = True)
	descripcion_lindero = fields.Text(string = 'Descripcion del lindero', default='NORTE:    SUR:    ESTE:   OESTE:', required = True)
	parroquia_nombre_inmueble = fields.Selection([
            ('SAN VICENTE','SAN VICENTE'),
            ('CANOA','CANOA'),
        ],string ='Parroquia Inmueble')
	canton_nombre_inmueble_id = fields.Many2one('rbs.canton', string ='Canton del Inmueble', required = True)
	cuantia_valor = fields.Char(string ='Valor del bien' )
	cuantia_unidad = fields.Selection([
            ('SUCRE','SUCRE'),
            ('DOLAR','DOLAR'),
        ],string ='Unidad Monetaria' )
	
	#Fin Categoria

	#Categoria Datos Registrales
	gravamen_limitacion = fields.Char (string='Gravamen / Limitación')
	tipo_gravamen = fields.Char (string='Tipo Gravamen/Limitación')
	genera_gravamen_limitacion = fields.Char (string='Genera Gravamen/Limitación')	
	fecha_const_gravamen = fields.Datetime (string='Fecha Const Gravamen/Limitacion')
	fecha_cancel_gravamen = fields.Datetime (string='Fecha Const Gravamen/Limitación')
	marginacion_tramite_origi = fields.Char (string='Marginacion Trámite')
	modificacion_fuente = fields.Datetime(string = 'Fecha modificacion de la fuente' )
	canton_registro_id = fields.Many2one('rbs.canton', string ='Canton Registro Propiedad', required = True)
	notaria_juzgado_entidad = fields.Char(string ='Nombre Notaria o juzgado')
	canton_notaria_id = fields.Many2one('rbs.notaria', string ='Canton de la Notaria', required = True)
	# Fin categoría

	# Datos Escritura
	escritura_fecha = fields.Datetime(string = 'Fecha Escritura')
	propiedad_horizontal = fields.Char (string='Propiedad Horizontal')
	porcentaje_alicuota = fields.Char (string='Porcentaje Alícuota')
	expensas = fields.Char (string='Expensas')
	acto_menor_edad = fields.Char (string='Comparece Acto Menores de Edad')
	tutor = fields.Char (string='Nombre Tutor')
	fecha_adjudicion = fields.Datetime(string = 'Fecha de la Escritura')
	fecha_insi_bienes = fields.Datetime(string = 'Fecha insinuación judicial/acta notarial')
	# Fin categoria

	#Categoria posicion efectiva
	causante = fields.Char (string='Causante')
	fecha_defuncion = fields.Datetime (string='Fecha Defunción')
	herederos = fields.Char (string='Herederos')
	conyuge_sobreviviente = fields.Char (string='Conyuge Sobreviviente')
	#Fin categoria
	
	
	
	
	
	
	
	

	

	
	
	juicio_numero = fields.Integer(string ='Numero del juicio')
	estado_inscripcion_id = fields.Many2one('rbs.estado.inscripcion', string ='Estado de la Inscripcion', required = True)
	ubicacion_dato_id = fields.Many2one('rbs.ubicacion.dato', string ='Ubicacion del Dato', required = True)

	
	


	
	#filedata = fields.Binary('Archivo',filters='*.pdf')
	#filename = fields.Char('Nombre de archivo', default="Archivo.pdf")
	filedata_id = fields.Many2one('rbs.archivo.pdf')
	filedata = fields.Binary(related='filedata_id.filedata',filters='*.pdf')
	esPesado = fields.Boolean(related='filedata_id.esPesado',string = '¿Es Pesado?')
	rutaFTP = fields.Char(related='filedata_id.rutaFTP', string = 'Escriba la ruta del Archivo')

	factura_ids = fields.One2many('account.invoice', 'propiedad_id', string= 'Factura')

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
			'url':   '/registro_mercantil/web/?binary='+str(ids[0])+'&tipo=propiedad',
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
					if propiedad.descripcion_bien_id:
						result['descripcion_bien_id'] = propiedad.descripcion_bien_id.id

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
					if propiedad.ubicacion_geografica:
						result['ubicacion_geografica'] = self.codigoascii(propiedad.ubicacion_geografica)
					
				except:
					pass

				try:
					if propiedad.descripcion_lindero:
						result['descripcion_lindero'] = self.codigoascii(propiedad.descripcion_lindero)
					
				except:
					pass

				try:
					if propiedad.parroquia_nombre_inmueble:
						result['parroquia_nombre_inmueble'] = self.codigoascii(propiedad.ubicacion_geografica)
					
				except:
					pass

				try:
					if propiedad.canton_nombre_inmueble_id:
						result['canton_nombre_inmueble_id'] = propiedad.parroquia_nombre_inmueble.id

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


class rbs_clavecatastral(models.Model):
	_name = 'rbs.clavecatastral'
	_description = "Tipo Bien"


	name = fields.Char(string = 'Clave Catastral')
	numero_predial = fields.Char(string = 'Numero Predial')
	clave_catastral = fields.Char(string = 'Clave Catastral' )
	descripcion_bien_id= fields.Many2one('rbs.tipo.bien', string ='Descripcion Bien', required = True)
	provincia_nombre_id = fields.Many2one('rbs.provincia', string ='Provincia', required = True)
	zona_nombre_id = fields.Many2one('rbs.zona', string ='Zona', required = True)
	superficie_bien = fields.Char(string = 'Superficie o Area')
	ubicacion_geografica = fields.Char(string = 'Ubicacion Geografica', default='NORTE/SUR/ESTE/OESTE', required = True)
	descripcion_lindero = fields.Text(string = 'Descripcion del lindero', default='NORTE:    SUR:    ESTE:   OESTE:', required = True)
	parroquia_nombre_inmueble = fields.Selection([
            ('SAN VICENTE','SAN VICENTE'),
            ('CANOA','CANOA'),
        ],string ='Parroquia Inmueble')
	canton_nombre_inmueble_id = fields.Many2one('rbs.canton', string ='Canton del Inmueble', required = True)
	cuantia_valor = fields.Char(string ='Valor del bien' )
	cuantia_unidad = fields.Selection([
            ('SUCRE','SUCRE'),
            ('DOLAR','DOLAR'),
        ],string ='Unidad Monetaria' )



class rbs_notaria(models.Model):
	_name = 'rbs.notaria'
	_description = "Nombre de la Notaria"
		
	notaria_juzgado_entidad = fields.Char(string ='Nombre Notaria o juzgado')
	canton_notaria = fields.Char(string = 'Canton Notaria' )
	


class rbs_provincia(models.Model):
	_name = 'rbs.provincia'
	_description = "Nombre de la provincia"
		
	name = fields.Char(string = 'Nombre de la provincia')



class rbs_zona(models.Model):
	_name = 'rbs.zona'
	_description = "Nombre de la zona"
	
	name = fields.Char(string = 'Nombre de la zona')

class factura_invoice(models.Model):
	_inherit = 'account.invoice'
	propiedad_id = fields.Many2one('rbs.documento.mercantil.propiedad', string='Propiedad')
