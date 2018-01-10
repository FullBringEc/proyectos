# -*- coding: utf-8 -*-

# import ast
# import base64
# import csv
# import functools
# import glob
# import itertools
# import jinja2
# import logging
# import operator
# import datetime
# import hashlib
# import os
# import re
# import simplejson
# import sys
# import time
# import urllib2
# import zlib
# from xml.etree import ElementTree
# from cStringIO import StringIO

# import babel.messages.pofile
# import werkzeug.utils
# import werkzeug.wrappers
# try:
#     import xlwt
# except ImportError:
#     xlwt = None

# import openerp
# import openerp.modules.registry
# from openerp.addons.web.controllers.main import Binary
# from openerp.addons.base.ir.ir_qweb import AssetsBundle
# from openerp.modules import get_module_resource
# from openerp.tools import topological_sort
# from openerp.tools.translate import _
# from openerp.tools import ustr
# from openerp import http

# from openerp.http import request, serialize_exception as _serialize_exception

# _logger = logging.getLogger(__name__)

# if hasattr(sys, 'frozen'):
    
#     path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'views'))
#     loader = jinja2.FileSystemLoader(path)
# else:
#     loader = jinja2.PackageLoader('openerp.addons.web_pdf_widget', "views")

# env = jinja2.Environment(loader=loader, autoescape=True)
# env.filters["json"] = simplejson.dumps


# BUNDLE_MAXAGE = 60 * 60 * 24 * 7
import json
import logging
import werkzeug.utils
import urllib
import ftputil
# from odoo import http
from openerp import http
# from odoo.http import request
from openerp.http import request

_logger = logging.getLogger(__name__)


class BinaryPdf(http.Controller):

    @http.route('/web_pdf_widget/BinaryPdf/pdf', type='http', auth="public")
    def pdf(self, model, id, field, **kw):
        last_update = '__last_update'
        Model = request.registry[model]
        cr, uid, context = request.cr, request.uid, request.context
        headers = [('Content-Type', 'application/pdf')]
        etag = request.httprequest.headers.get('If-None-Match')
        hashed_session = hashlib.md5(request.session_id).hexdigest()
        retag = hashed_session
        id = None if not id else simplejson.loads(id)
        if type(id) is list:
            id = id[0] # m2o
        try:
            if etag:
                if not id and hashed_session == etag:
                    return werkzeug.wrappers.Response(status=304)
                else:
                    date = Model.read(cr, uid, [id], [last_update], context)[0].get(last_update)
                    if hashlib.md5(date).hexdigest() == etag:
                        return werkzeug.wrappers.Response(status=304)

            if not id:
                res = Model.default_get(cr, uid, [field], context).get(field)
                image_base64 = res
            else:
                res = Model.read(cr, uid, [id], [last_update, field], context)[0]
                retag = hashlib.md5(res.get(last_update)).hexdigest()
                image_base64 = res.get(field)

            if kw.get('resize'):
                resize = kw.get('resize').split(',')
                if len(resize) == 2 and int(resize[0]) and int(resize[1]):
                    width = int(resize[0])
                    height = int(resize[1])
                    # resize maximum 500*500
                    if width > 500: width = 500
                    if height > 500: height = 500
                    image_base64 = openerp.tools.image_resize_image(base64_source=image_base64, size=(width, height), encoding='base64', filetype='PNG')

            image_data = base64.b64decode(image_base64)

        except Exception:
            image_data = self.placeholder()
        headers.append(('ETag', retag))
        headers.append(('Content-Length', len(image_data)))
        try:
            ncache = int(kw.get('cache'))
            headers.append(('Cache-Control', 'no-cache' if ncache == 0 else 'max-age=%s' % (ncache)))
        except:
            pass
        return request.make_response(image_data, headers)

    # @api.one
    @http.route('/ftp/web', type='http', auth='user',csrf=False)
    def ftp(self, debug=False,**k):
      
        cr, uid, context = request.cr, request.uid, request.context

        #ftp = self.pool.get("ir.config_parameter").get_param(cr, uid, "ftp.mercantil", default=None, context=context)
        ftp_tipo_documento = 'ftp.propiedad'#request.params.get('ftp','')   
        irconfig = request.env["ir.config_parameter"].get_param('ftp.propiedad', default=None)  
        ftp = irconfig
        


        ftp_host = ftputil.FTPHost(ftp,"anonymous","")
        r=['<ul class="jqueryFileTree" style="display: none;">']
        try:
            r=['<ul class="jqueryFileTree" style="display: none;">']
            d = urllib.unquote(request.params.get('dir',''))
            ftp_host.chdir(d)
            list = ftp_host.listdir(ftp_host.curdir)   
            if d[-1] == '/':
                d = d[:-1] 
            for ff in list:
               f = ff.split("/")[-1]
               if ftp_host.path.isdir(ff):
                   r.append('<li class="directory collapsed"><a href="#" rel="%s/">%s</a></li>' % (ftp_host.getcwd()+"/"+ff,f))
               else:
                   e=f[1][1:] # get .ext and remove dot
                   r.append('<li class="file ext_%s"><a href="#" rel="%s">%s</a></li>' % (e,ftp_host.getcwd()+"/"+ff,f))
            r.append('</ul>')
        except Exception,e:
           r.append('Could not load directory: %s' % str(e))
        r.append('</ul>')
        
        # return 
        return request.make_response(ftp+"?"+''.join(r))

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: