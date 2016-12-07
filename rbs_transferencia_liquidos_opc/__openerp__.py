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
    "name" : "OPC Transferencia de liquidos",
    "version" : "1.0",
    "author" : "RubikSoft",
    'website': 'http://www.facebook.com/RubikSoft15.com',
    "description": "Modulo para conectar con servidor opc ",

    "depends" : ["base","stock",],
    
    'js': [],
    'qweb': [], 
    "data" : [
        "views/stock_location.xml",
        "rbs_opc_config.xml"
    ],
    "demo" : [],
    "active":True,
    "installable": False,
    "certificate":"",
}

