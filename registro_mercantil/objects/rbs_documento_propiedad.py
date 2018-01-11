# -*- coding: utf-8 -*-
#!/usr/bin/env python
from dateutil import parser
from openerp import models, fields, api, _
from openerp.osv import osv
from io import BytesIO 
import base64
from docxtpl import DocxTemplate, RichText
import time
import datetime
from jinja2 import Environment, FileSystemLoader
import os

class rbs_documento_propiedad(models.Model):
	_name ="rbs.documento.propiedad"
	_description = "Documento de la Propiedad"
	#name= field.Char('Nombre')
	def name_get(self):
		res = []
		for record in self:
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
	#Encabezado
	anio_id = fields.Many2one('rbs.anio', string ='Año')
	libro_id = fields.Many2one('rbs.libro', string ='Libro' )

	tipo_libro_propiedad_id = fields.Many2one(related="libro_id.tipo_libro_propiedad_id",string='Tipo de Libro P')
	# reg_acto_contrato = fields.Selection([
 #            ('ACTO','ACTO'),
 #            ('CONTRATO','CONTRATO'),
 #        ],string ='Registra Acto/Contrato')
	tipo_tramite_id = fields.Many2one('rbs.tipo.tramite',string ='Tipo de trámite')
	# tipo_libro = fields.Char (string='Tipo Libro', required = True)
	tramite_id = fields.Many2one('rbs.tramite.propiedad',string='Trámite')
	tomo_id = fields.Many2one("rbs.tomo", string ='Tomo')
	observacion = fields.Char(string='Observación')
	foleo_desde = fields.Integer(string='Desde')
	foleo_hasta = fields.Integer (string='Hasta')
	
   #########Informacion de la inscripcion

	repertorio = fields.Char (string='Repertorio')
	fecha_repertorio = fields.Datetime (string='Fecha repertorio')
	numero_inscripcion = fields.Integer(string = 'Número de inscripción')
	fecha_inscripcion = fields.Datetime(string = 'Fecha de inscripción' )
	cuantia_unidad = fields.Selection([
            ('SUCRE','Sucre'),
            ('DOLAR','Dólar'),
        ],string ='Unidad monetaria' )
	
	
	
	fecha_const_gravamen = fields.Datetime (string='Fecha de constitución del gravamen  o limitación')
	fecha_cancel_gravamen = fields.Datetime (string='Fecha de cancelación del gravamen  o limitación')
	fecha_ultima_modificacion_inscripcion = fields.Datetime(string = 'Fecha de última modificación de la inscripción' )
	provincia_notaria_id = fields.Many2one('rbs.provincia', string ='Provincia de la notaria, juzgado o institución pública')
	canton_notaria_id = fields.Many2one('rbs.canton', string ='Canton de la notaria')
	notaria_id = fields.Many2one('rbs.institucion',string ='Nombre notaria o juzgado')
	expensas = fields.Selection([
            ('CERTIFICADO','Certificado'),
            ('DECLARACION','Declaración'),
        ],string ='Expensas')
	fecha_escritura = fields.Datetime(string = 'Fecha escritura')
	numero_acuerdo_ministerial = fields.Char("Número de acuerdo ministerial")
	fecha_adjudicion = fields.Datetime(string = 'Fecha de la adjudicación')
	tipo_acto_contrato = fields.Many2many('rbs.tipo.acto.contrato',relation="propiedad_tipo_acto_contrato_rel",string = 'Tipo de acto o contrato')
	fecha_insi_bienes = fields.Datetime(string = 'Fecha judicial/acta notarial')

	cuantia_valor = fields.Char(string ='Cuantía' )
   #


	parte_ids = fields.One2many('rbs.parte','documento_propiedad_id',string = 'Partes')
	parte_char_ids = fields.One2many('rbs.parte.char','documento_propiedad_id','Partes Char')
	bien_ids = fields.One2many('rbs.bien','documento_propiedad_id',string ='Bienes')
	# alicuota_ids = fields.One2many('rbs.bien.alicuota','documento_propiedad_id',string = 'Alicuotas')
	# parte_ids = fields.Many2many('rbs.parte',relation="propiedad_parte_rel",string = 'Partes')




	# genera_gravamen_limitacion = fields.Selection([
	#         ('SI','SI'),
	#         ('NO','NO'),
	#     ],string ='Genera Gravamen/Limitacion')	
	gravamen_limitacion = fields.Boolean(string ='Gravamen o limitación')
	tipo_gravamen_ids = fields.One2many('rbs.gravamen','documento_propiedad_id',string = 'Tipo Gravamen/Limitación')
	genera_gravamen_limitacion = fields.Boolean(string ='Genera gravamen o limitación')
	genera_tipo_gravamen_ids = fields.One2many('rbs.gravamen','documento_propiedad_genera_gravamen_id',string = 'Tipo gravamen/limitación')
	identificacion_unica = fields.Char(string = 'Identificador',compute='_compute_upper',store = True)

	marginacion_ids = fields.One2many('rbs.marginacion','documento_propiedad_id',string ='Marginaciones')

	causante = fields.Char (string='Causante')
	fecha_defuncion = fields.Datetime (string='Fecha defunción')
	conyuge_sobreviviente = fields.Char (string='Cónyuge sobreviviente')
	heredero_ids = fields.One2many('rbs.heredero','documento_propiedad_id',string = 'Herederos')
	
	
	juicio_numero = fields.Integer(string ='Número del juicio')
	# estado_inscripcion_id = fields.Many2one('rbs.estado.inscripcion', string ='Estado de la Inscripcion', required = True)
	
	state = fields.Selection([
			('borrador','Borrador'),
            ('activo','Activo'),
            ('sustituido','Sustituido'),
        ], 'state',default='borrador', readonly=True)
	
	

	dataWord=fields.Binary("word")
	
	@api.multi
	def word(self):
		output = BytesIO()
		tmpl_path = os.path.join(os.path.dirname(__file__), 'Documentos/DocPropiedad')
		tpl=DocxTemplate(tmpl_path+'/inscripcion.docx')

		compareciente = [] 
		for partes in self.parte_ids:
			detalle = {}
			detalle['cliente'] = partes.tipo_persona
			detalle['identi'] = partes.num_identificacion
			detalle['compareciente'] = RichText (str (partes.nombres)+' '+str(partes.apellidos ))
			detalle['estado'] = RichText (str (partes.estado_civil))
			detalle['interviniente'] = RichText (str(partes.tipo_interviniente_id.name))
			detalle['ciudad'] = RichText (str(self.canton_notaria_id.name))
			compareciente.append(detalle)

		datosbien = []
		for bien in self.bien_ids:
			detalle = {}
			# documento_mercantil = None
			# if bien.documento_mercantil_id:
			#     documento_mercantil = bien.documento_mercantil_id
			# else:
			#     documento_mercantil = bien.documento_propiedad_id

			detalle['numero'] = RichText (str (self.numero_inscripcion))
			detalle['fecha_inscripcion'] = RichText (str (self.fecha_inscripcion))
			detalle['tipobien'] = RichText (str(bien.tipo_bien_id.name))

			datosbien.append(detalle)

		context = {
			'acto' : RichText (self.tipo_tramite_id.name),
			'compareciente' : compareciente,
			'datosbien' : datosbien,
			'ntomo': RichText (str (self.tomo_id.name)),
			'ninscripcion' : RichText (str (self.numero_inscripcion)),
			'nrepertorio' : RichText (str (self.repertorio)),
			'frepertorio' : RichText (str (self.fecha_repertorio)),
			'natacto' : RichText ('SD'),
			'folioi' : RichText (str (self.foleo_desde)),
			'foliof' : RichText (str (self.foleo_hasta)),
			'periodo' : RichText (str (self.anio_id.name)),
			'natcontrato' : RichText (str (self.libro_id.name)),
			'notaria' : RichText (str (self.notaria_id.name)),
			'nomcanton' : RichText (str (self.canton_notaria_id.name)),
			'fechaprov' : RichText (str (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))),
			'fresolucion' : RichText (str (self.fecha_escritura)),
			'observacion' : RichText (str (self.observacion)),

		}



		tpl.render(context)
		tpl.save(output)

		self.write({'dataWord':base64.b64encode(output.getvalue())})
		# return self.word( cr, uid, ids, context=None)
		return {
			'type' : 	'ir.actions.act_url',
			'url':      '/web/binary/download_document?model=rbs.documento.propiedad&field=dataWord&id=%s&filename=Inscripcion.docx'%(str(self.id)),
			'target': 	'new'
			}


	
	

	factura_ids = fields.One2many('account.invoice', 'propiedad_id', string= 'Factura')
	
	
	@api.onchange('parte_ids','bien_ids')
	def onchange_parte_ids(self):
		parte_char_ids_num = []
		self.parte_char_ids = None
		for parte in self.parte_ids:
			nombres = parte.razon_social or parte.nombres
			r = [x for x in self.parte_char_ids if x.name == nombres]
			if r:
				continue
			parte_char = self.env['rbs.parte.char'].create({'name':parte.razon_social or parte.nombres or "",'parte_id':parte.id,'documento_propiedad_id':self.id})
			self.parte_char_ids |= parte_char
			parte_char_ids_num.append(parte_char.id)
		print parte_char_ids_num
		for bien in self.bien_ids:
			bien.parte_char_ids = [(6,0,parte_char_ids_num)]


		return

	def _getUltimoAnio(self, context=None):
		acta_id = self.search(  [], limit=1, order='id desc')
		return acta_id
	def _getUltimoLibro(self, context=None):
		libro_id = self.search( [], limit=1, order='id desc')
		return libro_id
	def _getUltimoTomo(self, context=None):
		tomo_id = self.search([], limit=1, order='id desc')
		return tomo_id

	_defaults = {
		'anio_id': _getUltimoAnio,
		'libro_id': _getUltimoLibro,
		'tomo_id' : _getUltimoTomo,
	}
	_rec_name='numero_inscripcion'

	@api.multi
	def open_ui(self, context=None):
		return {
			'type' : 'ir.actions.act_url',
			'url':   '/registro_mercantil/web/?binary='+str(self.id)+'&tipo=propiedad',
			'target': 'new',
		}

	# @api.depends('ubicacion_dato_id','numero_inscripcion')
	@api.depends('numero_inscripcion')
	def _compute_upper(self):
		for rec in self:
			try:
				rec.identificacion_unica = '02'+rec.ubicacion_dato_id.name+rec.numero_inscripcion
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

	def on_change_anio_id(self,anio_id,context=None):
		result = {}		
		if(self._getUltimoAnio(context=None) != anio_id):
			result['libro_id'] = 0;
		return { 'value':result, }

	def on_change_libro_id(self,libro_id,context=None):
		result = {}		
		if(self._getUltimoLibro(context=None) != libro_id):
			result['tomo_id'] = 0;
		return { 'value':result, }


	def onchange_inscripcion(self,inscripcion_num,libro_id,context=None):
		propiedad = self.search([('numero_inscripcion','=',inscripcion_num),('libro_id','=',libro_id)])
		# propiedad = self.browse(cr,uid,propiedad_id,context = None)
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
					if propiedad.tipo_acto_contrato_sel:
						result['tipo_acto_contrato_sel'] = propiedad.tipo_acto_contrato

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
					if propiedad.provincia_id:
						result['provincia_id'] = propiedad.provincia_id.id

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
				# try:
				# 	if propiedad.estado_inscripcion_id:
				# 		result['estado_inscripcion_id'] = propiedad.estado_inscripcion_id.id

				# except: 
				# 	pass

				# try:
				# 	if propiedad.ubicacion_dato_id:
				# 		result['ubicacion_dato_id'] = propiedad.ubicacion_dato_id.id

				# except: 
				# 	pass

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
					if propiedad.fecha_escritura:
						result['fecha_escritura'] = str(propiedad.fecha_escritura)
					
				except:
					pass

				try:
					if propiedad.filedata_id:
						result['filedata_id'] = propiedad.filedata_id.id

				except: 
					pass
			if not propiedad:
				result['filedata_id'] = self._create_pdf(context=None)

				
				
		except:
			pass
		
		return { 'value':result, }\


class rbs_heredero(models.Model):
	_name = 'rbs.heredero'
	name =  fields.Char (string='Herederos')
	documento_propiedad_id = fields.Many2one('rbs.documento.propiedad',"Documento de propiedad")


# class rbs_bien_alicuota(models.Model):
# 	_name = 'rbs.bien.alicuota'
# 	_description = "Bien Alicuota"
# 	name = fields.Char("Bien")
# 	alicuota_ids = fields.One2many('rbs.alicuota','bien_alicuota_id',"Porcentajes")
# 	documento_propiedad_id = fields.Many2one('rbs.documento.propiedad',"Documento de Propiedad")
class rbs_alicuota(models.Model):
	_name = 'rbs.alicuota'
	_description = u"Alícuotas"
	name = fields.Char("Descripción")
	porcentaje = fields.Integer('Porcentaje')
	# bien_alicuota_id = fields.Many2one('rbs.bien.alicuota',"Bien alicuota")
	bien_id = fields.Many2one('rbs.bien',"Bien")


class rbs_tipo_acto_contrato(models.Model):
	_name = 'rbs.tipo.acto.contrato'
	_description = "Tipos de acto/contrato"
	name = fields.Char(string = 'Nombre')
	is_acto = fields.Boolean(string = '¿Visible en acta?')
	is_contrato = fields.Boolean(string = '¿Visible en contrato?')

	tipo_acta_contrato_sel = fields.Selection([
            ('AMBOS','Ambos'),
			('ACTO','Acto'),
            ('CONTRATO','Contrato'),
        ],compute='get_tipo_acto_contrato_sel', string = "Tipo contrato/Acta" , store=True)

	@api.depends('is_acto','is_contrato')
	def get_tipo_acto_contrato_sel(self):

		if self.is_acto == self.is_contrato == True:
			self.tipo_acta_contrato_sel ='AMBOS'
			return
		if self.is_acto:
			self.tipo_acta_contrato_sel ='ACTO'
			return
		if self.is_contrato:
			self.tipo_acta_contrato_sel ='CONTRATO'
			return


class rbs_zona(models.Model):
	_name = 'rbs.zona'
	_description = "Nombre de la zona"
	name = fields.Char(string = 'Nombre de la zona')
	# parroquia_id = fields.Many2one('rbs.parroquia',"Parroquia")

class rbs_parroquia(models.Model):
	_name = 'rbs.parroquia'
	_description = "Nombre de la parroquia"
		
	name = fields.Char(string = 'Nombre de la parroquia')
	canton_id = fields.Many2one('rbs.canton',"Canton")
	provincia_id = fields.Many2one(related='canton_id.provincia_id',string = 'Provincia')
	pais_id = fields.Many2one(related='provincia_id.pais_id',string = "Pais")

	def name_get(self):
		res = []
		for record in self:
			name = record.name
			canton = record.canton_id.name
			# provincia = record.provincia_id.name
			# pais = record.pais_id.name
			tit = "%s/%s" % (name,canton)
			res.append((record.id, tit))
		return res

class rbs_canton(models.Model):
	_name = 'rbs.canton'
	_description = "Nombre Canton"
		
	
	name = fields.Char(string = 'Canton' )
	provincia_id = fields.Many2one('rbs.provincia','Provincia', domain="[('pais_id','=',pais_id)]")
	pais_id = fields.Many2one(related='provincia_id.pais_id',string = "Pais")

	def name_get(self):
		res = []
		for record in self:
			name = record.name
			provincia = record.provincia_id.name
			# pais = record.pais_id.name
			tit = "%s/%s" % (name,provincia)
			res.append((record.id, tit))
		return res


class rbs_provincia(models.Model):
	_name = 'rbs.provincia'
	_description = "Nombre de la provincia"
		
	name = fields.Char(string = 'Nombre de la provincia')
	pais_id = fields.Many2one('res.country',"Pais")


	
	def name_get(self):
		res = []
		for record in self:
			name = record.name
			pais = record.pais_id.name
			tit = "%s/%s" % (name, pais)
			res.append((record.id, tit))
		return res

class rbs_institucion(models.Model):
	_name = 'rbs.institucion'

	_description = "Notaria juzgado o institucion Publica"
		
	name = fields.Char(string = 'Notaria juzgado o institucion Publica')
	canton_id = fields.Many2one('rbs.canton','Canton de la notaria', domain="[('provincia_id','=',provincia_id)]")
	provincia_id = fields.Many2one('rbs.provincia','Provincia de la notaria', domain="[('pais_id','=',pais_id)]")
	pais_id = fields.Many2one('res.country',"Pais")



class factura_invoice(models.Model):
	_inherit = 'account.invoice'
	propiedad_id = fields.Many2one('rbs.documento.propiedad', string='Documento de ropiedad')
