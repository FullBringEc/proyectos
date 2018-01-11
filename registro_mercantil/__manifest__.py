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
    "name": "Registro Mercantil",
    "version": "1.0",
    "author": "RubikSoft",
    'website': 'http://www.facebook.com/RubikSoft15.com',
    "description": """Modulo que permite Crear, Obtener, Actualizar y Borrar informacion de tipos de Archivos""",

    "depends": ["base","web","account"],
    #'js': ['static/src/js/resource.js'],
    "data": [

              "view/compania_reg_view.xml",

              'wizard/informe_view.xml',
              "views/pdf_binary_template_widget.xml",

              "security/registro_security.xml",
              "security/ir.model.access.csv",
              'sequence.xml',
              "cron/pdf_cron.xml",
              'data/rbs.tramite.propiedad.csv',
              'data/rbs.tipo.libro.propiedad.csv',
              'data/rbs.tramite.mercantil.csv',
              'data/rbs.tipo.libro.mercantil.csv',

              'data/rbs.nombramiento.mercantil.csv',
              'data/rbs.provincia.csv',
              'data/rbs.canton.csv',
              'data/rbs.parroquia.csv',
              'data/rbs.calidad.compareciente.csv',
              'data/rbs.tipo.interviniente.csv',
              'data/rbs.zona.csv',
              'data/rbs.tipo.gravamen.csv',
              'data/rbs.tipo.tramite.csv',
              'data/rbs.tipo.bien.csv',



              "view/valores_view.xml",
              "view/factura_view.xml",
              "view/imagen_view.xml",
              "view/valores_division_politica_view.xml",
              "view/valores_persona_view.xml",
              "view/rbs_documento_propiedad.xml",
              "view/rbs_documento_mercantil.xml",
              "view/rbs_anio_view.xml",
              "view/rbs_libro_view.xml",
              "view/rbs_tomo_view.xml",
              "view/tarea_view.xml",
              'wizard/informe_view.xml',
              'view/certificado_propiedad_view.xml',
              'view/certificado_mercantil_view.xml',
              "view/rbs_documento_certificaciones.xml",
              'views/tiffEdit.xml',
              'views/assets_backend.xml',

    ],
    'qweb': ['static/src/xml/widget.xml'],
    "demo": [],
    "active": False,
    "installable": True,
    "certificate": "",
    'application': True,
}
