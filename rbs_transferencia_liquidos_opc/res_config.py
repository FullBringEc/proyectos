# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Business Applications
#    Copyright (C) 2004-2012 OpenERP S.A. (<http://openerp.com>).
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

from openerp.osv import osv
from openerp import pooler, fields, api, models
from openerp.tools.translate import _


class rbs_opc_config_settings(models.Model):
    _name = 'rbs.opc.config.settings'
    _inherit = 'res.config.settings'
    _rec_name = 'opc_ip'
    
    #default_name = fields.char(default_model='your.other.model')
    
    opc_ip = fields.Char(string ='Direccion del Servidor OPC',
     #compute='_default_opc_ip'
     )
    relacion_ids = fields.One2many(
        comodel_name='rbs.relacion',
        inverse_name='opc_conf_id',
        #compute='default_get'
    )

    @api.model
    def get_opc_ip(self):
        self._cr.execute(
            """ select opc_ip from rbs_opc_config_settings order by id desc limit 1""")
        dat = self._cr.dictfetchall()[0]
        #try:
        if dat['opc_ip'] != '' and dat['opc_ip'] !=None:
            return str(dat['opc_ip'])
        else:
            raise osv.except_osv('Configuracion',"Revise la direccion del Opc en Configuracion")
        #except:
        #    raise osv.except_osv('Error en configuracion',"Revise la direccion del Opc en Configuracion")
                

    @api.model
    def default_get(self,vals):
        res = super(rbs_opc_config_settings, self).default_get(vals)
        self._cr.execute(
            """ select rbs_plc_id,stock_location_id from rbs_relacion """)
        dat = self._cr.dictfetchall()
        self._cr.execute(
            """ delete from rbs_relacion """)
        dwz = self.env['rbs.relacion']
        dws = []
        if dat:
            for rbs_relacion in dat:
                try:
                    dw = dwz.create({
                        'rbs_plc_id':int(rbs_relacion['rbs_plc_id']),
                        'stock_location_id':int(rbs_relacion['stock_location_id']),
                    })
                    dws.append(dw.id)
                except:
                    pass


        opc_ip = False
        self._cr.execute(
            """ select max(id) as opc_ip_id from rbs_opc_config_settings """)
        dat = self._cr.dictfetchall()
        data = dat and dat[0]['opc_ip_id'] or False
        if data:
            opc_ip = self.browse(data).opc_ip
        res.update({
                        'relacion_ids':dws, # Many2one field
                        'opc_ip': opc_ip
                       })

        return res
    
#class YourSettings(models.TransientModel):
#    _inherit = 'res.config.settings'
#    _name = 'your.config.settings'