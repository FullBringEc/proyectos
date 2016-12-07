#!/usr/bin/env python
# -*- coding: utf-8 -*-
from openerp.osv import osv, fields as field
from openerp import pooler, fields, api, models

from openerp.tools.translate import _
from openerp.exceptions import Warning
import datetime
from datetime import datetime as datet, timedelta
import psycopg2
from ast import literal_eval

hostname = 'localhost'
username = 'odoopg'
password = 'openpgpwd'
database = 'hospital'

class Comprobante(models.Model):
    _name ="hrz.comprobante"
    _description = "Documentos"
    color = fields.Integer('Color')
    state = fields.Selection([
        ('draft','Borrador'),
        ('prescription','Recetado'),
        ('sent','Enviado'),
        ('deactivated','Desactivado')], 
        string = 'Estado Comprobante', index=True, default='draft')
    name = fields.Char(string = 'Numero de Comprobante',copy=False
        ,readonly=True)
    number = fields.Char(string = 'Numero de Comprobante',copy=False
        ,readonly=True, states={'draft': [('readonly', False)]})
    emisor_id = fields.Many2one('res.partner',string = 'Emisor'
        ,readonly=True, states={'draft': [('readonly', False)]})
    receptor_id = fields.Many2one('res.partner',string = 'Receptor'
        ,readonly=True, states={'draft': [('readonly', False)]})

    emisor_mail = fields.Char(related = 'emisor_id.email',string = 'Correo', store = True)
    emisor_street = fields.Char(related = 'emisor_id.street',string = 'Direccion', store = True)
    emisor_phone = fields.Char(related = 'emisor_id.phone',string = 'Telefono', store = True)

    emisor_mail = fields.Char(related = 'emisor_id.email',string = 'Correo', store = True)


    emisor_user_id = fields.Many2one('res.users',string = 'Emisor usuario'
        ,readonly=True, states={'draft': [('readonly', False)]})

    emisor_medico_id = fields.Many2one('hrz.medico',related = 'emisor_user_id.medico_id',string = 'Medico', store = True)
    receptor_paciente_id = fields.Many2one('hrz.paciente' ,string = 'Paciente', store = True,readonly=True, states={'draft': [('readonly', False)]})
    paciente_numero_archivo = fields.Char(related = 'receptor_paciente_id.numero_archivo',string = 'Numero de Archivo',store = True)
    paciente_alergia = fields.Char(related = 'receptor_paciente_id.alergia',string = 'Es alergico a:',store = True)
    paciente_cedula = fields.Char(related = 'receptor_paciente_id.cedula',string = 'Cedula',store = True)
    paciente_telefono = fields.Char(related = 'receptor_paciente_id.telefono',string = 'Telefono',store = True)
    paciente_celular = fields.Char(related = 'receptor_paciente_id.celular',string = 'Celular',store = True)
    paciente_direccion = fields.Char(related = 'receptor_paciente_id.direccion',string = 'Direccion',store = True)



    receptor_user_id = fields.Many2one('res.users',string = 'Receptor usuario'
        ,readonly=True, states={'draft': [('readonly', False)]})


    area_id = fields.Many2one('hrz.area',string = 'Area'
        ,readonly=True, states={'draft': [('readonly', False)]})
    fecha = fields.Datetime(string ="Fecha"
        ,readonly=True, states={'draft': [('readonly', False)]})
    
    
    tipo_comprobante = fields.Selection([
        ('recipe','Receta'),
        ('ingress','Ingreso'),
        ('assignment','Asignacion'),
        ('transfer','Transferencia'),
        ('transferInsumo','Transferencia de insumos'),
        ('transferMaterial','Transferencia de materiales'),
        ('transferMaterialMantenimiento','Transferencia de materiales de mantenimiento'),


        ], string = 'Tipo de Comprobante')
    total = fields.Float(compute='get_total',digits=(12,2), string='Total')
    iva = fields.Integer(string='IVA')
    total_iva = fields.Float(compute='get_total_iva',digits=(12,2), string='Total'
        ,readonly=True, states={'draft': [('readonly', False)]})
    observacion = fields.Text(string ='Observaciones'
        ,readonly=True, states={'draft': [('readonly', False)]})
    #_columns = {
    #    'detalle_ids': field.one2many('hrz.comprobante.detalle', 'comprobante_id', 'Order Lines', readonly=True, states={'draft': [('readonly', False)]}, copy=True),
    #    }
    detalle_ids = fields.One2many('hrz.comprobante.detalle',# modelo relacionado
                                'comprobante_id',
                               'Lineas de producto')
                               #,readonly=True, states={'draft': [('readonly', False)]})



    lote_ids = fields.One2many('hrz.producto.lote',# modelo relacionado
                                'comprobante_id',
                                'Lotes creados en este comprobante'
                                ,readonly=True, states={'draft': [('readonly', False)]})

    move_ids = fields.One2many('hrz.producto.move',# modelo relacionado
                                'comprobante_id',
                                'Movimientos de Producto'
                                ,readonly=True, states={'draft': [('readonly', False)]})

    asset_ids = fields.One2many('hrz.producto.asset',# modelo relacionado
                                'comprobante_id',
                                'Activos Generados'
                                ,readonly=True, states={'draft': [('readonly', False)]})
    
    Bodega_ingreso_id = fields.Many2one('hrz.bodega', string='Bodega a Ingresar'
        ,readonly=True, states={'draft': [('readonly', False)]})

    tipo_producto_Bodega_ingreso = fields.Selection(related='Bodega_ingreso_id.tipo_producto', string='Tipo Bodega a Ingresar'
        ,readonly=True, states={'draft': [('readonly', False)]})

    #producto_ids_Bodega_ingreso = fields.One2many('hrz.producto', string='Lineas de productos',compute ='_productos_ingreso')

    Bodega_egreso_id = fields.Many2one('hrz.bodega', string='Bodega a Retirar'
        ,readonly=True, states={'draft': [('readonly', False)]})

    tipo_producto_Bodega_egreso = fields.Selection(related='Bodega_egreso_id.tipo_producto', string='Tipo Bodega a Ingresar'
        ,readonly=True, states={'draft': [('readonly', False)]})
    char_productos_ids = fields.Char('Lista de Productos', compute="_char_productos_ids")

    responsable_ingreso_id = fields.Many2one(related='Bodega_ingreso_id.responsable_id', string='Responsable de bodega de ingreso'
        ,readonly=True, states={'draft': [('readonly', False)]})
    responsables_ingreso_ids = fields.Many2many(related='Bodega_ingreso_id.responsables_ids', string='Responsables de bodega de ingreso'
        ,readonly=True, states={'draft': [('readonly', False)]})

    @api.onchange('observacion')
    def _uppercase(self):
        if self.observacion != False:
            self.observacion = str(self.observacion).upper()

    @api.onchange('tipo_comprobante')
    def _bodega_egreso(self):
        if self.tipo_comprobante == 'recipe':
            farmacia = self.env['hrz.bodega'].search([['es_virtual', '=', False], ['tipo', '=', 'recipe']])
            paciente_virtual = self.env['hrz.bodega'].search([['es_virtual', '=', True], ['tipo', '=', 'recipe']])
            
            self.Bodega_ingreso_id = paciente_virtual.id
            self.Bodega_egreso_id = farmacia.id

        if self.tipo_comprobante == 'ingress':
            proveedor_virtual = self.env['hrz.bodega'].search([['es_virtual', '=', True], ['tipo', '=', 'ingress']])
            self.Bodega_egreso_id = proveedor_virtual.id

        if self.tipo_comprobante == 'assignment':
            usuario_virtual = self.env['hrz.bodega'].search([['es_virtual', '=', True], ['tipo', '=', 'assignment']])
            self.Bodega_ingreso_id = usuario_virtual.id

        if self.tipo_comprobante == 'transferMaterialMantenimiento':
            usuario_virtual = self.env['hrz.bodega'].search([['es_virtual', '=', True], ['tipo', '=', 'assignment']])
            self.Bodega_ingreso_id = usuario_virtual.id



    #Esto solo debe afectar a comprobante de transferencia
    #Dominio dinamico para el filtro de bodegas  ejemplo :  bodega medicamento solo a farmacia
    @api.onchange('Bodega_egreso_id')
    def onchange_Bodega_egreso_id(self):
        self.detalle_ids = None

        if self.tipo_comprobante != 'assignment' and self.tipo_comprobante != 'transferMaterialMantenimiento':
            self.Bodega_ingreso_id = None
        if self.tipo_comprobante == 'transfer':
            if self.Bodega_egreso_id.tipo == 'ingress' and self.Bodega_egreso_id.tipo_producto == 'medicamento':
                return {'domain':{'Bodega_ingreso_id':[('es_virtual', '=', False), ('tipo', '=', 'recipe')]}}
            elif self.Bodega_egreso_id.tipo == 'ingress' and self.Bodega_egreso_id.tipo_producto != 'medicamento':
                return {'domain':{'Bodega_ingreso_id':[('es_virtual', '=', False), ('tipo', 'not in', ('recipe','ingress'))]}}
            else:
                return {'domain':{'Bodega_ingreso_id':[('es_virtual', '=', False), ('id', '!=', self.Bodega_egreso_id.id)]}}

        #if self.tipo_comprobante in ['transferInsumo','transferMaterial','transferMaterialMantenimiento']:
        #    return {'domain':{'Bodega_ingreso_id':[('es_virtual', '=', False), ('tipo', '=', 'area')]}}


    esCreadoDesdeIngreso = fields.Boolean('esCreadoDesdeIngreso')
    @api.onchange('Bodega_ingreso_id')
    def onchange_Bodega_ingreso_id(self):

        if self.tipo_comprobante == 'ingress':
            self.detalle_ids = None
            self.esCreadoDesdeIngreso = True
        if self.tipo_comprobante in ['transferInsumo','transferMaterial','transferMaterialMantenimiento']:
            if self.Bodega_ingreso_id:
                self.receptor_user_id = self.Bodega_ingreso_id.responsable_id




    @api.depends('Bodega_egreso_id','detalle_ids')
    def _char_productos_ids(self):
        self.detalle_ids = None
        relation_ids = '('+ '|'.join([str(x.producto_id.id) for x in self.Bodega_egreso_id.producto_ids])+')'

        self.char_productos_ids = relation_ids
       
        
    @api.one
    def get_total(self):
        suma = 0
        for line in self.detalle_ids:
            suma += line.subtotal

        self.total = suma
        return True;

    @api.one
    def get_total_iva(self):
        iva = 0
        if self.iva != 0:
            iva = self.total*((float)(self.iva)/100)

        self.total_iva = self.total+iva
        return True;

    @api.one
    def _setNumber(self):
        if self.number == False:    # problemas 
            if self.tipo_comprobante == 'transfer':
                seq = self.env["ir.sequence"].get("code_transferencia")
                self.write({'number': seq})
                self.name = seq
            if self.tipo_comprobante == 'transferInsumo':
                seq = self.env["ir.sequence"].get("code_tranf_insumo")
                self.write({'number': seq})
                self.name = seq
            if self.tipo_comprobante == 'transferMaterial':
                seq = self.env["ir.sequence"].get("code_tranf_material")
                self.write({'number': seq})
                self.name = seq
            if self.tipo_comprobante == 'transferMaterialMantenimiento':
                seq = self.env["ir.sequence"].get("code_tranf_mat_mant")
                self.write({'number': seq})
                self.name = seq
            if self.tipo_comprobante == 'ingress':
                seq = self.env["ir.sequence"].get("code_ingreso")
                self.write({'number': seq})
                self.name = seq
            if self.tipo_comprobante == 'recipe':
                seq = self.env["ir.sequence"].get("code_receta")
                self.write({'number': seq})
                self.name = seq
            if self.tipo_comprobante == 'assignment':
                seq = self.env["ir.sequence"].get("code_asignacion")
                self.write({'number': seq})
                self.name = seq
        else:
            self.name = self.number


    @api.one
    def validate(self):
        if(len(self.detalle_ids) == 0):
            raise osv.except_osv('Advertencia',"No hay lineas de producto")
        if self.tipo_comprobante != 'ingress':
            self.val_cant_producto()
        self.val_repeticion_producto()
    #funcion que verifica que el producto en la bodega no haya cambiada    
    def val_cant_producto(self):
        for x in self.detalle_ids:
            if x.cantidad > x._getCantidaMaxima():
                raise osv.except_osv('Advertencia', "La cantidad de producto en la "+self.Bodega_egreso_id.name+" no es la misma por favor actualice")
    def val_repeticion_producto(self):
        productos = []
        for x in self.detalle_ids:
            if (x.producto_id,x.lote_id) in productos:
                raise osv.except_osv('Advertencia', "Tiene productos repetidos")
            else:
                productos.append((x.producto_id,x.lote_id))

    @api.multi
    def send(self):
        self.validate()
        self._setNumber()
        self.fecha = datetime.datetime.now()
        self.move_ids = None
        for line in self.detalle_ids:
            #   Esto crea el producto en la bodega si este no esta registrado en ella
            if self.env['hrz.bodega.producto'].search_count([['bodega_id', '=', self.Bodega_ingreso_id.id], ['producto_id', '=', line.producto_id.id]]) ==0:
                self.env['hrz.bodega.producto'].create({'bodega_id':self.Bodega_ingreso_id.id,'producto_id':line.producto_id.id})
            if self.env['hrz.bodega.producto'].search_count([['bodega_id', '=', self.Bodega_egreso_id.id], ['producto_id', '=', line.producto_id.id]]) == 0:
                self.env['hrz.bodega.producto'].create({'bodega_id':self.Bodega_egreso_id.id,'producto_id':line.producto_id.id})
            if self.tipo_comprobante == 'ingress':

                self.move_ids |= self.env['hrz.producto.move'].create(
                    {'producto_id':line.producto_id.id,
                    'bodega_id':self.Bodega_ingreso_id.id,
                    'precio_unitario':line.precio_unitario,
                    'entra':line.cantidad,
                    'sale':0,
                    'fecha_caducidad':line.fecha_caducidad,
                    'fecha_elaboracion':line.fecha_elaboracion,
                    })
                self.move_ids |= self.env['hrz.producto.move'].create(
                    {'producto_id':line.producto_id.id,
                    'bodega_id':self.Bodega_egreso_id.id,
                    'precio_unitario':line.precio_unitario,
                    'entra':0,
                    'sale':line.cantidad,
                    'fecha_caducidad':line.fecha_caducidad,
                    'fecha_elaboracion':line.fecha_elaboracion,
                    })
                #establece el precio promedio
                if line.producto_id.precio == 0.0:
                    line.producto_id.precio = line.precio_unitario
                else:
                    line.producto_id.precio = (line.producto_id.precio + line.precio_unitario)/2

                self.crearLotes(line)

            else:
                self.move_ids |= self.env['hrz.producto.move'].create(
                    {
                    'producto_id':line.producto_id.id,
                    'bodega_id':self.Bodega_ingreso_id.id,
                    'precio_unitario':line.precio_unitario,
                    'entra':line.cantidad,
                    'sale':0
                    })
                self.move_ids |= self.env['hrz.producto.move'].create(
                    {
                    'producto_id':line.producto_id.id,
                    'bodega_id':self.Bodega_egreso_id.id,
                    'precio_unitario':line.precio_unitario,
                    'entra':0,
                    'sale':line.cantidad
                    })
                self.moverLotes(line)
            
        if self.tipo_comprobante == 'assignment':
            if len(self.asset_ids) == 0:
                raise osv.except_osv('Advertencia', "No se puede generar un Acta de Entrega sin detallar las lineas de Equipos")
            self.entregarAsset()
        return self.write({'state': 'sent'})

    def crearLotes(self, line):
        if self.tipo_comprobante == 'ingress':
            try:
                if self.Bodega_ingreso_id.tipo_producto == 'medicamento':
                    lote = self.env['hrz.producto.lote'].create(
                        {
                        'name':line.lote,
                        'cantidad':line.cantidad,
                        'producto_id':line.producto_id.id,
                        'fecha_elaboracion':line.fecha_elaboracion,
                        'fecha_caducidad':line.fecha_caducidad,
                        'fecha_alerta':line.fecha_alerta,
                        'bodega_id':self.Bodega_ingreso_id.id,
                        })
                    lote.detalle_ids|= self.env['hrz.producto.lote.detalle'].create(
                        {
                        'bodega_id':self.Bodega_ingreso_id.id,
                        'cantidad':line.cantidad,
                        })
                    self.lote_ids |= lote
            except:
                raise osv.except_osv('Advertencia Capa 8','Es posible que un lote ya este creado con ese nombre')

    def moverLotes(self, line):

        tipo_p_ingreso  = self.Bodega_ingreso_id.tipo_producto
        tipo_ingreso  = self.Bodega_ingreso_id.tipo
        tipo_p_egreso   = self.Bodega_egreso_id.tipo_producto
        if (tipo_p_ingreso == 'medicamento' or tipo_ingreso == 'area')  and tipo_p_egreso == 'medicamento':
            #if self.Bodega_ingreso_id.tipo_producto == 'medicamento' and self.Bodega_egreso_id.tipo_producto == 'medicamento':
            detalles = line.lote_id.detalle_ids
            #raise osv.except_osv('Advertencia',line.lote_id.name)
            detalleA = [v  for v in detalles if (v.bodega_id in self.Bodega_egreso_id)][0]
            detalleA.cantidad -= line.cantidad
            if detalleA.cantidad==0:
                line.lote_id.state = 'agotado'
            try:
                detalleB = [v  for v in detalles if (v.bodega_id in self.Bodega_ingreso_id)][0]
                detalleB.cantidad += line.cantidad
            except:
                detalleB = self.env['hrz.producto.lote.detalle'].create(
                {
                'bodega_id':self.Bodega_ingreso_id.id,
                'cantidad':line.cantidad,
                })
                line.lote_id.detalle_ids |= detalleB

            #raise osv.except_osv('Advertencia',line.lote_id.detalle_ids)
            
    
    @api.one
    def entregarAsset(self):
        for line in self.asset_ids:
            line.state = 'delivered'
        return True
            
    @api.one
    def generarAsset(self):
        self.asset_ids = None
        for line in self.detalle_ids:
            for producto in range(0,line.cantidad):
                self.asset_ids |= self.env['hrz.producto.asset'].create(
                                {'producto_id':line.producto_id.id,
                                'name':line.producto_id.name,
                                })   

    @api.one
    def disable(self):

        #grupos_id  = self.env['res.users'].browse(self._uid).groups_id

        #valores = (map(lambda x: x.name, grupos_id))
        
        return self.write({'state': 'deactivated'})
    @api.one
    def prescribe(self):

        if(len(self.detalle_ids) == 0):
            raise osv.except_osv('Advertencia',"No hay nada en la receta")
        for line in self.detalle_ids:
            line.state = "farmaceuta"
        return self.write({'state': 'prescription'})

    @api.one
    def actualizarPacientes(self):
        #raise osv.except_osv('Advertencia',self.Bodega_egreso_id.name +' - '+self.Bodega_ingreso_id.name)
        self.env['hrz.paciente'].actualizarPacientes()
        return True

    @api.multi
    def unlink(self):
        for comp in self:
            if comp.state != 'draft':
                raise Warning(_('Este comprobante no se puede eliminar debido a que ya esta validado'))
        return super(Comprobante, self).unlink()

class ProductoAsset(models.Model):
    _name ="hrz.producto.asset"
    _description = "Activos"
    producto_id = fields.Many2one('hrz.producto',string = 'Producto')
    comprobante_id = fields.Many2one('hrz.comprobante',string = 'Comprobante')
    name = fields.Char(string = 'Descripcion')
    responsable_id = fields.Many2one('res.partner', related = 'comprobante_id.receptor_id',string = 'Responsable')
    state = fields.Selection([('draft','Borrador'),('delivered','Entregado')], string = 'Estado del Activo',default='draft')
    serie = fields.Char(string='Serie')
    garantia = fields.Char(string='Garantia')
    coodmsp = fields.Char(string='Codigo MSP',size=15)
    

class ProductoMove(models.Model):
    _name ="hrz.producto.move"
    _description = "movimiento de Productos"
    producto_id = fields.Many2one('hrz.producto',string = 'Producto')
    comprobante_id = fields.Many2one('hrz.comprobante',string = 'Comprobante')
    bodega_id = fields.Many2one('hrz.bodega', string='Bodega', required=True)
    origen = fields.Char(related='comprobante_id.name', string='Origen')
    entra = fields.Integer(string = 'Entra')
    sale = fields.Integer(string = 'Sale')
    precio_unitario = fields.Float(string = 'Precio Unitario')

    fecha_caducidad = fields.Date('Fecha de Caducidad')
    fecha_elaboracion = fields.Date('Fecha de elaboracion')


class DetalleComprobante(models.Model):
    _name ="hrz.comprobante.detalle"
    _description = "lineas de comprobante"
    state = fields.Selection([
        ('medico','Medico'),
        ('farmaceuta','Farmaceuta')], 
        string = 'Tipo receta', index=True, default='medico')
    producto_id = fields.Many2one('hrz.producto',string = 'Producto', 
        required= True, readonly = True, states={'medico':[('readonly','=',False)]})
    precio_relacion = fields.Float(related = 'producto_id.precio',string = 'Precio Producto', store = True)
    esInsumo = fields.Boolean(related = 'producto_id.esInsumo',string = 'Insumo?', store = True)
    comprobante_id = fields.Many2one('hrz.comprobante',string = 'Comprobante')

    cantidad = fields.Integer(string = 'Cantidad')

    cantidad_maxima = fields.Integer(string = 'Cantidad Maxima', compute='_getCantidaMaxima',store = True)
    precio_unitario = fields.Float(string = 'Precio Unitario',digits=(12,4))
    descuento = fields.Float(string = 'Descuento',digits=(12,4))
    subtotal = fields.Float(string = 'Subtotal', digits=(12,2), compute='get_subtotal' ,store = True)
    
    #solo para ingreso
    lote_id = fields.Many2one('hrz.producto.lote',string = 'Lote')
    lote = fields.Char(string='Lote')
    fecha_elaboracion = fields.Date('Fecha de elaboracion')
    fecha_caducidad = fields.Date('Fecha de Caducidad')
    
    #solo para receta
    dosis = fields.Integer(string = 'Dosis', 
         readonly = True, states={'medico':[('readonly','=',False)]})
    frecuencia = fields.Integer(string = 'Frecuencia (horas)', 
         readonly = True, states={'medico':[('readonly','=',False)]})
    duracion = fields.Integer(string = 'Duracion (dias)', 
         readonly = True, states={'medico':[('readonly','=',False)]})

    comentario = fields.Text("Comentario")

    fecha_alerta = fields.Date('Fecha de alerta de caducidad')

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
    @api.onchange('dosis','frecuencia','duracion') # if these fields are changed, call method
    def onchange_dosis_frecuencia_duracion(self):
        try:
            self.cantidad= self.dosis * self.frecuencia * self.duracion 
        except:
            pass
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

    @api.model
    def create(self, vals, context=None):
        

        new_id = super(DetalleComprobante, self).create(vals)
        comp = new_id.comprobante_id

        if comp.tipo_comprobante == 'transfer' and comp.tipo_producto_Bodega_egreso == comp.tipo_producto_Bodega_ingreso and comp.tipo_producto_Bodega_ingreso == 'medicamento':
            if len(new_id.lote_id) == 0:
                raise osv.except_osv('Advertencia', "Por favor Seleccione el lote")
        else:
            new_id.lote_id = None

        if comp.tipo_comprobante == 'ingress' and comp.tipo_producto_Bodega_ingreso == 'medicamento':
            if new_id.fecha_elaboracion==False or new_id.fecha_alerta==False or new_id.fecha_caducidad==False or new_id.lote==False:
                raise osv.except_osv('Advertencia', "Rellene los datos del medicamento")    
        return new_id
    @api.multi
    def write(self, vals):
        comp = self.comprobante_id
        resp = super(DetalleComprobante, self).write(vals)
        if comp.tipo_comprobante == 'transfer' and comp.tipo_producto_Bodega_egreso == comp.tipo_producto_Bodega_ingreso and comp.tipo_producto_Bodega_ingreso == 'medicamento':
            if len(self.lote_id) == 0:
                raise osv.except_osv('Advertencia', "Por favor Seleccione el lote")
        
        if comp.tipo_comprobante == 'ingress' and comp.tipo_producto_Bodega_ingreso == 'medicamento':
            if self.fecha_elaboracion==False or self.fecha_alerta==False or self.fecha_caducidad==False or self.lote==False:
                raise osv.except_osv('Advertencia', "Rellene los datos del medicamento")
        return resp




    

    @api.depends('cantidad','precio_unitario','descuento')
    @api.one
    def get_subtotal(self):
        self.subtotal = (self.cantidad * self.precio_unitario) - self.descuento
        return True ;
    @api.one
    @api.depends('producto_id','lote_id')
    def _getCantidaMaxima(self):
        tipo_p_ingreso  = self.comprobante_id.Bodega_ingreso_id.tipo_producto
        tipo_ingreso  = self.comprobante_id.Bodega_ingreso_id.tipo
        tipo_p_egreso   = self.comprobante_id.Bodega_egreso_id.tipo_producto
        if (tipo_p_ingreso == 'medicamento' or tipo_ingreso == 'area')  and tipo_p_egreso == 'medicamento':
            #if self.comprobante_id.Bodega_ingreso_id.tipo_producto == 'medicamento' and self.comprobante_id.Bodega_egreso_id.tipo_producto == 'medicamento':
            if len(self.lote_id) == 0:
                #raise osv.except_osv('Advertencia', "Porfavor Seleccione un lote")
                return True
            else:
                try:
                    detalle = [v  for v in self.lote_id.detalle_ids if (v.bodega_id in self.comprobante_id.Bodega_egreso_id)][0]
                except:
                    pass
                #raise osv.except_osv('Advertencia', detalle.cantidad)
                self.cantidad_maxima = detalle.cantidad
                return self.cantidad_maxima
        try:

            productos_en_bodega_ids = self.comprobante_id.Bodega_egreso_id.producto_ids
            producto = self.producto_id
            a = [v  for v in productos_en_bodega_ids if (v.producto_id in producto)][0]

            #raise osv.except_osv('Advertencia', str(producto)+str(a))
            self.cantidad_maxima = a.existencia
            return a.existencia
        except:
            return 0

        

    @api.one
    @api.onchange('producto_id') # if these fields are changed, call method
    def get_precio(self):
        #raise osv.except_osv('Advertencia', self.producto_id.name)
        self.precio_unitario = self.precio_relacion
        return True

    @api.one
    @api.onchange('cantidad') # if these fields are changed, call method
    def set_cantidad(self):
        #raise osv.except_osv('Advertencia', self.comprobante_id.tipo_comprobante)
        if self.comprobante_id.tipo_comprobante == 'ingress' or self.comprobante_id.tipo_comprobante == 'recipe':
            #raise osv.except_osv('Advertencia', 'ingress')
            return True
        if self.cantidad >= self.cantidad_maxima:
            self.cantidad = self.cantidad_maxima
        return True ;




class Area(models.Model):
    _name ="hrz.area"
    _description = "Area"
    name = fields.Char('Area')
    piso = fields.Char('Piso')




