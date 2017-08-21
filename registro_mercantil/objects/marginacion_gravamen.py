# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
from openerp.osv import osv
class rbs_marginacion(models.Model):
	_name = 'rbs.marginacion'
	anio_tramite_origi_id = fields.Many2one('rbs.anio', string ='Año',required = True)
	libro_tramite_origi_id = fields.Many2one('rbs.libro', string ='Nombre Acto/Contrato' ,required = True)

	marginacion_propiedad_tramite_origi_id = fields.Many2one('rbs.documento.propiedad',string='Marginacion Trámite',required = True)
	documento_propiedad_id = fields.Many2one('rbs.documento.propiedad',"Documento de propiedad")
	
	marginacion_mercantil_tramite_origi_id = fields.Many2one('rbs.documento.mercantil',string='Marginacion Trámite',required = True)
	documento_mercantil_id = fields.Many2one('rbs.documento.mercantil',"Documento mercantil")

class rbs_gravamen(models.Model):
	_name ='rbs.gravamen'
	name = fields.Many2one('rbs.tipo.gravamen',string='Tipo Gravamen/Limitación')
	documento_propiedad_id = fields.Many2one('rbs.documento.propiedad',"Documento de Propiedad")
	documento_mercantil_id = fields.Many2one('rbs.documento.mercantil',"Documento de Propiedad")
	documento_propiedad_genera_gravamen_id = fields.Many2one('rbs.documento.propiedad',"Documento de Propiedad")

class rbs_tipo_gravamen(models.Model):
	_name = 'rbs.tipo.gravamen'
	_description = "Tipos de gravamen"
	name = fields.Char(string = 'Nombre')
