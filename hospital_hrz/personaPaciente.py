#!/usr/bin/env python
# -*- coding: utf-8 -*-
from openerp.osv import osv
from openerp import pooler, fields, api, models
from openerp.tools.translate import _
from base_externa import connect

class paciente(models.Model):
    _name = "hrz.paciente"
    _description = "Persona"
    #is_patient  = fields.Boolean('Es paciente')
    id = fields.Integer('Id del paciente')
    name   = fields.Char('Nombre',readonly=True)
    numero_archivo = fields.Char('Numero de Archivo',readonly=True)
    cedula   = fields.Char('Cedula',readonly=True)
    telefono   = fields.Char('Telefono',    compute = "_getOtherFields")
    celular   = fields.Char('Celular',      compute = "_getOtherFields")
    direccion   = fields.Char('Direccion',  compute = "_getOtherFields")
    alergia   = fields.Char('Es alergico a:',  compute = "_getOtherFields")



    #cedula = fields.Integer('Cedula')mm
    
    @api.one
    def _getOtherFields(self):
        print( ' ------------------------------456879---------------------------- ')
        self.actualizarPacientes()
        myConnection = connect()
        cur = myConnection.cursor()
        
        cur.execute( "SELECT COALESCE(primer_apellido,' ')|| ' ' ||COALESCE(segundo_apellido,' ') || ' ' || COALESCE(primer_nombre,' '), numero_archivo,cedula,telefono,celular,direccion,alergia FROM agendamiento.paciente where id = "+str(self.id))
        resp = cur.fetchall()
        self.name =             resp[0][0]
        self.numero_archivo =   resp[0][1]
        self.cedula =           resp[0][2]
        self.telefono =         resp[0][3]
        self.celular =          resp[0][4]
        self.direccion =        resp[0][5]
        self.alergia =          resp[0][6]
        return True
    
    @api.v8
    def actualizarTablaPacientes(self):

        myConnection = connect()
        cur = myConnection.cursor()
        cur.execute( "SELECT count(*) from agendamiento.paciente")
        suma1 = cur.fetchall()[0][0]
        self._cr.execute("SELECT count(*) from hrz_paciente" )
        suma2 = self._cr.fetchall()[0][0]

        if suma1 != suma2:
            #raise osv.except_osv('Esto es un Mesaje!', str(suma1) +' - '+ str(suma2))
            
            #print(a)
            print( str(suma1) +' ------------------------------- '+ str(suma2))
            cur.execute( "SELECT '(' ||id|| ',''' || COALESCE(primer_apellido,' ')|| ' ' || COALESCE(segundo_apellido,' ') || ' ' || COALESCE(primer_nombre,' ') || ' ' ||COALESCE(segundo_nombre,' ') ||''',''' ||COALESCE(cedula,'S/D')|| ''',''' ||COALESCE(numero_archivo,'0')|| ''')' FROM agendamiento.paciente  order by id")
            a = cur.fetchall()

            valores = ",".join(map(lambda x: x[0], a))
            
            #for i in a:
            #        valores+=  i[0]
            #valores+='-'
            #valores = valores.replace(',-','')
            #raise osv.except_osv('Esto es un Mesaje!', 'llego2')
            

            self._cr.execute("DELETE from hrz_paciente" )
            #raise osv.except_osv('Esto es un Mesaje!', "INSERT INTO hrz_paciente (id) VALUES "+ valores)
            self._cr.execute("INSERT INTO hrz_paciente (id,name,cedula,numero_archivo) values "+ valores )
        return True

    @api.v8
    def actualizarPacientes(self):

        myConnection = connect()
        cur = myConnection.cursor()
        cur.execute( "SELECT MAX(id) from agendamiento.paciente")
        ultimo1 = cur.fetchall()[0][0]
        self._cr.execute("SELECT MAX(id) from hrz_paciente" )
        ultimo2 = self._cr.fetchall()[0][0]
        if ultimo2==None or ultimo2>ultimo1:
            self.actualizarTablaPacientes()
            pass
        elif ultimo1 != ultimo2 and ultimo2!=None:

            print( str(ultimo1) +' ------------------------------- '+ str(ultimo2))
            #raise osv.except_osv('Esto es un Mesaje!', "SELECT '(' ||id|| ',''' || COALESCE(primer_apellido,' ')|| ' ' || COALESCE(segundo_apellido,' ') || ' ' || COALESCE(primer_nombre,' ') || ' ' ||COALESCE(segundo_nombre,' ') ||''',''' ||COALESCE(cedula,'S/D')|| ''',''' ||COALESCE(numero_archivo,'0')|| ''')' FROM agendamiento.paciente where id > "+str(ultimo2)+"   order by id")
            cur.execute( "SELECT '(' ||id|| ',''' || COALESCE(primer_apellido,' ')|| ' ' || COALESCE(segundo_apellido,' ') || ' ' || COALESCE(primer_nombre,' ') || ' ' ||COALESCE(segundo_nombre,' ') ||''',''' ||COALESCE(cedula,'S/D')|| ''',''' ||COALESCE(numero_archivo,'0')|| ''')' FROM agendamiento.paciente where id > "+str(ultimo2)+"   order by id")
            a = cur.fetchall()

            valores = ",".join(map(lambda x: x[0], a))
            #raise osv.except_osv('Esto es un Mesaje!', valores)
            
            #for i in a:
            #        valores+=  i[0]
            #valores+='-'
            #valores = valores.replace(',-','')
            #print(valores)
            

            #self._cr.execute("DELETE from hrz_paciente" )
            #raise osv.except_osv('Esto es un Mesaje!', "INSERT INTO hrz_paciente (id) VALUES "+ valores)
            self._cr.execute("INSERT INTO hrz_paciente (id,name,cedula,numero_archivo) values "+ valores )
        return True


