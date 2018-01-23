# -*- coding: utf-8 -*-
from openerp import models, fields, api
from openerp.osv import osv


class rbs_bien(models.Model):

    _name = 'rbs.bien'
    _description = u"Bien"

    documento_propiedad_id = fields.Many2one('rbs.documento.propiedad', "Documento de propiedad")
    documento_mercantil_id = fields.Many2one('rbs.documento.mercantil', "Documento mercantil")
    numero_predial = fields.Char(string='Numero Predial')
    # name = fields.Char(string = 'Clave Catastral')
    clave_catastral = fields.Char(string='Clave Catastral')
    descripcion_bien = fields.Char(string='Descripcion del Bien')
    descripcion_lindero = fields.Text(string='Descripcion del lindero', default='NORTE:\n\nSUR:\n\nESTE:\n\nOESTE:')

    provincia_id = fields.Many2one('rbs.provincia', string='Provincia')
    canton_id = fields.Many2one('rbs.canton', string='Canton del Inmueble')
    parroquia_id = fields.Many2one('rbs.parroquia', string='Parroquia Inmueble')
    zona_id = fields.Many2one('rbs.zona', string='Zona')

    ubicacion_geografica = fields.Selection([
            ('NORTE', 'NORTE'),
            ('SUR', 'SUR'),
            ('ESTE', 'ESTE'),
            ('OESTE', 'OESTE'),
            ('SUROESTE', 'SUROESTE'),
            ('SURESTE', 'SURESTE'),
            ('NOROESTE', 'NOROESTE'),
            ('NORESTE', 'NORESTE'),
        ], string='Ubicacion Geografica', default='NORTE')
    superficie_area_numero = fields.Integer(string='Superficie o Area')
    superficie_area_letras = fields.Char(string='Superficie o Area')
    es_propiedad_horizontal = fields.Boolean(String='Propiedad Horizontal')
    parte_char_ids = fields.Many2many('rbs.parte.char', string='Partes')

    alicuota_ids = fields.One2many('rbs.alicuota', 'bien_id', "Alicuota")

    tipo_bien_id = fields.Many2one('rbs.tipo.bien', "Tipo de bien")
    chasis = fields.Char(string='Chasis/Serie')
    motor = fields.Char(string='Motor')
    marca = fields.Char(string='Marca')
    modelo = fields.Char(string='Modelo')
    anio_fabricacion = fields.Many2one('rbs.anio', string='Año de Fabricacion')
    placa = fields.Char(string='Placa')
    color = fields.Char(string='Color')
    numero_provisional = fields.Char(string='Numero Provisional')

    @api.multi
    def get_identificacionPropietario(self, clave_catastral):

        propiedad_ids = self.env['rbs.documento.propiedad'].search(
                [
                    ('bien_ids.clave_catastral', '=', clave_catastral),
                ], limit=1,
                order='fecha_inscripcion desc')
        print str(propiedad_ids) + "/" + clave_catastral
        duenoact = False
        for propiedad_line in propiedad_ids:
            for parte in propiedad_line.parte_ids:
                if parte.tipo_interviniente_id.name == 'COMPRADOR':
                    duenoact = parte.num_identificacion

                if duenoact:
                    break
            if duenoact:
                break
        return duenoact

    @api.multi
    def get_bienesPorIdentificacion(self, num_identificacion='9876543219001'):
        print "identificacion "+str(num_identificacion)
        # print "ctx "+str(ctx)
        # num_identificacion = '9876543219001'
        claves_catastrales = []
        resultado_sin_filtrar = self.env['rbs.documento.propiedad'].search(
            [
                ('parte_ids.num_identificacion', '=', num_identificacion),
                ('state', '=', 'done'),
            ],
            order='fecha_inscripcion desc')
        # raise osv.except_osv(str(resultado_sin_filtrar))
        # raise (num_identificacion)
        #   Hacer una lista de todas las claves catastrales
        for res in resultado_sin_filtrar:
            for bien in res.bien_ids:
                # print str(bien.clave_catastral)
                if bien.clave_catastral:
                    claves_catastrales.append(bien.clave_catastral)
        # elmininar claves repetidas
        claves_catastrales = list(set(claves_catastrales))
        # busca el ultimo movimiento de cada una de las claves catastrales y las agrega al campo 'propiedad_ids'
        # raise osv.except_osv(claves_catastrales)
        # print "claves_catastrales"
        bienes = []
        for clave_catastral in claves_catastrales:
            # raise osv.except_osv(self.get_propietario(clave_catastral))
            # print num_identificacion + "/" + self.get_propietario(clave_catastral).num_identificacion
            duenoact = self.get_identificacionPropietario(clave_catastral)
            print str(duenoact) + '/' + num_identificacion

            if num_identificacion == duenoact:
                bienes.append(clave_catastral)
        print bienes
        # raise osv.except_osv(bienes)
        return bienes

    def name_get(self):
        res = []
        for record in self:
            numero_predial = record.numero_predial
            clave_catastral = record.clave_catastral
            # pais = record.pais_id.name
            tit = "%s/%s" % (numero_predial, clave_catastral)
            res.append((record.id, tit))
        return res

    @api.onchange('numero_predial', 'clave_catastral')
    def onchange_numero_predial(self):
        parte_char_ids_num = []
        for parte_char in self.documento_propiedad_id.parte_char_ids:
            parte_char_ids_num.append(parte_char.id)
        self.parte_char_ids = [(6, 0, parte_char_ids_num)]
        # raise osv.except_osv('Esto es un Mesaje!',)


class rbs_tipo_bien(models.Model):
    _name = 'rbs.tipo.bien'
    _description = u"Tipo de bien"
    name = fields.Char("Descripción")
