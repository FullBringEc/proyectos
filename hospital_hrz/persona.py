#!/usr/bin/env python
# -*- coding: utf-8 -*-
from openerp.osv import osv
from openerp import pooler, fields, api, models
from openerp.tools.translate import _
import re

class persona(models.Model):
    _name = "res.partner"
    _inherit = "res.partner"
    _description = "Persona"
    #is_patient  = fields.Boolean('Es paciente')
    #is_doctor   = fields.Boolean('Es doctor')
    medico_id   = fields.Many2one('hrz.medico',string= 'Medico')
    is_provider = fields.Boolean('Es Proveedor')

    #numero_archivo = fields.Char('Numero de archivo')
    cedula = fields.Char('Cedula',size = 13)
    sexo = fields.Selection([('male','Masculino'),('female','Femenino')])

    especialidad_id = fields.Many2one('hrz.especialidad',related='medico_id.especialidad_id', string = 'Especialidad')

    empresa = fields.Char('Empresa')

    observacion = fields.Text('Observacion')
    Saldo = fields.Float('Saldo')

    

    @api.one
    def actualizarMedicos(self):
        self.env['hrz.medico'].actualizarMedicos()
        return True

    @api.onchange('empresa','observacion','name','street','street2','city','function')
    def _uppercase(self):
        def upperField(field):
            if field != False:
                field = str(unicode(field).encode('utf-8')).upper()         
            return field
        self.empresa =   upperField(self.empresa)
        self.observacion  =   upperField(self.observacion)
        self.name  =   upperField(self.name)
        self.street  =   upperField(self.street)
        self.street2  =   upperField(self.street2)
        self.city  =   upperField(self.city)
        self.function  =   upperField(self.function)

    @api.one
    @api.onchange('phone','cedula','mobile')
    def _soloNumeros(self):
        self.phone =   re.sub("\D", "", str(self.phone))
        self.cedula =   re.sub("\D", "", str(self.cedula))
        self.mobile =   re.sub("\D", "", str(self.mobile))

class usuario(models.Model):
    _name = "res.users"
    _inherit = "res.users"
    bodega_ids = fields.Many2many(
        comodel_name='hrz.bodega',
        inverse_name='responsables_ids',
        string='Bodegas autorizadas',
    )

    @api.onchange('medico_id') # if these fields are changed, call method
    def onchangeMedico(self):
        self.name = self.medico_id.name
        self.login = self.medico_id.correo

    @api.onchange('name') # if these fields are changed, call method
    def check_change(self):
        def upperField(field):
            if field != False:
                field = str(unicode(field).encode('utf-8')).upper()         
            return field
        self.name =   upperField(self.name)

    @api.one
    def actualizarMedicos(self):
        self.env['hrz.medico'].actualizarMedicos()
        return True




