# -*- encoding: utf-8 -*-
########################################################################


from openerp import models,  api, _
from openerp.osv import osv,fields
import openerp.addons.decimal_precision as dp
from openerp.tools.translate import _
from openerp.tools import config
import time
from xml.etree.ElementTree import Element, SubElement, ElementTree, tostring
import sys
import base64
import xlwt
from datetime import datetime , timedelta
import time
#import StringIO
from io import BytesIO , StringIO
import gzip
from openerp.exceptions import (
    except_orm,
    Warning as UserError,
    RedirectWarning
    )

#from xlsxwriter import workbook as Workbook
#import StringIO


class rbs_informe(osv.osv_memory):
    @api.one
    def generate_excel(self):
        
        output = BytesIO()
        ext = '.xls'
        style0 = xlwt.easyxf('font: name Times New Roman, colour red, bold on')
        style1 = xlwt.easyxf('',num_format_str='$#,##0.00')
        wb = xlwt.Workbook(encoding="utf-8")
        ws = wb.add_sheet('Hoja de Calculo',cell_overwrite_ok=True)

        if self.tipo == "propiedad":

            inscripcion_ids = self.env['rbs.documento.propiedad'].search([('fecha_inscripcion', '>=', self.fecha_inicio),('fecha_inscripcion', '<', (datetime.strptime(self.fecha_fin, '%Y-%m-%d')+ timedelta(days=1)).strftime('%Y-%m-%d'))])
            i=0  
            for line in inscripcion_ids:
                bienes = {}
                for bien_line in line.bien_ids:
                    for p_line in bien_line.parte_char_ids:
                        bienes[p_line.parte_id.id] = p_line.bien_ids


                for parte_line in line.parte_ids:
                    ws.write(i, 0, line.tramite_id.name or '')
                    ws.write(i, 1, line.tipo_tramite_id.name or '')
                    ws.write(i, 2, line.libro_id.tipo_libro_propiedad_id.name or '')
                    ws.write(i, 3, line.repertorio or '')
                    ws.write(i, 4, line.fecha_repertorio or '')
                    ws.write(i, 5, line.numero_inscripcion or '')
                    ws.write(i, 6, line.fecha_inscripcion or '')
                    ws.write(i, 7, parte_line.tipo_persona or '')
                    ws.write(i, 8, parte_line.razon_social or '')
                    ws.write(i, 9, parte_line.apellidos or '')
                    ws.write(i, 10, parte_line.nombres or '')
                    ws.write(i, 11, parte_line.tipo_interviniente_id.name or '')
                    ws.write(i, 12, parte_line.calidad_compareciente_id.name or '')
                    ws.write(i, 13, parte_line.tipo_documento or '')
                    ws.write(i, 14, parte_line.num_identificacion or '')
                    ws.write(i, 15, parte_line.estado_civil or '')
                    ws.write(i, 16, parte_line.nombres_conyuge or '')
                    ws.write(i, 17, parte_line.num_identificacion_conyuge or '')                    
                    ws.write(i, 18, parte_line.separacion_bienes or '')

                    try:
                        numero_predial = '|'.join([b.numero_predial for b in bienes[parte_line.id]] )
                        ws.write(i, 19, numero_predial or '')
                    except:
                        pass

                    try:
                        clave_catastral = '|'.join([b.clave_catastral for b in bienes[parte_line.id]] )
                        ws.write(i, 20, clave_catastral or '')
                    except:
                        pass

                    try:
                        descripcion_bien = '|'.join([b.descripcion_bien for b in bienes[parte_line.id]] )
                        ws.write(i, 21, descripcion_bien or '')
                    except:
                        pass

                    try:
                        descripcion_bien = '|'.join([b.descripcion_bien for b in bienes[parte_line.id]] )
                        ws.write(i, 22, descripcion_bien or '')
                    except:
                        pass

                    try:
                        provincia_id = '|'.join([b.provincia_id.name for b in bienes[parte_line.id]] )
                        ws.write(i, 23, provincia_id or '')
                    except:
                        pass

                    try:
                        zona_id = '|'.join([b.zona_id.name for b in bienes[parte_line.id]] )
                        ws.write(i, 24, zona_id or '')
                    except:
                        pass


                    try:
                        superficie_area_numero = '|'.join([b.superficie_area_numero for b in bienes[parte_line.id]] )
                        ws.write(i, 25, superficie_area_numero or '')
                    except:
                        pass

                    
                    try:
                        ubicacion_geografica = '|'.join([b.ubicacion_geografica for b in bienes[parte_line.id]] )
                        ws.write(i, 26, ubicacion_geografica or '')
                    except:
                        pass                    


                    try:
                        descripcion_lindero = '|'.join([b.descripcion_lindero for b in bienes[parte_line.id]] )
                        ws.write(i, 27, descripcion_lindero or '')
                    except:
                        pass

                    try:
                        parroquia_id = '|'.join([b.parroquia_id.name for b in bienes[parte_line.id]] )
                        ws.write(i, 28, parroquia_id or '')
                    except:
                        pass

                    try:
                        canton_id = '|'.join([b.canton_id.name for b in bienes[parte_line.id]] )
                        ws.write(i, 29, canton_id or '')
                    except:
                        pass


                    ws.write(i, 30, line.cuantia_valor or '')
                    ws.write(i, 31, line.cuantia_unidad or '')
                    # ws.write(i, 33, '03'+line.canton_notaria_id.name+parte_line.num_identificacion+line.numero_inscripcion or '')
                    ws.write(i, 32, line.gravamen_limitacion or '')
                    
                    # try:
                    #     tipo_gravamen = '|'.join([b.marginacion_propiedad_tramite_origi_id.name for b in line.tipo_gravamen_ids] )
                    #     ws.write(i, 33, tipo_gravamen or '')
                    # except:
                    #     pass    
                    ws.write(i, 35, line.fecha_const_gravamen or '')
                    ws.write(i, 36, line.fecha_cancel_gravamen or '')
                    ws.write(i, 37, line.fecha_ultima_modificacion_inscripcion or '')
                    ws.write(i, 38, line.fecha_cancel_gravamen or '')
                    ws.write(i, 39, line.canton_notaria_id.name or '')
                    ws.write(i, 40, line.notaria_id.name or '')
                    ws.write(i, 41, line.canton_notaria_id.name or '')
                    ws.write(i, 42, line.fecha_escritura or '')

                    try:
                        propiedad_horizontal = '|'.join([b.propiedad_horizontal for b in bienes[parte_line.id]] )
                        ws.write(i, 43, propiedad_horizontal or '')
                    except:
                        pass
                    ws.write(i, 44, line.expensas or '')
                    ws.write(i, 45, parte_line.es_menor or '')
                    ws.write(i, 46, parte_line.tutor or '')
                    ws.write(i, 47, line.fecha_adjudicion or '')
                    ws.write(i, 48, line.fecha_insi_bienes or '')
                    ws.write(i, 49, line.numero_acuerdo_ministerial or '')
                    ws.write(i, 50, line.causante or '')
                    ws.write(i, 51, line.fecha_defuncion or '')

                    i=i+1   
                
                               




        else:
            inscripcion_ids = self.env['rbs.documento.mercantil'].search([('fecha_inscripcion', '>=', self.fecha_inicio),('fecha_inscripcion', '<', (datetime.strptime(self.fecha_fin, '%Y-%m-%d')+ timedelta(days=1)).strftime('%Y-%m-%d'))])
    
            i=0   
            for line in inscripcion_ids:
                bienes = {}
                for bien_line in line.bien_ids:
                    for p_line in bien_line.parte_char_ids:
                        bienes[p_line.parte_id.id] = p_line.bien_ids
                
               
                    
                for parte_line in line.parte_ids:

                    ws.write(i, 0, line.tramite_id.name or '')
                    ws.write(i, 1, line.tipo_tramite_id.name or '')
                    ws.write(i, 2, line.libro_id.tipo_libro_mercantil_id.name or '')
                    ws.write(i, 3, parte_line.apellidos or '')
                    ws.write(i, 4, parte_line.nombres or '')
                    ws.write(i, 5, parte_line.estado_civil or '')
                    ws.write(i, 6, parte_line.nombres_conyuge or '')
                    ws.write(i, 7, parte_line.num_identificacion_conyuge or '')
                    ws.write(i, 8, parte_line.num_identificacion or '')
                    ws.write(i, 9, parte_line.tipo_interviniente_id.name or '')
                    ws.write(i, 10, parte_line.calidad_compareciente_id.name or '')
                    ws.write(i, 11, line.repr_razon_social or '')
                    ws.write(i, 12, line.repr_acreedor or '')
                    ws.write(i, 13, line.repertorio or '')
                    ws.write(i, 14, line.fecha_repertorio or '')
                    ws.write(i, 15, line.fecha_inscripcion or '')
                    ws.write(i, 16, line.numero_inscripcion or '')
                    ws.write(i, 17, line.fecha_cancelacion or '')
                    try:
                        tipobien = '|'.join([b.tipo_bien_id.name for b in bienes[parte_line.id]] )
                        ws.write(i, 18, tipobien or '')
                    except:
                        pass
                    try:
                        chasis = '|'.join([b.chasis for b in bienes[parte_line.id]] )
                        ws.write(i, 19, chasis or '')
                    except:
                        pass
                    try:
                        motor = '|'.join([b.motor for b in bienes[parte_line.id]] )
                        ws.write(i, 20, motor or '')
                    except:
                        pass
                    try:
                        marca = '|'.join([b.marca for b in bienes[parte_line.id]] )
                        ws.write(i, 21, marca or '')
                    except:
                        pass

                    try:
                        modelo = '|'.join([b.modelo for b in bienes[parte_line.id]] )
                        ws.write(i, 22, modelo or '')
                    except:
                        pass

                    try:
                        anio_fabricacion = '|'.join([b.anio_fabricacion.name for b in bienes[parte_line.id]] )
                        ws.write(i, 23, anio_fabricacion or '')
                    except:
                        pass

                    try:
                        placa = '|'.join([b.placa for b in bienes[parte_line.id]] )
                        ws.write(i, 24, placa or '')
                    except:
                        pass

                    try:
                        color = '|'.join([b.color for b in bienes[parte_line.id]] )
                        ws.write(i, 25, color or '')
                    except:
                        pass

                    try:
                        numero_provisional = '|'.join([(b.numero_provisional or '-') for b in bienes[parte_line.id]] )
                        ws.write(i, 26, numero_provisional or '')
                    except:
                        pass

                    ws.write(i, 27, line.canton_notaria_id.name or '')
                    ws.write(i, 28, line.fecha_ultima_modificacion or '')
                    # ws.write(i, 29, '03'+line.canton_notaria_id.name+parte_line.num_identificacion+line.numero_inscripcion or '')
                    ws.write(i, 30, line.provincia_notaria_id.name or '')
                    ws.write(i, 31, line.canton_notaria_id.name or '')
                    ws.write(i, 32, line.fecha_escritura or '')
                    ws.write(i, 33, line.fecha_ultima_modificacion or '')
                    ws.write(i, 34, line.libro_id.name or '')
                    # ws.write(i, 35, line.repr_nombramiento_id.name or '')
                    ws.write(i, 36, line.repr_nombramiento_id.name or '')
                    ws.write(i, 37, line.repr_apellido or '')
                    ws.write(i, 38, line.repr_nombre or '')
                    ws.write(i, 39, line.repr_identificacion or '')
                    ws.write(i, 40, line.cuantia_valor or '')


                    # ws.write(i, 41, numero accionista or '')

                    try:
                        nombre_accionista = '|'.join([b.accionista_nombre for b in line.accionista_ids] )
                        ws.write(i, 42, nombre_accionista or '')
                    except:
                        pass

                    try:
                        accionista_porcentaje_acciones = '|'.join([b.accionista_porcentaje_acciones for b in line.accionista_ids] )
                        ws.write(i, 43, accionista_porcentaje_acciones or '')
                    except:
                        pass

                    try:
                        accionista_valor_accion = '|'.join([b.accionista_valor_accion for b in line.accionista_ids] )
                        ws.write(i, 44, accionista_valor_accion or '')
                    except:
                        pass

                    ws.write(i, 45, line.fecha_acta_junta or '')
                    ws.write(i, 46, line.fecha_nombramiento or '')
                    ws.write(i, 47, line.nombramiento_mercantil_id.name or '')
                    # ws.write(i, 48, line.plazo_nombramiento_cant or '')
                    # ws.write(i, 49, line. or '')
                    ws.write(i, 50, line.fecha_const_gravamen or '')
                    ws.write(i, 51, line.fecha_cancel_gravamen or '')
                    i=i+1
    
                    


        # Registrosats = self.browse(cr, uid, ids, context=context)[0]

        # consulta = "select * from rbs_documento_mercantil_propiedad"
        # if Registrosats['tipo']=='propiedad':
        #     consulta=("select rbs_documento_mercantil_propiedad.persona_apellidos as \"Apellidos(n)\", rbs_documento_mercantil_propiedad.persona_nombres as \"Nombres(n)\", persona_cedula as \"Número de Identificación()n\","+
        #                 "(select rbs_tipo_compareciente_a.name from rbs_tipo_compareciente_a where rbs_documento_mercantil_propiedad.tipo_compareciente_id = rbs_tipo_compareciente_a.id ) as \"Tipo de Compareciente(n)\",rbs_documento_mercantil_propiedad.\"persona_razonSocial\" as \"Razón Social\","+
        #                 "(select rbs_tipo_contrato.name from rbs_tipo_contrato where rbs_tipo_contrato.id= rbs_documento_mercantil_propiedad.tipo_contrato_id ) as \"Tipo de Contrato\", rbs_documento_mercantil_propiedad.numero_inscripcion as \"Número de Inscripcón\", rbs_documento_mercantil_propiedad.fecha_inscripcion as \"Fecha de Inscripción\",rbs_documento_mercantil_propiedad.clave_catastral as \"Clave Catastral\","+
        #                 "(select rbs_tipo_bien.name from rbs_tipo_bien where rbs_tipo_bien.id=rbs_documento_mercantil_propiedad.tipo_bien_id) as \"Descripción del Bien \","+
        #                 "(select rbs_archivo_libro.name from rbs_archivo_libro where rbs_archivo_libro.id=rbs_documento_mercantil_propiedad.libro_id ) as \"Libro\" , "+
        #                 "(select rbs_provincia.name from rbs_provincia where rbs_provincia.id=rbs_documento_mercantil_propiedad.provincia_id ) as \"Provincia\" , "+
        #                 "(select rbs_zona.name from rbs_zona where rbs_zona.id= rbs_documento_mercantil_propiedad.zona_nombre_id  ) as \"Zona\" ,"+
        #                 "rbs_documento_mercantil_propiedad.superficie_bien as \"Superficie\","+
        #                 "rbs_documento_mercantil_propiedad.orientacio_lindero as \"Lindero-Orientación\","+
        #                 "rbs_documento_mercantil_propiedad.descripcion_lindero as \"Lindero-Descripción\","+
        #                 "rbs_documento_mercantil_propiedad.parroquia_nombre as \"Parroquia\","+
        #                 "(select rbs_canton.name from rbs_canton where rbs_canton.id= rbs_documento_mercantil_propiedad.canton_nombre_id) as \"Cantón\" ,"+
        #                 "rbs_documento_mercantil_propiedad.cuantia_valor as \"Cuantía\","+
        #                 "rbs_documento_mercantil_propiedad.cuantia_unidad as \"Unidada Cuantía\","+
        #                 "rbs_documento_mercantil_propiedad.identificacion_unica as \"Identificador Único Sistema Remoto\","+
        #                 "rbs_documento_mercantil_propiedad.juicio_numero as \"Número de Juicio\","+
        #                 "(select rbs_estado_inscripcion.name from rbs_estado_inscripcion where rbs_estado_inscripcion.id = rbs_documento_mercantil_propiedad.estado_inscripcion_id) as \"Ubicación de dato\" ,"+
        #                 "(select  rbs_ubicacion_dato.name from rbs_ubicacion_dato where rbs_ubicacion_dato.id=  rbs_documento_mercantil_propiedad.ubicacion_dato_id) as \"Ubicación de dato\" ,"+
        #                 "rbs_documento_mercantil_propiedad.modificacion_fuente as \"Última Modificación de la Fuente\","+
        #                 "rbs_documento_mercantil_propiedad.notaria_juzgado_entidad as \"Notaría/Juzgado/Entidad Pública\", "+
        #                 "(select rbs_canton.name from rbs_canton where rbs_canton.id= rbs_documento_mercantil_propiedad.canton_nombre_id ) as \"Cantón de la Notaría\" ,"+  
        #                 "rbs_documento_mercantil_propiedad.escritura_fecha as \"Fecha de Escritura\" from rbs_documento_mercantil_propiedad"+
        #                 " where rbs_documento_mercantil_propiedad.fecha_inscripcion>='"+ Registrosats['fecha_inicio']+"' and rbs_documento_mercantil_propiedad.fecha_inscripcion <='"+Registrosats['fecha_fin']+"'")
        
        #raise osv.except_osv('Esto es un asd!',consulta)
        # cr.execute(consulta.decode("utf-8", "replace"))
        
        # regi = cr.fetchall()

        # #num_fields = len(cr.description)
        # #field_names = [i[0] for i in cursor.description]
        # for i in range(len(cr.description)):
        #     ws.write(0, i, cr.description[i][0])

        # for i in range(len(regi)):
        #     for j in range(len(regi[i])):
        #         ws.write(i+1, j, regi[i][j])
        
        #ws.write(0, 0, 'Teasdaslkajsdlkjakldjaskldjklasjdlkasjdkljaskdjaksjdkajskdjassldsf;shflst', style0) #5632
        #ws.write(1, 0, datetime.now(), style1)
        #ws.write(2, 0, 4)
        #ws.write(2, 1, 7)
        #ws.write(3, 1, 4)
        #ws.write(2, 2, xlwt.Formula("A3+B3"))

        wb.save(output)
            
        
        #raise osv.except_osv('Esto es un asd!',Registrosats['tipo'] + Registrosats['fecha_inicio'] + Registrosats['fecha_fin'])
        # Saving file
        
        return base64.b64encode(output.getvalue())# base64.encodestring(f.read())
        

    def act_export(self, cr, uid, ids, context={}):
        this = self.browse(cr, uid, ids)[0]
        #root = self.generate_excel(cr,uid,ids)
        name_arch = "Reporte.xls"
        #self._write_attachment(cr,uid,ids,root,context)
        out = self.generate_excel(cr,uid,ids)
        self.write(cr, uid, ids, {'data':out, 'name':name_arch, 'state': 'get'}, context=context)
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


    

    _name = 'rbs.informe'
    
    _columns = {
                'name':fields.char('name', size=20, readonly=True), 
                #'fiscalyear_id':fields.many2one('account.fiscalyear', 'Fiscal Year', required=True),
                'fecha_inicio':fields.date('Dia inicial', required=True),
                'fecha_fin':fields.date('Dia final ', required=True),
                'data':fields.binary('File', readonly=True),
                'tipo':fields.selection([('mercantil','Registro Mercantil'),('propiedad','Registro Propiedad')],  'Elija el informe', required=True),
                'state':fields.selection([('choose','Choose'),('get','Get'),],  'state', required=True, readonly=True),}
    _defaults = {
                 'state': lambda *a: 'choose'
                 }
    
rbs_informe()