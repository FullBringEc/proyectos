# -*- coding: utf-8 -*-
from dateutil import parser
from openerp import models, fields, api, _
from openerp.osv import osv
from _csv import field_size_limit
from cgi import FieldStorage




class rbs_documento_mercantil_vehiculo(models.Model):
	_name ="rbs.documento.mercantil.vehiculo"
	_description = "Documento Mercantil Vehiculo"
	#name= field.Char('Nombre')

	# Ctegoria Libro
	anio_id = fields.Many2one('rbs.archivo.anio', string ='Año',required = True)
	libro_id = fields.Many2one('rbs.archivo.libro', string ='Nombre Acto/Contrato' ,required = True)
	reg_acto_contrato = fields.Selection([
            ('ACTO','ACTO'),
            ('CONTRATO','CONTRATO'),
        ],string ='Registra Acto/Contrato')
	tipo_contrato_id = fields.Many2one('rbs.tipo.contrato', string ='Tipo de Acto/Contrato', required = True)
	tipo_libro = fields.Char (string='Tipo Libro', required = True)
	tomo_id = fields.Many2one("rbs.archivo.tomo", string ='Tomo', required = True)
	foleo_desde = fields.Char(string='Desde', required = True)
	foleo_hasta = fields.Char (string='Hasta', required = True)
	repertorio = fields.Char (string='Repertorio', required = True)
	fecha_repertorio = fields.Datetime (string='Fecha Repertorio')
	numero_inscripcion = fields.Char(string = 'Numero de Inscripcion' , required = True)
	fecha_inscripcion = fields.Datetime(string = 'Fecha de Inscripcion' )
	fecha_cancelacion = fields.Datetime(string = 'Fecha de Cancelacion' )
	identificacion_unica = fields.Char(string = 'Identificador',compute='_compute_upper',store = True)
	ubicacion_dato_id = fields.Many2one('rbs.ubicacion.dato', string ='Ubicacion del Dato', required = True)
	#Fin categoria

	# Datos Persona
	tipo_persona_id = fields.Selection([
            ('NATURAL','NATURAL'),
            ('JURIDICA','JURIDICA'),
        ],string ='Tipo de Persona')
	persona_id = fields.Many2one('rbs.persona', string ='Compareciente(n)')
	persona_nombres = fields.Char(string = 'Nombres del Compareciente')
	persona_apellidos = fields.Char(string = 'Apellidos del Compareciente')
	persona_estado_civil = fields.Char(string = 'Estado Civil')
	persona_cedula = fields.Char(string = 'Cedula del Compareciente')
	persona_estado_civil = fields.Char(string = 'Estado Civil')
	persona_nombres_conyuge = fields.Char(string = 'Nombres de Conyuge')
	persona_apellidos_conyuge = fields.Char(string = 'Apellidos de Conyuge')
	persona_cedula_conyuge = fields.Char(string = 'Cedula del Conyuge')
	persona_tipo_interviniente_id = fields.Many2one('rbs.tipo.interviniente.a', string ='Tipo de Interviniente')
	persona_calidad_compareciente = fields.Char(string = 'Calidad Compareciente')
	persona_razonSocial = fields.Char(string = 'Razon Social')
	acreedor_id = fields.Many2one('rbs.persona', string = 'Acreedor')
	# Fin categoria

	# Datos Bien
	tipo_bien_id = fields.Many2one('rbs.tipo.bien', string ='Tipo de Bien', required = True)
	chasis = fields.Char(string = 'Chasis' )
	motor = fields.Char(string = 'Motor' )
	marca = fields.Char(string = 'Marca' )
	modelo = fields.Char(string = 'Modelo' )
	anio_fabricacion = fields.Char(string = 'Año de Fabricacion' )
	placa = fields.Char(string = 'Placa' )
	numero_provisional = fields.Char(string = 'Numero Provisional' )
	# Fin categoria

	# Datos Registrales
	canton_registro_id = fields.Many2one('rbs.canton', string ='Canton Registro Mercantil', required = True)
	ultima_modificacion = fields.Char(string = 'Ultima Modificacion' )
	notaria_juzgado_entidad = fields.Char(string ='Nombre Notaria o juzgado')
	canton_notaria_id = fields.Many2one('rbs.canton', string ='Canton de la Notaria', required = True)
	fecha_escritura_contrato = fields.Datetime(string = 'Fecha de Escritura', required = True )
	marginacion_tramite_origi = fields.Char (string='Marginacion Trámite')
	# Fin categoria

	# Datos Representante
	cargo = fields.Char (string='Cargo')
	representante_id = fields.Many2one('rbs.persona', string ='Representante')
	apellido_representante = fields.Char(string = 'Apellido Representante' )
	nombre_representante = fields.Char(string ='Nombre Representante')
	cedula_representante = fields.Char(string =u'Cédula Representante')
	#Fin Categoria

	# Categoria Accionistas
	No_accionistas = fields.Char(string ='Numero Accionistas')
	accionistas_id = fields.Many2one('rbs.persona', string ='Accionista')
	Nombre_acci_socios = fields.Char(string ='Nombre Socios')
	porecentaje_acciones = fields.Char(string ='Porcentaje de Acciones')
	valor_acciones = fields.Char(string ='Valor de Acciones')
	acta_junta = fields.Char(string ='Acta de Junta')
	#Fin Categoria

	# Categoria Nombramiento
	fechaNombramiento = fields.Datetime(string = 'Fecha Nombramiento')
	tipo_nombra = fields.Datetime(string = 'Tipo Nombraiento')
	plazo_nombramiento = fields.Datetime(string = 'Plazo Nombramiento')
	tipo_gravamen= fields.Datetime(string = 'Tipo Gravamen')
	fecha_gravamen = fields.Datetime(string = 'Fecha Gravamen')
	fecha_cancelacion = fields.Datetime(string = 'Fecha Cancelacion')
	# Fin categoria















	tipo_contrato_id = fields.Many2one('rbs.tipo.contrato', string ='Tipo de Contrato', required = True)
	
	
	
	
	
	
	nombre_institucion = fields.Char(string = 'Nombre de la Institucion', required = True )
	canton_notaria = fields.Char(string = 'Canton de Notaria', required = True )
	


	estado = fields.Selection([
            ('VIGENTE','VIGENTE'),
            ('NOVIGENTE','NO VIGENTE'),
            
        ], string = 'Estado', required = True)
	#filedata = fields.Binary('Archivo',filters='*.pdf')
	#filename = fields.Char('Nombre de archivo', default="Archivo.pdf")
	filedata_id = fields.Many2one('rbs.archivo.pdf')
	filedata = fields.Binary(related='filedata_id.filedata',filters='*.pdf')
	esPesado = fields.Boolean(related='filedata_id.esPesado',string = '¿Es Pesado?')
	rutaFTP = fields.Char(related='filedata_id.rutaFTP', string = 'Escriba la ruta del Archivo')

	identificacion_unica = fields.Char(string = 'Identificador Unico Sistema Remoto',compute='_compute_upper',store = True) 
	ubicacion_dato_id = fields.Many2one('rbs.ubicacion.dato', string ='Ubicacion del Dato', required = True)

	factura_ids = fields.One2many('account.invoice', 'vehiculo_id', string= 'Factura')

	def _getUltimoAnio(self, cr, uid, context=None):
		acta_id = self.pool.get("rbs.documento.mercantil.vehiculo").search(cr, uid,  [], limit=1, order='id desc')
		anio = self.pool.get("rbs.documento.mercantil.vehiculo").browse(cr,uid,acta_id,context = None).anio_id.id
		return anio
	def _getUltimoLibro(self, cr, uid, context=None):
		acta_id = self.pool.get("rbs.documento.mercantil.vehiculo").search(cr, uid,  [], limit=1, order='id desc')
		libro = self.pool.get("rbs.documento.mercantil.vehiculo").browse(cr,uid,acta_id,context = None).libro_id.id
		return libro
	def _getUltimoTomo(self, cr, uid, context=None):
		acta_id = self.pool.get("rbs.documento.mercantil.vehiculo").search(cr, uid,  [], limit=1, order='id desc')
		tomo = self.pool.get("rbs.documento.mercantil.vehiculo").browse(cr,uid,acta_id,context = None).tomo_id.id
		return tomo

	def _create_pdf(self, cr, uid, context=None):
		return self.pool.get("rbs.archivo.pdf").create(cr, uid,{},context=None)

	_defaults = {
		'anio_id': _getUltimoAnio,
		'libro_id': _getUltimoLibro,
		'tomo_id' : _getUltimoTomo,
		'filedata_id' : _create_pdf,
	}

	def open_ui(self, cr, uid, ids, context=None):
		data = self.browse(cr, uid, ids[0], context=context)
		context = dict(context or {})
		#context['active_id'] = data.ids[0]
		return {
			'type' : 'ir.actions.act_url',
			'url':   '/registro_mercantil/web/?binary='+str(ids[0])+'&tipo=vehiculo',
			'target': 'current',
		}

	_rec_name='numero_inscripcion'
	@api.depends('ubicacion_dato_id','persona_cedula','numero_inscripcion')
	def _compute_upper(self):
		for rec in self:
			try:
				rec.identificacion_unica = '03'+rec.ubicacion_dato_id.name+rec.persona_cedula+rec.numero_inscripcion
			except:
				try:
					rec.identificacion_unica = '03'+rec.ubicacion_dato_id.name+rec.numero_inscripcion+rec.numero_inscripcion
				except:
					pass
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

	def codigoascii(self, text):
		return unicode(text).encode('utf-8')
			

	def onchange_persona_id(self, cr, uid, ids, persona_id,context=None):
		persona_id = self.pool.get('rbs.persona').search(cr, uid, [('id','=',persona_id),])
		persona = self.pool.get('rbs.persona').browse(cr,uid,persona_id,context = None)
		result = {}
		
		try:
			
		       			
			if persona:
				#raise osv.except_osv('Esto es un Mesaje!',establecimiento)
				try:
					if persona.persona_nombres:
						result['persona_nombres'] = self.codigoascii(persona.persona_nombres)
				except:
					pass
				
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
					if persona.persona_representante:
						result['persona_representante'] = self.codigoascii(persona.persona_representante) 
				except: 
					pass
				try:
					if persona.persona_razonSocial:
						result['persona_razonSocial'] = self.codigoascii(persona.persona_razonSocial) 
				except: 
					pass
		except:
			pass
		
		return { 'value':result, }


	def onchange_inscripcion(self, cr, uid, ids, inscripcion_num,libro_id,context=None):
		vehiculo_id = self.pool.get('rbs.documento.mercantil.vehiculo').search(cr, uid, [('numero_inscripcion','=',inscripcion_num),('libro_id','=',libro_id)])
		vehiculo = self.pool.get('rbs.documento.mercantil.vehiculo').browse(cr,uid,vehiculo_id,context = None)
		result = {}

		
		try:

			if vehiculo:
				vehiculo = vehiculo[0]
				#raise osv.except_osv('Esto es un Mesaje!',establecimiento)
				try:
					if vehiculo.fecha_inscripcion:
						result['fecha_inscripcion'] = str(vehiculo.fecha_inscripcion)
					
				except:
					pass
				try:
					if vehiculo.anio_id:
						result['anio_id'] = vehiculo.anio_id.id
					
				except:
					pass
				try:
					if vehiculo.libro_id:
						result['libro_id'] = vehiculo.libro_id.id
					
				except:
					pass
				try:
					if vehiculo.tomo_id:
						result['tomo_id'] = vehiculo.tomo_id.id
					
				except:
					pass
				try:
					if vehiculo.tipo_contrato_id:
						result['tipo_contrato_id'] = vehiculo.tipo_contrato_id.id
					
				except:
					pass
				
				try:
					if vehiculo.fecha_cancelacion:
						result['fecha_cancelacion'] = str(vehiculo.fecha_cancelacion)
					
				except:
					pass
				try:
					if vehiculo.tipo_bien_id:
						result['tipo_bien_id'] = vehiculo.tipo_bien_id
										
				except:
					pass

				try:
					if vehiculo.chasis:
						result['chasis'] = self.codigoascii(vehiculo.chasis)
					
				except:
					pass
				
				try:
					if vehiculo.motor:
						result['motor'] = self.codigoascii(vehiculo.motor)
					
				except:
					pass
				
				try:
					if vehiculo.marca:
						result['marca'] = self.codigoascii(vehiculo.marca)
					
				except:
					pass
				
				try:
					if vehiculo.modelo:
						result['modelo'] = self.codigoascii(vehiculo.modelo)
					
				except:
					pass
				
				try:
					if vehiculo.anio_fabricacion:
						result['anio_fabricacion'] = str(vehiculo.anio_fabricacion)
					
				except:
					pass
				
				try:
					if vehiculo.placa:
						result['placa'] = self.codigoascii(vehiculo.placa)
					
				except:
					pass

				try:
					if vehiculo.ultima_modificacion:
						result['ultima_modificacion'] = str(vehiculo.ultima_modificacion)
					
				except:
					pass
				try:
					if vehiculo.nombre_institucion:
						result['nombre_institucion'] = self.codigoascii(vehiculo.nombre_institucion)
					
				except:
					pass
				try:
					if vehiculo.canton_notaria:
						result['canton_notaria'] = self.codigoascii(vehiculo.canton_notaria)
					
				except:
					pass
				try:
					if vehiculo.fecha_escritura_contrato:
						result['fecha_escritura_contrato'] = str(vehiculo.fecha_escritura_contrato)
					
				except:
					pass
				
				try:
					if vehiculo.estado:
						result['estado'] = vehiculo.estado
					
				except:
					pass
				
				try:
					if vehiculo.filedata_id:
						result['filedata_id'] = vehiculo.filedata_id.id
					
				except:
					pass
				
				try:
					if vehiculo.ubicacion_dato_id:
						result['ubicacion_dato_id'] = vehiculo.ubicacion_dato_id.id
					
				except:
					pass

			if not vehiculo:
				result['filedata_id'] = self._create_pdf(cr, uid, context=None)
		except:
			pass
		
		return { 'value':result, }


		

class rbs_persona(models.Model):
	_name ="rbs.persona"
	_description = "persona"
	
	tipo_persona_id = fields.Many2one('rbs.persona', string ='Tipo de Persona')
	persona_razonSocial = fields.Char(string = 'Razon Social')
	persona_id = fields.Many2one('rbs.persona', string ='Compareciente(n)')
	persona_nombres = fields.Char(string = 'Nombres del Compareciente')
	persona_apellidos = fields.Char(string = 'Apellidos del Compareciente')
	persona_tipo_interviniente_id = fields.Many2one('rbs.tipo.interviniente.a', string ='Tipo de Interviniente')
	persona_calidad_compareciente = fields.Char(string = 'Calidad Compareciente')
	persona_tipo_documento = fields.Char(string = 'Tipo Documento')
	name = fields.Char(string = 'Cedula del Compareciente', required = True)
	persona_estado_civil = fields.Char(string = 'Estado Civil')
	conyugue_id = fields.Many2one('rbs.persona', string ='Conyugue')
	_sql_constraints = [
        ('namea_uniq', 'unique(name)',
            'La identificacion de la Persona debe ser unica'),
    ]
	_order = 'persona_nombres'
	
	
class rbs_tipo_compareciente_v(models.Model):
	_name = "rbs.tipo.compareciente.v"
	_description = "Tipo de Compareciente"
	
	name = fields.Char(string = 'Tipo Del Compareciente')
	
class rbs_tipo_contrato(models.Model):
	_name = "rbs.tipo.contrato"
	_description = "Tipo de Contrato"
	
	name = fields.Char(string = 'Tipo Del Contrato')
	
class rbs_tipo_bien(models.Model):
	_name = "rbs.tipo.bien"
	_description = "Tipo de Bien"
	
	name = fields.Char(string = 'Tipo Del Bien')
	
class factura_invoice(models.Model):
	_inherit = 'account.invoice'
	vehiculo_id = fields.Many2one('rbs.documento.mercantil.vehiculo', string='Vehiculo')

		
	
'''
class crud_tipo_archivo(models.Model):
	_name = "crud.tipo.archivo"
	_description = "Informacion especifica de los tipos de Archivo"

	name = fields.Char(string = 'Nombre del Libro' )
	crud_departamento_id = fields.Many2one('crud.departamento', string='departamento del tipo de Archivo')	


class crud_ubicacion_arch(models.Model):
	_name ="crud.ubicacion.arch"
	_description = "Informacion especifica de la ubicacion de cada Archivo"

	caja_ubicacionArch = fields.Char(string = 'Caja donde se encuentra el Archivo')
	bandeja_ubicacionArch = fields.Char(string = 'Bandeja donde se encuentra el Archivo')
	name = fields.Char(string = 'Estante donde se encuentra el Archivo')


class crud_archivo(models.Model):
	_name = "crud.archivo"
	_description = "Informacion especifica de cada archivo"
	
	name = fields.Integer(string = 'Numero del Archivo' )
	fecha_archivo = fields.Date (string = 'Fecha del Archivo' )
	destino_archivo = fields.Char(string = 'Destino del Archivo' )
	asunto_archivo = fields.Char(string = 'Asunto del Archivo' )
	crud_tipo_archivo_id = fields.Many2one('crud.tipo.archivo', string = 'Tipo de archivo' )
	crud_ubicacion_arch_id = fields.Many2one('crud.ubicacion.arch', string = 'Ubicacion del archivo')
	filedata = fields.Binary('Texto',filters='*.pdf')
	comprobante_fname = fields.Char('Comp', default="libro.pdf")




'''

	
