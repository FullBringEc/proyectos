# -*- encoding: utf-8 -*-
 
#importamos la clase osv del modulo osv y fields
from openerp.osv import osv, fields
#from xml.etree.ElementTree import Element, SubElement, Comment, tostring
 
 #tabla dos
class sri_tpidprov_t2(osv.osv):
    _name = 'sri.tpidprov.t2' 
    _columns = {
                'codigo': fields.char('Código',size=2),
                'codigoC': fields.char('Código',size=2),
                'name': fields.char('Tipo de Identificación'),
                
        }
sri_tpidprov_t2()

#tabla cinco
class sri_codsustento_t5(osv.osv):
    _name = 'sri.codsustento.t5' 
    _columns = {
                'codigo': fields.char('Código',size=2),
                'name': fields.char('Tipo de Sustento'),

        }
sri_codsustento_t5()

#tabla cuatro
class sri_tipocomprobante_t4(osv.osv):
    _name = 'sri.tipocomprobante.t4' # Aqui va el mismo nombre de la clase que se hereda
    _columns = {
                'codigo': fields.char('Código',size=3),
                'name': fields.char('Tipo de Comprobante'),
        }
sri_tipocomprobante_t4()
#tabla 16
class sri_formapag_t16(osv.osv):
    _name = 'sri.formapag.t16' # Aqui va el mismo nombre de la clase que se hereda
    _columns = {
                'codigo': fields.char('Código',size=2),
                'name': fields.char('Formas de pago'),
        }
sri_formapag_t16()
#tabla 18
class sri_pagolocext_t18(osv.osv):
    _name = 'sri.pagolocext.t18' # Aqui va el mismo nombre de la clase que se hereda
    _columns = {
                'codigo': fields.char('Código',size=2),
                'name': fields.char('Pago Local o al Exterior'),
        }
sri_pagolocext_t18()
#tabla 19
class sri_paisefecpago_t19(osv.osv):
    _name = 'sri.paisefecpago.t19' # Aqui va el mismo nombre de la clase que se hereda
    _columns = {
                'codigo': fields.char('Código',size=2),
                'name': fields.char('Pago Local o al Exterior'),
        }
sri_paisefecpago_t19()

