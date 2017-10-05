from openerp import models, fields, api, _
from openerp.osv import osv
from PIL import Image
import base64
import cStringIO

class rbs_contenedor(models.Model):
	_name="rbs.contenedor"
	_description=""

	name = fields.Char(string='Contenedor')
	imagenes_ids = fields.One2many("rbs.imagenes","contenedor_id","imagenes")

		


class rbs_imagenes(models.Model):
	_name="rbs.imagenes"
	_description=""
	_order = 'posicion asc'
	imagen = fields.Binary(string="Imagen")
	contenedor_id = fields.Many2one("rbs.contenedor", string="Contenedor de imagenes")
	posicion = fields.Integer("Posicion" , required = True)
	@api.one
	def actualizarImagen (self, binary, posicion):
		# raise osv.except_osv('Esto es un Mesaje!',"sada")
		return self.write({"imagen":binary,"posicion":posicion})
	
	@api.multi		
	def insertarImagen (self, contenedor_id,posicion):
		imagenes = self.search([['contenedor_id', '=', contenedor_id]])

		for l in imagenes:
			if l.posicion >=(posicion+1):
				l.posicion = l.posicion+1
		# self.create({"contenedor_id":contenedor_id,"posicion":posicion})
		buffer = cStringIO.StringIO()
		img = Image.new('RGB', (1000, 1400),(255,255,255))
		img.save(buffer, format="PNG")
		img_str = base64.b64encode(buffer.getvalue())
		# raise osv.except_osv('Esto es un Mesaje!',img_str)
		return self.create({"contenedor_id":contenedor_id,"posicion":posicion+1,"imagen":img_str}).id

	@api.one		
	def eliminarImagen (self):
		# imagenes = self.search([['contenedor_id', '=', contenedor_id]])
		
		
		contenedor_id = self.contenedor_id.id
		posicion = self.posicion
		self.unlink()

		imagenes = self.search([['contenedor_id', '=', contenedor_id]])

		for l in imagenes:
			if l.posicion >=(posicion+1):
				l.posicion = l.posicion-1
		


		return True
