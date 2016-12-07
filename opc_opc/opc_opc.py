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
from opcua import Client
from opcua import ua

class OpcOpc(models.Model):
    _name = 'opc.opc'
    
    name = fields.Char(string ='Descripcion')
    server_address = fields.Char(string ='Direccion del Servidor OPC')
    item_ids = fields.One2many(
        comodel_name='opc.item',
        inverse_name='opc_id',
        #compute='default_get'
    )

class task(models.AbstractModel):
    _name ="opc.task"
    _description = "Modelo platilla para tarea"
    name = fields.Char(string ='name')  
    #opc_id = fields.Many2one('opc.opc',string = 'Opc')

    
class Item(models.Model):
    _name ="opc.item"
    _description = "Modelo estandard de un Item"
    name = fields.Char('Descripcion')
    description = fields.Text('Descripcion', size=200, )
    typeData = fields.Selection([('integer','Entero'),('float','Flotante'),('double','Doble'),('boolean','Booleano'),('string','Caracteres')],'Tipo')
    item = fields.Char('Item')
    value = fields.Char('Valor', 
        #readonly = True , 
        compute='get_value',
        #search   ='_search_stage_fold',
        inverse  ='set_value')

    color = fields.Integer('Color')
    opc_id = fields.Many2one('opc.opc', string='Opc', required=True)



    @api.one
    def get_value(self):
        c = self.ConnectToServer() # se 
        n = c.get_node(str(self.item))
        v = n.get_value()
        #raise osv.except_osv('resultado',str(v))
        c.disconnect()
        self.value = str(v)
        return True

    @api.one
    def set_value(self):
        #raise osv.except_osv('resultado',str(self.value)+' - '+str(self.item))
        #try:
            
        c = self.ConnectToServer() # se 
        try:
            n = c.get_node(str(self.item))
            if self.typeData == 'integer':
                n.set_value(int(self.value))
            if self.typeData == 'float':
                
                n.set_value(ua.Variant(float(self.value), ua.VariantType.Float))
            if self.typeData == 'double':
                
                n.set_value(ua.Variant(float(self.value), ua.VariantType.Double))
           
            if self.typeData == 'string':
                n.set_value(str(self.value))

            if self.typeData == 'boolean':
                if self.value in ['True','true', '1', 't', 'y', 'yes']:
                    n.set_value(True)
                elif self.value in ['False','false', '0', 'f', 'n', 'not']:
                    n.set_value(False)
        except:
            pass
        c.disconnect()
        #    return True
        #except:
        #    return False
    #@api.one
    def ConnectToServer(self):
        # revisar esta parte  como se obtendra la direccion del servidor si el modelo de tareas variara para cada heredero
        # ya esta resuelto se manejara la conexion desde las tareas enviandolo como parametro al item cuando se cambie el valor
        #raise osv.except_osv('sd',str(self.opc_id.name))
        client = Client(str(self.opc_id.server_address))  
        client.connect()
        return client


    #opc_task_id = fields.Many2one('opc.task',string = 'Opc')





