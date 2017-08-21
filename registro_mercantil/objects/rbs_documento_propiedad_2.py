# -*- coding: utf-8 -*-
#!/usr/bin/env python
from dateutil import parser
from openerp import models, fields, api, _
from openerp.osv import osv



class rbs_documento_propiedad(models.Model):
	_name ="rbs.documento.propiedad"
	_description = "Documento de la Propiedad"
	#name= field.Char('Nombre')

	#Encabezado
	anio_id = fields.Many2one('rbs.anio', string ='Año',required = True)
	libro_id = fields.Many2one('rbs.libro', string ='Libro' ,required = True)

	tipo_libro_propiedad_id = fields.Many2one(related="libro_id.tipo_libro_propiedad_id",string='Tipo de Libro P')
	# reg_acto_contrato = fields.Selection([
 #            ('ACTO','ACTO'),
 #            ('CONTRATO','CONTRATO'),
 #        ],string ='Registra Acto/Contrato')
	tipo_tramite_id = fields.Many2one('rbs.tipo.tramite',string ='Tipo de tramite', required = True)
	# tipo_libro = fields.Char (string='Tipo Libro', required = True)
	tramite_id = fields.Many2one('rbs.tramite.propiedad',string='Tramite', required= True)
	tomo_id = fields.Many2one("rbs.tomo", string ='Tomo', required = True)
	observacion = fields.Char(string='Observación')
	foleo_desde = fields.Integer(string='Desde', required = True)
	foleo_hasta = fields.Integer (string='Hasta', required = True)
	
   #########Informacion de la inscripcion

	repertorio = fields.Char (string='Repertorio', required = True)
	fecha_repertorio = fields.Datetime (string='Fecha Repertorio')
	numero_inscripcion = fields.Integer(string = 'Numero de Inscripcion' , required = True)
	fecha_inscripcion = fields.Datetime(string = 'Fecha de Inscripcion' )
	cuantia_unidad = fields.Selection([
            ('SUCRE','SUCRE'),
            ('DOLAR','DOLAR'),
        ],string ='Unidad Monetaria' )
	
	
	
	fecha_const_gravamen = fields.Datetime (string='Fecha Const Gravamen/Limitacion')
	fecha_cancel_gravamen = fields.Datetime (string='Fecha Const Gravamen/Limitación')
	provincia_notaria_id = fields.Many2one('rbs.provincia', string ='Provincia de la notaria, Juzgado o institucion publica', required = True)
	canton_notaria_id = fields.Many2one('rbs.canton', string ='Canton de la Notaria', required = True)
	notaria_id = fields.Many2one('rbs.institucion',string ='Nombre Notaria o juzgado')
	expensas = fields.Selection([
            ('CERTIFICADO','CERTIFICADO'),
            ('DECLARACION','DECLARACION'),
        ],string ='Expensas')
	fecha_escritura = fields.Datetime(string = 'Fecha Escritura')
	numero_acuerdo_ministerial = fields.Char("Numero de acuerdo Ministerial")
	fecha_adjudicion = fields.Datetime(string = 'Fecha de la Adjudicacion')
	tipo_acto_contrato = fields.Many2many('rbs.tipo.acto.contrato',relation="propiedad_tipo_acto_contrato_rel",string = 'Tipo de acto o contrato')
	fecha_insi_bienes = fields.Datetime(string = 'Fecha judicial/acta notarial')

	cuantia_valor = fields.Char(string ='Cuantia' )
   #


	parte_ids = fields.One2many('rbs.parte','documento_propiedad_id',string = 'Partes')
	parte_bien_ids = fields.One2many('rbs.parte.bien.rel','documento_propiedad_id','Asignacion de Bienes')
	bien_ids = fields.One2many('rbs.bien','documento_propiedad_id',string ='Bienes')
	bien_auxiliar_ids = fields.One2many('rbs.bienauxiliar','documento_propiedad_id',string ='Bienes')
	alicuota_ids = fields.One2many('rbs.bien.alicuota','documento_propiedad_id',string = 'Alicuotas')
	# parte_ids = fields.Many2many('rbs.parte',relation="propiedad_parte_rel",string = 'Partes')




	# genera_gravamen_limitacion = fields.Selection([
	#         ('SI','SI'),
	#         ('NO','NO'),
	#     ],string ='Genera Gravamen/Limitacion')	
	gravamen_limitacion = fields.Boolean(string ='Gravamen o limitacion')
	tipo_gravamen_ids = fields.One2many('rbs.gravamen','documento_propiedad_gravamen_id',string = 'Tipo Gravamen/Limitación')
	genera_gravamen_limitacion = fields.Boolean(string ='Genera gravamen o limitacion')
	genera_tipo_gravamen_ids = fields.One2many('rbs.gravamen','documento_propiedad_genera_gravamen_id',string = 'Tipo Gravamen/Limitación')
	identificacion_unica = fields.Char(string = 'Identificador',compute='_compute_upper',store = True)
	# ubicacion_dato_id = fields.Many2one('rbs.ubicacion.dato', string ='Ubicacion del Dato', required = True)


	#Categoria Datos Registrales
	marginacion_ids = fields.One2many('rbs.marginacion','documento_propiedad_id',string ='Marginaciones')
	# anio_tramite_origi_id = fields.Many2one('rbs.anio', string ='Año',required = True)
	# libro_tramite_origi_id = fields.Many2one('rbs.libro', string ='Nombre Acto/Contrato' ,required = True)
	# marginacion_tramite_origi_id = fields.Many2one('rbs.documento.propiedad',string='Marginacion Trámite')

	# modificacion_fuente = fields.Datetime(string = 'Fecha modificacion de la fuente' )
	# canton_registro_id = fields.Many2one('rbs.canton', string ='Canton Registro Propiedad', required = True)
	

	# Fin categoría

	# Datos Escritura
	# Fin categoria
	# Categoria Posesion Efectiva
	causante = fields.Char (string='Causante')
	fecha_defuncion = fields.Datetime (string='Fecha Defunción')
	conyuge_sobreviviente = fields.Char (string='Cónyuge Sobreviviente')
	heredero_ids = fields.One2many('rbs.heredero','documento_propiedad_id',string = 'Herederos')
	
	
	juicio_numero = fields.Integer(string ='Numero del juicio')
	# estado_inscripcion_id = fields.Many2one('rbs.estado.inscripcion', string ='Estado de la Inscripcion', required = True)
	
	state = fields.Selection([
			('borrador','Borrador'),
            ('activo','Activo'),
            ('sustituido','Sustituido'),
        ], 'state',default='borrador', readonly=True)
	
	


	
	#filedata = fields.Binary('Archivo',filters='*.pdf')
	#filename = fields.Char('Nombre de archivo', default="pdf")
	filedata_id = fields.Many2one('rbs.pdf')
	filedata = fields.Binary(related='filedata_id.filedata',filters='*.pdf')
	esPesado = fields.Boolean(related='filedata_id.esPesado',string = '¿Es Pesado?')
	rutaFTP = fields.Char(related='filedata_id.rutaFTP', string = 'Escriba la ruta del Archivo')

	factura_ids = fields.One2many('account.invoice', 'propiedad_id', string= 'Factura')

	# def myonchange(self,cr,uid,ids,context=None):
	# 	return
	@api.onchange('parte_ids')
	def onchange_parte_ids(self):

		for parte in self.parte_ids:
			nombres = parte.razon_social or parte.nombres
			r = [x for x in self.parte_bien_ids if x.parte == nombres]
			if r:
				continue
			print nombres+"------------"
			bien_auxiliar_ids_num=[]
			for bienauxiliar in self.bien_auxiliar_ids:
				bien_auxiliar_ids_num.append(bienauxiliar.id)
			self.parte_bien_ids |= self.env['rbs.parte.bien.rel'].create({
				'parte':parte.razon_social or parte.nombres,
				'bienauxiliar_ids':[(6, 0, bien_auxiliar_ids_num)]})
		# parte_bien_ids_num = []
		# for parte_bien in self.parte_bien_ids:

		# 	nombres = parte_bien.parte
		# 	r = [x for x in self.parte_ids if (x.razon_social or x.nombres) == nombres]
		# 	if r:
		# 		parte_bien_ids_num.append(parte_bien.id)
		# 		continue

		# 	self.parte_bien_ids =[(6,0,parte_bien_ids_num)]

		# 	print "hay que quitarlo"+nombres+" - "+str(parte_bien.id)
		# # self.parte_bien_ids=None
		# 	# parte_bien = None
		# self.write({'parte_bien_ids':[(6,0,parte_bien_ids_num)]})
		return
	@api.onchange('bien_ids')
	def onchange_bien_ids(self):
		# print "OnChange("
		# algoritmo para detectar un cambio en bien_ids.numero_predial
		self.alicuota_ids = None
		band1=False
		for bien in self.bien_ids:
			band2 = False
			for x in self.bien_auxiliar_ids:
				print x.name + " - " +bien.numero_predial+"\n"
				if x.name == bien.numero_predial:
					band2 = True
					print x.name + " , " +bien.numero_predial+"Son iguales"

			if not band2:
				band1 = True
		print "OnChange("+str(band1)+")"

		if band1: # Si hubo un cambio se actualiza todos los registros de parte_bien_ids
			self.bien_auxiliar_ids = None
			bien_auxiliar_ids_num=[]
			for bien in self.bien_ids:
				b = self.env['rbs.bienauxiliar'].create({'name':bien.numero_predial})
				bien_auxiliar_ids_num.append(b.id)
			print bien_auxiliar_ids_num
			self.bien_auxiliar_ids = [(6,0,bien_auxiliar_ids_num)]

			for parte_bien in self.parte_bien_ids:
				parte_bien.bienauxiliar_ids = None
				parte_bien.bienauxiliar_ids = [(6,0,bien_auxiliar_ids_num)]


			# self.alicuota_ids |= self.env['rbs.bien.alicuota'].create({'name':bien.numero_predial})
		# for parte in self.parte_ids:
		# 	nombres = parte.razon_social or parte.nombres
		# 	r = [x for x in self.parte_bien_ids if x.parte == nombres]
		# 	if r:
		# 		continue
		# 	print nombres
		# 	bien_auxiliar_ids_num=[]
		# 	for bienauxiliar in self.bien_auxiliar_ids:
		# 		bien_auxiliar_ids_num.append(bienauxiliar.id)
		# 	self.parte_bien_ids |= self.env['rbs.parte.bien.rel'].create({
		# 		'parte':parte.razon_social or parte.nombres,
		# 		'bienauxiliar_ids':[(6, 0, bien_auxiliar_ids_num)]})
		# parte_bien_ids_num = []
		
		return

	def _getUltimoAnio(self, cr, uid, context=None):
		acta_id = self.pool.get("rbs.documento.propiedad").search(cr, uid,  [], limit=1, order='id desc')
		anio = self.pool.get("rbs.documento.propiedad").browse(cr,uid,acta_id,context = None).anio_id.id
		return anio
	def _getUltimoLibro(self, cr, uid, context=None):
		acta_id = self.pool.get("rbs.documento.propiedad").search(cr, uid,  [], limit=1, order='id desc')
		libro = self.pool.get("rbs.documento.propiedad").browse(cr,uid,acta_id,context = None).libro_id.id
		return libro
	def _getUltimoTomo(self, cr, uid, context=None):
		acta_id = self.pool.get("rbs.documento.propiedad").search(cr, uid,  [], limit=1, order='id desc')
		tomo = self.pool.get("rbs.documento.propiedad").browse(cr,uid,acta_id,context = None).tomo_id.id
		return tomo

	def _create_pdf(self, cr, uid, context=None):
		return self.pool.get("rbs.pdf").create(cr, uid,{},context=None)

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
		propiedad_id = self.pool.get('rbs.documento.propiedad').search(cr, uid, [('numero_inscripcion','=',inscripcion_num),('libro_id','=',libro_id)])
		propiedad = self.pool.get('rbs.documento.propiedad').browse(cr,uid,propiedad_id,context = None)
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
				result['filedata_id'] = self._create_pdf(cr, uid, context=None)

				
				
		except:
			pass
		
		return { 'value':result, }\

class rbs_gravamen(models.Model):
	_name ='rbs.gravamen'
	name = fields.Many2one('rbs.tipo.gravamen',string='Tipo Gravamen/Limitación')
	documento_propiedad_gravamen_id = fields.Many2one('rbs.documento.propiedad',"Documento de Propiedad")
	documento_propiedad_genera_gravamen_id = fields.Many2one('rbs.documento.propiedad',"Documento de Propiedad")
class rbs_marginacion(models.Model):
	_name = 'rbs.marginacion'
	anio_tramite_origi_id = fields.Many2one('rbs.anio', string ='Año',required = True)
	libro_tramite_origi_id = fields.Many2one('rbs.libro', string ='Nombre Acto/Contrato' ,required = True)
	marginacion_tramite_origi_id = fields.Many2one('rbs.documento.propiedad',string='Marginacion Trámite',required = True)
	documento_propiedad_id = fields.Many2one('rbs.documento.propiedad',"Documento de Propiedad")
class rbs_heredero(models.Model):
	_name = 'rbs.heredero'
	name =  fields.Char (string='Herederos')
	documento_propiedad_id = fields.Many2one('rbs.documento.propiedad',"Documento de Propiedad")

class rbs_parte_bien_rel(models.Model):
	_name = 'rbs.parte.bien.rel'
	_description = "Parte Bien"
	parte = fields.Char("Parte")
	bienauxiliar_ids = fields.Many2many('rbs.bienauxiliar',string = "Bienes")
	documento_propiedad_id = fields.Many2one('rbs.documento.propiedad',"Documento de Propiedad")

class rbs_bien_alicuota(models.Model):
	_name = 'rbs.bien.alicuota'
	_description = "Bien Alicuota"
	name = fields.Char("Bien")
	alicuota_ids = fields.One2many('rbs.alicuota','bien_alicuota_id',"Porcentajes")
	documento_propiedad_id = fields.Many2one('rbs.documento.propiedad',"Documento de Propiedad")
class rbs_alicuota(models.Model):
	_name = 'rbs.alicuota'
	_description = "Alicuotas"
	name = fields.Char("Descripcion")
	porcentaje = fields.Integer('Porcentaje')
	bien_alicuota_id = fields.Many2one('rbs.bien.alicuota',"Bien alicuota")
class rbs_bienauxiliar(models.Model):
	_name = 'rbs.bienauxiliar'
	_description = "Modelo auxiliar utilizado para relacionar partes con bienes"
	name = fields.Char("Bien")
	documento_propiedad_id = fields.Many2one('rbs.documento.propiedad',"Documento de Propiedad")
class rbs_parte(models.Model):
	_name = 'rbs.parte'
	_description = "Parte"
	documento_propiedad_id = fields.Many2one('rbs.documento.propiedad',"Documento de Propiedad")
	tipo_persona = fields.Selection([
            ('NATURAL','NATURAL'),
            ('JURIDICA','JURIDICA'),
        ],string ='Tipo de Persona')

	razon_social = fields.Char(string = 'Razon Social')
	persona_id = fields.Many2one('rbs.persona', string ='Compareciente(n)')
	nombres = fields.Char(string = 'Nombres del Compareciente')
	apellidos = fields.Char(string = 'Apellidos del Compareciente')
	
	tipo_interviniente_id = fields.Many2one('rbs.tipo.interviniente', string ='Tipo de Interviniente')
	calidad_compareciente_id = fields.Many2one('rbs.calidad.compareciente', string ='Calidad de Compareciente')
	tipo_documento = fields.Selection([
            ('CEDULA','CEDULA'),
            ('RUC','RUC'),
            ('PASAPORTE','PASAPORTE'),
        ], string = 'Tipo Documento')
	cedula = fields.Char(string = 'Cedula del Compareciente')
	estado_civil = fields.Selection([
            ('CASADO','CASADO'),
            ('DIVORCIADO','DIVORCIADO'),
            ('NO APLICA','NO APLICA'),
            ('SOLTERO','SOLTERO'),
            ('UNION DE HECHO','UNION DE HECHO'),
            ('UNION LIBRE','UNION LIBRE'),
            ('VIUDO','VIUDO'),
        ], string = 'Estado Civil')
	num_identificacion_conyuge = fields.Char(string = 'Numero de Identificacion del cónyuge')
	nombres_conyuge = fields.Char(string = 'Nombres y apellidos del Cónyuge')
	separacion_bienes = fields.Boolean(string ='Separacion de Bienes')
	es_menor = fields.Boolean(string ='Es menor')
	tutor = fields.Char(string ='Tutor o curador')
	def name_get(self, cr, uid, ids, context=None):
		if context is None:
			context = {}
		res = []
		for record in self.browse(cr, uid, ids, context=context):
			razon_social = record.razon_social or ''
			nombres = record.nombres or ''
			# pais = record.pais_id.name
			tit = "%s%s" % (razon_social,nombres)
			res.append((record.id, tit))
		return res

class rbs_tipo_acto_contrato(models.Model):
	_name = 'rbs.tipo.acto.contrato'
	_description = "Tipos de acto/contrato"
	name = fields.Char(string = 'Nombre')
	is_acto = fields.Boolean(string = '¿Visible en acta?')
	is_contrato = fields.Boolean(string = '¿Visible en contrato?')

	tipo_acta_contrato_sel = fields.Selection([
            ('AMBOS','AMBOS'),
			('ACTO','ACTO'),
            ('CONTRATO','CONTRATO'),
        ],compute='get_tipo_acto_contrato_sel', string = "Tipo Contrato/Acta" , store=True)

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

class rbs_tipo_gravamen(models.Model):
	_name = 'rbs.tipo.gravamen'
	_description = "Tipos de gravamen"
	name = fields.Char(string = 'Nombre')
class rbs_bien(models.Model):
	_name = 'rbs.bien'
	_description = "Bien"

	documento_propiedad_id = fields.Many2one('rbs.documento.propiedad',"Documento de Propiedad")
	numero_predial = fields.Char(string = 'Numero Predial')
	# name = fields.Char(string = 'Clave Catastral')
	clave_catastral = fields.Char(string = 'Clave Catastral' )
	descripcion_bien= fields.Char(string ='Descripcion del Bien', required = True)
	descripcion_lindero = fields.Text(string = 'Descripcion del lindero', default='NORTE:    SUR:    ESTE:   OESTE:', required = True)
	

	provincia_id = fields.Many2one('rbs.provincia', string ='Provincia', required = True)
	canton_id = fields.Many2one('rbs.canton', string ='Canton del Inmueble', required = True)
	parroquia_id = fields.Many2one('rbs.parroquia',string ='Parroquia Inmueble', required = True)
	zona_id = fields.Many2one('rbs.zona', string ='Zona', required = True)
	
	ubicacion_geografica = fields.Selection([
            ('NORTE','NORTE'),
            ('SUR','SUR'),
            ('ESTE','ESTE'),
            ('OESTE','OESTE'),
            ('SUROESTE','SUROESTE'),
            ('SURESTE','SURESTE'),
            ('NOROESTE','NOROESTE'),
            ('NORESTE','NORESTE'),
        ],string = 'Ubicacion Geografica', default='NORTE', required = True)
	superficie_area_numero = fields.Integer(string = 'Superficie o Area')
	superficie_area_letras = fields.Char(string = 'Superficie o Area')
	es_propiedad_horizontal = fields.Boolean(String = 'Propiedad Horizontal')

	def name_get(self, cr, uid, ids, context=None):
		if context is None:
			context = {}
		res = []
		for record in self.browse(cr, uid, ids, context=context):
			numero_predial = record.numero_predial
			clave_catastral = record.clave_catastral
			# pais = record.pais_id.name
			tit = "%s/%s" % (numero_predial,clave_catastral)
			res.append((record.id, tit))
		return res
	# cuantia_valor = fields.Char(string ='Valor del bien' )
	# cuantia_unidad = fields.Selection([
 #            ('SUCRE','SUCRE'),
 #            ('DOLAR','DOLAR'),
 #        ],string ='Unidad Monetaria' )

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

	def name_get(self, cr, uid, ids, context=None):
		if context is None:
			context = {}
		res = []
		for record in self.browse(cr, uid, ids, context=context):
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

	def name_get(self, cr, uid, ids, context=None):
		if context is None:
			context = {}
		res = []
		for record in self.browse(cr, uid, ids, context=context):
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

	def name_get(self, cr, uid, ids, context=None):
		if context is None:
			context = {}
		res = []
		for record in self.browse(cr, uid, ids, context=context):
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
	propiedad_id = fields.Many2one('rbs.documento.propiedad', string='Propiedad')
