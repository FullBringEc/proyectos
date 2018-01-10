# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
# from openerp.osv import osv


class rbs_compania_reg(models.Model):
	_name = 'res.company'
	_inherit = 'res.company'
	registrador_nombre = fields.Char(string = 'Nombre Registrador')
	registrador_fecha_ingreso = fields.Datetime(string = 'Fecha de Ingreso')