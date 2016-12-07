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
    "name" : "Registro Mercantil",
    "version" : "1.0",
    "author" : "RubikSoft",
    'website': 'http://www.facebook.com/RubikSoft15.com',
    "description": "Modulo que permite Crear, Obtener, Actualizar y Borrar informacion de tipos de Archivos",

    "depends" : ["widget_PDF","base","web"],
    
    'js': [],
    'qweb': [], 
    "data" : [
              #"view/crud_tabla_view.xml",
              "view/rbs_documento_mercantil_acta.xml",
              "view/rbs_documento_mercantil_vehiculo.xml",
              "view/rbs_documento_mercantil_propiedad.xml",
              "view/rbs_archivo_anio_view.xml",
              "view/rbs_archivo_libro_view.xml",
              "view/rbs_archivo_tomo_view.xml",
              'wizard/informe_view.xml'

    ],
    "demo" : [],
    "active":False,
    "installable": True,
    "certificate":"",
}

