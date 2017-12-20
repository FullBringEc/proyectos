
from openerp import models, fields, api, _
from io import BytesIO 
import base64
import pdfmod
class rbs_documento_propiedad(models.Model):
	_inherit ="rbs.documento.propiedad"
	def _create_pdf(self, context=None):
		return self.env["rbs.pdf"].create({})
	filedata_id = fields.Many2one('rbs.pdf' , default=_create_pdf)
	filedata = fields.Binary(related='filedata_id.filedata',filters='*.pdf')
	esPesado = fields.Boolean(related='filedata_id.esPesado',string = '100 mb')
	rutaFTP = fields.Char(related='filedata_id.rutaFTP', string = 'Ruta del Archivo')
	contenedor_id = fields.Many2one("rbs.contenedor", string="Contenedor")
	state_filedata = fields.Selection([
            ('empty','Vacio'),
            ('done','Listo'),
            ('error','Error'),
        ],default='empty',string ='Estado del archivo' )
	
	
	@api.one 
	def borrar_contenedor(self):
		self.contenedor_id = None

	@api.model
	def cron_procesar_pdfs(self):

		today = fields.Date.today()
		documento_propiedad_ids = self.with_context(cron=True).search([
		    ('state_filedata', '=', 'empty'),
		])
		return documento_propiedad_ids.procesar_pdf()
	@api.onchange('filedata')
	def onchange_filedata(self):
		self.state_filedata = 'empty'
		return

	@api.multi
	def procesar_pdf(self):
		for propiedad in self:
			print "-------------------------------funciono"
		# raise osv.except_osv('Esto es un Mesaje!',"repr(im.info)")

		# if self.filedata!= None and self.filedata != False  and self.anio_id and self.libro_id and self.tomo_id and (self.numero_inscripcion!=0):
		 	try:
		 		propiedad.borrar_contenedor()
		 		contenedor = self.env['rbs.contenedor'].create({'name': str(propiedad.anio_id.name) + str(propiedad.libro_id.name) + str(propiedad.tomo_id.name) + str(propiedad.numero_inscripcion) + str("propiedad")})
				filedataByte = BytesIO(base64.b64decode(propiedad.filedata))
				# print filedataByte
				pdfmod.pdfOrTiff2image(self,filedataByte,contenedor)
				propiedad.contenedor_id=contenedor.id
				propiedad.state_filedata = 'done'
				# raise osv.except_osv('Esto es un Mesaje!',"repr(im.sd)")
			except Exception as e:
				propiedad.state_filedata = 'error'
				print "------------------\n"
				print e
				print "------------------\n"
