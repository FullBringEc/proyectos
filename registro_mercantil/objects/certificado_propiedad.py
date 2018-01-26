
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- encoding: utf-8 -*-
########################################################################

from openerp.osv import osv
from openerp import models, fields as field, api
import time
import base64
import datetime
from io import BytesIO
from docxtpl import DocxTemplate, RichText
from odoo.exceptions import UserError
import os


class rbs_certificado_propiedad(osv.osv):
    _name = 'rbs.certificado.propiedad'
    _rec_name = 'valor_busqueda'

    @api.multi
    def word_certificado(self):

        if self.tipo_certificado_id.codigo == "certificado_solvencia":

            output = BytesIO()
            tmpl_path = os.path.join(os.path.dirname(__file__))
            tpl = DocxTemplate(tmpl_path+self.tipo_certificado_id.ubicacion_certificado)

            resumen = []
            libro = {}
            lindero = self.propiedad_ids[0].bien_ids[0].descripcion_lindero
            duenoact = False
            solvencia = ''

            if self.propiedad_ids[0].gravamen_limitacion is True:
                solvencia = str(self.propiedad_ids[0].tipo_gravamen_ids[0].name.name)
            else:
                solvencia = "El bien esta libre de limitaciones"

            for propiedad_line in self.propiedad_ids:
                for parte in propiedad_line.parte_ids:
                    if parte.tipo_interviniente_id.name == 'COMPRADOR':
                        duenoact = parte.nombres + ' ' + parte.apellidos
                        # raise UserError(duenoact)
                    if duenoact != False:
                        break
                if duenoact != False:
                    break

            for propiedad_line in self.propiedad_ids:

                    detalle = {}

                    detalle['libro'] = propiedad_line.libro_id.name
                    detalle['acto'] = propiedad_line.tipo_tramite_id.name
                    detalle['numero'] = RichText(str(propiedad_line.numero_inscripcion))
                    detalle['finscrip'] = RichText(propiedad_line.fecha_inscripcion.encode('utf-8'))
                    detalle['finicial'] = RichText(str(propiedad_line.foleo_desde))
                    detalle['ffinal'] = RichText(str(propiedad_line.foleo_hasta))
                    resumen.append(detalle)

                    if libro.has_key(propiedad_line.libro_id.name):
                        libro[propiedad_line.libro_id.name] = libro[propiedad_line.libro_id.name]+1
                    else:
                        libro[propiedad_line.libro_id.name] = 1

            resmov = []

            for propiedad_line1 in self.propiedad_ids:

                    detalle2 = {}

                    detalle2['libro'] = propiedad_line1.libro_id.name.encode('utf-8')
                    detalle2['acto'] = propiedad_line1.tipo_tramite_id.name.encode('utf-8')
                    detalle2['tomo'] = propiedad_line1.tomo_id.name
                    detalle2['finscrip'] = RichText(propiedad_line1.fecha_inscripcion.encode('utf-8'))
                    detalle2['numero'] = RichText(str(propiedad_line1.numero_inscripcion))
                    detalle2['numeroreper'] = RichText(str(propiedad_line1.repertorio))
                    detalle2['finicial'] = RichText(str(propiedad_line1.foleo_desde))
                    detalle2['ffinal'] = RichText(str(propiedad_line1.foleo_hasta))
                    detalle2['notariares'] = RichText(propiedad_line1.notaria_id.name.encode('utf-8'))
                    detalle2['notariaprov'] = RichText(propiedad_line1.provincia_notaria_id.name.encode('utf-8'))
                    detalle2['canton'] = RichText(propiedad_line1.canton_notaria_id.name.encode('utf-8'))
                    detalle2['fechaescri'] = RichText(str(propiedad_line1.fecha_escritura))
                    detalle2['fechaadju'] = RichText(str(propiedad_line1.fecha_adjudicion))
                    detalle2['observacion'] = RichText(propiedad_line1.observacion.encode('utf-8'))
                    partes_certificado = []
                    for parte in propiedad_line1.parte_ids:

                            partes_detalle = {}

                            partes_detalle['tipointer'] = parte.tipo_interviniente_id.name.encode('utf-8')
                            partes_detalle['numcel'] = parte.num_identificacion
                            partes_detalle['nombreparte'] = RichText(parte.nombres.encode('utf-8')+' '+parte.apellidos.encode('utf-8'))
                            partes_detalle['estadocivil'] = RichText(parte.estado_civil.encode('utf-8'))
                            partes_certificado.append(partes_detalle)
                    detalle2['partes'] = partes_certificado

                    resmov.append(detalle2)


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
                        'lindero': RichText(lindero.encode('utf-8')),
                        'duenoact': RichText(duenoact.encode('utf-8')),
                        'solvencia': RichText(solvencia.encode('utf-8')),
                        # 'infmuni' : RichText (str (self.canton_notaria_id.name)),
                        # 'tpredio' : RichText (str (self.descripcion_bien)),
                        # 'parroquia' : RichText (str (self.parroquia_id.name)),
                        # 'lindero' : RichText (str (self.descripcion_lindero)),
                        'nombresoli': RichText(self.solicitante.encode('utf-8')),
                        'sesion': RichText(usuario_actual.name.encode('utf-8')),
                        'fechaactual': RichText(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))),
                        'nomregistrador': RichText(usuario_actual.company_id.registrador_nombre.encode('utf-8')),
                        'movimientos': movimientos,
                        'resumenmov': resmov,

                }

        if self.tipo_certificado_id.codigo == "certificado_negativo":

            # Segundo certificado o el que este en segundo
            output = BytesIO()
            tmpl_path = os.path.join(os.path.dirname(__file__))
            tpl = DocxTemplate(tmpl_path+self.tipo_certificado_id.ubicacion_certificado)
            # from docx import Document
            # style = tpl.styles['estiloregistro']
            # font = style.font
            # from docx.shared import Pt
            # font.name = 'Times New Roman'
            # font.size = Pt(72)
            resumen = []
            libro = {}

            for propiedad_line in self.propiedad_ids:

                    detalle = {}
                    detalle['libro'] = propiedad_line.libro_id.name
                    detalle['acto'] = propiedad_line.tipo_tramite_id.name
                    detalle['numero'] = RichText(str(propiedad_line.numero_inscripcion))
                    detalle['finscrip'] = RichText(propiedad_line.fecha_inscripcion.encode('utf-8'))
                    detalle['finicial'] = RichText(str(propiedad_line.foleo_desde))
                    detalle['ffinal'] = RichText(str(propiedad_line.foleo_hasta))
                    resumen.append(detalle)

                    if libro.has_key(propiedad_line.libro_id.name):
                        libro[propiedad_line.libro_id.name] = libro[propiedad_line.libro_id.name]+1
                    else:
                        libro[propiedad_line.libro_id.name] = 1

            movimientos = []

            for clave in libro:

                detalle = {}
                l = clave
                ni = libro[clave]

                detalle['libro'] = l
                detalle['sumainscrp'] = RichText(str(ni))

                movimientos.append(detalle)

            if len(movimientos) == 0 and len(resumen) == 0:
                usuario_actual = self.env['res.users'].search([('id', '=', self._uid)])[0]

                context = {
                            'numerocertificado': RichText(self.name.encode('utf-8')),
                            'fechainiact': RichText(usuario_actual.company_id.registrador_fecha_ingreso.encode('utf-8')),
                            'direccionreg': RichText(usuario_actual.company_id.street.encode('utf-8')),
                            'telefonoreg': RichText(usuario_actual.company_id.phone.encode('utf-8')),
                            'nomregistrador': RichText(usuario_actual.company_id.registrador_nombre.encode('utf-8')),
                            'nombresoli': RichText(self.solicitante.encode('utf-8')),
                            'sesion': RichText(usuario_actual.name.encode('utf-8')),
                            'fechaactual': RichText(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))),

                    }
            else:

                raise osv.except_osv('Error', "Verificar el solicitante tiene movimientos prediales")

        tpl.render(context)
        tpl.save(output)

        self.write({'dataWord': base64.b64encode(output.getvalue())})
        # return self.word( cr, uid, ids, context=None)
        return {
                'type': 'ir.actions.act_url',
                'url': '/web/binary/download_document?model=rbs.certificado.propiedad&field=dataWord&id=%s&filename=%s.docx' %
                        (str(self.id), str(self.tipo_certificado_id.name)),
                'target': 'new'
            }

    # }
    # clave_catastral = field.Char('Clave Catastral', size=30, required=True)
    # cedula = field.Char('Cedula', size=30, required=True)
    state = field.Selection([
        ('draft', 'Borrador'),
        ('done', 'Realizado'),
        ('error', 'Error'),
        # ('deactivated','Desactivado')
        ], string='Estado', index=True, default='draft', readonly=True)
    solicitante = field.Char('Solicitante', size=90, required=True, readonly=True, states={'draft': [('readonly', False)]})
    # tipo_certificado = field.Selection([
    #     ('certificado_solvencia', 'Certificado de solvencia'),
    #     ('certificado_negativo', 'Certificado Negativo')], readonly=True, states={'draft': [('readonly', False)]})

    tipo_certificado_id = field.Many2one(
                                "rbs.tipo.certificado",
                                string="Tipo de certificado",
                                readonly=True, states={'draft': [('readonly', False)]})
    name = field.Char('Numero de Certificado', readonly=True)
    dataWord = field.Binary("word")

    propiedad_ids = field.Many2many('rbs.documento.propiedad', string='Documentos', compute='get_documentos')
    criterio_busqueda = field.Selection([
        ('identificacion', 'Identificacion'),
        ('clave_catastral', 'Clave Catastral'),
        ], string="Criterio de busqueda", readonly=True, states={'draft': [('readonly', False)]})

    valor_busqueda = field.Char('Busqueda', size=30, required=True, readonly=True, states={'draft': [('readonly', False)]})

    fecha_certificado = field.Datetime(
                                'Fecha del certificado',
                                default=lambda self: datetime.datetime.now(),
                                readonly=True,
                                states={'draft': [('readonly', False)]})

    @api.multi
    def validate(self):
        if self.tipo_certificado_id.codigo == "certificado_negativo" and len(self.propiedad_ids) != 0:
            raise osv.except_osv('Error', "Verificar el solicitante tiene movimientos prediales o Posee bienes")
        else:
            if self.tipo_certificado_id.codigo == "certificado_solvencia" and len(self.propiedad_ids) == 0:
                raise osv.except_osv('Error', "Verificar el solicitante no tiene movimientos prediales o no posee bienes")
            else:
                if self.state == 'draft':
                    self.state = 'done'
                    if not self.name:
                        self.name = self.env["ir.sequence"].get("number_certificado_propiedad")

    @api.multi
    def invalidate(self):
        if self.state == 'done':
            self.state = 'draft'

    @api.onchange('valor_busqueda', 'criterio_busqueda')
    def get_documentos(self):

        if self.criterio_busqueda == 'Identificacion':
            #  buscar todos las inscripciones donde el comprador tenga la cedula buscada
            claves_catastrales = []
            resultado_sin_filtrar = self.env['rbs.documento.propiedad'].search(
                [
                    ('parte_ids.num_identificacion', '=', self.valor_busqueda),
                    ('parte_ids.tipo_interviniente_id.name', '=', 'COMPRADOR'),
                ],
                order='fecha_inscripcion desc')

            #   Hacer una lista de todas las claves catastrales
            for res in resultado_sin_filtrar:
                for bien in res.bien_ids:
                    # print str(bien.clave_catastral)
                    if bien.clave_catastral:
                        claves_catastrales.append(bien.clave_catastral)
            # elmininar claves repetidas
            claves_catastrales = list(set(claves_catastrales))
            print str(claves_catastrales)
            # busca el ultimo movimiento de cada una de las claves catastrales y las agrega al campo 'propiedad_ids'
            self.propiedad_ids = None
            for clv_cat in claves_catastrales:

                resultado = self.env['rbs.documento.propiedad'].search(
                    [
                        ('bien_ids.clave_catastral', '=', clv_cat),
                    ], limit=1,
                    order='fecha_inscripcion desc')
                for parte in resultado.parte_ids:
                    if parte.num_identificacion == self.valor_busqueda:
                        self.propiedad_ids |= resultado

        elif self.criterio_busqueda == 'clave_catastral':
            resultado = self.env['rbs.documento.propiedad'].search(
                    [
                        ('bien_ids.clave_catastral', '=', self.valor_busqueda),
                    ],
                    order='fecha_inscripcion desc')
            self.propiedad_ids = None
            self.propiedad_ids |= resultado

    @api.multi
    def unlink(self):
        for propiedad in self:
            if propiedad.state not in ('draft'):
                raise UserError(('No se puede eliminar un certificado ya validadado'))
            return super(rbs_certificado_propiedad, propiedad).unlink()


class rbs_documento_propiedad(models.Model):
    # _name ="rbs.documento.propiedad"
    _inherit = "rbs.documento.propiedad"
    _description = "Documento de la Propiedad"
    certificado_propiedad_ids = field.Many2many('rbs.certificado.propiedad', string='Certificados Propiedad')
    # certificado_mercantil_ids = field.Many2many('rbs.certificado.mercantil',string ='Certificados Mercantil')
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
