from openerp import models, fields, api, _
from openerp.osv import osv


class rbs_contenedor(models.Model):
	_name="rbs.contenedor"
	_description=""

	name = fields.Char(string='Contenedor')
	imagenes_ids = fields.One2many("rbs.imagenes","contenedor_id","imagenes")

		


class rbs_imagenes(models.Model):
	_name="rbs.imagenes"
	_description=""

	imagen = fields.Binary(string="Imagen")
	contenedor_id = fields.Many2one("rbs.contenedor", string="Contenedor de imagenes")

	def actualizarImagen (self, cr, uid, id, binary):
		# raise osv.except_osv('Esto es un Mesaje!',"sada")
		return self.browse(cr, uid, id).write({"imagen":binary})