# -*- encoding: utf-8 -*-
########################################################################


from openerp.osv import fields,osv
from openerp import  models, fields as field, api
import openerp.addons.decimal_precision as dp
from openerp.tools.translate import _
from openerp.tools import config
import time
from xml.etree.ElementTree import Element, SubElement, ElementTree, tostring
import sys
import base64
import xlwt
import time
import datetime
#import StringIO
from io import BytesIO , StringIO
import gzip
from docxtpl import DocxTemplate, RichText

#from xlsxwriter import workbook as Workbook
#import StringIO


class rbs_certificado_propiedad(osv.osv):
    _name = 'rbs.certificado.propiedad'
    def generate_word(self, cr, uid, ids, context=None):
        datos  = self.read(cr, uid, ids, context=context)[0]
        # elId = repr(datos['caczxcgs<'])


        output = BytesIO()
        # import os

        tpl=DocxTemplate('certificado.docx')
        bien_obj =  self.pool.get('rbs.bien')
        bien_ids = bien_obj.search(cr, uid, [('clave_catastral', '=', datos['clave_catastral'])], context=context)
        bienes = bien_obj.browse(cr, uid, bien_ids, context=context)
        user = self.pool.get('res.users').browse(cr, uid, [uid], context=context)[0]
        resumen = []
        libro = {}
        for bien in bienes:
            detalle = {}
            doc = None
            if bien.documento_mercantil_id:
                doc = bien.documento_mercantil_id
            else:
                doc = bien.documento_propiedad_id

            detalle['libro'] = doc.libro_id.name
            detalle['acto'] = doc.tipo_tramite_id.name
            detalle['numero'] = RichText (str (doc.numero_inscripcion))
            detalle['finscrip'] = RichText (str (doc.fecha_inscripcion))
            detalle['finicial'] = RichText (str(doc.foleo_desde))
            detalle['ffinal'] = RichText (str(doc.foleo_hasta))
            resumen.append(detalle)
            if libro.has_key(doc.libro_id.name):
                libro[doc.libro_id.name] = libro[doc.libro_id.name]+1
            else:
                libro[doc.libro_id.name] = 1

        movimientos  = []

        for clave in libro:

            detalle = {}
            l = clave
            ni = libro[clave]
            # raise osv.except_osv('Esto es un Mesaje!',str(ni))
            detalle['libro'] = l
            detalle['sumainscrp'] = RichText (str(ni))

            movimientos.append(detalle)

        context = {
            'campo' : RichText ('fecha'),
            'resumen' : resumen,
            'ccatastral': RichText (str (bien.clave_catastral)),
            'fapertura' : RichText (str (doc.fecha_adjudicion)),
            'infmuni' : RichText (str (doc.canton_notaria_id.name)),
            'tpredio' : RichText (str (bien.descripcion_bien)),
            'parroquia' : RichText (str (bien.parroquia_id.name)),
            'lindero' : RichText (str (bien.descripcion_lindero)),
            'nombresoli' : RichText (str (datos['solicitante'])),
            'sesion' : RichText (str (user.name)),
            'fechaactual' : RichText ( str (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))),
            'movimientos':movimientos,

        }

        tpl.render(context)
        tpl.save(output)

        self.write( cr, uid, ids,{'dataWord':base64.b64encode(output.getvalue())})
        return self.download_word( cr, uid, ids, context=None)
        # return base64.b64encode(output.getvalue())
    
    def word(self, cr, uid, ids, context=None):
        out = self.generate_word( cr, uid, ids, context=None)
        self.write( cr, uid, ids,{'dataWord':out})
        return self.download_word( cr, uid, ids, context=None)

    def download_word(self, cr, uid, ids, context=None):
        data = self.browse(cr, uid, ids[0], context=context)
        context = dict(context or {})
        return {
                'type' :    'ir.actions.act_url',
                'url':      '/web/binary/download_document?model=rbs.certificado.propiedad&field=dataWord&id=%s&filename=Certificado.docx'%(str(ids[0])),
                'target':   'new'
            }

    
    
    # _columns = {
                
                
    # }
    # clave_catastral = field.Char('Clave Catastral', size=30, required=True)
    # cedula = field.Char('Cedula', size=30, required=True)
    solicitante = field.Char('Solicitante', size=90, required=True)
    dataWord=field.Binary("word")
    state=field.Selection([
        ('draft','Borrador'),
        ('done','Realizado'),
        ('error','Error'),
        # ('deactivated','Desactivado')
        ], string = 'Estado', index=True, default='draft')


    propiedad_ids = field.Many2many('rbs.documento.propiedad',string ='Documentos')
    criterio_busqueda = field.Selection([
        ('cedula','Cedula'),
        ('clave_catastral','Clave Catastral'),
        ], string="Criterio de busqueda")

    valor_busqueda = field.Char('Busqueda', size=30, required=True)

    @api.onchange('valor_busqueda','criterio_busqueda')
    def get_documentos(self):
        if self.state == 'draft':
            # resultado=None
            if self.criterio_busqueda == 'cedula':
                #######  buscar todos las inscripciones donde el comprador tenga la cedula buscada
                claves_catastrales = []
                resultado_sin_filtrar = self.env['rbs.documento.propiedad'].search(
                    [
                    ('parte_ids.num_identificacion', '=', self.valor_busqueda),
                    ('parte_ids.tipo_interviniente_id.name', '=', 'COMPRADOR'),
                    ],
                    order='fecha_inscripcion desc')

                #######  Hacer una lista de todas las claves catastrales
                for res in resultado_sin_filtrar:
                    for bien in res.bien_ids:
                        # print str(bien.clave_catastral)
                        if bien.clave_catastral:
                            claves_catastrales.append(bien.clave_catastral)
                ####### elmininar claves repetidas
                claves_catastrales = list(set(claves_catastrales))
                print str(claves_catastrales)
                ####### busca el ultimo movimiento de cada una de las claves catastrales y las agrega al campo 'propiedad_ids'
                self.propiedad_ids = None
                for clv_cat in claves_catastrales:
                    
                    resultado = self.env['rbs.documento.propiedad'].search(
                        [
                        ('bien_ids.clave_catastral', '=', clv_cat),
                        ],limit=1,
                        order='fecha_inscripcion desc')
                    for parte in resultado.parte_ids:
                        if parte.num_identificacion == self.valor_busqueda:
                            self.propiedad_ids |= resultado

            elif self.criterio_busqueda == 'clave_catastral':
                resultado = self.env['rbs.documento.propiedad'].search(
                        [
                        ('bien_ids.clave_catastral', '=', self.valor_busqueda),
                        ],limit=1,
                        order='fecha_inscripcion desc')
                self.propiedad_ids = None
                self.propiedad_ids |= resultado



class rbs_documento_propiedad(models.Model):
    # _name ="rbs.documento.propiedad"
    _inherit ="rbs.documento.propiedad"
    _description = "Documento de la Propiedad"
    certificado_propiedad_ids = field.Many2many('rbs.certificado.propiedad',string ='Certificados Propiedad')
    # certificado_mercantil_ids = field.Many2many('rbs.certificado.mercantil',string ='Certificados Mercantil')
    dataWord=field.Binary("word")

    vendedor_virtual = field.Char(string="Vendedor",compute="get_vendedor")
    comprador_virtual = field.Char(string="Comprador",compute="get_comprador")
    clave_catastral_virtual = field.Char(string="Clave Catastral",compute="get_clave_catastral")
    descripcion_lindero_virtual = field.Char(string="Clave Catastral",compute="get_descripcion_lindero")
    canton_virtual = field.Char(string="Clave Catastral",compute="get_canton")
    @api.one
    def get_descripcion_lindero(self):
        descripcion_lindero_virtual=''
        for bien in self.bien_ids:
            # if parte.tipo_interviniente_id.name=='VENDEDOR':
            descripcion_lindero_virtual = bien.descripcion_lindero +'/'+ descripcion_lindero_virtual
        self.descripcion_lindero_virtual = descripcion_lindero_virtual

    @api.one
    def get_canton(self):
        canton_virtual=''
        for bien in self.bien_ids:
            # if parte.tipo_interviniente_id.name=='VENDEDOR':
            try:
                canton_virtual = bien.canton_id.name+'/'+ canton_virtual
            except:
                pass
        self.canton_virtual = canton_virtual


    @api.one
    def get_vendedor(self):
        vendedor_virtual=''
        for parte in self.parte_ids:
            if parte.tipo_interviniente_id.name=='VENDEDOR':
                vendedor_virtual = parte.nombres + ' ' + parte.apellidos +'/'+ vendedor_virtual
        self.vendedor_virtual = vendedor_virtual

    @api.one
    def get_comprador(self):
        comprador_virtual=''
        for parte in self.parte_ids:
            if parte.tipo_interviniente_id.name=='COMPRADOR':
                comprador_virtual = parte.nombres + ' ' + parte.apellidos +'/'+ comprador_virtual
        self.comprador_virtual = comprador_virtual

    @api.one
    def get_clave_catastral(self):
        clave_catastral_virtual=''
        for bien in self.bien_ids:
            clave_catastral_virtual = bien.clave_catastral +'/'+ clave_catastral_virtual
        self.clave_catastral_virtual = clave_catastral_virtual




    @api.one
    def imprimirCertificado(self):
        
        return self.word()
        # raise osv.except_osv('Esto es un Mesaje!','Hola')
    def generate_word(self, cr, uid, ids, context=None):
        datos  = self.read(cr, uid, ids, context=context)[0]
        # elId = repr(datos['caczxcgs<'])

        raise osv.except_osv('Esto es un Mesaje!',str(datos))
        output = BytesIO()
        # import os

        tpl=DocxTemplate('certificado.docx')
        bien_obj =  self.pool.get('rbs.bien')
        bien_ids = bien_obj.search(cr, uid, [('clave_catastral', '=', datos['clave_catastral'])], context=context)
        bienes = bien_obj.browse(cr, uid, bien_ids, context=context)
        user = self.pool.get('res.users').browse(cr, uid, [uid], context=context)[0]
        resumen = []
        libro = {}
        for bien in bienes:
            detalle = {}
            doc = None
            if bien.documento_mercantil_id:
                doc = bien.documento_mercantil_id
            else:
                doc = bien.documento_propiedad_id

            detalle['libro'] = doc.libro_id.name
            detalle['acto'] = doc.tipo_tramite_id.name
            detalle['numero'] = RichText (str (doc.numero_inscripcion))
            detalle['finscrip'] = RichText (str (doc.fecha_inscripcion))
            detalle['finicial'] = RichText (str(doc.foleo_desde))
            detalle['ffinal'] = RichText (str(doc.foleo_hasta))
            resumen.append(detalle)
            if libro.has_key(doc.libro_id.name):
                libro[doc.libro_id.name] = libro[doc.libro_id.name]+1
            else:
                libro[doc.libro_id.name] = 1

        movimientos  = []

        for clave in libro:

            detalle = {}
            l = clave
            ni = libro[clave]
            # raise osv.except_osv('Esto es un Mesaje!',str(ni))
            detalle['libro'] = l
            detalle['sumainscrp'] = RichText (str(ni))

            movimientos.append(detalle)

        context = {
            'campo' : RichText ('fecha'),
            'resumen' : resumen,
            'ccatastral': RichText (str (bien.clave_catastral)),
            'fapertura' : RichText (str (doc.fecha_adjudicion)),
            'infmuni' : RichText (str (doc.canton_notaria_id.name)),
            'tpredio' : RichText (str (bien.descripcion_bien)),
            'parroquia' : RichText (str (bien.parroquia_id.name)),
            'lindero' : RichText (str (bien.descripcion_lindero)),
            'nombresoli' : RichText (str (datos['solicitante'])),
            'sesion' : RichText (str (user.name)),
            'fechaactual' : RichText ( str (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))),
            'movimientos':movimientos,

        }

        tpl.render(context)
        tpl.save(output)

        self.write( cr, uid, ids,{'dataWord':base64.b64encode(output.getvalue())})
        return self.download_word( cr, uid, ids, context=None)
        # return base64.b64encode(output.getvalue())
    
    def word(self, cr, uid, ids, context=None):
        out = self.generate_word( cr, uid, ids, context=None)
        self.write( cr, uid, ids,{'dataWord':out})
        return self.download_word( cr, uid, ids, context=None)

    def download_word(self, cr, uid, ids, context=None):
        data = self.browse(cr, uid, ids[0], context=context)
        context = dict(context or {})
        return {
                'type' :    'ir.actions.act_url',
                'url':      '/web/binary/download_document?model=rbs.documento.propiedad&field=dataWord&id=%s&filename=Certificado.docx'%(str(ids[0])),
                'target':   'new'
            }