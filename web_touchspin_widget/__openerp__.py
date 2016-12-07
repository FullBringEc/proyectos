# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2016 ePillars Systems (<http://epillars.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Web touchspin Widget',
    'version': '1.0',
    'category': 'Extra Tools',
    'summary': 'Display attractive range sliders for number selection in form view',
    'description': """ 
    
Web Touchspin Widget


        if (opt2.min
        if (opt2.max
        if (opt2.initval
        if (opt2.decimals
        if (opt2.postfix
        if (opt2.prefix
        if (opt2.step
        if (opt2.buttondown_txt!=undefined)
            options.buttondown_txt = opt2.buttondown_txt
        if (opt2.buttonup_txt!=undefined)
            options.buttonup_txt = opt2.buttonup_txt
        return options

  
=================
Add touchspin to char or int fields. For 2 way range, sliders, the field must be
of char type.

Usage
--------------

widget="touchspin" in Form View


Options
--------------

Use options as illustrated in the examples to define additional options for the widget

    * Minimum value.
        min: -50, 
    * Maximum value.
        max: 100, 
    * Applied when no explicit value is set on the input with the value attribute. 
    * Empty string means that the value remains empty on initialization.
        initval: '7',
    * Number of decimal points.
        decimals: 3,
    * Text after the input.
        postfix: '%', 
    * Text before the input.
        prefix: '$', 
    * Incremental/decremental step on up/down change.
        step: 0.5, 
    * Text for down button
        buttondown_txt: '-',
    * Text for up button
        buttonup_txt: '+'

Examples
--------------

<group>
    <field name="bedrooms" string="Bedrooms" 
            widget="touchspin" options="{'max':7,'min':1}" />
    
    <field name="area" 
            string="Built-up Area" 
            widget="touchspin" 
            options="{'step':0.5,'buttonup_txt':'MAS','buttondown_txt':'MENOS','max':10000}" />
    
</group>

Notes
--------------

Before setting the widget, avoid garbage values in the field to avoid errors.
                    
                    """,
    "author" : "RubikSoft",
    'website': 'http://www.facebook.com/RubikSoft15',
    'depends': ['base','web'],
    'data':[
            "views/touchspin_view.xml",
            ],
    'qweb':["static/src/xml/touchspin.xml"],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
   # 'price':1.00,
   # 'currency':'EUR',
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
