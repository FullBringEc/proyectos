from openerp import models, fields, api, _

class rbs_imagenes(models.Model):
	_name="rbs.imagenes"
	_description=""

	imagen = fields.Binary(string="Imagen")
	contenedor_id = fields.Many2one("rbs.contenedor", string="Contenedor de imagenes")


class rbs_contenedor(models.Model):
	_name="rbs.contenedor"
	_description=""

	name = fields.char(string="Contenedor")