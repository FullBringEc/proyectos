from openerp import models, fields, api, _
from openerp.osv import osv
import time

#!/usr/bin/python
#import os

import subproceso
class opc_prueba(models.Model):
	_name ="opc.prueba"
	_description = "Prueba OPC"
	
	name = fields.Char(string ='name')	
	_defaults = {
        
    }
	'''@api.multi
	def obtenerDatoOpc(self):
		import OpenOPC
		opc = OpenOPC.open_client('192.168.1.115')
		v = opc.servers()[3]
		opc.connect(v)
		self.name = int(opc.read('Bucket Brigade.Int1')[0]) * 2
		#opc.write(('Bucket Brigade.Int1', self.name))
		opc.write(('Bucket Brigade.Int1', self.name))
		#opc.read(opc.list('Square Waves.*'))
		#self.name = v
		return True
	'''
	@api.multi
	def ejecutar_comando(self):
		time.sleep(60)
		raise osv.except_osv('prueba',_(subproceso.ejecutar("echo 'holasdsa'")))
		
		#self.name = v
		return True

		'''import OpenOPC

		opc = OpenOPC.client()
		import datetime, threading, time
		opc.connect('Citect.OPC.1')
		tags = ['Loop_3_SP']
		opc.read(tags, group='mygroup', update=1)
		while True:
		  try:
		     value = opc.read(group='mygroup')
		     print value
		  except OpenOPC.TimeoutError:
		     print "TimeoutError occured"

		  time.sleep(10)
		'''


