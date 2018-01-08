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
    "name" : "Widget para visualizar PDF",
    "version" : "1.0",
    "author" : "RubikSoft",
    'website': 'http://www.facebook.com/RubikSoft15',
    "description": "Agrega un widget para visualizar pdf",
    "category":"web",
    "depends" : ["base_setup","base","web"],
    "data" : [
              #"view/crud_tabla_view.xml",
              "view/web_pdf_widget_view.xml",
              "ftp_config.xml",
              "ir_parameter.xml",

    ],
    'qweb': [
      'static/src/xml/widget.xml'
    ], 
    'license': 'AGPL-3',
    'auto_install': False,
    'installable': True,
    'web_preload': True,
}

