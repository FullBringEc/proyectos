#!/usr/bin/env python
# -*- coding: utf-8 -*-
from openerp.osv import osv
from openerp import pooler, fields, api, models
from openerp.tools.translate import _
from base_externa import connect

class medico(models.Model):
    _name = "hrz.medico"
    _description = "Medico"
    #is_patient  = fields.Boolean('Es paciente')
    id = fields.Integer('Id del Medico')
    name   = fields.Char('Nombre',readonly=True)
    cedula   = fields.Char('Cedula',readonly=True)
    telefono   = fields.Char('Telefono',readonly=True)
    #titulo   = fields.Char('Titulo',  readonly=True)
    especialidad_id = fields.Many2one('hrz.especialidad', string = 'Especialidad',readonly = True, store=True)
    correo = fields.Char('Email',compute='_getEmail')
    @api.one
    def _getEmail(self):
        myConnection = connect()
        cur = myConnection.cursor()
        cur.execute( "SELECT mail FROM inventario.persona where ci = '"+str(self.cedula)+"'")
        resp = cur.fetchall()
        self.correo =           resp[0][0]
        return True
    '''
    @api.one
    def _getOtherFields(self):
        print( ' ------------------------------456879---------------------------- ')
        self.actualizarPacientes()
        myConnection = connect()
        cur = myConnection.cursor()
        
        cur.execute( "SELECT nombre|| ' ' ||apellido,cedula,telefono,titulo FROM agendamiento.medico where idmedico = "+str(self.id))
        resp = cur.fetchall()
        self.name =           resp[0][0]
        self.cedula =         resp[0][1]
        self.telefono =       resp[0][2]
        self.titulo =         resp[0][3]
       
        return True
    '''

    @api.one
    def _getOtherFields(self):
        print( ' ------------------------------456879---------------------------- ')
        self.actualizarPacientes()
        myConnection = connect()
        cur = myConnection.cursor()
        
        cur.execute( "SELECT nom1|| ' ' ||nom2|| ' ' ||ape1|| ' ' ||ape2,ci,tel1 FROM inventario.persona where idper = "+str(self.id))
        resp = cur.fetchall()
        self.name =           resp[0][0]
        self.cedula =         resp[0][1]
        self.telefono =       resp[0][2]
        #self.titulo =         resp[0][3]
       
        return True
    

    @api.v8
    def actualizarMedicos(self):
        self.env['hrz.especialidad'].actualizarEspecialidad()
        myConnection = connect()
        cur = myConnection.cursor()
        cur.execute( "SELECT count(*) from agendamiento.medico")
        suma1 = cur.fetchall()[0][0]
        self._cr.execute("SELECT count(*) from hrz_medico" )
        suma2 = self._cr.fetchall()[0][0]

        if suma1 != suma2:
            print( str(suma1) +' ------------------------------- '+ str(suma2))
            SqlConsulta = """SELECT '(' ||p.idper|| ',''' || nom1|| ' ' ||nom2|| ' ' ||ape1|| ' ' ||ape2 ||''',''' ||COALESCE(ci,'S/D')|| ''',''' ||COALESCE(tel1,'S/D')|| ''',' ||pr.idespecialidad|| ')'
                FROM inventario.persona p,inventario.personaxrol pr, inventario.rol r
                where p.idper = pr.idper and pr.idrol = r.idrol and r.nrol = 'MEDICO'
                order by p.idper"""

            #cur.execute( "SELECT '(' ||idper|| ',''' || nom1|| ' ' ||nom2|| ' ' ||ape1|| ' ' ||ape2 ||''',''' ||COALESCE(ci,'S/D')|| ''',''' ||COALESCE(tel1,'S/D')|| ''',' ||COALESCE(idespecialidad,'0')|| ')' FROM inventario.persona  order by idper")
            cur.execute( SqlConsulta)
            a = cur.fetchall()
            valores = ",".join(map(lambda x: x[0], a))
            self._cr.execute("DELETE from hrz_medico" )
            #raise osv.except_osv('Esto es un Mesaje!', "INSERT INTO hrz_paciente (id) VALUES "+ valores)
            self._cr.execute("INSERT INTO hrz_medico (id,name,cedula,telefono,especialidad_id) values "+ valores )
        return True

class Especialidad(models.Model):
    _name ="hrz.especialidad"
    _description = "Especialidad"
    name = fields.Char('Nombre de Especialidad')
    @api.v8
    def actualizarEspecialidad(self):

        myConnection = connect()
        cur = myConnection.cursor()
        cur.execute( "SELECT count(*) from agendamiento.especialidadmedica")
        suma1 = cur.fetchall()[0][0]
        self._cr.execute("SELECT count(*) from hrz_especialidad" )
        suma2 = self._cr.fetchall()[0][0]

        if suma1 != suma2:
            print( str(suma1) +' ------------------------------- '+ str(suma2))
            cur.execute( "SELECT '(' ||idespecialidad|| ',''' ||COALESCE(especialidad,' ')|| ''')' FROM agendamiento.especialidadmedica  order by idespecialidad")
            a = cur.fetchall()
            valores = ",".join(map(lambda x: x[0], a))
            self._cr.execute("DELETE from hrz_especialidad" )
            #raise osv.except_osv('Esto es un Mesaje!', "SELECT '(' ||idespecialidad|| ',''' ||COALESCE(especialidad,' ')|| ''')' FROM agendamiento.especialidadmedica  order by idespecialidad")
            self._cr.execute("INSERT INTO hrz_especialidad (id,name) values "+ valores )
        return True







