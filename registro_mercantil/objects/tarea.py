# -*- coding: utf-8 -*-
from openerp import models, fields, api
from openerp.osv import osv
from datetime import datetime, timedelta
from odoo.exceptions import UserError


class rbs_tarea(models.Model):
    _name = 'rbs.tarea'
    _description = "Tareas"
    # name = fields.Char("Parte")
    # _rec_name = 'name'

    @api.model
    def get_numero_tarea(self):
        # seq = self.env["ir.sequence"].get("numero_tarea")
        return self.env["ir.sequence"].get("numero_tarea")
    fecha_registro = fields.Datetime("Fecha del registro", default=datetime.now(), required=True)
    fecha_estimada = fields.Datetime("Fecha estimada", required=True)
    user_id = fields.Many2one('res.users', string="Asignado a", required=True)
    state = fields.Selection([
        ('pendiente', 'Pendiente'),
        ('por_firmar', 'Por firmar'),
        ('por_entregar', 'Por entregar'),
        ('done', 'Realizado'),
        ], string="Estado de tarea", default='pendiente')
    tipo_servicio = fields.Selection([
        ('inscripcion_propiedad', 'Inscripcion Propiedad'),
        ('inscripcion_mercantil', 'Inscripcion Mercantil'),
        ('certificacion_propiedad', 'Certificacion Propiedad'),
        ('certificacion_mercantil', 'Certificacion Mercantil'),
        ], string="Tipo de servicio", required=True)
    name = fields.Char(string='Numero de tarea', default=get_numero_tarea, required=True)
    factura_id = fields.Many2one('account.invoice', string='Factura relacionada', required=True)
    cliente_factura_id = fields.Many2one(related="factura_id.partner_id", string='Cliente factura', required=True)
    propiedad_id = fields.Many2one('rbs.documento.propiedad', string='Documento de propiedad')
    mercantil_id = fields.Many2one('rbs.documento.mercantil', string='Documento mercantil')

    certificado_propiedad_id = fields.Many2one('rbs.certificado.propiedad', string='Certificado de propiedad')
    certificado_mercantil_id = fields.Many2one('rbs.certificado.mercantil', string='Certificado de propiedad')

    persona_id = fields.Many2one("rbs.persona", string="Persona")
    bien_id = fields.Many2one("rbs.bien.inmueble", string="Bien")
    descripcion = fields.Text("Descripcion")

    @api.multi
    def crear_inscripcion_propiedad(self):
        self.validar_usuario()
        if self.tipo_servicio == 'inscripcion_propiedad':
            self.propiedad_id = self.env['rbs.documento.propiedad'].create({})
            self.iniciar_tarea()

    @api.multi
    def crear_inscripcion_mercantil(self):
        self.validar_usuario()
        if self.tipo_servicio == 'inscripcion_mercantil':
            self.mercantil_id = self.env['rbs.documento.mercantil'].create({})
            self.iniciar_tarea()

    @api.multi
    def crear_certificacion_propiedad(self):
        self.validar_usuario()
        if self.tipo_servicio == 'certificacion_propiedad':
            if self.bien_id:
                valor_busqueda = self.bien_id.clave_catastral
                criterio_busqueda = 'clave_catastral'

            else:
                valor_busqueda = self.persona_id.num_identificacion
                criterio_busqueda = 'identificacion'
            self.certificado_propiedad_id = self.env['rbs.certificado.propiedad'].create(
                                                                            {
                                                                                'valor_busqueda': valor_busqueda,
                                                                                'criterio_busqueda': criterio_busqueda,
                                                                                'solicitante': self.cliente_factura_id.name
                                                                            })
            self.iniciar_tarea()

    @api.multi
    def crear_certificacion_mercantil(self):
        self.validar_usuario()
        if self.tipo_servicio == 'certificacion_mercantil':
            self.certificado_mercantil_id = self.env['rbs.certificado.mercantil'].create(
                                                                            {
                                                                                'valor_busqueda': self.cliente_factura_id.identifier,
                                                                                'criterio_busqueda': 'Identificacion',
                                                                                'solicitante': self.cliente_factura_id.name
                                                                            })
            self.iniciar_tarea()

    @api.one
    def iniciar_tarea(self):
        self.write({'state': 'por_firmar'})
    dict_servicios = {
        'inscripcion_propiedad': {
                                        'field': 'propiedad_id',
                                        'model': 'rbs.documento.propiedad',
                                    },
        'inscripcion_mercantil': {
                                        'field': 'mercantil_id',
                                        'model': 'rbs.documento.mercantil',
                                    },
        'certificacion_propiedad': {
                                        'field': 'certificado_propiedad_id',
                                        'model': 'rbs.certificado.propiedad',
                                    },
        'certificacion_mercantil': {
                                        'field': 'certificado_mercantil_id',
                                        'model': 'rbs.certificado.mercantil',
                                    },
    }

    @api.one
    def firmar(self):
        field = self.dict_servicios[self.tipo_servicio]['field']
        print self[field].state
        if self[field].state not in ('done'):
            raise UserError('Para firmar primero valide el documento')
        self.write({'state': 'por_entregar'})

    def open_document(self):
        '''
        This function returns an action that display invoices/refunds made for the given partners.
        '''
        field = self.dict_servicios[self.tipo_servicio]['field']
        model = self.dict_servicios[self.tipo_servicio]['model']
        view_id = self.env['ir.ui.view'].search([("model", "=", model), ('type', "=", "form")]).id

        # print action.res_model
        # action = self.env.ref('account.action_invoice_refund_out_tree').read()[0]
        # action['domain'] = literal_eval(action['domain'])
        # action['domain'].append(('partner_id', 'child_of', self.ids))
        # view_id = self.env.ref('modul_name._id_of_form_view').id
        if self[field].id:
            context = self._context.copy()
            return {
                'name': 'form_name',
                'view_type': 'form',
                'view_mode': 'tree',
                'views': [(view_id, 'form')],
                'res_model': model,
                'view_id': view_id,
                'type': 'ir.actions.act_window',
                'res_id': self[field].id,
                'target': 'current',
                'context': context,
            }

    @api.one
    def entregar(self):
        self.write({'state': 'done'})

    @api.one
    def validar_usuario(self):
        user_actual_id = self.env["res.users"].search([('id', '=', self._uid)], limit=1, order='id desc')
        group_hr_manager_id = self.env['ir.model.data'].get_object_reference('registro_mercantil', 'group_administrador')[1]
        if not (group_hr_manager_id in [g.id for g in user_actual_id.groups_id] or self._uid == self.user_id.id):
            raise osv.except_osv('Esto es un Mesaje!', 'Este documento no fue asignado a tu usuario ')


class factura_invoice(models.Model):
    _inherit = 'account.invoice'
    tarea_ids = fields.One2many('rbs.tarea', 'factura_id', string='Tareas Generadas')

    @api.multi
    def invoice_validate(self):
        # raise osv.except_osv('Esto es un Mesaje!','Hola')
        for line in self.invoice_line_ids:

            if line.tipo_servicio:

                self.tarea_ids |= self.env['rbs.tarea'].create(
                                        {
                                            'descripcion': line.name,
                                            'tipo_servicio': line.tipo_servicio,
                                            'user_id': line.user_id.id,
                                            'fecha_estimada': line.fecha_estimada,
                                            'factura_id': self.id,
                                            'persona_id': line.persona_id.id,
                                            'bien_id': line.bien_id.id
                                        })

        return super(factura_invoice, self).invoice_validate()


class account_invoice_line(models.Model):

    _inherit = "account.invoice.line"
    tipo_servicio = fields.Selection(related="product_id.tipo_servicio")
    user_id = fields.Many2one('res.users', string="Asignado a", required=True)

    fecha_estimada = fields.Datetime("Fecha estimada", required=True)

    persona_id = fields.Many2one("rbs.persona", string="Persona")
    bien_id = fields.Many2one("rbs.bien.inmueble", string="Bien")
    # domain=[('clave_catastral', '=', _get_domain())]

    @api.onchange('persona_id')
    def onchange_persona_id(self):
        self.bien_id = None
        clave_catastral = self.env["rbs.bien"].get_bienesPorIdentificacion(self.persona_id.num_identificacion)
        return {'domain': {'bien_id': [('clave_catastral', 'in', clave_catastral)]}}

    @api.onchange('tipo_servicio')
    def onchange_tipo_servicio(self):
        self.user_id = None

        if self.tipo_servicio in ('inscripcion_propiedad', 'inscripcion_mercantil'):
            ids = self.env.ref('registro_mercantil.group_registrador').ids
            return {'domain': {'user_id': [('groups_id', 'in', ids)]}}

        if self.tipo_servicio in ('certificacion_propiedad', 'certificacion_mercantil'):
            ids = self.env.ref('registro_mercantil.group_certificador').ids
            return {'domain': {'user_id': [('groups_id', 'in', ids)]}}

    @api.onchange('name')
    def onchange_product_id_cant_dias(self):
        # try:
        self.fecha_estimada = (
                                datetime.strptime(datetime.now().strftime('%Y-%m-%d'), '%Y-%m-%d') +
                                timedelta(days=self.product_id.cantidad_dias + 1)
                              ).strftime('%Y-%m-%d')


class product_template(models.Model):
    _inherit = "product.template"
    tipo_servicio = fields.Selection([
        ('inscripcion_propiedad', 'Inscripcion Propiedad'),
        ('inscripcion_mercantil', 'Inscripcion Mercantil'),
        ('certificacion_propiedad', 'Certificacion Propiedad'),
        ('certificacion_mercantil', 'Certificacion Mercantil'),
        ], string="Tipo de servicio")\

    cantidad_dias = fields.Integer("Dias estimados para realizar el trabajo", required=True)
