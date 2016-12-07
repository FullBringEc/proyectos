#!/usr/bin/env python
# -*- coding: utf-8 -*-

from openerp import models, fields, api, _
from openerp.osv import osv



class rbs_archivo_anio(models.Model):
	_name ="rbs.archivo.anio"
	_description = "Anio"
	name = fields.Integer(string = 'Año', required=True)
	libro_mercantil_line = fields.One2many('rbs.archivo.libro', 'anio_id', string='Lineas de Libro m',domain=[('libro_tipo','=','mercantil')])
	libro_propiedad_line = fields.One2many('rbs.archivo.libro', 'anio_id', string='Lineas de Libro p',domain=[('libro_tipo','=','propiedad')])
	libro_acta_line = fields.One2many('rbs.archivo.libro', 'anio_id', string='Lineas de Libro a',domain=[('libro_tipo','=','acta')])
	state = fields.Selection([
            ('open','Abierto'),
            ('close','Validado'),
            
        ], 'state', readonly=True)
	_defaults = {
		'state': 'open',
	}


	_sql_constraints = [
        ('anio_name_uniq', 'unique(name)',
            'Ha duplicado el Año'),
    ]

	@api.multi
	def validarAnio(self):
		self.state = 'close'
		return True

class rbs_archivo_libro(models.Model):
	_name ="rbs.archivo.libro"
	_description = "Libros"
	name = fields.Char(string = 'Nombre del Libro', required=True)
	anio_id = fields.Many2one('rbs.archivo.anio', string ='Año')
	libro_tipo = fields.Selection([
            ('propiedad','Libro de Propiedad'),
            ('mercantil','Libro Mercantil'),
            ('acta','Libro de Acta'),
        ], string='Tipo de Libros')
	tomo_line = fields.One2many('rbs.archivo.tomo', 'libro_id', string='Lineas de Tomo')
	state = fields.Selection([
            ('open','Abierto'),
            ('close','Validado'),
            
        ], 'state', readonly=True)
		
	
	_defaults = {
   		'anio_id': lambda self, cr, uid, context: context.get('anio_id', False),
		'libro_tipo': lambda self, cr, uid, context: context.get('libro_tipo', False),
		'state': 'open',}
	_sql_constraints = [
        ('anio_id_name_uniq', 'unique(anio_id,name)',
            'El libro debe ser unico por Año'),
    ]
	@api.multi
	def validarLibro(self):
		self.state = 'close'
		return True
	
class rbs_archivo_tomo(models.Model):
	_name ="rbs.archivo.tomo"
	_description = "Tomos"
	name = fields.Integer(string = 'Nombre del Tomo',required=True)
	
	libro_id = fields.Many2one('rbs.archivo.libro', string ='Libro')
	libro_tipo = fields.Selection(string='Tipo de Libro', related='libro_id.libro_tipo',store = True)
	anio_id = fields.Many2one(string='Año', related='libro_id.anio_id',store = True )
	acta_line = fields.One2many('rbs.documento.mercantil.acta', 'tomo_id', string='Lineas de Registro de Acta')
	vehiculo_line = fields.One2many('rbs.documento.mercantil.vehiculo', 'tomo_id', string='Lineas de Registro Vehicular')
	propiedad_line = fields.One2many('rbs.documento.mercantil.propiedad', 'tomo_id', string='Lineas de Registro Propiedad')
	_defaults = {
   		'libro_id': lambda self, cr, uid, context: context.get('libro_id', False),
		}
	_sql_constraints = [
        ('tomo_name_uniq', 'unique(name,libro_id)',
            'El nombre del tomo debe ser unico por Libro'),
    ]
class rbs_archivo_pdf(models.Model):
	_name ="rbs.archivo.pdf"
	_description = "pdf"
	filedata = fields.Binary(string = 'Archivo',filters='*.pdf')
	esPesado = fields.Boolean(string = '¿Es Pesado?')
	rutaFTP = fields.Char(string = 'Escriba la ruta del Archivo')
	