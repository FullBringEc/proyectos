#!/usr/bin/env python
# -*- coding: utf-8 -*-
from openerp.osv import osv
from openerp import pooler, fields, api, models
from openerp.tools.translate import _
from openerp.exceptions import Warning



from time import time

class Bodega(models.Model):
	_name ="hrz.bodega"
	_description = "Bodega"
	name = fields.Char('Nombre Bodega')
	observacion = fields.Text('Observacion')
	responsable_id = fields.Many2one('res.users',string = 'Responsable')
	es_virtual = fields.Boolean('¿Es virtual?')
	esvirtual = fields.Boolean('¿Es virtual?', required=True)

	tipo = fields.Selection([
        ('transfer','Solo para transferencias'),
        ('ingress','Ingreso'),
        ('recipe','Receta'),
        ('assignment','Asignacion de equipos'),
        ('area','Area'),
        ], 
        string = 'Tipo', required=True)
	tipo_producto = fields.Selection([
        ('medicamento','Medicamento'),
        ('herramienta','Herramientas y Materiales de Mantenimiento'),
        ('material','Material'),
        #('no_medicamento','Herramientas equipos y materiales')
        ], string = 'Tipo de Producto')
	responsables_ids = fields.Many2many(
	    comodel_name='res.users',
	    inverse_name='bodega_ids',
	    string='Personas autorizadas para retirar e ingresar en esta bodega',
	)

	producto_ids = fields.One2many('hrz.bodega.producto', 'bodega_id', string='Lineas de productos')

	'''producto_ids = fields.Many2many(
	    comodel_name='hrz.producto',
	    inverse_name='bodega_ids',
	    string='Productos en esta bodega',
	    relation='hrz_bodega_producto',
	)
	'''

	@api.multi
	def unlink(self):
		for bodega in self:
			if len(bodega.producto_ids) != 0:
				raise Warning(_('No se puede borrar una bodega que tenga Productos almacenados'))
			if (bodega.producto_ids) == 0:
				raise Warning(_('No se puede borrar una bodega que tenga Productos almacenados 2 '))
		return super(Bodega, self).unlink()

	@api.onchange('name','observacion')
	def _uppercase(self):

		def upperField(field):
			if field != False:
				field = str(unicode(field).encode('utf-8')).upper()         
			return field
		self.observacion = upperField(self.observacion)
		self.name = upperField(self.name)

class BodegaProductoRel(models.Model):
	_name ="hrz.bodega.producto"
	_description = "Bodega por Producto"

	bodega_id = fields.Many2one('hrz.bodega',string = 'Bodega')
	producto_id = fields.Many2one('hrz.producto',string = 'Producto')

	existencia = fields.Integer('Existencia', compute = '_getPrecio')
	existencia_maxima = fields.Integer('Existencia maxima')
	existencia_minima = fields.Integer('Existencia minima')

	precio = fields.Float('Precio')

	fecha_caducidad = fields.Date('Fecha de Caducidad')
	fecha_elaboracion = fields.Date('Fecha de elaboracion')


	@api.one
	def _check_cantidad_maxima(self, cr, uid, ids, context=None):
		raise osv.except_osv('Advertencia', self.cantidad_maxima)

	_constraints = [
		(_check_cantidad_maxima, 'Error ! No puedes crear registros en donde la fecha fin sea menor a la fecha inicio del contrato ', ['existenciaexistencia'])
	]
    

	#@api.one
	#def _getPrecio():
	#	productoMove = self.env['hrz.producto.move'].search_count([['bodega_id', '=', self.Bodega_ingreso_id.id], ['producto_id', '=', line.producto_id.id]]) ==0:

	@api.one
	@api.depends('bodega_id','producto_id')
	def _getPrecio(self):
		productoMove = self.env['hrz.producto.move'].search([['bodega_id', '=', self.bodega_id.id], ['producto_id', '=', self.producto_id.id]])
		if len(productoMove)>0:
			self.existencia = sum(line.entra-line.sale for line in productoMove)
			self.precio = sum(line.precio_unitario for line in productoMove)/len(productoMove)
	_sql_constraints = [
	    ('productobodega_unique','unique(bodega_id,producto_id)','No puede haber el mismo producto mas de 1 vez en la misma bodega'),
	]


