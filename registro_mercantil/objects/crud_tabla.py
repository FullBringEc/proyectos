# -*- coding: utf-8 -*-

from openerp import models, fields, api, _

class crud_ubicacion_dep(models.Model):
	_name ="crud.ubicacion.dep"
	_description = "Informacion especifica sobre la ubicacion de los departamentos"

	sector_ubicacionDep = fields.Char(string = 'Sector de Ubicacion del departamento')
	name = fields.Char(string = 'Direccion Ubicacion del departamento')
	ciudad_ubicacionDep = fields.Char(string = 'Ciudad de Ubicacion del departamento')


class crud_departamento(models.Model):
	_name ="crud.departamento"
	_description = "Informacion especifica del departamento"

	name = fields.Char(string = 'Nombre del departamento')
	crud_ubicacion_dep_id = fields.Many2one('crud.ubicacion.dep', string ='Ubicacion del departamento')
	

class crud_tipo_archivo(models.Model):
	_name = "crud.tipo.archivo"
	_description = "Informacion especifica de los tipos de Archivo"

	name = fields.Char(string = 'Nombre del Libro' )
	crud_departamento_id = fields.Many2one('crud.departamento', string='departamento del tipo de Archivo')	


class crud_ubicacion_arch(models.Model):
	_name ="crud.ubicacion.arch"
	_description = "Informacion especifica de la ubicacion de cada Archivo"

	caja_ubicacionArch = fields.Char(string = 'Caja donde se encuentra el Archivo')
	bandeja_ubicacionArch = fields.Char(string = 'Bandeja donde se encuentra el Archivo')
	name = fields.Char(string = 'Estante donde se encuentra el Archivo')


class crud_archivo(models.Model):
	_name = "crud.archivo"
	_description = "Informacion especifica de cada archivo"
	
	name = fields.Integer(string = 'Numero del Archivo' )
	fecha_archivo = fields.Date (string = 'Fecha del Archivo' )
	destino_archivo = fields.Char(string = 'Destino del Archivo' )
	asunto_archivo = fields.Char(string = 'Asunto del Archivo' )
	crud_tipo_archivo_id = fields.Many2one('crud.tipo.archivo', string = 'Tipo de archivo' )
	crud_ubicacion_arch_id = fields.Many2one('crud.ubicacion.arch', string = 'Ubicacion del archivo')
	filedata = fields.Binary('Texto',filters='*.pdf')
	comprobante_fname = fields.Char('Comp', default="libro.pdf")






	
