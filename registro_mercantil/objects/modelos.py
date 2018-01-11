#!/usr/bin/env python
# -*- coding: utf-8 -*-

from openerp import models, fields, api, _
from openerp.osv import osv



class rbs_anio(models.Model):
	_name ="rbs.anio"
	_description = "Anio"
	name = fields.Integer(string = 'Año', required=True)
	libro_mercantil_line = fields.One2many('rbs.libro', 'anio_id', string='Lineas de Libro m',domain=[('libro_tipo','=','mercantil')])
	libro_propiedad_line = fields.One2many('rbs.libro', 'anio_id', string='Lineas de Libro p',domain=[('libro_tipo','=','propiedad')])
	libro_acta_line = fields.One2many('rbs.libro', 'anio_id', string='Lineas de Libro a',domain=[('libro_tipo','=','acta')])
	state = fields.Selection([
            ('open','Abierto'),
            ('close','Validado'),
            
        ], 'state', default= "open", readonly=True)
	# _defaults = {
	# 	'state': 'open',
	# }


	_sql_constraints = [
        ('anio_name_uniq', 'unique(name)',
            'Ha duplicado el Año'),
    ]

	@api.multi
	def validarAnio(self):
		self.state = 'close'
		return True

class rbs_libro(models.Model):
	_name ="rbs.libro"
	_description = "Libros"
	name = fields.Char(string = 'Nombre del Libro', required=True)
	anio_id = fields.Many2one('rbs.anio', string ='Año')
	libro_tipo = fields.Selection([
            ('propiedad','Libro de Propiedad'),
            ('mercantil','Libro Mercantil'),
            # ('acta','Libro de Acta'),
        ], string='Tipo Propiedad/Mercantil')
	tomo_line = fields.One2many('rbs.tomo', 'libro_id', string='Lineas de Tomo')
	state = fields.Selection([
            ('open','Abierto'),
            ('close','Validado'),
            
        ], 'state', default= "open" , readonly=True)

	tipo_libro_propiedad_id = fields.Many2one('rbs.tipo.libro.propiedad', string='Tipo de Libro P')
	tipo_libro_mercantil_id = fields.Many2one('rbs.tipo.libro.mercantil', string='Tipo de Libro M')
	# es_propiedad = fields.Boolean(string = "Es propiedad", compute="domain_compute_def", help= "artificio para el dominio del tipo libro")
	# es_mercantil = fields.Boolean(string = "Es mercantil", compute="domain_compute_def", help= "artificio para el dominio del tipo libro")
	_defaults = {
   		'anio_id': lambda self, cr, uid, context: context.get('anio_id', False),
		'libro_tipo': lambda self, cr, uid, context: context.get('libro_tipo', False),
		}
	_sql_constraints = [
        ('anio_id_name_uniq', 'unique(anio_id,name)',
            'El libro debe ser unico por Año'),
    ]
	@api.multi
	def validarLibro(self):
		self.state = 'close'
		return True

class rbs_tomo(models.Model):
	_name ="rbs.tomo"
	_description = "Tomos"
	name = fields.Integer(string = 'Nombre del Tomo',required=True)
	
	libro_id = fields.Many2one('rbs.libro', string ='Libro')
	libro_tipo = fields.Selection(string='Tipo de Libro', related='libro_id.libro_tipo',store = True)
	anio_id = fields.Many2one(string='Año', related='libro_id.anio_id',store = True )
	# acta_line = fields.One2many('rbs.documento.mercantil.acta', 'tomo_id', string='Lineas de Registro de Acta')
	mercantil_line = fields.One2many('rbs.documento.mercantil', 'tomo_id', string='Lineas de Registro Vehicular')
	propiedad_line = fields.One2many('rbs.documento.propiedad', 'tomo_id', string='Lineas de Registro Propiedad')
	_defaults = {
   		'libro_id': lambda self, cr, uid, context: context.get('libro_id', False),
		}
	_sql_constraints = [
        ('tomo_name_uniq', 'unique(name,libro_id)',
            'El nombre del tomo debe ser unico por Libro'),
    ]
# class rbs_tipo_libro_tramite_propiedad_rel(models.Model):
# 	_name ="rbs.tipo.libro.tramite.propiedad.rel"
# 	_description = "Relacion entre tipo de libro y tramite para pripiedad"
class rbs_tramite_propiedad(models.Model):
	_name ="rbs.tramite.propiedad"
	_description = "Tramite propiedad"
	name = fields.Char(string = 'Tramite')
	# es_mercantil = fields.Boolean(string = '¿Es Mercantil?')
	# es_propiedad = fields.Boolean(string = '¿Es Propiedad?')

	tipo_libro_propiedad_ids = fields.Many2many(comodel_name='rbs.tipo.libro.propiedad', relation='rbs_tipo_libro_tramite_propiedad_rel', column1='tramite_id', column2='tipo_libro_id', string='Tipos de Libros Permitidos')
	
	
class rbs_tipo_libro_propiedad(models.Model):
	_name ="rbs.tipo.libro.propiedad"
	_description = "Tipo de libro propiedad"
	name = fields.Char(string = 'Tipo de libro')
	# es_mercantil = fields.Boolean(string = '¿Es Mercantil?')
	# es_propiedad = fields.Boolean(string = '¿Es Propiedad?')

	tramite_propiedad_ids = fields.Many2many(comodel_name='rbs.tramite.propiedad', relation='rbs_tipo_libro_tramite_propiedad_rel', column1='tipo_libro_id', column2='tramite_id', string='Tramites Permitidos')

class rbs_tramite_mercantil(models.Model):
	_name ="rbs.tramite.mercantil"
	_description = "Tramite mercantil"
	name = fields.Char(string = 'Tramite')
	# es_mercantil = fields.Boolean(string = '¿Es Mercantil?')
	# es_propiedad = fields.Boolean(string = '¿Es Propiedad?')

	tipo_libro_mercantil_ids = fields.Many2many(comodel_name='rbs.tipo.libro.mercantil', relation='rbs_tipo_libro_tramite_mercantil_rel', column1='tramite_id', column2='tipo_libro_id', string='Tipos de Libros Permitidos')
	
	
class rbs_tipo_libro_mercantil(models.Model):
	_name ="rbs.tipo.libro.mercantil"
	_description = "Tipo de libro mercantil"
	name = fields.Char(string = 'Tipo de libro')
	# es_mercantil = fields.Boolean(string = '¿Es Mercantil?')
	# es_propiedad = fields.Boolean(string = '¿Es Propiedad?')

	tramite_mercantil_ids = fields.Many2many(comodel_name='rbs.tramite.mercantil', relation='rbs_tipo_libro_tramite_mercantil_rel', column1='tipo_libro_id', column2='tramite_id', string='Tramites Permitidos')


class rbs_tipo_tramite(models.Model):
	_name ="rbs.tipo.tramite"
	_description = "Tipo de tramite"
	name = fields.Char(string = 'Tipo de tramite')

class rbs_nombramiento_mercantil(models.Model):
	_name ="rbs.nombramiento.mercantil"
	_description = "Nombramiento mercantil"
	name = fields.Char(string = 'Nombramiento')

class rbs_pdf(models.Model):
	_name ="rbs.pdf"
	_description = "pdf"
	filedata = fields.Binary(string = 'Archivo',filters='*.pdf')
	esPesado = fields.Boolean(string = '¿Es Pesado?')
	rutaFTP = fields.Char(string = 'Escriba la ruta del Archivo')
	