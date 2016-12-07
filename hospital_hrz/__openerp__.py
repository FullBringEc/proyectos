# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module is Copyright (c) 2009-2013 General Solutions (http://gscom.vn) All Rights Reserved.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    "name" : "Hospital Rodriguez Zambrano",
    "version" : "1.0",
    "author" : "RubikSoft",
    'website': 'http://www.facebook.com/RubikSoft15',
    "description": "",

    "depends" : ["base",],
    
    'js': [],
    'qweb': [], 
    "data" : [
        "security/hospital_security.xml",
        "security/ir.model.access.csv",
        "comprobante_workflow.xml",
        "sequences.xml",
        "views/res_partner_view.xml",
        "views/comprobante_receta_view.xml",
        "views/comprobante_ingreso_medicamento_view.xml",
        "views/comprobante_ingreso_herramienta_view.xml",
        "views/comprobante_ingreso_material_view.xml",







        "views/comprobante_transferencia_view.xml",
        "views/comprobante_asignacion_view.xml",
        "views/bodega_view.xml",
        "views/bodegas_personales_view.xml",
        "views/producto_view.xml",
        "views/asset_view.xml",
        "views/impresion_receta_confirmad_view.xml",
        "views/producto_atributos_view.xml",
        "views/comprobante_transferencia_insumo_view.xml",
        "views/comprobante_asignacion_materiales_view.xml",
        "views/comprobante_asignacion_herramientas_view.xml",
        "views/producto_lote_view.xml",
        "data/bodega_data.xml",
        "data/presentacion_data.xml",
        "data/viaadministracion_data.xml",
        "report/report_comprobantes.xml",
        "report/layouts.xml",
        "report/wizart_report_kardex.xml",
        "report/report_kardex.xml",
        "comprobante_report.xml",
        

    ],
    "installable": True,
    'auto_install': False,
}


