#!/usr/bin/env python
# -*- coding: utf-8 -*-
from openerp.osv import osv
from openerp import pooler, fields, api, models
from openerp.tools.translate import _

class Item(models.Model):
    _inherit = "opc.item"
    task_dispensing_liquid_id = fields.Many2one('task.dispensing.liquid')

class TaskDispensingLiquid(models.Model):
    _name ="task.dispensing.liquid"
    _inherit ="opc.task"
    _description = "Dispensador de liquido entre ubicaciones"

    
    itemLocationActivacion = fields.Many2one('opc.item',string = 'Activacion')
    itemLocationCantidad = fields.Many2one('opc.item',string = 'Cantidad a despachar')
    
    
    itemLocationCantidadAgua = fields.Many2one('opc.item',string = 'Cantidad de agua en el tanque')

    item_ids = fields.One2many('opc.item',# modelo relacionado
                                'task_dispensing_liquid_id',
                                'Items Adicionales'
    )
    #datos para la vista Kanban
    cantidadAgua = fields.Char(related='itemLocationCantidadAgua.value', string='Stage State')
    color = fields.Integer('Color')
    capacidad_maxima = fields.Integer(string = 'Cantidad Maxima que almacena el servidor')
    


    @api.one
    def activar(self,listaItem):
        res1 = self.itemLocationActivacion.value = listaItem[0]
        res2 = self.itemLocationCantidad.value = listaItem[1]
        #raise osv.except_osv('Esto es un Meadssaje!',str(res1)+";"+str(res2))
        return str(res1)+";"+str(res2)



class stock_location(models.Model):
    _inherit = "stock.location"
    task_id = fields.Many2one('task.dispensing.liquid',string = 'Tarea de Despacho')






class StockTransferDetails(osv.osv):
    _inherit = 'stock.transfer_details'
    se_transfiere = fields.Boolean(string = '¿Se quiere despachar por OPC?', default=True)

    
    @api.one
    def do_detailed_transfer(self):
        if self.se_transfiere == True:
            lstits = []
            for lstits in [self.item_ids, self.packop_ids]:
                for prod in lstits:
                    #raise osv.except_osv('Esto es un Mesaje!',str(len(lstits)))
                    conte = prod.sourceloc_id
                    if conte.task_id and conte.task_id.itemLocationActivacion.item and conte.task_id.itemLocationCantidad.item:
                        r = conte.task_id.activar(
                            [
                                True,
                                prod.quantity
                            ])
                        raise osv.except_osv('resultado',str(r))
                    else:
                        raise osv.except_osv('Esto es un Mesaje!',"Hay un error en la cofiguracion de datos del OPC en la ubicacion "+prod.sourceloc_id.name)

            super(StockTransferDetails, self).do_detailed_transfer()
        else:
            super(StockTransferDetails, self).do_detailed_transfer()
    