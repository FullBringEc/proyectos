# -*- coding: utf-8 -*-
# from _csv import field_size_limit
# from cgi import FieldStorage

# from dateutil import parser
from openerp import models, fields, api
# from openerp.osv import osv
from docxtpl import DocxTemplate, RichText
# from jinja2 import Environment, FileSystemLoader

import base64
import os
# from openerp import http
# from openerp.http import request
# from openerp.addons.web.controllers.main import serialize_exception,content_disposition
# import time
import datetime
# from PIL import Image
# import StringIO
from io import BytesIO
from odoo.exceptions import UserError
# import base64
# import cStringIO
# import warnings


class rbs_documento_mercantil(models.Model):
    _name = "rbs.documento.mercantil"
    _description = "Documento Mercantil"
    _rec_name = 'numero_inscripcion'
    # name= field.Char('Nombre')

    def _getUltimoAnio(self, context=None):
        anio_id = self.search([], limit=1, order='id desc').anio_id.id
        return anio_id

    def _getUltimoLibro(self, context=None):
        libro_id = self.search([], limit=1, order='id desc').libro_id.id
        print libro_id
        if libro_id:
            return libro_id
        # return libro_id

    def _getUltimoTomo(self, context=None):
        tomo_id = self.search([], limit=1, order='id desc').tomo_id.id
        return tomo_id

    def name_get(self):
        res = []
        for record in self:
            if record.anio_id:
                anio = record.anio_id.name
                libro = record.libro_id.name
                tomo = record.tomo_id.name
                tit = "%s-%s-%s" % (anio, libro, tomo)
                res.append((record.id, tit))

            else:
                tit = "Sin registro"
                res.append((record.id, tit))
        return res

    name = fields.Char('Secuencial de la Inscripcion', readonly=True)
    # Ctegoria Libro
    anio_id = fields.Many2one('rbs.anio', string='Año', default=_getUltimoAnio, readonly=True, states={'draft': [('readonly', False)]})
    libro_id = fields.Many2one('rbs.libro', string='Libro', default=_getUltimoLibro, readonly=True, states={'draft': [('readonly', False)]})
    tipo_libro_mercantil_id = fields.Many2one(
        related="libro_id.tipo_libro_mercantil_id",
        string='Tipo de Libro M',
        readonly=True,
        states={'draft': [('readonly', False)]})
    # reg_acto_contrato = fields.Selection([
    #            ('ACTO', 'ACTO'),
    #            ('CONTRATO', 'CONTRATO'),
    #        ], string='Registra Acto/Contrato')
    tipo_tramite_id = fields.Many2one('rbs.tipo.tramite', string='Tipo de trámite', readonly=True, states={'draft': [('readonly', False)]})
    # tipo_contrato_id = fields.Many2one('rbs.tipo.contrato', string='Tipo de Acto/Contrato')
    tramite_id = fields.Many2one('rbs.tramite.mercantil', string='Trámite', readonly=True, states={'draft': [('readonly', False)]})
    # tipo_libro = fields.Char (string='Tipo Libro')
    tomo_id = fields.Many2one("rbs.tomo", string='Tomo', default=_getUltimoTomo, readonly=True, states={'draft': [('readonly', False)]})

    state = fields.Selection([
            ('draft', 'Borrador'),
            ('done', 'Realizado'),
            # ('sustituido', 'Sustituido'),
        ], 'Estado', default='draft', readonly=True)

    observacion = fields.Text(string='Observación', readonly=True, states={'draft': [('readonly', False)]})
    foleo_desde = fields.Char(string='Desde', readonly=True, states={'draft': [('readonly', False)]})
    foleo_hasta = fields.Char(string='Hasta', readonly=True, states={'draft': [('readonly', False)]})

    # INFORMACION DE LA INSCRIPCION

    numero_inscripcion = fields.Integer(string='Número de inscripción', readonly=True, states={'draft': [('readonly', False)]})
    repertorio = fields.Char(string='Repertorio', readonly=True, states={'draft': [('readonly', False)]})
    provincia_notaria_id = fields.Many2one(
        'rbs.provincia',
        string='Provincia de la notaria, juzgado o institución pública',
        readonly=True,
        states={'draft': [('readonly', False)]})
    canton_notaria_id = fields.Many2one('rbs.canton', string='Canton de la notaria', readonly=True, states={'draft': [('readonly', False)]})
    notaria_id = fields.Many2one('rbs.institucion', string='Nombre notaria o juzgado', readonly=True, states={'draft': [('readonly', False)]})
    cuantia_valor = fields.Char(string='Cuantia', readonly=True, states={'draft': [('readonly', False)]})
    fecha_acta_junta = fields.Datetime(string='Fecha de acta de la junta', readonly=True, states={'draft': [('readonly', False)]})
    fecha_cancel_gravamen = fields.Datetime(string='Fecha de cancelación de gravamen/limitación', readonly=True, states={'draft': [('readonly', False)]})
    fecha_const_gravamen = fields.Datetime(string='Fecha Const gravamen/limitacion', readonly=True, states={'draft': [('readonly', False)]})
    fecha_inscripcion = fields.Datetime(string='Fecha de inscripción', readonly=True, states={'draft': [('readonly', False)]})
    fecha_repertorio = fields.Datetime(string='Fecha repertorio', readonly=True, states={'draft': [('readonly', False)]})
    fecha_cancelacion = fields.Datetime(string='Fecha de cancelación', readonly=True, states={'draft': [('readonly', False)]})
    fecha_ultima_modificacion = fields.Datetime(string='Fecha de última modificación de la fuente', readonly=True, states={'draft': [('readonly', False)]})
    fecha_escritura = fields.Datetime(string='Fecha de escritura, sentencia o resolución', readonly=True, states={'draft': [('readonly', False)]})
    nombramiento_mercantil_id = fields.Many2one(
        'rbs.nombramiento.mercantil',
        string='Tipo de nombramiento',
        readonly=True,
        states={'draft': [('readonly', False)]})
    plazo_nombramiento_cant = fields.Integer(string='Plazo nombramiento', readonly=True, states={'draft': [('readonly', False)]})
    plazo_nombramiento_tipo = fields.Selection([
            ('DIAS', 'Dias'),
            ('SEMANAS', 'Semanas'),
            ('MESES', 'Meses'),
            ('AÑOS', 'Años'),
        ], readonly=True, states={'draft': [('readonly', False)]})
    fecha_nombramiento = fields.Datetime(string='Fecha de nombramiento', readonly=True, states={'draft': [('readonly', False)]})

    tipo_acto_contrato = fields.Many2many(
        'rbs.tipo.acto.contrato',
        relation="mercantil_tipo_acto_contrato_rel",
        string='Tipo de acto o contrato',
        readonly=True,
        states={'draft': [('readonly', False)]})

    parte_ids = fields.One2many('rbs.parte', 'documento_mercantil_id', string='Partes', readonly=True, states={'draft': [('readonly', False)]})
    repr_identificacion = fields.Char(string='Cédula o pasaporte del representante', readonly=True, states={'draft': [('readonly', False)]})
    repr_nombre = fields.Char(string='Nombres del representante', readonly=True, states={'draft': [('readonly', False)]})
    repr_apellido = fields.Char(string='Apellido del representante')
    repr_razon_social = fields.Char(string='Razón social del representante', readonly=True, states={'draft': [('readonly', False)]})
    repr_acreedor = fields.Char(string='Acreedor', readonly=True, states={'draft': [('readonly', False)]})
    repr_nombramiento_id = fields.Many2one(
        'rbs.nombramiento.mercantil',
        string='Cargo del representante',
        readonly=True,
        states={'draft': [('readonly', False)]})

    parte_char_ids = fields.One2many('rbs.parte.char', 'documento_mercantil_id', 'Partes Char', readonly=True, states={'draft': [('readonly', False)]})
    bien_ids = fields.One2many('rbs.bien', 'documento_mercantil_id', string='Bienes', readonly=True, states={'draft': [('readonly', False)]})
    accionista_ids = fields.One2many('rbs.accionista', 'documento_mercantil_id', string='Accionistas', readonly=True, states={'draft': [('readonly', False)]})
    marginacion_ids = fields.One2many(
        'rbs.marginacion',
        'documento_mercantil_id',
        string='Marginaciones',
        readonly=True,
        states={'draft': [('readonly', False)]})
    tipo_gravamen_ids = fields.One2many(
        'rbs.gravamen',
        'documento_mercantil_id',
        string='Tipo gravamen/limitación',
        readonly=True,
        states={'draft': [('readonly', False)]})
    identificacion_unica = fields.Char(string='Identificador', compute='_compute_upper', store=True, readonly=True, states={'draft': [('readonly', False)]})
    ubicacion_dato_id = fields.Many2one('rbs.ubicacion.dato', string='Ubicación del dato', readonly=True, states={'draft': [('readonly', False)]})
    tipo_persona_id = fields.Selection([
            ('NATURAL', 'Natural'),
            ('JURIDICA', 'Jurídica'),
        ], string='Tipo de persona', readonly=True, states={'draft': [('readonly', False)]})
    persona_id = fields.Many2one('rbs.persona', string='Compareciente(n)', readonly=True, states={'draft': [('readonly', False)]})
    persona_nombres = fields.Char(string='Nombres del compareciente', readonly=True, states={'draft': [('readonly', False)]})
    persona_apellidos = fields.Char(string='Apellidos del compareciente', readonly=True, states={'draft': [('readonly', False)]})
    persona_estado_civil = fields.Char(string='Estado civil', readonly=True, states={'draft': [('readonly', False)]})
    persona_cedula = fields.Char(string='Cedula del compareciente', readonly=True, states={'draft': [('readonly', False)]})
    persona_estado_civil = fields.Char(string='Estado civil', readonly=True, states={'draft': [('readonly', False)]})
    persona_nombres_conyuge = fields.Char(string='Nombres de cónyuge', readonly=True, states={'draft': [('readonly', False)]})
    persona_apellidos_conyuge = fields.Char(string='Apellidos de cónyuge', readonly=True, states={'draft': [('readonly', False)]})
    persona_cedula_conyuge = fields.Char(string='Cedula del cónyuge', readonly=True, states={'draft': [('readonly', False)]})
    persona_tipo_interviniente_id = fields.Many2one(
        'rbs.tipo.interviniente.a',
        string='Tipo de interviniente',
        readonly=True,
        states={'draft': [('readonly', False)]})
    persona_calidad_compareciente = fields.Char(string='Calidad compareciente', readonly=True, states={'draft': [('readonly', False)]})
    persona_razonSocial = fields.Char(string='Razón social', readonly=True, states={'draft': [('readonly', False)]})
    acreedor_id = fields.Many2one('rbs.persona', string='Acreedor', readonly=True, states={'draft': [('readonly', False)]})
    # Fin categoria

    # Datos Bien

    # Fin categoria

    # Datos Registrales
    canton_registro_id = fields.Many2one('rbs.canton', string='Cantón registro mercantil', readonly=True, states={'draft': [('readonly', False)]})
    ultima_modificacion = fields.Char(string='Última modificación', readonly=True, states={'draft': [('readonly', False)]})
    notaria_juzgado_entidad = fields.Char(string='Nombre notaria o juzgado', readonly=True, states={'draft': [('readonly', False)]})
    canton_notaria_id = fields.Many2one('rbs.canton', string='Cantón de la notaria', readonly=True, states={'draft': [('readonly', False)]})
    fecha_escritura_contrato = fields.Datetime(string='Fecha de escritura', readonly=True, states={'draft': [('readonly', False)]})
    marginacion_tramite_origi = fields.Char(string='Marginacion trámite', readonly=True, states={'draft': [('readonly', False)]})
    # Fin categoria

    # Categoria Accionistas
    No_accionistas = fields.Char(string='Número accionistas', readonly=True, states={'draft': [('readonly', False)]})
    accionistas_id = fields.Many2one('rbs.persona', string='Accionista', readonly=True, states={'draft': [('readonly', False)]})
    Nombre_acci_socios = fields.Char(string='Nombre socios', readonly=True, states={'draft': [('readonly', False)]})
    porecentaje_acciones = fields.Char(string='Porcentaje de acciones', readonly=True, states={'draft': [('readonly', False)]})
    valor_acciones = fields.Char(string='Valor de acciones', readonly=True, states={'draft': [('readonly', False)]})
    acta_junta = fields.Char(string='Acta de junta', readonly=True, states={'draft': [('readonly', False)]})
    # Fin Categoria

    # Categoria Nombramiento
    fechaNombramiento = fields.Datetime(string='Fecha nombramiento', readonly=True, states={'draft': [('readonly', False)]})
    tipo_nombra = fields.Datetime(string='Tipo nombraiento', readonly=True, states={'draft': [('readonly', False)]})
    plazo_nombramiento = fields.Datetime(string='Plazo nombramiento', readonly=True, states={'draft': [('readonly', False)]})
    tipo_gravamen = fields.Datetime(string='Tipo gravamen', readonly=True, states={'draft': [('readonly', False)]})
    fecha_gravamen = fields.Datetime(string='Fecha gravamen', readonly=True, states={'draft': [('readonly', False)]})
    # Fin categoria

    tipo_contrato_id = fields.Many2one('rbs.tipo.contrato', string='Tipo de contrato', readonly=True, states={'draft': [('readonly', False)]})

    nombre_institucion = fields.Char(string='Nombre de la institución', readonly=True, states={'draft': [('readonly', False)]})
    canton_notaria = fields.Char(string='Canton de notaria', readonly=True, states={'draft': [('readonly', False)]})

    estado = fields.Selection([
            ('VIGENTE', 'Vigente'),
            ('NOVIGENTE', 'No vigente'),
        ], string='Estado', readonly=True, states={'draft': [('readonly', False)]})

    identificacion_unica = fields.Char(
        string='Identificador único sistema remoto',
        compute='_compute_upper',
        store=True,
        readonly=True,
        states={'draft': [('readonly', False)]})
    ubicacion_dato_id = fields.Many2one('rbs.ubicacion.dato', string='Ubicación del dato', readonly=True, states={'draft': [('readonly', False)]})
    dataWord = fields.Binary("word", readonly=True, states={'draft': [('readonly', False)]})

    @api.multi
    def validate(self):
        if self.state == 'draft':
            self.state = 'done'
            if not self.name:
                self.name = self.env["ir.sequence"].get("number_inscripcion_mercantil")

    @api.multi
    def invalidate(self):
        if self.state == 'done':
            self.state = 'draft'

    @api.multi
    def word(self):
        output = BytesIO()
        tmpl_path = os.path.join(os.path.dirname(__file__), 'Documentos/DocMercantil')
        tpl = DocxTemplate(tmpl_path + '/inscripcion.docx')

        compareciente = []
        for partes in self.parte_ids:
            detalle = {}
            detalle['cliente'] = partes.tipo_persona
            detalle['identi'] = partes.num_identificacion
            detalle['compareciente'] = RichText(str(partes.nombres) + ' ' + str(partes.apellidos))
            detalle['estado'] = RichText(str(partes.estado_civil))
            detalle['interviniente'] = RichText(str(partes.tipo_interviniente_id.name))
            detalle['ciudad'] = RichText(str(self.canton_notaria_id.name))
            compareciente.append(detalle)

        datosbien = []
        for bien in self.bien_ids:
            detalle = {}
            # documento_mercantil = None
            # if bien.documento_mercantil_id:
            #     documento_mercantil = bien.documento_mercantil_id
            # else:
            #     documento_mercantil = bien.documento_propiedad_id

            detalle['numero'] = RichText(str(self.numero_inscripcion))
            detalle['fecha_inscripcion'] = RichText(str(self.fecha_inscripcion))
            detalle['tipobien'] = RichText(str(bien.tipo_bien_id.name))

            datosbien.append(detalle)

        context = {
            'acto': RichText(self.tipo_tramite_id.name),
            'compareciente': compareciente,
            'datosbien': datosbien,
            'ntomo': RichText(str(self.tomo_id.name)),
            'ninscripcion': RichText(str(self.numero_inscripcion)),
            'nrepertorio': RichText(str(self.repertorio)),
            'frepertorio': RichText(str(self.fecha_repertorio)),
            'natacto': RichText('SD'),
            'folioi': RichText(str(self.foleo_desde)),
            'foliof': RichText(str(self.foleo_hasta)),
            'periodo': RichText(str(self.anio_id.name)),
            'natcontrato': RichText(str(self.libro_id.name)),
            'notaria': RichText(str(self.notaria_id.name)),
            'nomcanton': RichText(str(self.canton_notaria_id.name)),
            'fechaprov': RichText(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))),
            'fresolucion': RichText(str(self.fecha_escritura)),
            'observacion': RichText(str(self.observacion)),

        }

        tpl.render(context)
        tpl.save(output)

        self.write({'dataWord': base64.b64encode(output.getvalue())})
        # return self.word( cr, uid, ids, context=None)
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/binary/download_document?model=rbs.documento.mercantil&field=dataWord&id=%s&filename=Inscripcion.docx' % (str(self.id)),
            'target': 'new'
            }

    @api.multi
    def open_ui(self,context=None):
        return {
            'type': 'ir.actions.act_url',
            'url': '/registro_mercantil/web/?binary='+str(self.id)+'&tipo=mercantil',
            'target': 'new',
        }

    @api.onchange('parte_ids', 'bien_ids')
    def onchange_parte_ids(self):
        parte_char_ids_num = []
        self.parte_char_ids = None
        for parte in self.parte_ids:
            nombres = parte.razon_social or parte.nombres
            r = [x for x in self.parte_char_ids if x.name == nombres]
            if r:
                continue
            parte_char = self.env['rbs.parte.char'].create(
                                                        {
                                                            'name': parte.razon_social or parte.nombres or "",
                                                            'parte_id': parte.id,
                                                            'documento_mercantil_id': self.id
                                                        })
            self.parte_char_ids |= parte_char
            parte_char_ids_num.append(parte_char.id)
        print parte_char_ids_num
        for bien in self.bien_ids:
            bien.parte_char_ids = [(6, 0, parte_char_ids_num)]
        return

    @api.depends('ubicacion_dato_id', 'persona_cedula', 'numero_inscripcion')
    def _compute_upper(self):
        for rec in self:
            try:
                rec.identificacion_unica = '03'+rec.ubicacion_dato_id.name+rec.persona_cedula+rec.numero_inscripcion
            except:
                try:
                    rec.identificacion_unica = '03'+rec.ubicacion_dato_id.name+rec.numero_inscripcion+rec.numero_inscripcion
                except:
                    pass

    def on_change_anio_id(self, anio_id, context=None):
        result = {}
        if(self._getUltimoAnio(context=None) != anio_id):
            result['libro_id'] = 0
        return {'value': result}

    def on_change_libro_id(self, libro_id, context=None):
        result = {}
        if(self._getUltimoLibro(context=None) != libro_id):
            result['tomo_id'] = 0
        return {'value': result}

    def codigoascii(self, text):
        return unicode(text).encode('utf-8')

    def onchange_persona_id(self, cr, uid, ids, persona_id, context=None):
        persona_id = self.pool.get('rbs.persona').search(cr, uid, [('id', '=', persona_id)])
        persona = self.pool.get('rbs.persona').browse(cr, uid, persona_id, context=None)
        result = {}
        try:
            if persona:
                # raise osv.except_osv('Esto es un Mesaje!',establecimiento)
                try:
                    if persona.persona_nombres:
                        result['persona_nombres'] = self.codigoascii(persona.persona_nombres)
                except:
                    pass

                try:
                    if persona.persona_apellidos:
                        result['persona_apellidos'] = self.codigoascii(persona.persona_apellidos)
                except:
                    pass
                try:
                    if persona.name:
                        result['persona_cedula'] = str(persona.name)
                except:
                    pass
                try:
                    if persona.persona_representante:
                        result['persona_representante'] = self.codigoascii(persona.persona_representante)
                except:
                    pass
                try:
                    if persona.persona_razonSocial:
                        result['persona_razonSocial'] = self.codigoascii(persona.persona_razonSocial)
                except:
                    pass
        except:
            pass

        return {'value': result}

    def onchange_inscripcion(self, inscripcion_num, libro_id, context=None):
        mercantil = self.search([('numero_inscripcion', '=', inscripcion_num), ('libro_id', '=', libro_id)])
        # mercantil = self.browse(cr,uid,mercantil_id,context = None)
        result = {}

        try:

            if mercantil:
                mercantil = mercantil[0]
                # raise osv.except_osv('Esto es un Mesaje!',establecimiento)
                try:
                    if mercantil.fecha_inscripcion:
                        result['fecha_inscripcion'] = str(mercantil.fecha_inscripcion)

                except:
                    pass
                try:
                    if mercantil.anio_id:
                        result['anio_id'] = mercantil.anio_id.id
                except:
                    pass
                try:
                    if mercantil.libro_id:
                        result['libro_id'] = mercantil.libro_id.id
                except:
                    pass
                try:
                    if mercantil.tomo_id:
                        result['tomo_id'] = mercantil.tomo_id.id
                except:
                    pass
                try:
                    if mercantil.tipo_contrato_id:
                        result['tipo_contrato_id'] = mercantil.tipo_contrato_id.id
                except:
                    pass
                try:
                    if mercantil.fecha_cancelacion:
                        result['fecha_cancelacion'] = str(mercantil.fecha_cancelacion)
                except:
                    pass
                try:
                    if mercantil.tipo_bien_id:
                        result['tipo_bien_id'] = mercantil.tipo_bien_id
                except:
                    pass

                try:
                    if mercantil.chasis:
                        result['chasis'] = self.codigoascii(mercantil.chasis)
                except:
                    pass
                try:
                    if mercantil.motor:
                        result['motor'] = self.codigoascii(mercantil.motor)
                except:
                    pass
                try:
                    if mercantil.marca:
                        result['marca'] = self.codigoascii(mercantil.marca)
                except:
                    pass
                try:
                    if mercantil.modelo:
                        result['modelo'] = self.codigoascii(mercantil.modelo)
                except:
                    pass
                try:
                    if mercantil.anio_fabricacion:
                        result['anio_fabricacion'] = str(mercantil.anio_fabricacion)
                except:
                    pass
                try:
                    if mercantil.placa:
                        result['placa'] = self.codigoascii(mercantil.placa)
                except:
                    pass

                try:
                    if mercantil.ultima_modificacion:
                        result['ultima_modificacion'] = str(mercantil.ultima_modificacion)
                except:
                    pass
                try:
                    if mercantil.nombre_institucion:
                        result['nombre_institucion'] = self.codigoascii(mercantil.nombre_institucion)
                except:
                    pass
                try:
                    if mercantil.canton_notaria:
                        result['canton_notaria'] = self.codigoascii(mercantil.canton_notaria)
                except:
                    pass
                try:
                    if mercantil.fecha_escritura_contrato:
                        result['fecha_escritura_contrato'] = str(mercantil.fecha_escritura_contrato)
                except:
                    pass
                try:
                    if mercantil.estado:
                        result['estado'] = mercantil.estado
                except:
                    pass
                try:
                    if mercantil.filedata_id:
                        result['filedata_id'] = mercantil.filedata_id.id
                except:
                    pass
                try:
                    if mercantil.ubicacion_dato_id:
                        result['ubicacion_dato_id'] = mercantil.ubicacion_dato_id.id
                except:
                    pass

            if not mercantil:
                result['filedata_id'] = self._create_pdf(context=None)
        except:
            pass
        return {'value': result}

    @api.multi
    def unlink(self):
        for mercantil in self:
            if mercantil.state not in ('draft'):
                raise UserError(('No se puede eliminar una incripcion ya validadada'))
            return super(rbs_documento_mercantil, mercantil).unlink()


class rbs_tipo_compareciente_v(models.Model):
    _name = "rbs.tipo.interviniente.v"
    _description = "Tipo de interviniente"
    name = fields.Char(string='Tipo del compareciente')


class rbs_tipo_contrato(models.Model):
    _name = "rbs.tipo.contrato"
    _description = "Tipo de Contrato"
    name = fields.Char(string='Tipo del contrato')


class rbs_compania(models.Model):
    _name = "rbs.compania"
    _description = u"Companía"
    compania_nombres = fields.Char(string='Nombre de la Compañía', required=True)
    name = fields.Char(string='Indentificacion de la Compañía', required=True)
    compania_especie_id = fields.Many2one('rbs.compania.especie', string='Especie de Compañía', required=True)
    _sql_constraints = [
        ('compania_identificacion_uniq', 'unique(name)',
            'La identificacion debe ser unica por Compañía'),
    ]
    _order = 'compania_nombres'
    # _rec_name = 'compania_identificacion'


class rbs_tipo_interviniente(models.Model):
    _name = "rbs.tipo.interviniente"
    _description = "Tipo de interviniente"

    name = fields.Char(string='Tipo del interviniente')


class rbs_calidad_compareciente(models.Model):
    _name = "rbs.calidad.compareciente"
    _description = "Calidad del compareciente"
    name = fields.Char(string='Calidad del Compareciente')


class rbs_tipo_compareciente_a(models.Model):
    _name = "rbs.tipo.interviniente.a"
    _description = "Tipo de compareciente"
    name = fields.Char(string='Tipo del compareciente')


class rbs_compania_especie(models.Model):
    _name = "rbs.compania.especie"
    _description = "Especie de Compañia"
    name = fields.Char(string='Especie')


class rbs_cargo(models.Model):
    _name = 'rbs.cargo'
    _description = "Tipo de cargo"
    name = fields.Char(string='Tipo de cargo')


class rbs_tipo_tramite(models.Model):
    _name = 'rbs.tipo.tramite'
    _description = "Tipo de trámite"
    name = fields.Char(string='Tipo De trámite')


class rbs_ubicacion_dato(models.Model):
    _name = 'rbs.ubicacion.dato'
    _description = "Ubicación de dato"
    name = fields.Char(string='Ubicacion del dato')


class rbs_estado_inscripcion(models.Model):
    _name = 'rbs.estado.inscripcion'
    _description = "Estado de Inscripción"
    name = fields.Char(string='Estado de Inscripción')


# class factura_invoice(models.Model):
#   _inherit = 'account.invoice'
#   acta_id = fields.Many2one('rbs.documento.mercantil.acta', string='Acta')

class reportes_doc_mercantiles(models.Model):
    _inherit = 'res.company'
    certificacion = fields.Binary(string='Certificación')
    inscripcion = fields.Binary(string='Inscripción')
