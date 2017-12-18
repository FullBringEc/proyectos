# -*- coding: utf-8 -*-
from _csv import field_size_limit
from cgi import FieldStorage

from dateutil import parser
from openerp import models, fields, api, _
from openerp.osv import osv
from docxtpl import DocxTemplate, RichText
import base64

from openerp import http
from openerp.http import request
from openerp.addons.web.controllers.main import serialize_exception,content_disposition
import time
import datetime
from PIL import Image
import StringIO
from io import BytesIO
import base64
import cStringIO
import pdfmod
import warnings


class rbs_documento_mercantil(models.Model):
	_name ="rbs.documento.mercantil"
	_description = "Documento Mercantil"
	#_rec_name='numero_inscripcion'
	#name= field.Char('Nombre')
	def name_get(self, cr, uid, ids, context=None):
		if context is None:
			context = {}
		res = []
		for record in self.browse(cr, uid, ids, context=context):
			if record.anio_id:
				anio = record.anio_id.name
				libro = record.libro_id.name
				tomo = record.tomo_id.name
				tit = "%s-%s-%s" % (anio, libro,tomo)
				res.append((record.id, tit))

			else:
				tit = "Sin registro"
				res.append((record.id,tit))
		return res
	# Ctegoria Libro
	anio_id = fields.Many2one('rbs.anio', string ='Año')
	libro_id = fields.Many2one('rbs.libro', string ='Libro')
	tipo_libro_mercantil_id = fields.Many2one(related="libro_id.tipo_libro_mercantil_id",string='Tipo de Libro M')
	# reg_acto_contrato = fields.Selection([
	#            ('ACTO','ACTO'),
	#            ('CONTRATO','CONTRATO'),
	#        ],string ='Registra Acto/Contrato')
	tipo_tramite_id = fields.Many2one('rbs.tipo.tramite',string ='Tipo de trámite')
	# tipo_contrato_id = fields.Many2one('rbs.tipo.contrato', string ='Tipo de Acto/Contrato')
	tramite_id = fields.Many2one('rbs.tramite.mercantil',string='Trámite')
	# tipo_libro = fields.Char (string='Tipo Libro')
	tomo_id = fields.Many2one("rbs.tomo", string ='Tomo')
	observacion = fields.Char(string='Observación')
	foleo_desde = fields.Char(string='Desde')
	foleo_hasta = fields.Char (string='Hasta')
	


	# INFORMACION DE LA INSCRIPCION

	numero_inscripcion = fields.Integer(string = 'Número de inscripción' )
	repertorio = fields.Char (string='Repertorio')
	provincia_notaria_id = fields.Many2one('rbs.provincia', string ='Provincia de la notaria, juzgado o institución pública')
	canton_notaria_id = fields.Many2one('rbs.canton', string ='Canton de la notaria')
	notaria_id = fields.Many2one('rbs.institucion',string ='Nombre notaria o juzgado')
	cuantia_valor = fields.Char(string ='Cuantia' )
	fecha_acta_junta = fields.Datetime (string='Fecha de acta de la junta')
	fecha_cancel_gravamen = fields.Datetime (string='Fecha de cancelación de gravamen/limitación')
	fecha_const_gravamen = fields.Datetime (string='Fecha Const gravamen/limitacion')
	fecha_inscripcion = fields.Datetime(string = 'Fecha de inscripción' )
	fecha_repertorio = fields.Datetime (string='Fecha repertorio')
	fecha_cancelacion = fields.Datetime(string = 'Fecha de cancelación' )
	fecha_ultima_modificacion = fields.Datetime(string = 'Fecha de última modificación de la fuente')
	fecha_escritura = fields.Datetime(string = 'Fecha de escritura, sentencia o resolución')
	nombramiento_mercantil_id = fields.Many2one('rbs.nombramiento.mercantil', string ='Tipo de nombramiento')
	plazo_nombramiento_cant = fields.Integer(string = 'Plazo nombramiento')
	plazo_nombramiento_tipo = fields.Selection([
            ('DÍAS','Días'),
            ('SEMANAS','Semanas'),
            ('MESES','Meses'),
            ('AÑOS','Años'),
        ])
	fecha_nombramiento = fields.Datetime(string = 'Fecha de nombramiento')



	tipo_acto_contrato = fields.Many2many('rbs.tipo.acto.contrato',relation="mercantil_tipo_acto_contrato_rel",string = 'Tipo de acto o contrato')
	
	
	
	# expensas = fields.Selection([
 #            ('CERTIFICADO','CERTIFICADO'),
 #            ('DECLARACION','DECLARACION'),
 #        ],string ='Expensas')
	# numero_acuerdo_ministerial = fields.Char("Numero de acuerdo Ministerial")
	# fecha_adjudicion = fields.Datetime(string = 'Fecha de la Adjudicacion')
	# fecha_insi_bienes = fields.Datetime(string = 'Fecha judicial/acta notarial')

	

	parte_ids = fields.One2many('rbs.parte','documento_mercantil_id',string = 'Partes')
	repr_identificacion = fields.Char(string = 'Cédula o pasaporte del representante')
	repr_nombre = fields.Char(string = 'Nombres del representante')
	repr_apellido = fields.Char(string = 'Apellido del representante')
	repr_razon_social = fields.Char(string = 'Razón social del representante')
	repr_acreedor = fields.Char(string = 'Acreedor')
	repr_nombramiento_id = fields.Many2one('rbs.nombramiento.mercantil', string ='Cargo del representante')

	parte_char_ids = fields.One2many('rbs.parte.char','documento_mercantil_id','Partes Char')
	bien_ids = fields.One2many('rbs.bien','documento_mercantil_id',string ='Bienes')
	accionista_ids = fields.One2many('rbs.accionista','documento_mercantil_id',string ='Accionistas')
	marginacion_ids = fields.One2many('rbs.marginacion','documento_mercantil_id',string ='Marginaciones')
	tipo_gravamen_ids = fields.One2many('rbs.gravamen','documento_mercantil_id',string = 'Tipo gravamen/limitación')
	identificacion_unica = fields.Char(string = 'Identificador',compute='_compute_upper',store = True)
	ubicacion_dato_id = fields.Many2one('rbs.ubicacion.dato', string ='Ubicación del dato')
	#Fin categoria

	# Datos Persona
	tipo_persona_id = fields.Selection([
            ('NATURAL','Natural'),
            ('JURIDICA','Jurídica'),
        ],string ='Tipo de persona')
	persona_id = fields.Many2one('rbs.persona', string ='Compareciente(n)')
	persona_nombres = fields.Char(string = 'Nombres del compareciente')
	persona_apellidos = fields.Char(string = 'Apellidos del compareciente')
	persona_estado_civil = fields.Char(string = 'Estado civil')
	persona_cedula = fields.Char(string = 'Cedula del compareciente')
	persona_estado_civil = fields.Char(string = 'Estado civil')
	persona_nombres_conyuge = fields.Char(string = 'Nombres de cónyuge')
	persona_apellidos_conyuge = fields.Char(string = 'Apellidos de cónyuge')
	persona_cedula_conyuge = fields.Char(string = 'Cedula del cónyuge')
	persona_tipo_interviniente_id = fields.Many2one('rbs.tipo.interviniente.a', string ='Tipo de interviniente')
	persona_calidad_compareciente = fields.Char(string = 'Calidad compareciente')
	persona_razonSocial = fields.Char(string = 'Razón social')
	acreedor_id = fields.Many2one('rbs.persona', string = 'Acreedor')
	# Fin categoria

	# Datos Bien
	
	# Fin categoria

	# Datos Registrales
	canton_registro_id = fields.Many2one('rbs.canton', string ='Cantón registro mercantil')
	ultima_modificacion = fields.Char(string = 'Última modificación' )
	notaria_juzgado_entidad = fields.Char(string ='Nombre notaria o juzgado')
	canton_notaria_id = fields.Many2one('rbs.canton', string ='Cantón de la notaria')
	fecha_escritura_contrato = fields.Datetime(string = 'Fecha de escritura')
	marginacion_tramite_origi = fields.Char (string='Marginacion trámite')
	# Fin categoria


	# Categoria Accionistas
	No_accionistas = fields.Char(string ='Número accionistas')
	accionistas_id = fields.Many2one('rbs.persona', string ='Accionista')
	Nombre_acci_socios = fields.Char(string ='Nombre socios')
	porecentaje_acciones = fields.Char(string ='Porcentaje de acciones')
	valor_acciones = fields.Char(string ='Valor de acciones')
	acta_junta = fields.Char(string ='Acta de junta')
	#Fin Categoria

	# Categoria Nombramiento
	fechaNombramiento = fields.Datetime(string = 'Fecha nombramiento')
	tipo_nombra = fields.Datetime(string = 'Tipo nombraiento')
	plazo_nombramiento = fields.Datetime(string = 'Plazo nombramiento')
	tipo_gravamen= fields.Datetime(string = 'Tipo gravamen')
	fecha_gravamen = fields.Datetime(string = 'Fecha gravamen')
	# Fin categoria















	tipo_contrato_id = fields.Many2one('rbs.tipo.contrato', string ='Tipo de contrato')
	
	
	
	
	
	
	nombre_institucion = fields.Char(string = 'Nombre de la institución' )
	canton_notaria = fields.Char(string = 'Canton de notaria')
	


	estado = fields.Selection([
            ('VIGENTE','Vigente'),
            ('NOVIGENTE','No vigente'),
            
        ], string = 'Estado')
	#filedata = fields.Binary('Archivo',filters='*.pdf')
	#filename = fields.Char('Nombre de archivo', default="pdf")
	filedata_id = fields.Many2one('rbs.pdf')
	filedata = fields.Binary(related='filedata_id.filedata',filters='*.pdf')
	esPesado = fields.Boolean(related='filedata_id.esPesado',string = '100 mb')
	rutaFTP = fields.Char(related='filedata_id.rutaFTP', string = 'Ruta del Archivo')
	contenedor_id = fields.Many2one("rbs.contenedor", string="Contenedor")

	@api.one 
	def borrar_contenedor(self):
		self.contenedor_id = None

	@api.onchange('filedata')
	def on_change_filedata(self):
	 	try:
	 		contenedor = self.env['rbs.contenedor'].create({'name': str(self.anio_id.name) + str(self.libro_id.name) + str(self.tomo_id.name) + str(self.numero_inscripcion) + str("mercantil")})
			filedataByte = BytesIO(base64.b64decode(self.filedata))
			pdfmod.pdfOrTiff2image(self,filedataByte,contenedor)
			self.contenedor_id=contenedor.id
		except:
			pass
	identificacion_unica = fields.Char(string = 'Identificador único sistema remoto',compute='_compute_upper',store = True) 
	ubicacion_dato_id = fields.Many2one('rbs.ubicacion.dato', string ='Ubicación del dato')
	factura_ids = fields.One2many('account.invoice', 'mercantil_id', string= 'Factura')
	dataWord=fields.Binary("word")
	def generate_word(self, cr, uid, ids, context=None):
		datos  = self.read(cr, uid, ids, context=context)[0]
		output = BytesIO()
		tpl=DocxTemplate('inscripcion.docx')
		documento_mercantil = self.browse(cr,uid,ids,context = context)
		compareciente = [] 
		for partes in documento_mercantil.parte_ids:
			detalle = {}
			detalle['cliente'] = partes.tipo_persona
			detalle['identi'] = partes.num_identificacion
			detalle['compareciente'] = RichText (str (partes.nombres)+' '+str(partes.apellidos ))
			detalle['estado'] = RichText (str (partes.estado_civil))
			detalle['interviniente'] = RichText (str(partes.tipo_interviniente_id.name))
			detalle['ciudad'] = RichText (str(documento_mercantil.canton_notaria_id.name))
			compareciente.append(detalle)
		datosbien = []
		for bien in documento_mercantil.bien_ids:
		    detalle = {}
		    documento_mercantil = None
		    if bien.documento_mercantil_id:
		        documento_mercantil = bien.documento_mercantil_id
		    else:
		        documento_mercantil = bien.documento_propiedad_id

		    detalle['numero'] = RichText (str (documento_mercantil.numero_inscripcion))
		    detalle['fecha_inscripcion'] = RichText (str (documento_mercantil.fecha_inscripcion))
		    detalle['tipobien'] = RichText (str(bien.tipo_bien_id.name))
		    datosbien.append(detalle)
		  

		context = {
		    'acto' : RichText (documento_mercantil.tipo_tramite_id.name),
		    'compareciente' : compareciente,
		    'datosbien' : datosbien,
		    'ntomo': RichText (str (documento_mercantil.tomo_id.name)),
		    'ninscripcion' : RichText (str (documento_mercantil.numero_inscripcion)),
		    'nrepertorio' : RichText (str (documento_mercantil.repertorio)),
		    'frepertorio' : RichText (str (documento_mercantil.fecha_repertorio)),
		    'natacto' : RichText ('SD'),
		    'folioi' : RichText (str (documento_mercantil.foleo_desde)),
		    'foliof' : RichText (str (documento_mercantil.foleo_hasta)),
		    'periodo' : RichText (str (documento_mercantil.anio_id.name)),
		    'natcontrato' : RichText (str (documento_mercantil.libro_id.name)),
		    'notaria' : RichText (str (documento_mercantil.notaria_id.name)),
		    'nomcanton' : RichText (str (documento_mercantil.canton_notaria_id.name)),
		    'fechaprov' : RichText (str (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))),
		    'fresolucion' : RichText (str (documento_mercantil.fecha_escritura)),
		    'observacion' : RichText (str (documento_mercantil.observacion)),

		}





		tpl.render(context)
		tpl.save(output)
		return base64.b64encode(output.getvalue())
	
	def word(self, cr, uid, ids, context=None):
		out = self.generate_word( cr, uid, ids, context=None)
		self.write( cr, uid, ids,{'dataWord':out})
		return self.download_word( cr, uid, ids, context=None)

	def download_word(self, cr, uid, ids, context=None):
		data = self.browse(cr, uid, ids[0], context=context)
		context = dict(context or {})
		return {
				'type' : 	'ir.actions.act_url',
                'url':      '/web/binary/download_document?model=rbs.documento.mercantil&field=dataWord&id=%s&filename=Inscripcion.docx'%(str(ids[0])),
				'target': 	'new'
			}




	def _getUltimoAnio(self, cr, uid, context=None):
		acta_id = self.pool.get("rbs.documento.mercantil").search(cr, uid,  [], limit=1, order='id desc')
		anio = self.pool.get("rbs.documento.mercantil").browse(cr,uid,acta_id,context = None).anio_id.id
		return anio
	def _getUltimoLibro(self, cr, uid, context=None):
		acta_id = self.pool.get("rbs.documento.mercantil").search(cr, uid,  [], limit=1, order='id desc')
		libro = self.pool.get("rbs.documento.mercantil").browse(cr,uid,acta_id,context = None).libro_id.id
		return libro
	def _getUltimoTomo(self, cr, uid, context=None):
		acta_id = self.pool.get("rbs.documento.mercantil").search(cr, uid,  [], limit=1, order='id desc')
		tomo = self.pool.get("rbs.documento.mercantil").browse(cr,uid,acta_id,context = None).tomo_id.id
		return tomo

	def _create_pdf(self, cr, uid, context=None):
		return self.pool.get("rbs.pdf").create(cr, uid,{},context=None)

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
			'url':   '/registro_mercantil/web/?binary='+str(ids[0])+'&tipo=mercantil',
			'target': 'current',
		}

	

	@api.onchange('parte_ids','bien_ids')
	def onchange_parte_ids(self):
		parte_char_ids_num = []
		self.parte_char_ids = None
		for parte in self.parte_ids:
			nombres = parte.razon_social or parte.nombres
			r = [x for x in self.parte_char_ids if x.name == nombres]
			if r:
				continue
			parte_char = self.env['rbs.parte.char'].create({'name':parte.razon_social or parte.nombres or "",'parte_id':parte.id,'documento_mercantil_id':self.id})
			self.parte_char_ids |= parte_char
			parte_char_ids_num.append(parte_char.id)
		print parte_char_ids_num
		for bien in self.bien_ids:
			bien.parte_char_ids = [(6,0,parte_char_ids_num)]
		return
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
		mercantil_id = self.pool.get('rbs.documento.mercantil').search(cr, uid, [('numero_inscripcion','=',inscripcion_num),('libro_id','=',libro_id)])
		mercantil = self.pool.get('rbs.documento.mercantil').browse(cr,uid,mercantil_id,context = None)
		result = {}

		
		try:

			if mercantil:
				mercantil = mercantil[0]
				#raise osv.except_osv('Esto es un Mesaje!',establecimiento)
				try:
					if mercantil.fecha_inscripcion:
						result['fecha_inscripcion'] = str(mercantil.fecha_inscripcion)
					
				except:
					pass
				try:
					if mercantil.anio_id:
						result['anio_id'] = mercantil.anio_id.id
					
				except:
					pass
				try:
					if mercantil.libro_id:
						result['libro_id'] = mercantil.libro_id.id
					
				except:
					pass
				try:
					if mercantil.tomo_id:
						result['tomo_id'] = mercantil.tomo_id.id
					
				except:
					pass
				try:
					if mercantil.tipo_contrato_id:
						result['tipo_contrato_id'] = mercantil.tipo_contrato_id.id
					
				except:
					pass
				
				try:
					if mercantil.fecha_cancelacion:
						result['fecha_cancelacion'] = str(mercantil.fecha_cancelacion)
					
				except:
					pass
				try:
					if mercantil.tipo_bien_id:
						result['tipo_bien_id'] = mercantil.tipo_bien_id
										
				except:
					pass

				try:
					if mercantil.chasis:
						result['chasis'] = self.codigoascii(mercantil.chasis)
					
				except:
					pass
				
				try:
					if mercantil.motor:
						result['motor'] = self.codigoascii(mercantil.motor)
					
				except:
					pass
				
				try:
					if mercantil.marca:
						result['marca'] = self.codigoascii(mercantil.marca)
					
				except:
					pass
				
				try:
					if mercantil.modelo:
						result['modelo'] = self.codigoascii(mercantil.modelo)
					
				except:
					pass
				
				try:
					if mercantil.anio_fabricacion:
						result['anio_fabricacion'] = str(mercantil.anio_fabricacion)
					
				except:
					pass
				
				try:
					if mercantil.placa:
						result['placa'] = self.codigoascii(mercantil.placa)
					
				except:
					pass

				try:
					if mercantil.ultima_modificacion:
						result['ultima_modificacion'] = str(mercantil.ultima_modificacion)
					
				except:
					pass
				try:
					if mercantil.nombre_institucion:
						result['nombre_institucion'] = self.codigoascii(mercantil.nombre_institucion)
					
				except:
					pass
				try:
					if mercantil.canton_notaria:
						result['canton_notaria'] = self.codigoascii(mercantil.canton_notaria)
					
				except:
					pass
				try:
					if mercantil.fecha_escritura_contrato:
						result['fecha_escritura_contrato'] = str(mercantil.fecha_escritura_contrato)
					
				except:
					pass
				
				try:
					if mercantil.estado:
						result['estado'] = mercantil.estado
					
				except:
					pass
				
				try:
					if mercantil.filedata_id:
						result['filedata_id'] = mercantil.filedata_id.id
					
				except:
					pass
				
				try:
					if mercantil.ubicacion_dato_id:
						result['ubicacion_dato_id'] = mercantil.ubicacion_dato_id.id
					
				except:
					pass

			if not mercantil:
				result['filedata_id'] = self._create_pdf(cr, uid, context=None)
		except:
			pass
		
		return { 'value':result, }


		


	
class rbs_tipo_compareciente_v(models.Model):
	_name = "rbs.tipo.interviniente.v"
	_description = "Tipo de interviniente"
	
	name = fields.Char(string = 'Tipo del compareciente')
	
class rbs_tipo_contrato(models.Model):
	_name = "rbs.tipo.contrato"
	_description = "Tipo de Contrato"
	
	name = fields.Char(string = 'Tipo del contrato')
	
	
class rbs_compania(models.Model):
	_name ="rbs.compania"
	_description = "Compañia"
	
	
	compania_nombres = fields.Char(string = 'Nombre de la Compañía', required=True)
	name = fields.Char(string = 'Indentificacion de la Compañía', required = True)
	compania_especie_id = fields.Many2one('rbs.compania.especie', string ='Especie de Compañía', required = True)
	_sql_constraints = [
        ('compania_identificacion_uniq', 'unique(name)',
            'La identificacion debe ser unica por Compañía'),
    ]
	_order = 'compania_nombres'
	#_rec_name = 'compania_identificacion'
	
class rbs_tipo_interviniente(models.Model):
	_name = "rbs.tipo.interviniente"
	_description = "Tipo de interviniente"
	
	name = fields.Char(string = 'Tipo del interviniente')

class rbs_calidad_compareciente(models.Model):
	_name = "rbs.calidad.compareciente"
	_description = "Calidad del compareciente"
	
	name = fields.Char(string = 'Calidad del Compareciente')

	
class rbs_tipo_compareciente_a(models.Model):
	_name = "rbs.tipo.interviniente.a"
	_description = "Tipo de compareciente"
	
	name = fields.Char(string = 'Tipo del compareciente')
	
class rbs_compania_especie(models.Model):
	_name = "rbs.compania.especie"
	_description = "Especie de Compañia"
	
	name = fields.Char(string = 'Especie')
	
class rbs_cargo(models.Model):
	_name = 'rbs.cargo'
	_description = "Tipo de cargo"
	
	name = fields.Char(string = 'Tipo de cargo')

class rbs_canton(models.Model):
	_name = 'rbs.canton'
	_description = "Nombre del cantón"
	
	name = fields.Char(string = 'Nombre del cantón')
	
class rbs_tipo_tramite(models.Model):
	_name = 'rbs.tipo.tramite'
	_description = "Tipo de trámite"
	
	name = fields.Char(string = 'Tipo De trámite')
	
class rbs_ubicacion_dato(models.Model):
	_name = 'rbs.ubicacion.dato'
	_description = "Ubicación de dato"
	
	name = fields.Char(string = 'Ubicacion del dato')

class rbs_estado_inscripcion(models.Model):
	_name = 'rbs.estado.inscripcion'
	_description = "Estado de Inscripción"
	
	name = fields.Char(string = 'Estado de Inscripción')


# class factura_invoice(models.Model):
# 	_inherit = 'account.invoice'
# 	acta_id = fields.Many2one('rbs.documento.mercantil.acta', string='Acta')

class reportes_doc_mercantiles(models.Model):
	_inherit = 'res.company'
	certificacion = fields.Binary(string='Certificación')
	inscripcion = fields.Binary(string='Inscripción')
			
	
class factura_invoice(models.Model):
	_inherit = 'account.invoice'
	mercantil_id = fields.Many2one('rbs.documento.mercantil', string='Documento mercantil')
