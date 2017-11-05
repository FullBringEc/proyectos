# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
from openerp.osv import osv
from datetime import datetime
class rbs_tarea(models.Model):
	_name = 'rbs.tarea'
	_description = "Parte"
	# name = fields.Char("Parte")
	_rec_name = 'numero_tarea'
	@api.model
	def get_numero_tarea(self):
		# seq = self.env["ir.sequence"].get("numero_tarea")
		return self.env["ir.sequence"].get("numero_tarea")
	fecha_registro = fields.Datetime("Fecha del registro",default=datetime.now(), required = True)
	user_id = fields.Many2one('res.users', string="Asignado a", required = True)
	state = fields.Selection([
		('pendiente','Pendiente'),
		('por_firmar','Por firmar'),
		('por_entregar','Por entregar'),
		('done','Realizado'),
		], string="Estado de tarea",default='pendiente')


	tipo_servicio = fields.Selection([
		('inscripcion_propiedad','Inscripcion Propiedad'),
		('inscripcion_mercantil','Inscripcion Mercantil'),
		('certificacion_propiedad','Certificacion Propiedad'),
		('certificacion_mercantil','Certificacion Mercantil'),
		], string="Tipo de servicio", required = True)
	numero_tarea = fields.Char(string='Numero de tarea',default=get_numero_tarea, required = True)
	factura_id = fields.Many2one('account.invoice',string='Factura relacionada', required = True)
	cliente_factura_id = fields.Many2one(related="factura_id.partner_id",string='Cliente factura', required = True)
	propiedad_id = fields.Many2one('rbs.documento.propiedad',string='Documento de propiedad')
	mercantil_id = fields.Many2one('rbs.documento.mercantil',string='Documento mercantil')

	certificado_propiedad_id = fields.Many2one('rbs.certificado',string='Certificado de propiedad')
	certificado_mercantil_id = fields.Many2one('rbs.certificado',string='Certificado de propiedad')
	@api.multi
	def crear_inscripcion_propiedad(self):
		self.validar_usuario()
		if self.tipo_servicio == 'inscripcion_propiedad':
			self.propiedad_id = self.env['rbs.documento.propiedad'].create({})
			self.iniciar_tarea()
	

	@api.multi
	def crear_inscripcion_mercantil(self):
		self.validar_usuario()
		if  self.tipo_servicio == 'inscripcion_mercantil':
			self.mercantil_id = self.env['rbs.documento.mercantil'].create({})
			self.iniciar_tarea()

	@api.multi
	def crear_certificacion_propiedad(self):
		self.validar_usuario()
		if self.tipo_servicio == 'certificacion_propiedad':
			self.certificado_propiedad_id = self.env['rbs.certificado'].create({})
			self.iniciar_tarea()

	@api.multi
	def crear_certificacion_mercantil(self):
		self.validar_usuario()
		if self.tipo_servicio == 'certificacion_mercantil':
			self.certificado_mercantil_id = self.env['rbs.certificado'].create({})
			self.iniciar_tarea()
	@api.one
	def iniciar_tarea(self):
		self.write({'state':'por_firmar'})
	@api.one
	def firmar(self):
		self.write({'state':'por_entregar'})

	@api.one
	def entregar(self):
		self.write({'state':'done'})


	@api.one
	def validar_usuario(self):
		user_actual_id = self.env["res.users"].search( [('id','=',self._uid)], limit=1, order='id desc')
		group_hr_manager_id = self.env['ir.model.data'].get_object_reference('registro_mercantil', 'group_administrador')[1]
		if not (group_hr_manager_id in [g.id for g in user_actual_id.groups_id] or self._uid == self.user_id.id):
			raise osv.except_osv('Esto es un Mesaje!','Este documento no fue asignado a tu usuario ')	

class factura_invoice(models.Model):
	_inherit = 'account.invoice'
	tarea_ids = fields.One2many('rbs.tarea', 'factura_id', string='Tareas Generadas')
	@api.multi
	def invoice_validate(self):
		# raise osv.except_osv('Esto es un Mesaje!','Hola')
		for line in self.invoice_line:
			# if line.tipo_servicio == 'inscripcion_propiedad' or line.tipo_servicio == 'inscripcion_mercantil':
			if line.tipo_servicio:

				self.tarea_ids |= self.env['rbs.tarea'].create({'tipo_servicio':line.tipo_servicio,'user_id':line.user_id.id})
			# if line.tipo_servicio == 'certificacion_propiedad' or line.tipo_servicio == 'certificacion_mercantil':
				# self.tarea_ids |= self.env['rbs.tarea'].create({'tipo_servicio':line.tipo_servicio,'user_id':line.user_id.id})
		return super(factura_invoice, self).invoice_validate()
class account_invoice_line(models.Model):
	_inherit = "account.invoice.line"
	tipo_servicio = fields.Selection(related = "product_id.tipo_servicio")
	user_id = fields.Many2one('res.users', string="Asignado a",required=True) 

class product_template(models.Model):
	_inherit = "product.template"
	tipo_servicio = fields.Selection([
		('inscripcion_propiedad','Inscripcion Propiedad'),
		('inscripcion_mercantil','Inscripcion Mercantil'),
		('certificacion_propiedad','Certificacion Propiedad'),
		('certificacion_mercantil','Certificacion Mercantil'),
		], string="Tipo de servicio")
