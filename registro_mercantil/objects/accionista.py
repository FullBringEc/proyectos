# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
from openerp.osv import osv

class rbs_accionista(models.Model):
	_name = 'rbs.accionista'
	_description = "Accionista"

	documento_mercantil_id = fields.Many2one('rbs.documento.mercantil',"Documento mercantil")
	accionista_nombre = fields.Char(string = 'Nombre del accionista', required = True)
	accionista_porcentaje_acciones = fields.Char(string = 'Porcentaje en acciones o participaciones', required = True)
	accionista_valor_accion = fields.Char(string = 'Valor de acciones o partipaciones', required = True)