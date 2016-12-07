#!/usr/bin/env python
# -*- coding: utf-8 -*-
from openerp.osv import osv
from openerp import pooler, fields, api, models
from openerp.tools.translate import _


# hacer un modelo product_move
# para relacionar detalle comprobante con 
class Producto(models.Model):
    _name ="hrz.producto"
    _description = "Productos"

    name = fields.Char('Nombre',copy=False)
    
    caracteristica = fields.Text(string = 'Caracteristicas')
    state = fields.Selection([('stado1','Estado 1')], string = 'Estado del producto')

    active = fields.Boolean('Active',default= True)

    tipo = fields.Selection([
        ('medicamento','Medicamento'),
        ('herramienta','Herramientas y Materiales de Mantenimiento'),
        ('material','Material')
        ], string = 'Tipo de Producto')
    '''
    tipo_producto_ingreso = fields.Selection([
        ('medicamento','Medicamento'),
        ('herramienta','Herramientas y equipos'),
        ('material','Material'),
        ('no_medicamento','Herramientas equipos y materiales')
        ], string = 'Tipo de producto para el ingreso',compute = '_getTipo_producto_ingreso',store = True)


    @api.one
    @api.depends('tipo')
    def _getTipo_producto_ingreso(self):
        if self.tipo == 'medicamento':
            self.tipo_producto_ingreso = 'medicamento'
        else:
            self.tipo_producto_ingreso = 'no_medicamento'
    '''

    precio = fields.Float(string = 'Precio Unitario')

    #campos para medicamento
    presentacion_id = fields.Many2one('hrz.producto.presentacion',string = 'Presentacion')

    via_administracion = fields.Many2one('hrz.producto.viaadministracion',string = 'Via de administracion')
   
    dosis = fields.Text(string='Dosis')
    coservacion = fields.Char('Conservacion')
    preparacion = fields.Char('Preparacion')
    codate = fields.Char('Codate',size=12)

    #campo usado para hacer o no editable el tipo de producto,
    #se usa especialmente en el comprobante de ingreso ya que los tipos de productos vienen definidos segun la bodega
    esCreadoDesdeIngreso = fields.Boolean('esCreadoDesdeIngreso')
    esInsumo = fields.Boolean('El producto es un insumo?')
    tipoinsumo_id = fields.Many2one('hrz.producto.tipoinsumo',string = 'Tipo de Insumo')



    #campos para herramientas y materiales de mantenimiento

    esMaterial = fields.Boolean('Es material de mantenimiento?')
    tipomaterial_id = fields.Many2one('hrz.producto.tipomaterial',string = 'Tipo de Material')

    marca_id = fields.Many2one('hrz.producto.marca',string = 'Marca')
    description_fabricante = fields.Text('Descripcion del fabricante')
    garantia = fields.Char('Garantia')
    modelo = fields.Char('Modelo')
    codinst = fields.Char('Codinst')
    accesorios = fields.Char('Accesorios')
    esInsumo = fields.Boolean('El producto es un insumo?')

    #campos para materiales

    
    es_toxico = fields.Boolean('Toxico')
    medidas = fields.Char('Medidas')
    accesorios = fields.Char('Accesorios')
    tipomaterial_oficina_id = fields.Many2one('hrz.producto.tipomaterial_oficina',string = 'Tipo de Material de oficina')
    #marca_id = fields.Many2one('hrz.producto.marca',string = 'Marca')
    #description_fabricante = fields.Text('Descripcion del fabricante')
    #garantia = fields.Char('Garantia')
    #modelo = fields.Char('Modelo')
    #codinst = fields.Char('Codinst')
    #accesorios = fields.Char('Accesorios')

    bodega_ids = fields.One2many('hrz.bodega.producto', 'producto_id', string='Bodegas')
    bodegas_producto_ids = fields.One2many('hrz.bodega', compute ='_bodegas' , string='Bodegas')
    id_comas = fields.Char('id entre comas')

    @api.v8
    def _bodegas(self):
        arr = self.bodega_ids
        for line in arr:
            self.bodegas_producto_ids |= line.bodega_id
  
    _sql_constraints = [
        ('name','unique(name)','No puede Haber dos productors con el mismo nombre')
    ]

    @api.model
    def create(self, vals, context=None):
        new_id = super(Producto, self).create(vals)

        #self.id_comas = ','+str(self.id)+','
        new_id.id_comas = str(new_id.id)
        return new_id

    @api.onchange('name','caracteristica','dosis','coservacion','preparacion','codate','garantia','modelo','codinst','accesorios','medidas','accesorios','description_fabricante','garantia','modelo','codinst','accesorios')
    def _uppercase(self):

        def upperField(field):
            if field != False:
                field = str(unicode(field).encode('utf-8')).upper()         
            return field

        self.name   =   upperField(self.name)
        self.caracteristica =   upperField(self.caracteristica)
        self.dosis  =   upperField(self.dosis)
        self.coservacion    =   upperField(self.coservacion)
        self.preparacion    =   upperField(self.preparacion)
        self.codate =   upperField(self.codate)
        self.garantia   =   upperField(self.garantia)
        self.modelo =   upperField(self.modelo)
        self.codinst    =   upperField(self.codinst)
        self.accesorios =   upperField(self.accesorios)
        self.medidas    =   upperField(self.medidas)
        self.accesorios =   upperField(self.accesorios)
        self.description_fabricante =   upperField(self.description_fabricante)
        self.garantia   =   upperField(self.garantia)
        self.modelo =   upperField(self.modelo)
        self.codinst    =   upperField(self.codinst)
        self.accesorios =   upperField(self.accesorios)

    


class Marca(models.Model):
    _name ="hrz.producto.marca"
    _description = "Marca de producto"
    name = fields.Char('Nombre de Marca')

    @api.onchange('name')
    def _uppercase(self):
        def upperField(field):
            if field != False:
                field = str(unicode(field).encode('utf-8')).upper()         
            return field
        self.name   =   upperField(self.name)

class Presentacion(models.Model):
    _name ="hrz.producto.presentacion"
    _description = "Presentacion de producto"
    name = fields.Char('Nombre de Presentacion')
    @api.onchange('name')
    def _uppercase(self):
        def upperField(field):
            if field != False:
                field = str(unicode(field).encode('utf-8')).upper()         
            return field
        self.name   =   upperField(self.name)


class viaAdministracion(models.Model):
    _name ="hrz.producto.viaadministracion"
    _description = "Via de Administracion"
    name = fields.Char('Via de administracion')
    @api.onchange('name')
    def _uppercase(self):
        def upperField(field):
            if field != False:
                field = str(unicode(field).encode('utf-8')).upper()         
            return field
        self.name   =   upperField(self.name)

class tipoInsumo(models.Model):
    _name ="hrz.producto.tipoinsumo"
    _description = "Tipos de Insumo"
    name = fields.Char('Tipo de Insumo')
    @api.onchange('name')
    def _uppercase(self):
        def upperField(field):
            if field != False:
                field = str(unicode(field).encode('utf-8')).upper()         
            return field
        self.name   =   upperField(self.name)
class tipoMaterial(models.Model):
    _name ="hrz.producto.tipomaterial"
    _description = "Tipos de Material"
    name = fields.Char('Tipo de Material')
    @api.onchange('name')
    def _uppercase(self):
        def upperField(field):
            if field != False:
                field = str(unicode(field).encode('utf-8')).upper()         
            return field
        self.name   =   upperField(self.name)


class tipoMaterialOficina(models.Model):
    _name = 'hrz.producto.tipomaterial_oficina'
    _description = "Tipos de Material de oficina"
    name = fields.Char('Tipo de Material de oficina')
    @api.onchange('name')
    def _uppercase(self):
        def upperField(field):
            if field != False:
                field = str(unicode(field).encode('utf-8')).upper()         
            return field
        self.name   =   upperField(self.name)







