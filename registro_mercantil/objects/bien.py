# -*- coding: utf-8 -*-
from openerp import models, fields, api
from openerp.osv import osv


class rbs_bien(models.Model):

    _name = 'rbs.bien'
    _description = u"Bien"

    documento_propiedad_id = fields.Many2one('rbs.documento.propiedad', "Documento de propiedad")
    documento_mercantil_id = fields.Many2one('rbs.documento.mercantil', "Documento mercantil")
    bien_inmueble_id = fields.Many2one('rbs.bien.inmueble', 'Bien inmueble', required=True)
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
    superficie_area_numero = fields.Integer(string='Superficie o area')
    superficie_area_letras = fields.Char(string='Superficie o area en letras')
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
                    ('state', '=', 'done'),
                ],
                order='fecha_inscripcion desc')
        print str(propiedad_ids) + "/" + clave_catastral
        duenoact = False
        # raise osv.except_osv('Esto es un Mesaje!',str(propiedad_ids))
        for propiedad_line in propiedad_ids:
            for parte in propiedad_line.parte_ids:
                if parte.tipo_interviniente_id.name == 'COMPRADOR':
                    duenoact = parte.num_identificacion
                    print parte.num_identificacion
                if duenoact:
                    break
            if duenoact:
                break
        

        return duenoact

    @api.multi
    def get_bienesPorIdentificacion(self, num_identificacion):

        print "identificacion "+str(num_identificacion)
        claves_catastrales = []
        resultado_sin_filtrar = self.env['rbs.documento.propiedad'].search(
            [
                ('parte_ids.num_identificacion', '=', num_identificacion),
                ('state', '=', 'done'),
            ],
            order='fecha_inscripcion desc')
        for res in resultado_sin_filtrar:
            for bien in res.bien_ids:
                if bien.clave_catastral:
                    claves_catastrales.append(bien.clave_catastral)
        claves_catastrales = list(set(claves_catastrales))
        bienes = []
        for clave_catastral in claves_catastrales:
            duenoact = self.get_identificacionPropietario(clave_catastral)
            print str(duenoact) + '/' + num_identificacion
            if num_identificacion == duenoact:
                bienes.append(clave_catastral)
        print bienes
        return bienes

    def name_get(self):
        res = []
        for record in self:
            numero_predial = record.numero_predial
            clave_catastral = record.clave_catastral
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

    @api.onchange('bien_inmueble_id')
    def onchangeConyuge(self):

        self.numero_predial = self.bien_inmueble_id.numero_predial
        self.clave_catastral = self.bien_inmueble_id.clave_catastral
        self.descripcion_bien = self.bien_inmueble_id.descripcion_bien
        self.descripcion_lindero = self.bien_inmueble_id.descripcion_lindero
        self.provincia_id = self.bien_inmueble_id.provincia_id
        self.canton_id = self.bien_inmueble_id.canton_id
        self.parroquia_id = self.bien_inmueble_id.parroquia_id
        self.zona_id = self.bien_inmueble_id.zona_id
        self.ubicacion_geografica = self.bien_inmueble_id.ubicacion_geografica
        self.superficie_area_numero = self.bien_inmueble_id.superficie_area_numero
        self.superficie_area_letras = self.bien_inmueble_id.superficie_area_letras
        self.es_propiedad_horizontal = self.bien_inmueble_id.es_propiedad_horizontal


class rbs_bien_inmueble(models.Model):
    _name = "rbs.bien.inmueble"
    _description = "Bien inmueble"
    _rec_name = 'clave_catastral'

    numero_predial = fields.Char(string='Numero Predial')
    clave_catastral = fields.Char(string='Clave Catastral', )
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
    superficie_area_numero = fields.Integer(string='Superficie o area')
    superficie_area_letras = fields.Char(string='Superficie o area en letras')
    es_propiedad_horizontal = fields.Boolean(String='Propiedad Horizontal')

    _sql_constraints = [
        ('bien_inmueble_clave_catastral_uniq',
         'UNIQUE (clave_catastral)',
         '!La clave catastral debe ser unica por bien!')]


class rbs_tipo_bien(models.Model):
    _name = 'rbs.tipo.bien'
    _description = u"Tipo de bien"
    name = fields.Char("Descripción")
