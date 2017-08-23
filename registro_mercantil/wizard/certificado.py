# -*- encoding: utf-8 -*-
########################################################################


from openerp.osv import fields,osv
from openerp import fields as field, api
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


class rbs_certificado(osv.osv_memory):

    def generate_excel(self, cr, uid, ids, context=None):
        output = BytesIO()
        style0 = xlwt.easyxf('font: name Times New Roman, colour red, bold on')
        style1 = xlwt.easyxf('',num_format_str='DD-MMM-YY')
        wb = xlwt.Workbook(encoding="utf-8")
        ws = wb.add_sheet('A Test Sheet',cell_overwrite_ok=True)
        Registrosats = self.browse(cr, uid, ids, context=context)[0]
        consulta = "select * from rbs_documento_mercantil_propiedad"
        if Registrosats['tipo']=='propiedad':
            consulta=("select rbs_documento_mercantil_propiedad.persona_apellidos as \"Apellidos(n)\", rbs_documento_mercantil_propiedad.persona_nombres as \"Nombres(n)\", persona_cedula as \"Número de Identificación()n\","+
                        "(select rbs_tipo_compareciente_a.name from rbs_tipo_compareciente_a where rbs_documento_mercantil_propiedad.tipo_compareciente_id = rbs_tipo_compareciente_a.id ) as \"Tipo de Compareciente(n)\",rbs_documento_mercantil_propiedad.\"persona_razonSocial\" as \"Razón Social\","+
                        "(select rbs_tipo_contrato.name from rbs_tipo_contrato where rbs_tipo_contrato.id= rbs_documento_mercantil_propiedad.tipo_contrato_id ) as \"Tipo de Contrato\", rbs_documento_mercantil_propiedad.numero_inscripcion as \"Número de Inscripcón\", rbs_documento_mercantil_propiedad.fecha_inscripcion as \"Fecha de Inscripción\",rbs_documento_mercantil_propiedad.clave_catastral as \"Clave Catastral\","+
                        "(select rbs_tipo_bien.name from rbs_tipo_bien where rbs_tipo_bien.id=rbs_documento_mercantil_propiedad.tipo_bien_id) as \"Descripción del Bien \","+
                        "(select rbs_archivo_libro.name from rbs_archivo_libro where rbs_archivo_libro.id=rbs_documento_mercantil_propiedad.libro_id ) as \"Libro\" , "+
                        "(select rbs_provincia.name from rbs_provincia where rbs_provincia.id=rbs_documento_mercantil_propiedad.provincia_id ) as \"Provincia\" , "+
                        "(select rbs_zona.name from rbs_zona where rbs_zona.id= rbs_documento_mercantil_propiedad.zona_nombre_id  ) as \"Zona\" ,"+
                        "rbs_documento_mercantil_propiedad.superficie_bien as \"Superficie\","+
                        "rbs_documento_mercantil_propiedad.orientacio_lindero as \"Lindero-Orientación\","+
                        "rbs_documento_mercantil_propiedad.descripcion_lindero as \"Lindero-Descripción\","+
                        "rbs_documento_mercantil_propiedad.parroquia_nombre as \"Parroquia\","+
                        "(select rbs_canton.name from rbs_canton where rbs_canton.id= rbs_documento_mercantil_propiedad.canton_nombre_id) as \"Cantón\" ,"+
                        "rbs_documento_mercantil_propiedad.cuantia_valor as \"Cuantía\","+
                        "rbs_documento_mercantil_propiedad.cuantia_unidad as \"Unidada Cuantía\","+
                        "rbs_documento_mercantil_propiedad.identificacion_unica as \"Identificador Único Sistema Remoto\","+
                        "rbs_documento_mercantil_propiedad.juicio_numero as \"Número de Juicio\","+
                        "(select rbs_estado_inscripcion.name from rbs_estado_inscripcion where rbs_estado_inscripcion.id = rbs_documento_mercantil_propiedad.estado_inscripcion_id) as \"Ubicación de dato\" ,"+
                        "(select  rbs_ubicacion_dato.name from rbs_ubicacion_dato where rbs_ubicacion_dato.id=  rbs_documento_mercantil_propiedad.ubicacion_dato_id) as \"Ubicación de dato\" ,"+
                        "rbs_documento_mercantil_propiedad.modificacion_fuente as \"Última Modificación de la Fuente\","+
                        "rbs_documento_mercantil_propiedad.notaria_juzgado_entidad as \"Notaría/Juzgado/Entidad Pública\", "+
                        "(select rbs_canton.name from rbs_canton where rbs_canton.id= rbs_documento_mercantil_propiedad.canton_nombre_id ) as \"Cantón de la Notaría\" ,"+  
                        "rbs_documento_mercantil_propiedad.escritura_fecha as \"Fecha de Escritura\" from rbs_documento_mercantil_propiedad"+
                        " where rbs_documento_mercantil_propiedad.fecha_inscripcion>='"+ Registrosats['fecha_inicio']+"' and rbs_documento_mercantil_propiedad.fecha_inscripcion <='"+Registrosats['fecha_fin']+"'")
        
        #raise osv.except_osv('Esto es un asd!',consulta)
        cr.execute(consulta.decode("utf-8", "replace"))
        
        regi = cr.fetchall()

        #num_fields = len(cr.description)
        #field_names = [i[0] for i in cursor.description]
        for i in range(len(cr.description)):
            ws.write(0, i, cr.description[i][0])

        for i in range(len(regi)):
            for j in range(len(regi[i])):
                ws.write(i+1, j, regi[i][j])
        
        #ws.write(0, 0, 'Teasdaslkajsdlkjakldjaskldjklasjdlkasjdkljaskdjaksjdkajskdjassldsf;shflst', style0) #5632
        #ws.write(1, 0, datetime.now(), style1)
        #ws.write(2, 0, 4)
        #ws.write(2, 1, 7)
        #ws.write(3, 1, 4)
        #ws.write(2, 2, xlwt.Formula("A3+B3"))

        wb.save(output)
            
        
        #raise osv.except_osv('Esto es un asd!',Registrosats['tipo'] + Registrosats['fecha_inicio'] + Registrosats['fecha_fin'])
        # Saving file
        
        # self.filedata =  # base64.encodestring(f.read())
        self.write( cr, uid, ids,{'dataWord':base64.encodestring(output.getvalue())})
        return self.download_word( cr, uid, ids, context=None)


        # self.write( cr, uid, ids,{'filedata':})
        # a = self.read(cr, uid, ids, context=context)[0]
        # elId = repr(a['id'])
        # return {
        #     'type': 'ir.actions.act_window',
        #     'res_model': 'rbs.certificado',
        #     'view_mode': 'form',
        #     'view_type': 'form',
        #     'res_id': int(elId),
        #     'views': [(False, 'form')],
        #     'target': 'new',
        #      }

        

    def act_export(self, cr, uid, ids, context={}):
        this = self.browse(cr, uid, ids)[0]
        #root = self.generate_excel(cr,uid,ids)
        this.name = "REPORTE.xls"
        #self._write_attachment(cr,uid,ids,root,context)
        out = self.generate_excel(cr,uid,ids)
        self.write(cr, uid, ids, {'data':out, 'name':this.name, 'state': 'get'}, context=context)
        a = self.read(cr, uid, ids, context=context)[0]
        elId = repr(a['id'])
        
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'rbs.informe',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': int(elId),
            'views': [(False, 'form')],
            'target': 'new',
             }


    dataWord=field.Binary("word")
    def generate_word(self, cr, uid, ids, context=None):

        datos  = self.read(cr, uid, ids, context=context)[0]
        # elId = repr(datos['caczxcgs<'])


        output = BytesIO()
        # import os

        tpl=DocxTemplate('certificado.docx')
        bien_obj =  self.pool.get('rbs.bien')
        bien_ids = bien_obj.search(cr, uid, [('clave_catastral', '=', datos['name'])], context=context)
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




            # 'telefono': 
            # 'fechaactual':
            # 'ccatastral':
            # 'fapertura':
            # 'infmuni':
            # 'tpredio':
            # 'parroquia':
            # 'lindero':
            # 'nombresoli':
            # 'sesion':

            

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
                'url':      '/web/binary/download_document?model=rbs.certificado&field=dataWord&id=%s&filename=Certificado.docx'%(str(ids[0])),
                'target':   'new'
            }

    _name = 'rbs.certificado'
    
    _columns = {
                'name':fields.char('Clave Catastral', size=30, required=True), 
                'solicitante':fields.char('Solicitante', size=90, required=True), 

                # 'filedata':fields.binary('archivo')
                #'fiscalyear_id':fields.many2one('account.fiscalyear', 'Fiscal Year', required=True),
                
    }
    
rbs_certificado()