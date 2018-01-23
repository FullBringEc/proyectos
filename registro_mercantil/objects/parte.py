# -*- coding: utf-8 -*-
from openerp import models, fields, api
# from openerp.osv import osv


class rbs_parte_char(models.Model):
    _name = 'rbs.parte.char'
    _description = "Parte"
    name = fields.Char("Parte")
    parte_id = fields.Many2one('rbs.parte', string='Parte')
    bien_ids = fields.Many2many('rbs.bien', string='Bien')
    documento_propiedad_id = fields.Many2one('rbs.documento.propiedad', "Documento de Propiedad")
    documento_mercantil_id = fields.Many2one('rbs.documento.mercantil', "Documento mercantil")


class rbs_parte(models.Model):
    _name = 'rbs.parte'
    _description = "Parte"
    documento_propiedad_id = fields.Many2one('rbs.documento.propiedad', "Documento de propiedad")
    documento_mercantil_id = fields.Many2one('rbs.documento.mercantil', "Documento mercantil")
    persona_id = fields.Many2one('rbs.persona', string='Compareciente(n)', required=True)
    tipo_persona = fields.Selection([
            ('NATURAL', 'NATURAL'),
            ('JURIDICA', 'JURIDICA'),
        ], string='Tipo de Persona')

    razon_social = fields.Char(string='Razon Social')
    persona_id_tipo_persona = fields.Selection(related='persona_id.tipo_persona')
    nombres = fields.Char(string='Nombres del Compareciente')
    apellidos = fields.Char(string='Apellidos del Compareciente')

    tipo_interviniente_id = fields.Many2one('rbs.tipo.interviniente', string='Tipo de Interviniente')
    calidad_compareciente_id = fields.Many2one('rbs.calidad.compareciente', string='Calidad de Compareciente')
    tipo_documento = fields.Selection([
            ('CEDULA', 'CEDULA'),
            ('RUC', 'RUC'),
            ('PASAPORTE', 'PASAPORTE'),
        ], string='Tipo Documento')
    num_identificacion = fields.Char(string='Cedula del Compareciente')
    estado_civil = fields.Selection([
            ('CASADO', 'CASADO'),
            ('DIVORCIADO', 'DIVORCIADO'),
            ('NO APLICA', 'NO APLICA'),
            ('SOLTERO', 'SOLTERO'),
            ('UNION DE HECHO', 'UNION DE HECHO'),
            ('UNION LIBRE', 'UNION LIBRE'),
            ('VIUDO', 'VIUDO'),
        ], string='Estado Civil')
    num_identificacion_conyuge = fields.Char(string='Numero de Identificacion del cónyuge')
    nombres_conyuge = fields.Char(string='Nombres y apellidos del Cónyuge')
    separacion_bienes = fields.Boolean(string='Separacion de Bienes')
    es_menor = fields.Boolean(string='Es menor')
    tutor = fields.Char(string='Tutor o curador')

    def name_get(self):
        res = []
        for record in self:
            razon_social = record.razon_social or ''
            nombres = record.nombres or ''
            # pais = record.pais_id.name
            tit = "%s%s" % (razon_social, nombres)
            res.append((record.id, tit))
        return res

    @api.onchange('persona_id')
    def onchangeConyuge(self):

        self.nombres = self.persona_id.persona_nombres
        self.apellidos = self.persona_id.persona_apellidos
        self.tipo_documento = self.persona_id.tipo_documento
        self.num_identificacion = self.persona_id.num_identificacion
        self.estado_civil = self.persona_id.estado_civil
        self.razon_social = self.persona_id.persona_razonSocial
        self.tipo_persona = self.persona_id.tipo_persona
        # self.conyuge_id.conyuge_id = self.id


class rbs_persona(models.Model):
    _name = "rbs.persona"
    _description = "persona"
    _rec_name = 'num_identificacion'
    tipo_persona = fields.Selection([
            ('NATURAL', 'NATURAL'),
            ('JURIDICA', 'JURIDICA'),
        ], string='Tipo de Persona', required=True)
    persona_razonSocial = fields.Char(string='Razon Social')
    persona_nombres = fields.Char(string='Nombres del Compareciente')
    persona_apellidos = fields.Char(string='Apellidos del Compareciente')
    tipo_documento = fields.Selection([
            ('CEDULA', 'CEDULA'),
            ('RUC', 'RUC'),
            ('PASAPORTE', 'PASAPORTE'),
        ], string='Tipo Documento', required=True)
    num_identificacion = fields.Char(string='Cedula del Compareciente', required=True)
    estado_civil = fields.Selection([
            ('CASADO', 'CASADO'),
            ('DIVORCIADO', 'DIVORCIADO'),
            ('NO APLICA', 'NO APLICA'),
            ('SOLTERO', 'SOLTERO'),
            ('UNION DE HECHO', 'UNION DE HECHO'),
            ('UNION LIBRE', 'UNION LIBRE'),
            ('VIUDO', 'VIUDO'),
        ], string='Estado Civil')
    # conyuge_id = fields.Many2one('rbs.persona', string ='Cónyuge')
    _sql_constraints = [
        ('namea_uniq', 'unique(num_identificacion)',
            'La identificacion de la Persona debe ser unica'),
    ]
    _order = 'persona_nombres'

    @api.onchange('tipo_persona')
    def onchangeTipo_persona(self):
        if self.tipo_persona == 'JURIDICA':
            self.persona_nombres = ""
            self.persona_apellidos = ""
            self.estado_civil = ""
            self.conyuge_id = None
        if self.tipo_persona == 'NATURAL':
            self.persona_razonSocial = ""
    # @api.multi
    # @api.onchange('conyuge_id')
    # def onchangeConyuge(self):
    #   # raise osv.except_osv('Esto es un Mesaje!',self.conyuge_id)
    #   self.conyuge_id.conyuge_id = self.id
