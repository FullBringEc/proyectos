# -*- encoding: utf-8 -*-
########################################################################


from openerp.osv import osv
from openerp import models, fields as field, api
import base64
import datetime
from io import BytesIO
from docxtpl import DocxTemplate, RichText
from odoo.exceptions import UserError
import os


class rbs_certificado_mercantil(osv.osv):
    _name = 'rbs.certificado.mercantil'
    _rec_name = 'valor_busqueda'

    @api.multi
    def word_certificado(self):
        output = BytesIO()
        tmpl_path = os.path.join(os.path.dirname(__file__), 'Documentos/DocMercantil')
        tpl = DocxTemplate(tmpl_path+'/certificado.docx')

        resumen = []
        libro = {}

        for mercantil_line in self.mercantil_ids:

                detalle = {}
                detalle['libro'] = mercantil_line.libro_id.name
                detalle['acto'] = mercantil_line.tipo_tramite_id.name
                detalle['numero'] = RichText(str(mercantil_line.numero_inscripcion))
                detalle['finscrip'] = RichText(str(mercantil_line.fecha_inscripcion))
                detalle['finicial'] = RichText(str(mercantil_line.foleo_desde))
                detalle['ffinal'] = RichText(str(mercantil_line.foleo_hasta))
                resumen.append(detalle)

                if libro.has_key(mercantil_line.libro_id.name):
                    libro[mercantil_line.libro_id.name] = libro[mercantil_line.libro_id.name]+1
                else:
                    libro[mercantil_line.libro_id.name] = 1

        movimientos = []

        for clave in libro:

            detalle = {}
            l = clave
            ni = libro[clave]
            detalle['libro'] = l
            detalle['sumainscrp'] = RichText(str(ni))

            movimientos.append(detalle)
        usuario_actual = self.env['res.users'].search([('id', '=', self._uid)])[0]
        context = {
                    # 'campo' : RichText ('fecha'),
                    'resumen': resumen,
                    'ccatastral': RichText(str(self.valor_busqueda)),
                    'fapertura': RichText(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))),
                    # 'infmuni' : RichText (str (self.canton_notaria_id.name)),
                    # 'tpredio' : RichText (str (self.descripcion_bien)),
                    # 'parroquia' : RichText (str (self.parroquia_id.name)),
                    # 'lindero' : RichText (str (self.descripcion_lindero)),
                    'nombresoli': RichText(str(self.solicitante)),
                    'sesion': RichText(str(usuario_actual.name)),
                    'fechaactual': RichText(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))),
                    'movimientos': movimientos,

                }

        tpl.render(context)
        tpl.save(output)

        self.write({'dataWord': base64.b64encode(output.getvalue())})
        # return self.word( cr, uid, ids, context=None)
        return {
                'type': 'ir.actions.act_url',
                'url': '/web/binary/download_document?model=rbs.certificado.mercantil&field=dataWord&id=%s&filename=Certificado.docx' % (str(self.id)),
                'target': 'new'
            }
    name = field.Char('Numero de Certificado', readonly=True)
    tipo_certificado = field.Selection([
        ('certificado_mercantil_1', 'Certificado Mercantil 1'),
        ('certificado_mercantil_2', 'Certificado Mercantil 2')], readonly=True, states={'draft': [('readonly', False)]})
    solicitante = field.Char('Solicitante', size=90, required=True)
    dataWord = field.Binary("word")
    state = field.Selection([
        ('draft', 'Borrador'),
        ('done', 'Realizado'),
        ('error', 'Error'),
        # ('deactivated','Desactivado')
        ], string='Estado', index=True, default='draft')

    mercantil_ids = field.Many2many('rbs.documento.mercantil', string='Documentos')
    criterio_busqueda = field.Selection([
        ('cedula', 'Cedula'),
        ('clave_catastral', 'Clave Catastral'),
        ], string="Criterio de busqueda", readonly=True, states={'draft': [('readonly', False)]})

    valor_busqueda = field.Char('Busqueda', size=30, required=True, readonly=True, states={'draft': [('readonly', False)]})

    @api.multi
    def validate(self):
        if self.state == 'draft':
            self.state = 'done'
            if not self.name:
                self.name = self.env["ir.sequence"].get("number_certificado_mercantil")

    @api.multi
    def invalidate(self):
        if self.state == 'done':
            self.state = 'draft'

    @api.onchange('valor_busqueda', 'criterio_busqueda')
    def get_documentos(self):
        if self.state == 'draft':
            # resultado=None
            if self.criterio_busqueda == 'cedula':
                # buscar todos las inscripciones donde el comprador tenga la cedula buscada
                claves_catastrales = []
                resultado_sin_filtrar = self.env['rbs.documento.mercantil'].search(
                    [
                        ('parte_ids.num_identificacion', '=', self.valor_busqueda),
                        ('parte_ids.tipo_interviniente_id.name', '=', 'COMPRADOR'),
                    ],
                    order='fecha_inscripcion desc')

                #  Hacer una lista de todas las claves catastrales
                for res in resultado_sin_filtrar:
                    for bien in res.bien_ids:
                        # print str(bien.clave_catastral)
                        if bien.clave_catastral:
                            claves_catastrales.append(bien.clave_catastral)
                # elmininar claves repetidas
                claves_catastrales = list(set(claves_catastrales))
                print str(claves_catastrales)
                # busca el ultimo movimiento de cada una de las claves catastrales y las agrega al campo 'mercantil_ids'
                self.mercantil_ids = None
                for clv_cat in claves_catastrales:
                    resultado = self.env['rbs.documento.mercantil'].search(
                        [
                         ('bien_ids.clave_catastral', '=', clv_cat),
                        ], limit=1,
                        order='fecha_inscripcion desc')
                    for parte in resultado.parte_ids:
                        if parte.num_identificacion == self.valor_busqueda:
                            self.mercantil_ids |= resultado

            elif self.criterio_busqueda == 'clave_catastral':
                resultado = self.env['rbs.documento.mercantil'].search(
                        [
                            ('bien_ids.clave_catastral', '=', self.valor_busqueda),
                        ], limit=1,
                        order='fecha_inscripcion desc')
                self.mercantil_ids = None
                self.mercantil_ids |= resultado

    @api.multi
    def unlink(self):
        for mercantil in self:
            if mercantil.state not in ('draft'):
                raise UserError(('No se puede eliminar un certificado ya validadado'))
            return super(rbs_certificado_mercantil, mercantil).unlink()


class rbs_documento_mercantil(models.Model):
    # _name ="rbs.documento.mercantil"
    _inherit = "rbs.documento.mercantil"
    _description = "Documento de la mercantil"
    certificado_mercantil_ids = field.Many2many('rbs.certificado.mercantil', string='Certificados Mercantil')
    dataWord = field.Binary("word")

    vendedor_virtual = field.Char(string="Vendedor", compute="get_vendedor")
    comprador_virtual = field.Char(string="Comprador", compute="get_comprador")
    clave_catastral_virtual = field.Char(string="Clave Catastral", compute="get_clave_catastral")
    descripcion_lindero_virtual = field.Char(string="Clave Catastral", compute="get_descripcion_lindero")
    canton_virtual = field.Char(string="Clave Catastral", compute="get_canton")

    @api.one
    def get_descripcion_lindero(self):
        descripcion_lindero_virtual = ''
        for bien in self.bien_ids:
            # if parte.tipo_interviniente_id.name=='VENDEDOR':
            descripcion_lindero_virtual = bien.descripcion_lindero + '/' + descripcion_lindero_virtual
        self.descripcion_lindero_virtual = descripcion_lindero_virtual

    @api.one
    def get_canton(self):
        canton_virtual = ''
        for bien in self.bien_ids:
            # if parte.tipo_interviniente_id.name=='VENDEDOR':
            try:
                canton_virtual = bien.canton_id.name + '/' + canton_virtual
            except:
                pass
        self.canton_virtual = canton_virtual

    @api.one
    def get_vendedor(self):
        vendedor_virtual = ''
        for parte in self.parte_ids:
            if parte.tipo_interviniente_id.name == 'VENDEDOR':
                vendedor_virtual = parte.nombres + ' ' + parte.apellidos + '/' + vendedor_virtual
        self.vendedor_virtual = vendedor_virtual

    @api.one
    def get_comprador(self):
        comprador_virtual = ''
        for parte in self.parte_ids:
            if parte.tipo_interviniente_id.name == 'COMPRADOR':
                comprador_virtual = parte.nombres + ' ' + parte.apellidos + '/' + comprador_virtual
        self.comprador_virtual = comprador_virtual

    @api.one
    def get_clave_catastral(self):
        clave_catastral_virtual = ''
        for bien in self.bien_ids:
            clave_catastral_virtual = bien.clave_catastral + '/' + clave_catastral_virtual
        self.clave_catastral_virtual = clave_catastral_virtual
