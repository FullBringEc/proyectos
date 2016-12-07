# -*- encoding: utf-8 -*-
########################################################################


from openerp.osv import fields,osv
import openerp.addons.decimal_precision as dp
from openerp.tools.translate import _
from openerp.tools import config
import time
from xml.etree.ElementTree import Element, SubElement, ElementTree, tostring
import sys
import base64

class sri_ats(osv.osv_memory):
    mes_lista=[]


    
    def indent(self,elem, level=0):
        i = "\n" + level*"  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                self.indent(elem, level+1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i

    def tipo_identificacion_compra(self,type):
        if type=='ruc':
            return '01'
        elif type=='cedula':
            return '02'
        
        
    def tipo_identificacion_venta(self,type):
        if type=='ruc':
            return '04'
        elif type=='cedula':
            return '05'
        elif type=='consumidor':
            return '07'
        
    def formato_numero(self,valor):
        tup= valor.split('.')
        if len(tup[1])== 1:
            return valor+"0"
        return valor
    
    def valor(self,tup):
        if tup:
            return tup[0]
        else:
            return 0.0
    
    def act_cancelar(self, cr, uid, ids, context=None):
        return {'type':'ir.actions.act_window_close' }
    
    def act_destroy(self, *args):
        return {'type':'ir.actions.act_window_close' }
    def numeroPositivo(self, numero):
        if numero<0:
            numero = numero*-1
        return numero
    
    def generate_xml(self, cr, uid, ids, context=None):
        tieneErrores=False
        errores = 'aa'
        root = ''
        totalVentas = 0
        for anexo in self.browse(cr, uid, ids, context=context):
            #Facturas en compras que pertenecen al periodo
            invoice_compras_ids = self.pool.get('account.invoice').search(cr, uid, [('period_id.id','=',anexo['period_id']['id']),('type','=','in_invoice'),('state','in',('open','paid')),])
            invoice_compras = self.pool.get('account.invoice').browse(cr, uid, invoice_compras_ids, context)
            #Facturas en ventas que pertenecen al periodo
            invoice_ventas_ids = self.pool.get('account.invoice').search(cr, uid, [('period_id.id','=',anexo['period_id']['id']),('type','=','out_invoice'),('state','in',('open','paid')),])
            invoice_ventas = self.pool.get('account.invoice').browse(cr, uid, invoice_ventas_ids, context)
            
            
            #Notas de Credito en ventas que pertenecen al periodo
            refund_ventas_ids = self.pool.get('account.invoice').search(cr, uid, [('period_id.id','=',anexo['period_id']['id']),('type','=','out_refund'),('state','in',('open','paid')),])
            refund_ventas = self.pool.get('account.invoice').browse(cr, uid, refund_ventas_ids, context)
            
            
            #Notas de Credito en compras que pertenecen al periodo
            refund_compras_ids = self.pool.get('account.invoice').search(cr, uid, [('period_id.id','=',anexo['period_id']['id']),('type','=','in_refund'),('state','in',('open','paid')),])
            refund_compras = self.pool.get('account.invoice').browse(cr, uid, refund_compras_ids, context)
            #Comprobantes anulados
            comprobantes_anulados_ids  = self.pool.get('sri.comprobantes.anulados').search(cr, uid, [('period_id.id','=',anexo['period_id']['id']),])
            comprobantes_anulados = self.pool.get('sri.comprobantes.anulados').browse(cr, uid, comprobantes_anulados_ids, context)
            #Facturas de Ventas Canceladas
            invoice_canceled_ids = self.pool.get('account.invoice').search(cr, uid, [('period_id.id','=',anexo['period_id']['id']),('type','=','out_invoice'),('state','=','cancel'),])
            invoice_canceled = self.pool.get('account.invoice').browse(cr, uid, invoice_canceled_ids, context)
            #Notas de Credito en Ventas Canceladas
            credit_note_canceled_ids = self.pool.get('account.invoice').search(cr, uid, [('period_id.id','=',anexo['period_id']['id']),('type','=','out_refund'),('state','=','cancel'),])
            credit_note_canceled = self.pool.get('account.invoice').browse(cr, uid, credit_note_canceled_ids, context)
            #Liquidacion de Compras Canceladas
            """
            liquidation_canceled_ids = self.pool.get('account.invoice').search(cr, uid, [('period_id.id','=',anexo['period_id']['id']),('type','=','in_invoice'),('state','=','cancel'),('liquidation','=',True)])
            liquidation_canceled = self.pool.get('account.invoice').browse(cr, uid, liquidation_canceled_ids, context)
            """
            errores = Element("error")
            company = self.pool.get('res.users').browse(cr, uid, [uid,], context)[0].company_id.partner_id
            root = Element("iva")
            mes= anexo['period_id']['name']
            self.mes_lista=mes.split('/')
            SubElement(root,"TipoIDInformante").text='R'

            try:
                SubElement(root,"IdInformante").text=company.vat[2:]
            except:
                SubElement(errores,"ErrorIdInformante").text="Pongale_ruc"
                tieneErrores=True
                pass
            SubElement(root,"razonSocial").text=company.name
            SubElement(root,"Anio").text=self.mes_lista[1]
            SubElement(root,"Mes").text=self.mes_lista[0]
            if company.establecimiento:
                SubElement(root,"numEstabRuc").text=company.establecimiento
            else:
                SubElement(errores,"ErrorEstablecimiento").text="Falta_establecimiento_en_la_empresa_"+company.name
                tieneErrores=True
            totalve  = SubElement(root,"totalVentas")
            SubElement(root,"codigoOperativo").text="IVA"
           

            
            #Se verifica que existan facturas en compras o Notas de Credito
            if invoice_compras:            
                compras = SubElement(root,"compras")
                for inv in invoice_compras:

                    #numero_factura=inv.number.split('-') 
                    fecha_emision=(str(inv.date_invoice))
                    fecha_emision=fecha_emision.split('-')
                    #fecha_registro=(str(inv.create_date))
                    #fecha_registro=fecha_registro.split(' ')
                    fecha_registro=fecha_emision
#                    fecha_registro=fecha_registro[0].split('-')
                    detalle = SubElement(compras,"detalleCompras")#
                    SubElement(detalle, "codSustento").text = inv.codsustento.codigo
                    SubElement(detalle, "tpIdProv").text = inv.tpidprov.codigoC

                    try:
                        SubElement(detalle, "idProv").text = inv.ruc
                    except:
                        pass

                    #Al escoger el voucher type se agregan tambien las liquidaciones de compras
                    SubElement(detalle, "tipoComprobante").text = '01'
                    SubElement(detalle, "fechaRegistro").text = fecha_registro[2]+"/"+fecha_registro[1]+"/"+fecha_registro[0]
                    if inv.establecimiento and inv.puntoemision and inv.secuencial:
                        SubElement(detalle, "establecimiento").text = inv.establecimiento
                        SubElement(detalle, "puntoEmision").text = inv.puntoemision
                        SubElement(detalle, "secuencial").text = inv.secuencial
                    else:
                         SubElement(errores,"errorEstPuntSec").text="Falta_establecimiento,_Punto_de_Emision_o_Secuencial_de_la_factura_"+inv.number
                         tieneErrores=True
                    SubElement(detalle, "fechaEmision").text = fecha_emision[2]+"/"+fecha_emision[1]+"/"+fecha_emision[0]

                    if inv.autorizacion:
                        SubElement(detalle, "autorizacion").text = inv.autorizacion     
                    else:
                        SubElement(errores,"errorAutorizacion").text="Falta_Autorizacion_en_la_factura_"+inv.number
                        tieneErrores=True


    
                    #CHECK: SE DEBE VERIFICAR QUE CADA LINEA DE FACTURA TENGA UN IMPUESTO AL MENOS, EN CASO DE NO TENER SE CONSIDERA COMO BASE QUE NO APLICA IVA
                    SubElement(detalle, "baseNoGraIva").text = str("%.2f" %inv.basenograiva)
                    SubElement(detalle, "baseImponible").text = str("%.2f" %inv.baseimponible)
                    SubElement(detalle, "baseImpGrav").text = str("%.2f" %inv.baseimpgrav)
                    SubElement(detalle, "montoIce").text = str("%.2f" %inv.montoice)
                    SubElement(detalle, "montoIva").text = str("%.2f" %inv.montoiva)
                    SubElement(detalle, "valorRetBienes").text = str("%.2f" %inv.valorretbienes)
                    SubElement(detalle, "valorRetServicios").text = str("%.2f" %inv.valorretservicios)
                    SubElement(detalle, "valRetServ100").text = str("%.2f" %inv.valretserv100)

                    ##esto no tiene que ir!!!!
                    #SubElement(detalle, "idfactura").text = str(inv.id)
                    #Pago local o exterior
                    pagoExterior = SubElement(detalle,"pagoExterior")
                    SubElement(pagoExterior,"pagoLocExt").text = '01'
                    SubElement(pagoExterior,"paisEfecPago").text = 'NA'
                    SubElement(pagoExterior,"aplicConvDobTrib").text = 'NA'
                    SubElement(pagoExterior,"pagExtSujRetNorLeg").text = 'NA'


                    #Retenciones en COmpras

                    retencionids = self.pool.get('account.invoice.tax').search(cr, uid, [('invoice_id.id','=',inv.id),('type_ec','=','renta'),('base_code_id.code','not in',('721','723','725'))])
                    retenciones = self.pool.get('account.invoice.tax').browse(cr, uid, retencionids, context)
                    if retenciones:
                        retencion = SubElement(detalle, "air")
                    for ret in retenciones:

                        #if ret.description == 'renta':
                        
                        detalle_retencion = SubElement(retencion, "detalleAir")
                        SubElement(detalle_retencion, "codRetAir").text = ret.base_code_id.code
                        SubElement(detalle_retencion, "baseImpAir").text = str("%.2f" %(ret.base_amount))#self.formato_numero(str(abs(ret.tax_base)))
                        valRetAir = float(ret.amount)
                        if valRetAir<0:
                            valRetAir = -valRetAir
                        
                        porcentaje_ids = self.pool.get('account.tax').search(cr, uid, [('base_code_id.id','=',ret.base_code_id.id)])
                        porcentaje = self.pool.get('account.tax').browse(cr, uid, porcentaje_ids, context)
                        porcentajeAir = porcentaje[0].amount *100
                        if porcentajeAir<0:
                            porcentajeAir = -porcentajeAir
                        SubElement(detalle_retencion, "porcentajeAir").text = self.formato_numero(str(porcentajeAir))#ret.tax_code_id#self.formato_numero(str(abs(ret.retention_percentage)))
                        SubElement(detalle_retencion, "valRetAir").text = self.formato_numero(str(valRetAir))#self.formato_numero(str(abs(ret.retained_value)))
        
                    
                    
    
                       
            #Notas de Credito de Proveedores
                for inv in refund_compras:
                    numero_factura = inv.number.split('-')
                    #numero_nota_credito = inv.invoice_rectification_id.split('-')
                    fecha_emision=(str(inv.date_invoice))
                    fecha_emision=fecha_emision.split('-')
                    fecha_registro=(str(inv.date_invoice))
                    fecha_registro=fecha_registro.split(' ')
                    fecha_registro=fecha_emision
                   #fecha_registro=fecha_registro[0].split('-')
                    detalle = SubElement(compras,"detalleCompras")
                    
                    SubElement(detalle, "codSustento").text = inv.codsustento.codigo
                    SubElement(detalle, "tpIdProv").text = inv.tpidprov.codigo
                    try:
                        SubElement(detalle, "idProv").text = inv.partner_id.vat[2:]
                    except:
                        pass
                    SubElement(detalle, "tipoComprobante").text = '04'
                    SubElement(detalle, "fechaRegistro").text = fecha_registro[2]+"/"+fecha_registro[1]+"/"+fecha_registro[0]

                    if inv.establecimiento and inv.puntoemision and inv.secuencial:
                        SubElement(detalle, "establecimiento").text = inv.establecimiento
                        SubElement(detalle, "puntoEmision").text = inv.puntoemision
                        SubElement(detalle, "secuencial").text = inv.secuencial
                    else:
                         SubElement(errores,"errorEstPuntSec").text="Falta_establecimiento_o_Punto_de_Emision_o_Secuencial_de_la_factura_"+inv.number
                         tieneErrores=True
                    SubElement(detalle, "fechaEmision").text = fecha_emision[2]+"/"+fecha_emision[1]+"/"+fecha_emision[0]

                    if inv.autorizacion:
                        SubElement(detalle, "autorizacion").text = inv.autorizacion     
                    else:
                        SubElement(errores,"errorAutorizacion").text="Falta_Autorizacion_en_la_factura_"+inv.number
                        tieneErrores=True


                    SubElement(detalle, "baseNoGraIva").text = str("%.2f" %inv.basenograiva)
                    SubElement(detalle, "baseImponible").text = str("%.2f" %inv.baseimponible)
                    SubElement(detalle, "baseImpGrav").text = str("%.2f" %inv.baseimpgrav)
                    SubElement(detalle, "montoIce").text = str("%.2f" %inv.montoice)
                    SubElement(detalle, "montoIva").text = str("%.2f" %inv.montoiva)
                    SubElement(detalle, "valorRetBienes").text = str("%.2f" %inv.valorretbienes)
                    SubElement(detalle, "valorRetServicios").text = str("%.2f" %inv.valorretservicios)
                    SubElement(detalle, "valRetServ100").text = str("%.2f" %inv.valretserv100)




                    pagoExterior = SubElement(detalle,"pagoExterior")
                    SubElement(pagoExterior,"pagoLocExt").text = '01'
                    SubElement(pagoExterior,"paisEfecPago").text = 'NA'
                    SubElement(pagoExterior,"aplicConvDobTrib").text = 'NA'
                    SubElement(pagoExterior,"pagExtSujRetNorLeg").text = 'NA'

                    
                    SubElement(detalle, "docModificado").text = inv.docmodificado.codigo
                    SubElement(detalle, "estabModificado").text = inv.estabmodificado
                    SubElement(detalle, "ptoEmiModificado").text = inv.ptoemimodificado
                    SubElement(detalle, "secModificado").text = inv.secmodificado
                    SubElement(detalle, "autModificado").text = inv.autmodificado
            #TODO: Liquidacion de Compras
            #TODO: NOTAS DE CREDITO EN VENTAS
            else:
                compras = SubElement(root,"compras")
        




            #FACTURAS DE VENTAS


        if invoice_ventas or refund_ventas:
            ventas = SubElement(root,"ventas")
        if invoice_ventas:
                list_client = []
                for inv in invoice_ventas:
                    client_id = self.pool.get('res.partner').search(cr, uid, [('id','=',inv['partner_id']['id']),])
                    if not client_id[0] in list_client:
                        list_client.append(client_id[0])
                cliente = self.pool.get('res.partner').browse(cr, uid, list_client, context)
                
                for cli in cliente:
                    #Facturas en Ventas
                    num_comprobantes_facturas=0
                    base=0.0
                    base_0=0.0
                    iva=0.0
                    iva_ret=0.0
                    renta_ret=0.0
                    inv_vent_ids=               self.pool.get('account.invoice').search(cr, uid, [('partner_id.id','=',cli['id']),('period_id.id','=',anexo['period_id']['id']),('type','=','out_invoice'),('state','in',('open','paid')),])
                    num_comprobantes_facturas= len(inv_vent_ids)
                    inv_ventas = self.pool.get('account.invoice').browse(cr, uid, inv_vent_ids, context)
                    for inv in inv_ventas:
                        base=base+self.valor([n.base for n in inv.tax_line if n.base_code_id.code in ("411",)])
                        base_0=base_0+self.valor([n.base for n in inv.tax_line if n.base_code_id.code in ("415","416","413","414")])
                        iva=iva+self.valor([n.amount for n in inv.tax_line if n.tax_code_id.code in ("421",)])
                        renta_ret=renta_ret+self.valor([n.amount for n in inv.tax_line if n.type_ec == "renta"])
                        iva_ret = iva_ret + inv.valretserv100 + inv.valorretservicios + inv.valorretbienes
                        
                    if inv_ventas:
                        detalle = SubElement(ventas,"detalldeVentas")
                        SubElement(detalle, "tpIdCliente").text = inv_ventas[0].tpidprov.codigo
                        try:
                            SubElement(detalle, "idCliente").text = inv_ventas[0].partner_id.vat[2:]
                        except:
                            pass
                        SubElement(detalle, "tipoComprobante").text = "18"
                        SubElement(detalle, "numeroComprobantes").text = str(num_comprobantes_facturas)
                        SubElement(detalle, "baseNoGraIva").text = "0.00"
                        SubElement(detalle, "baseImponible").text = self.formato_numero(str(base_0))
                        SubElement(detalle, "baseImpGrav").text = self.formato_numero(str(base))
                        SubElement(detalle, "montoIva").text = self.formato_numero(str(iva))
                        SubElement(detalle, "valorRetIva").text = self.formato_numero(str(self.numeroPositivo(iva_ret)))
                        SubElement(detalle, "valorRetRenta").text = self.formato_numero(str(self.numeroPositivo(renta_ret)))
                        '''if inv_ventas[0].partner_id.com1:
                            SubElement(detalle, "ventasEstab").text = inv_ventas[0].partner_id.com1
                        else:
                            SubElement(errores,"errorEstabVentas").text="Falta_establecimiento_en_cliente_"+inv_ventas[0].partner_id.name
                            tieneErrores=True
                        '''
                        totalVentas = totalVentas + float(base) + float(base_0)

        if refund_ventas:
                list_client = []
                for inv in refund_ventas:
                    client_id = self.pool.get('res.partner').search(cr, uid, [('id','=',inv['partner_id']['id']),])
                    if not client_id[0] in list_client:
                        list_client.append(client_id[0])
                cliente = self.pool.get('res.partner').browse(cr, uid, list_client, context)
                
                for cli in cliente:
                        
                    #Notas de Credito
                    num_comprobantes_nc=0
                    base_nc=0.0
                    base_nc_0=0.0
                    iva_nc=0.0
                    iva_ret_nc=0.0
                    renta_ret_nc=0.0
                    inv_notas_credito_ids=      self.pool.get('account.invoice').search(cr, uid, [('partner_id.id','=',cli['id']),('period_id.id','=',anexo['period_id']['id']),('type','=','out_refund'),('state','in',('open','paid')),])
                    num_comprobantes_nc= len(inv_notas_credito_ids)
                    inv_notas_credito = self.pool.get('account.invoice').browse(cr, uid, inv_notas_credito_ids, context)
                    for inv in inv_notas_credito:
                        '''
                        base_nc=base_nc+self.valor([n.base for n in inv.tax_line if n.base_code_id.code in ("411")])
                        base_nc_0=base_nc_0+self.valor([n.base for n in inv.tax_line if n.base_code_id.code in ("415","416","413","414")])
                        iva_nc=iva_nc+self.valor([n.amount for n in inv.tax_line if n.tax_code_id.code in ("421")])
                        renta_ret_nc=renta_ret_nc+self.valor([n.amount for n in inv.tax_line if n.type_ec == "renta"])
                        iva_ret_nc = iva_ret_nc + inv.valretserv100 + inv.valorretservicios + inv.valorretbienes
                        '''
                        base_nc=base_nc+float(inv.baseimpgrav)
                        base_nc_0=base_nc_0+float(inv.baseimponible)
                        iva_nc=iva_nc+float(inv.montoiva)
                        renta_ret_nc=renta_ret_nc+self.valor([n.amount for n in inv.tax_line if n.type_ec == "renta"])
                        iva_ret_nc = iva_ret_nc + inv.valretserv100 + inv.valorretservicios + inv.valorretbienes
                        
                    if inv_notas_credito:
                       
                        detalle = SubElement(ventas,"detalleVentas")
                        SubElement(detalle, "tpIdCliente").text = inv_notas_credito[0].tpidprov.codigo
                        try:
                            SubElement(detalle, "idCliente").text = inv_notas_credito[0].partner_id.vat[2:]
                        except:
                            pass
                        SubElement(detalle, "tipoComprobante").text = "04"
                        SubElement(detalle, "numeroComprobantes").text = str(num_comprobantes_nc)
                        SubElement(detalle, "baseNoGraIva").text = "0.00"
                        SubElement(detalle, "baseImponible").text = self.formato_numero(str(base_nc_0))
                        SubElement(detalle, "baseImpGrav").text = self.formato_numero(str(base_nc))
                        SubElement(detalle, "montoIva").text = self.formato_numero(str(iva_nc))
                        SubElement(detalle, "valorRetIva").text = self.formato_numero(str(self.numeroPositivo(iva_ret_nc)))
                        SubElement(detalle, "valorRetRenta").text = self.formato_numero(str(self.numeroPositivo(renta_ret_nc)))
                        
                        totalVentas = totalVentas - float(base_nc) - float(base_nc_0)

        ventasEstablecimiento = SubElement(root, "ventasEstablecimiento")
        codEstab = SubElement(ventasEstablecimiento, "ventaEst")
        SubElement(codEstab, "codEstab").text=company.establecimiento
        SubElement(codEstab, "ventasEstab").text= "%.2f" %totalVentas
        totalve.text = "%.2f" %totalVentas

        if comprobantes_anulados:
            anulados = SubElement(root,"anulados")
            for inv in comprobantes_anulados:
                detalle = SubElement(anulados,"detalleAnulados")
                SubElement(detalle, "tipoComprobante").text = inv.tipocomprobante.codigo
                SubElement(detalle, "establecimiento").text = inv.establecimiento
                SubElement(detalle, "puntoEmision").text = inv.emision
                SubElement(detalle, "secuencialInicio").text = inv.secuencialInicio
                SubElement(detalle, "secuencialFin").text = inv.secuencialFin
                SubElement(detalle, "autorizacion").text = inv.autorizacion
        #SubElement(root,"totalVentas").text= "%.2f" %totalVentas

           


            #TODO: Retenciones en Ventas es necesario sumar los valores por IVA y RENTA de las retenciones emitidos por cada cliente
            #TODO: Se debe iterar por cada cliente que se ha emitido un documento en el periodo que se informa
            
            #TODO: Escenario, se anulan documentos de diferentes autorizaciones en un mes
            #Si existe algun tipo de documento anulado 
        

        #TODO: NOTAS DE DEBITO, EN ESPERA DE MODULO DE NOTAS DE DEBITO
        
        
        #TODO: Exportaciones, en espera de modulo de Exportaciones) 
        
        if not tieneErrores:
            self.indent(root)
            return tostring(root,encoding="ISO-8859-1")
        else:
            self.indent(errores)
            return tostring(errores,encoding="ISO-8859-1")
        
    

    def act_export(self, cr, uid, ids, context={}):
        this = self.browse(cr, uid, ids)[0]
        root = self.generate_xml(cr,uid,ids)
        this.name = "AT.xml"
        #self._write_attachment(cr,uid,ids,root,context)
        out=base64.encodestring(root)
        self.write(cr, uid, ids, {'data':out, 'name':this.name, 'state': 'get'}, context=context)
        a = self.read(cr, uid, ids, context=context)[0]
        elId = repr(a['id'])
        
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'sri.ats',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': int(elId),
            'views': [(False, 'form')],
            'target': 'new',
             }


    

    _name = 'sri.ats'
    
    _columns = {
                'name':fields.char('name', size=20, readonly=True), 
                #'fiscalyear_id':fields.many2one('account.fiscalyear', 'Fiscal Year', required=True),
                'period_id':fields.many2one('account.period', 'Period', required=True),
                'data':fields.binary('File', readonly=True),
                'state':fields.selection([('choose','Choose'),('get','Get'),],  'state', required=True, readonly=True),}
    _defaults = {
                 'state': lambda *a: 'choose'
                 }
    
sri_ats()