# -*- encoding: utf-8 -*-
 
#importamos la clase osv del modulo osv y fields
from openerp.osv import osv, fields
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
import base64
from openerp import  models, fields as field, api, _
from datetime import date, datetime, timedelta
from sys import api_version


TYPE2REFUND = {
    'out_invoice': 'out_refund',        # Customer Invoice
    'in_invoice': 'in_refund',          # Supplier Invoice
    'out_refund': 'out_invoice',        # Customer Refund
    'in_refund': 'in_invoice',          # Supplier Refund
}

 
class account_invoice(osv.osv_memory):
    _name = 'account.invoice' # Aqui va el mismo nombre de la clase que se hereda
    _inherit = 'account.invoice' # Permite la herencia propiamente dicho del objeto account.invoice 
    _columns = {
                'invoiceOrigen': fields.many2one('account.invoice','Documento Fuente'),
                'state_stock': fields.selection([
                                                 ('sinStock','Productos no Recibidos'),
                                                 ('conStock','Productos Recibidos')
                                                 ], 'Estado Stock'),
                'codsustento' : fields.many2one('sri.codsustento.t5','Codigo de Sustento'),
                'tpidprov' : fields.many2one('sri.tpidprov.t2','Tipo id Proveedor'),
                #'tipocomprobante' : fields.many2one('sri.tipocomprobante.t4','Tipo de Comprobante'),
                'formapag' : fields.many2one('sri.formapag.t16','Forma de Pago'),
                'pagolocext' : fields.many2one('sri.pagolocext.t18','Pago Local o Exterior',),
                'ruc' : fields.char('Ruc.'),
                'establecimiento': fields.char('Establecimiento.',size=3),
                'puntoemision': fields.char('Punto de emision.',size=3),
                'secuencial': fields.char('Secuencial.',size=49),
                'autorizacion' : fields.char('No. de autorización del comprobante de venta.',size=37),
                'paisefecpago' : fields.many2one('sri.paisefecpago.t19','Pais al que se Efectua el Pago.'),
                 #'genero':fields.selection([('hombre','Hombre'),('mujer','Mujer')],'Género', required=True),
                'aplicconvdobtrib' : fields.selection([('si','Si'),('no','No')],'Aplica Convenio de Doble Tributacion de Pago.'),
                'pagextsujretnorleg' : fields.char('Pago al exte. sujeto a retención',size=31),
                'basenograiva' : fields.float('Base Imponible No objeto a Iva'),
                'baseimponible' : fields.float('Base Imponible tarifa 0 IVA'),
                'baseimpgrav' : fields.float('Base Imponible tarifa IVA diferente de 0%'),
                'montoice' : fields.float('Monto ICE'),
                'montoiva' : fields.float('Monto Iva'),
                'valorretbienes' : fields.float('Retención IVA Bienes'),
                'valorretservicios' : fields.float('Retención IVA Servicios'),
                'valretserv100' : fields.float('Retención IVA 100%'),

                'estabretencion1' : fields.char('No. de serie del comprobante de retención establecimiento',size = 3),
                'ptoemiretencion1': fields.char('No. de serie del comprobante de retención punto de emisión',size = 3),
                'secretencion1'   : fields.char('No. secuencial del comprobante de retención',size = 9),
                'autretencion1'   : fields.char('No. de autorización del comprobante de retención',size = 37),
                'fechaemiRet1'    : fields.date('Fecha de emisión del comprobante de retención'),

                'docmodificado' : fields.many2one('sri.tipocomprobante.t4','Documento Modificado'),
                'estabmodificado': fields.char('Establecimiento Modificado',size=3),
                'ptoemimodificado': fields.char('Punto de emision Modificado',size=3),
                'secmodificado': fields.char('Secuencial.',size=49),
                
                'autmodificado' : fields.char('No. de autorización Modificado',size=37),}
    _defaults = {
        'codsustento': lambda self, cr, uid, c: self.default(cr, uid, 'sri.formapag.t16','01'),
        'tpidprov' : lambda self, cr, uid, c: self.default(cr, uid, 'sri.formapag.t16','01'),
        #'tipocomprobante' : lambda s, cr, u, c: u,
        'formapag' :lambda self, cr, uid, c: self.default(cr, uid, 'sri.formapag.t16','01'),
        
        'pagolocext' : lambda self, cr, uid, c: self.default(cr, uid,'sri.formapag.t16','01'),
        'state_stock' : 'sinStock',

        
    }
    def default(self, cr, uid,model,codigo,context=None):
        ids=self.pool.get(model).search(cr, uid, [('codigo','=',codigo),])
        return self.pool.get(model).browse(cr, uid, ids, context).id
    def _prepare_refund(self, invoice, date=None, period_id=None, description=None, journal_id=None):

        values = {}
        
        for field in ['name','invoiceOrigen','establecimiento','puntoemision','secuencial','autorizacion', 'reference', 'comment', 'date_due', 'partner_id', 'company_id',
                'account_id', 'currency_id', 'payment_term', 'user_id', 'fiscal_position']:
            if field == 'invoiceOrigen':
                values[field] = invoice['id']
            elif field =='establecimiento':
                values['estabmodificado'] = invoice[field]
            elif field =='puntoemision':
                values['ptoemimodificado'] = invoice[field]
            elif field =='secuencial':
                values['secmodificado'] = invoice[field]
            elif field =='autorizacion':
                values['autmodificado'] = invoice[field]
            elif invoice._fields[field].type == 'many2one':
                values[field] = invoice[field].id
            else:
                values[field] = invoice[field] or False

        values['invoice_line'] = self._refund_cleanup_lines(invoice.invoice_line)

        tax_lines = filter(lambda l: l.manual, invoice.tax_line)
        values['tax_line'] = self._refund_cleanup_lines(tax_lines)

        if journal_id:
            journal = self.env['account.journal'].browse(journal_id)
        elif invoice['type'] == 'in_invoice':
            journal = self.env['account.journal'].search([('type', '=', 'purchase_refund')], limit=1)
        else:
            journal = self.env['account.journal'].search([('type', '=', 'sale_refund')], limit=1)
        values['journal_id'] = journal.id

        values['type'] = TYPE2REFUND[invoice['type']]
        values['date_invoice'] = date or fields.Date.context_today(invoice)
        values['state'] = 'draft'
        values['number'] = False
        
        if period_id:
            values['period_id'] = period_id
        if description:
            values['name'] = description
        return values
    
    def onchange_invoice_id(self, cr, uid, ids,invoiceOrigen,context=None):
        result = {}
        try:
            invoice_ids = self.pool.get('account.invoice').search(cr, uid, [('id','=',invoiceOrigen),])
            invoice  = self.pool.get('account.invoice').browse(cr, uid, invoice_ids,context=None)
            
            if invoice:
                try:
                    result['estabmodificado'] = str(invoice[0].establecimiento) 
                except: 
                    pass
                try:
                    result['ptoemimodificado'] = str(invoice[0].puntoemision)
                except: 
                    pass
                try:
                    result['secmodificado'] = str(invoice[0].secuencial)
                except: 
                    pass
                try:
                    result['autmodificado'] = str(invoice[0].autorizacion)
                except: 
                    pass
        except:
            pass
        #raise osv.except_osv('Esto es un Mesaje!',result['estabmodificado']+'\t'+result['ptoemimodificado']+'\t'+result['secmodificado']+'\t'+result['autmodificado'])
        return { 'value':result, }
    def onchange_partner_id(self, cr, uid, ids, type, partner_id,date_invoice=False, payment_term=False, partner_bank_id=False, company_id=False,context=None):
        super(account_invoice,self).onchange_partner_id(cr, uid, ids, type, partner_id,date_invoice=False, payment_term=False, partner_bank_id=False, company_id=False,context=None)
        
        return self.onchange_partner_id_datos_sujeto(cr, uid, ids, type,partner_id)
    def onchange_partner_id_datos_sujeto(self, cr, uid, ids, type, partner_id,context=None):
        result = {}
        try:
            partner_ids = self.pool.get('res.partner').search(cr, uid, [('id','=',partner_id),])
            partner  = self.pool.get('res.partner').browse(cr, uid, partner_ids, context=None)
            
            
            if partner:
                #raise osv.except_osv('Esto es un Mesaje!',establecimiento)
                if  type == 'in_invoice':
                    try:
                        result['establecimiento'] = partner[0].establecimiento 
                    except: 
                        pass
                    try:
                        result['puntoemision'] = partner[0].puntoemision
                    except: 
                        pass
                    try:
                        result['autorizacion'] = partner[0].autorizacion_no
                    except: 
                        pass
                try:
                    result['ruc'] = partner[0].vat[2:]
                except: 
                    pass
                try:
                    result['tpidprov'] = partner[0].tpidprov
                except: 
                    pass
                
        except:
            pass
        return { 'value':result, }
    
    def button_reset_taxes(self, cr, uid, ids, context=None):
        super(account_invoice,self).button_reset_taxes(cr, uid, ids, context=None)
        a = self.read(cr, uid, ids, context=context)[0]

        inv_ids = self.pool.get('account.invoice').search(cr, uid, [('id','=',repr(a['id'])),])
        inv  = self.pool.get('account.invoice').browse(cr, uid, inv_ids, context)
        if inv:
            try:
                cr.execute("update account_invoice SET establecimiento = '"+inv[0].partner_id.establecimiento+"' WHERE id = '"+repr(a['id'])+"'")
            except:
                pass
            try:
                cr.execute("update account_invoice SET puntoemision = '"+inv[0].partner_id.puntoemision+"'  WHERE id = '"+repr(a['id'])+"'")
            except:
                pass
            try:
                cr.execute("update account_invoice SET ruc = '"+inv[0].partner_id.vat[2:]+"'  WHERE id = '"+repr(a['id'])+"'")
            except:
                pass
            try:
                cr.execute("update account_invoice SET autorizacion = '"+inv[0].partner_id.autorizacion_no+"' WHERE id = '"+repr(a['id'])+"'")
            except:
                pass
        #raise osv.except_osv('Esto es un Mesaje!',inv[0].state)
        
        self.obtener(cr,uid,a)
        return True
    
    def crear_stock_move_en_notaCredito(self, cr, uid,ids, context=None):
        Factura = self.read(cr, uid, ids, context=context)[0]
        if Factura['state_stock']=='conStock':
            raise osv.except_osv('Esto es un Mesaje!',Factura['state_stock'])
        
        stock_picking_ids = self.pool.get('stock.picking.type').search(cr, uid, [('name','=','Delivery Orders'),])
        stock_picking = self.pool.get('stock.picking.type').browse(cr, uid, stock_picking_ids, context)
        #raise osv.except_osv('Error!', stock_picking.id)
        
        stock_locaion_wh_ids = self.pool.get('stock.location').search(cr, uid, [('name','=','Stock'),])
        stock_location_wh = self.pool.get('stock.location').browse(cr, uid, stock_locaion_wh_ids, context)
        
        stock_locaion_cli_ids = self.pool.get('stock.location').search(cr, uid, [('name','=','Customers'),])
        stock_location_cli = self.pool.get('stock.location').browse(cr, uid, stock_locaion_cli_ids, context)
        
            
        invoice_ventas = self.pool.get('account.invoice').browse(cr, uid, ids, context)
        
        stock_move_obj = self.pool.get('stock.move')
        if invoice_ventas:
            for inv in invoice_ventas:
                if inv.invoice_line:
                    for product in inv.invoice_line:
                        
                        
                        vals = {
                            'name': product.name,
                            'product_id': product.product_id.id,
                            'product_uom': product.uos_id.id,
                            'date': inv.date_invoice,
                            'picking_type_id': stock_picking.id,
                            #'company_id': inventory.company_id.id,
                            #'inventory_id': inventory.id,
                            'state': 'assigned',
                            'origin': inv.number,
                            #'restrict_lot_id': todo_line.get('prod_lot_id'),
                            #'restrict_partner_id': todo_line.get('partner_id'),
                         }
                
                        
                            #found less than expected
                        if inv.type == 'out_refund': 
                            vals['partner_id'] = inv.partner_id.id
                            vals['location_id'] = stock_location_cli.id
                            vals['location_dest_id'] = stock_location_wh.id
                            vals['product_uom_qty'] = product.quantity
                        elif inv.type == 'out_invoice':
                            vals['partner_id'] = inv.partner_id.id
                            vals['location_id'] = stock_location_wh.id
                            vals['location_dest_id'] = stock_location_cli.id
                            vals['product_uom_qty'] = product.quantity
                        #stock_move_obj.create(cr, uid, vals, None)
                        
                        stock_move_obj.action_done(cr, uid, stock_move_obj.create(cr, uid, vals, None), context=None)
        self.write(cr, uid, Factura['id'], {'state_stock': 'conStock'}, context=context)
        return True

     
    def obtener(self, cr, uid, a,context=None):
        
        inv_tax_ids = self.pool.get('account.invoice.tax').search(cr, uid, [('invoice_id.id','=',repr(a['id'])),('tax_code_id.code','in',('511','521','421','422'))])
        inv_tax  = self.pool.get('account.invoice.tax').browse(cr, uid, inv_tax_ids, context)
        if inv_tax:
            montoiva = inv_tax[0].amount
            baseimpgrav = inv_tax[0].base_amount
            cr.execute("update account_invoice SET montoiva = "+repr(montoiva)+", baseimpgrav = "+repr(baseimpgrav)+" WHERE id = '"+repr(a['id'])+"'")
        
        inv_tax_ids = self.pool.get('account.invoice.tax').search(cr, uid, [('invoice_id.id','=',repr(a['id'])),('tax_code_id.code','in',('421','422'))])
        inv_tax  = self.pool.get('account.invoice.tax').browse(cr, uid, inv_tax_ids, context)
        if inv_tax:
            montoiva = inv_tax[0].amount
            baseimpgrav = inv_tax[0].base_amount
            cr.execute("update account_invoice SET montoiva = "+repr(montoiva)+", baseimpgrav = "+repr(baseimpgrav)+" WHERE id = '"+repr(a['id'])+"'")
        
        cr.execute("select amount_untaxed from account_invoice WHERE id = '"+repr(a['id'])+"'")
        try:
            baseimponible = cr.fetchall()[0][0] - baseimpgrav
            cr.execute("update account_invoice SET baseimponible = "+repr(baseimponible)+" WHERE id = '"+repr(a['id'])+"'")
        except:
            pass
        try:
            cr.execute("select amount from account_invoice_tax,account_tax_code where invoice_id = '"+repr(a['id'])+"' and account_tax_code.id = tax_code_id and account_tax_code.code = '721'")
            valorretbienes = cr.fetchall()[0][0]
            cr.execute("update account_invoice SET valorretbienes = "+repr(float(str(valorretbienes)[1:]))+" WHERE id = '"+repr(a['id'])+"'")
        except:
            cr.execute("update account_invoice SET valorretbienes = 0 WHERE id = '"+repr(a['id'])+"'")
            pass
        try:
            cr.execute("select amount from account_invoice_tax,account_tax_code where invoice_id = '"+repr(a['id'])+"' and account_tax_code.id = tax_code_id and account_tax_code.code = '723'")
            valorretservicios = cr.fetchall()[0][0]
            cr.execute("update account_invoice SET valorretservicios = "+repr(float(str(valorretservicios)[1:]))+" WHERE id = '"+repr(a['id'])+"'")
        except:
            cr.execute("update account_invoice SET valorretservicios = 0 WHERE id = '"+repr(a['id'])+"'")
            pass
        try:
            cr.execute("select amount from account_invoice_tax,account_tax_code where invoice_id = '"+repr(a['id'])+"' and account_tax_code.id = tax_code_id and account_tax_code.code = '725'")
            valretserv100 = cr.fetchall()[0][0]
            cr.execute("update account_invoice SET valretserv100 = "+repr(float(str(valretserv100)[1:]))+" WHERE id = '"+repr(a['id'])+"'")
        except:
            cr.execute("update account_invoice SET valretserv100 = 0 WHERE id = '"+repr(a['id'])+"'")
            pass

        return True


    def obtenertodo(self, cr, uid=1): 
        inv_ids = self.pool.get('account.invoice.tax').search(cr, uid,)
        inv  = self.pool.get('account.invoice.tax').browse(cr, uid, inv_ids, context)
        for i in inv:
            self.obtener(cr,uid,i.id)
    

account_invoice()
class res_partner(osv.osv):
    _name = 'res.partner' # Aqui va el mismo nombre de la clase que se hereda
    _inherit = 'res.partner'
    _columns = {
                'razonSocial': fields.char(size=300),
                'tpidprov' : fields.many2one('sri.tpidprov.t2','Tipo de Identificacion'),
                'autorizacion_no': fields.char('No de Autorizacion',size=10),
                'establecimiento': fields.char('Establecimiento',size=3),
                'puntoemision': fields.char('Punto Emision',size=3),
                'Ob_contabilidad': fields.boolean('Obligado a llevar contabilidad', required=False),
                'Con_especial': fields.char('N. Contrib. E.',size=5, required=False),
                
        }
res_partner()
class sri_punto_emision(models.Model):
    _name = 'sri.punto.emision'
    
    name= field.Char('Punto de Emision')
    secuencialFactura= field.Integer(string='Secuencias de Factura',size=9,default = 1)
    secuencialNotaCredito= field.Integer(string='Secuencial Nota de Credito',size=9,default = 1)
    secuencialGuiaRemision= field.Integer(string='Secuencial de Guia Remision',size=9,default = 1)
    secuencialNotaDebito= field.Integer(string='Secuencial de Nota Debito',size=9,default = 1)
    secuencialComprobnteRetencion= field.Integer(string='Secuencial Comprobante de Retencion',size=9,default = 1)
    company_id = field.Many2one('res.company',string='company',default=lambda self: self.env.user.company_id.id,readonly = True,)
    #lambda self, cr, uid, c: self.default(cr, uid, 'sri.formapag.t16','01'),
    #default=lambda self: self._context.get('type', 'out_invoice')
    @api.multi
    def getSecuencialFactura(self):
        secuencial = self.secuencialFactura
        self.secuencialFactura = secuencial+1
        #raise osv.except_osv('Esto es un Mesafsje!',str(secuencial))
        return secuencial
        
    @api.multi
    def getSecuencialNotaCredito(self):
        secuencial = self.secuencialNotaCredito
        self.secuencialNotaCredito = secuencial + 1
        return secuencial
    @api.multi
    def getSecuencialGuiaRemision(self):
        secuencial = self.secuencialGuiaRemision
        self.secuencialGuiaRemision = secuencial + 1
        return secuencial
    @api.multi
    def getSecuencialNotaDebito(self):
        secuencial = self.secuencialNotaDebito
        self.secuencialNotaDebito = secuencial + 1
        return secuencial
    @api.multi
    def getSecuencialComprobanteRetencion(self):
        secuencial = self.secuencialComprobnteRetencion
        self.secuencialComprobnteRetencion = secuencial + 1
        return secuencial
    
    
sri_punto_emision()

class res_users(osv.osv):
    _name = 'res.users' # Aqui va el mismo nombre de la clase que se hereda
    _inherit = 'res.users'
    ptoEmision = field.Many2one('sri.punto.emision',string='Punto de emision',
                                domain=lambda self: [('company_id', '=',  self.env.user.company_id.id)])
        #domain=lambda self: [('model', '=', self._name)]
    
    
res_users()

class account_tax(osv.osv):
    _name = 'account.tax' # Aqui va el mismo nombre de la clase que se hereda
    _inherit = 'account.tax'
    _columns = {
                'fae_codigo': fields.char('Codigo para Fae',size=1),
                'fae_codigoPorcentaje': fields.char('CodigoPorcentaje para Fae',size=5),
 
        }
    
account_tax()


#anulados
class sri_comprobantes_anulados(osv.osv):
    _name = 'sri.comprobantes.anulados'
    _columns = {
                'tipocomprobante': fields.many2one('sri.tipocomprobante.t4','Tipo de Comprobante'),
                'establecimiento': fields.char('Establecimiento',size=3),
                'emision': fields.char('Punto de Emision',size=3),
                'secuencialInicio': fields.char('Secuencial Inicio'),
                'secuencialFin': fields.char('Secuencial Fin'),
                'autorizacion': fields.char('No. de autorizacion',size=37),
                'period_id':fields.many2one('account.period', 'Periodo', required=True),
        }
sri_comprobantes_anulados()


