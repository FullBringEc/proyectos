from openerp.osv import osv, orm, fields
import openerp.addons.decimal_precision as dp
from openerp import pooler, fields as field, api, models

class sale_order(osv.osv):
    _name = "sale.order"
    _inherit = ['sale.order']
     
    def _discount_all(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for order in self.browse(cr, uid, ids, context=context):
            tot_disc = 0.0
            for line in order.order_line:
                tot_disc += line.disc_line
            res[order.id] = tot_disc
        return res
     
    def _total_all(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for order in self.browse(cr, uid, ids, context=context):
            tot_all = 0.0
            for line in order.order_line:
                tot_all += line.total_line
            res[order.id] = tot_all
        return res
     
    _columns = {
        'disc_total': fields.function(_discount_all, string='Total Discount', type="float", digits_compute= dp.get_precision('Account'), store=True),
        'total_b4_disc':fields.function(_total_all, string='Total Before Discount', type="float", digits_compute= dp.get_precision('Account'), store=True),
    }
    


class sale_order_line(osv.osv):
    _name = "sale.order.line"
    _inherit = ['sale.order.line']
    
    def _discount_line (self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for line in self.browse(cr, uid, ids):
            discount = line.price_unit * ((line.discount or 0.0)/100.0) * line.product_uom_qty
            res[line.id] = discount
        return res
    
    
    disc_line = field.Float(string='Discount', digits_compute= dp.get_precision('Account'),readonly=True, states={'draft': [('readonly', False)]})
    total_line = field.Float(compute="_total_line", string='Total', digits_compute= dp.get_precision('Account'), store=True)

    @api.depends('product_uom_qty','price_unit')
    def _total_line(self):
        self.total_line = self.price_unit * self.product_uom_qty

    @api.onchange('disc_line','total_line')
    def onchange_disc_line(self):
        try:
            self.discount =  (self.disc_line*100)/self.total_line 
        except:
            pass
        

    
    

    
    
    
    
    
    
    
    
    
    
