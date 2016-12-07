#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dateutil import parser
from openerp import models, fields, api, _
from openerp.osv import osv



class rbs_documento_mercantil_acta(models.Model):
	_name ="rbs.documento.mercantil.acta"
	_description = "Documento Mercantil de Acta"
	#name= field.Char('Nombre')

	anio_id = fields.Many2one('rbs.archivo.anio', string ='Año',required = True)
	libro_id = fields.Many2one('rbs.archivo.libro', string ='Libro' ,required = True)
	tomo_id = fields.Many2one("rbs.archivo.tomo", string ='Tomo', required = True)

	compania_id = fields.Many2one('rbs.compania', string ='Compania')
	compania_nombres = fields.Char(string = 'Nombres de la Compañia')
	compania_identificacion = fields.Char(string = 'Indentificacion de la Compañia')
	compania_especie_id = fields.Many2one('rbs.compania.especie', string ='Especie de Compañia')
	fecha_inscripcion = fields.Datetime(string = 'Fecha de Inscripcion', required = True )
	
	persona_id = fields.Many2one('rbs.persona', string ='Compareciente(n)')
	persona_nombres = fields.Char(string = 'Nombres del Compareciente')
	persona_apellidos = fields.Char(string = 'Apellidos del Compareciente')
	persona_cedula = fields.Char(string = 'Cedula del Compareciente')
	
	cargo_id = fields.Many2one('rbs.cargo', string ='Cargo')
	tipo_compareciente_id = fields.Many2one('rbs.tipo.compareciente.a', string ='Tipo de Compareciente')
	numero_inscripcion = fields.Char(string = 'Numero de Inscripcion', required = True )
	autoridad_emisora = fields.Char(string = 'Autoridad que emitio el Acta' )

	
	disposicion = fields.Char(string ='Disposicion')	
	fecha_disposicion = fields.Datetime(string = 'Fecha de Disposicion' )
	numero_Disposicion = fields.Char(string = 'Numero de Disposicion' )
	fecha_ecritura = fields.Datetime(string = 'Fecha de Escritura' , required = True)
	nombre_instancia_publica = fields.Char(string = 'Nombre de Instancia Publica')
	
	canton_id = fields.Many2one('rbs.canton', string ='Canton de Notaria', required = True)
	
	tipo_tramite_id = fields.Many2one('rbs.tipo.tramite', string ='Tipo de Tramite', required = True)
	
	ubicacion_dato_id = fields.Many2one('rbs.ubicacion.dato', string ='Ubicacion del Dato', required = True)
	
	fecha_ultima_modificacion = fields.Datetime(string = 'Ultima Modificacion de la Fuente' )
	
	
	estado_inscripcion_id = fields.Many2one('rbs.estado.inscripcion', string ='Estado de la Inscripcion', required = True)
	#filedata = fields.Binary('Archivo',filters='*.pdf')
	#filename = fields.Char( compute='_get_value', string = 'Nombre de archivo', default="Archivo.pdf")
	
	
	
	filedata_id = fields.Many2one('rbs.archivo.pdf')
	filedata = fields.Binary(related='filedata_id.filedata',filters='*.pdf')
	esPesado = fields.Boolean(related='filedata_id.esPesado',string = '¿Es Pesado?')
	rutaFTP = fields.Char(related='filedata_id.rutaFTP', string = 'Escriba la ruta del Archivo')

	#libro_tipo = fields.Selection(string='Tipo de Libro', related='libro_id.libro_tipo',store = True)

	identificacion_unica = fields.Char(string = 'Identificador Unico Sistema Remoto',compute='_compute_upper',store = True) 
	
	_defaults = {
        
    }

	def _getUltimoAnio(self, cr, uid, context=None):
		acta_id = self.pool.get("rbs.documento.mercantil.acta").search(cr, uid,  [], limit=1, order='id desc')
		anio = self.pool.get("rbs.documento.mercantil.acta").browse(cr,uid,acta_id,context = None).anio_id.id
		return anio
	def _getUltimoLibro(self, cr, uid, context=None):
		acta_id = self.pool.get("rbs.documento.mercantil.acta").search(cr, uid,  [], limit=1, order='id desc')
		libro = self.pool.get("rbs.documento.mercantil.acta").browse(cr,uid,acta_id,context = None).libro_id.id
		return libro
	def _getUltimoTomo(self, cr, uid, context=None):
		acta_id = self.pool.get("rbs.documento.mercantil.acta").search(cr, uid,  [], limit=1, order='id desc')
		tomo = self.pool.get("rbs.documento.mercantil.acta").browse(cr,uid,acta_id,context = None).tomo_id.id
		return tomo
	def _getUltimoTomo(self, cr, uid, context=None):
		acta_id = self.pool.get("rbs.documento.mercantil.acta").search(cr, uid,  [], limit=1, order='id desc')
		tomo = self.pool.get("rbs.documento.mercantil.acta").browse(cr,uid,acta_id,context = None).tomo_id.id
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

	

	@api.depends('ubicacion_dato_id','persona_cedula','numero_inscripcion')
	def _compute_upper(self):
		for rec in self:
			try:
				rec.identificacion_unica = '01'+rec.ubicacion_dato_id.name+rec.persona_cedula+rec.numero_inscripcion
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
				
		except:
			pass
		
		return { 'value':result, }
	
	def onchange_compania_id(self, cr, uid, ids, companiaid,context=None):
		compania_id = self.pool.get('rbs.compania').search(cr, uid, [('id','=',companiaid),])
		compania = self.pool.get('rbs.compania').browse(cr,uid,compania_id,context = None)
		result = {}
		try:
			if compania:
				try:
					if compania.compania_nombres:
						result['compania_nombres'] = self.codigoascii(compania.compania_nombres)
				except:
					pass
				try:
					if compania.name:
						result['compania_identificacion'] = str(compania.name)
				except: 
					pass
				try:
					if compania.compania_especie_id.id:
						result['compania_especie_id'] = compania.compania_especie_id.id
				except: 
				    pass
				
		except:
			pass
		
		return { 'value':result, }
	
	def onchange_inscripcion(self, cr, uid, ids, inscripcion_num,libro_id,context=None):
		acta_id = self.pool.get('rbs.documento.mercantil.acta').search(cr, uid, [('numero_inscripcion','=',inscripcion_num),('libro_id','=',libro_id)])
		acta = self.pool.get('rbs.documento.mercantil.acta').browse(cr,uid,acta_id,context = None)
		result = {}

		try:
		       			
			if acta:
				acta = acta[0]
				#raise osv.except_osv('Esto es un Mesaje!',establecimiento)
				try:
					if acta.fecha_inscripcion:
						result['fecha_inscripcion'] = str(acta.fecha_inscripcion)
					
				except:
					pass

				try:
					if acta.tomo_id:
						result['tomo_id'] = acta.tomo_id.id
				except:
					pass
				
				try:
					if acta.anio_id:
						result['anio_id'] = acta.anio_id.id
				except:
					pass
				
				try:
					if acta.libro_id:
						result['libro_id'] = acta.libro_id.id
				except:
					pass
				 
				
				 
				
				
				try:
					if acta.numero_inscripcion:
						result['numero_inscripcion'] = acta.numero_inscripcion.id
				except:
					pass

				try:
					if acta.autoridad_emisora:
						result['autoridad_emisora'] = self.codigoascii(acta.autoridad_emisora)
				except:
					pass

				try:
					if acta.disposicion:
						result['disposicion'] = self.codigoascii(acta.disposicion)
				except:
					pass
				try:
					if acta.fecha_disposicion:
						result['fecha_disposicion'] = str(acta.fecha_disposicion)
				except:
					pass
				 
				
				try:
					if acta.numero_Disposicion:
						result['numero_Disposicion'] = str(acta.numero_Disposicion)
				except:
					pass
				
				try:
					if acta.fecha_ecritura:
						result['fecha_ecritura'] = str(acta.fecha_ecritura)
				except:
					pass
				 
				try:
					if acta.nombre_instancia_publica:
						result['nombre_instancia_publica'] = self.codigoascii(acta.nombre_instancia_publica)
				except:
					pass

				try:
					if acta.canton_id:
						result['canton_id'] = acta.canton_id.id

				except: 
					pass

				try:
					if acta.tipo_tramite_id:
						result['tipo_tramite_id'] = acta.tipo_tramite_id.id

				except: 
					pass
				 
				try:
					if acta.fecha_ultima_modificacion:
						result['fecha_ultima_modificacion'] = str(acta.fecha_ultima_modificacion)
				except:
					pass

				  

				try:
					if acta.estado_inscripcion_id:
						result['estado_inscripcion_id'] = acta.estado_inscripcion_id.id

				except: 
					pass

				try:
					if acta.ubicacion_dato_id:
						result['ubicacion_dato_id'] = acta.ubicacion_dato_id.id

				except: 
					pass

				try:
					if acta.canton_id:
						result['canton_id'] = acta.canton_id.id

				except: 
					pass
				
				try:
					if acta.filedata_id:
						result['filedata_id'] = acta.filedata_id.id

				except: 
					pass

				
			if not acta:
				result['filedata_id'] = self._create_pdf(cr, uid, context=None)

				
				
		except:
			pass
		
		return { 'value':result, }


class rbs_compania(models.Model):
	_name ="rbs.compania"
	_description = "Compania"
	
	
	compania_nombres = fields.Char(string = 'Nombre de la Compania', required=True)
	name = fields.Char(string = 'Indentificacion de la Compania', required = True)
	compania_especie_id = fields.Many2one('rbs.compania.especie', string ='Especie de Compania', required = True)
	_sql_constraints = [
        ('compania_identificacion_uniq', 'unique(name)',
            'La identificacion debe ser unica por Compania'),
    ]
	_order = 'compania_nombres'
	#_rec_name = 'compania_identificacion'
	
	
class rbs_tipo_compareciente_a(models.Model):
	_name = "rbs.tipo.compareciente.a"
	_description = "Tipo de Compareciente"
	
	name = fields.Char(string = 'Tipo Del Compareciente')
	
class rbs_compania_especie(models.Model):
	_name = "rbs.compania.especie"
	_description = "Especie de Compania"
	
	name = fields.Char(string = 'Especie')
	
class rbs_cargo(models.Model):
	_name = 'rbs.cargo'
	_description = "Tipo de Cargo"
	
	name = fields.Char(string = 'Tipo De Cargo')

class rbs_canton(models.Model):
	_name = 'rbs.canton'
	_description = "Nombre del canton"
	
	name = fields.Char(string = 'Nombre del canton')
	
class rbs_tipo_tramite(models.Model):
	_name = 'rbs.tipo.tramite'
	_description = "Tipo de tramite"
	
	name = fields.Char(string = 'Tipo De tramite')
	
class rbs_ubicacion_dato(models.Model):
	_name = 'rbs.ubicacion.dato'
	_description = "Ubicacion de dato"
	
	name = fields.Char(string = 'Ubicacion del Dato')

class rbs_estado_inscripcion(models.Model):
	_name = 'rbs.estado.inscripcion'
	_description = "Estado de Inscripion"
	
	name = fields.Char(string = 'Estado de Inscripion')
	
			

	


	
