# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import time
from lxml import etree

from openerp.osv import osv
from openerp import fields, api, models
from openerp.osv.orm import setup_modifiers
from openerp.tools.translate import _
from openerp.exceptions import Warning
#from datetime import  date, timedelta
from datetime import datetime , timedelta
import time



class hrz_kardex_report(models.Model):
    _name = "hrz.kardex.report"
    _description = "Kardex"

    producto_id = fields.Many2one('hrz.producto', 'Producto', help='Seleccione el producto', required=True)
    date_from = fields.Date("Fecha inicio")
    date_to = fields.Date("Fecha Fin")

    
    def _print_report(self, cr, uid, ids, data, context=None):
        raise (_('Error!'), _('Not implemented.'))


    def get_movimientos(self):
        #filtra todos los movimientos sean del producto escogido en wl wizard y que se encuentre entre las fechas establecidas
        movimientos = self.env['hrz.producto.move'].search([('producto_id', '=', self.producto_id.id),('create_date', '>=', self.date_from),('create_date', '<', (datetime.strptime(self.date_to, '%Y-%m-%d')+ timedelta(days=1)).strftime('%Y-%m-%d'))])
        return movimientos


    @api.multi
    def check_report(self):
        '''data = {}
                                data = {'ids': [self.id], 'model': 'hrz.kardex.report'}
                                comp = self.env['report'].browse([2])
                                report_obj = self.env['report']
                                report = report_obj._get_report_from_name('hospital_hrz.report_comprobantes')
                                docargs = {
                                    'doc_ids': comp._ids,
                                    'doc_model': report.model,
                                    'docs': comp,
                                    }
                                assert len(self) == 1, 'This option should only be used for a single id at a time.'''
        return self.env['report'].get_action(self, 'hospital_hrz.report_kardex')


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
