#!/usr/bin/env python
# -*- coding: utf-8 -*-
from openerp.osv import osv
from openerp import pooler, fields, api, models
from openerp.tools.translate import _
from openerp.exceptions import ValidationError
from datetime import datetime as datet, timedelta

# hacer un modelo product_move
# para relacionar detalle comprobante con 
class Lote(models.Model):
    _name ="hrz.producto.lote"
    _description = "Lote"

    name = fields.Char('Nombre',copy=False, required= True)
    comprobante_id = fields.Many2one('hrz.comprobante',string = 'Comprobante')
    cantidad = fields.Integer('Cantidad', required= True)
    producto_id = fields.Many2one('hrz.producto',string = 'Producto', required= True)
    fecha_elaboracion = fields.Date('Fecha de elaboracion', required= True)
    fecha_alerta = fields.Date('Fecha de alerta de caducidad', required= True)
    fecha_caducidad = fields.Date('Fecha de caducidad', required= True)


    @api.one
    @api.onchange('fecha_caducidad') # if these fields are changed, call method
    def onchange_fecha_caducidad(self):
        try:
            inicio = (datet.strptime(self.fecha_caducidad, '%Y-%m-%d') - timedelta(days=60)).strftime('%Y-%m-%d')
            self.fecha_alerta = inicio
        except:
            self.fecha_alerta = self.fecha_caducidad
        self.validarFechas()
        return True

    
    @api.one
    @api.onchange('fecha_elaboracion','fecha_alerta')
    def validarFechas(self):

        try:
            ela   = datet.strptime(self.fecha_elaboracion, '%Y-%m-%d')
            cad   = datet.strptime(self.fecha_caducidad, '%Y-%m-%d')
            alert = datet.strptime(self.fecha_alerta, '%Y-%m-%d')
            if ela > cad:
                #raise osv.except_osv('Advertencia', "ela")
                self.fecha_elaboracion = (cad - timedelta(days=90)).strftime('%Y-%m-%d')
            if alert > cad:
                #raise osv.except_osv('Advertencia', "cad")
                self.fecha_alerta = (cad - timedelta(days=60)).strftime('%Y-%m-%d')
        except:
            pass
        return True


    detalle_ids = fields.One2many('hrz.producto.lote.detalle',# modelo relacionado
                                'lote_id',
                                'Lineas de lote', required= True)
    bodega_id = fields.Many2one('hrz.bodega', string='Bodega Inicial')
    state = fields.Selection([
        ('disponible','Disponible'),
        ('agotado','Agotado')], 
        string = 'Estado del Lote', index=True, default='disponible')
    
    _sql_constraints = [
        ('name_lote_unique', 'unique(name)', 'Ya exite un lote con el mismo nombre!'),
    ]
    @api.one
    @api.constrains('detalle_ids')
    def constrains_cantidades(self):
        suma = 0
        for line in self.detalle_ids:
            suma += line.cantidad
        if suma != self.cantidad:
            raise ValidationError("La cantidad en bodegas es distinta que la global")

class DetalleLote(models.Model):
    _name = "hrz.producto.lote.detalle"
    _description = "lineas de lote"
    lote_id = fields.Many2one('hrz.producto.lote',string = 'Lote')
    bodega_id = fields.Many2one('hrz.bodega', string='Bodega')
    cantidad = fields.Integer('Cantidad')