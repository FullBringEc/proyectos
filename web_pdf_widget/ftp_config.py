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
    _name = 'ftp.config.settings'
    _inherit = 'res.config.settings'
    _rec_name = 'ftp_propiedad'
    
    #default_name = fields.char(default_model='your.other.model')
    
    ftp_mercantil = fields.Char(string ='Direccion del Servidor FTP')
    ftp_propiedad = fields.Char(string ='Direccion del Servidor FTP')
    @api.one
    def set_ftp_mercantil(self):
        #raise osv.except_osv('Configuracion',"Revise la direccion del Opc en Configuracion"+self.ftp)
        self.env["ir.config_parameter"].set_param("ftp.mercantil", self.ftp_mercantil or '')

    def get_default_ftp_mercantil(self, cr, uid, ids, context=None):
        #raise osv.except_osv('Configuracion',"Revise la direccion del Opc en Configuracion"+self.ftp)
        #ftp = self.env["ir.config_parameter"].get_param("ftp.mercantil")
        ftp = self.pool.get("ir.config_parameter").get_param(cr, uid, "ftp.mercantil", default=None, context=context)
        #raise osv.except_osv('Configuracion',"Revise la direccion del Opc en Configuracion"+ftp)
        return {'ftp_mercantil': ftp or False}

    @api.one
    def set_ftp_propiedad(self):
        #raise osv.except_osv('Configuracion',"Revise la direccion del Opc en Configuracion"+self.ftp)
        self.env["ir.config_parameter"].set_param("ftp.propiedad", self.ftp_propiedad or '')

    def get_default_ftp_propiedad(self, cr, uid, ids, context=None):
        #raise osv.except_osv('Configuracion',"Revise la direccion del Opc en Configuracion"+self.ftp)
        #ftp = self.env["ir.config_parameter"].get_param("ftp.mercantil")
        ftp = self.pool.get("ir.config_parameter").get_param(cr, uid, "ftp.propiedad", default=None, context=context)
        #raise osv.except_osv('Configuracion',"Revise la direccion del Opc en Configuracion"+ftp)
        return {'ftp_propiedad': ftp or False}


    def _get_alias_domain(self, cr, uid, ids, name, args, context=None):
        ir_config_parameter = self.pool.get("ir.config_parameter")
        domain = ir_config_parameter.get_param(cr, uid, "mail.catchall.domain", context=context)
        return dict.fromkeys(ids, domain or "")
