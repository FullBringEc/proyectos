# -*- coding: utf-8 -*-

import ast
import base64
import csv
import functools
import glob
import itertools
import jinja2
import logging
import operator
import datetime
import hashlib
import os
import re
import simplejson
import sys
import time
import urllib2
import zlib
from xml.etree import ElementTree
from cStringIO import StringIO

import babel.messages.pofile
import werkzeug.utils
import werkzeug.wrappers
try:
    import xlwt
except ImportError:
    xlwt = None

import openerp
import openerp.modules.registry
from openerp.addons.web.controllers.main import Binary,  module_boot, login_redirect
from openerp.addons.base.ir.ir_qweb import AssetsBundle, QWebTemplateNotFound
from openerp.modules import get_module_resource
from openerp.tools import topological_sort
from openerp.tools.translate import _
from openerp.tools import ustr
from openerp import http
from PIL import Image
from io import BytesIO
import cStringIO
from openerp.http import request, serialize_exception as _serialize_exception

_logger = logging.getLogger(__name__)

if hasattr(sys, 'frozen'):
    # When running on compiled windows binary, we don't have access to package loader.
    path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'views'))
    loader = jinja2.FileSystemLoader(path)
else:
    loader = jinja2.PackageLoader('openerp.addons.web_tiff_widget', "views")

env = jinja2.Environment(loader=loader, autoescape=True)
env.filters["json"] = simplejson.dumps

# 1 week cache for asset bundles as advised by Google Page Speed
BUNDLE_MAXAGE = 60 * 60 * 24 * 7

class psController(http.Controller):

    @http.route('/web_tiff_widget/web', type='http', auth='user')
    def a(self,binary,tipo, **k):

        
        cr, uid, context, session = request.cr, request.uid, request.context, request.session
        print str(k) + "---------------------------------------------------------------------------------------------------------------------\
        ---------------------------------------------------------------------------------------------------------------"
        if not session.uid:
            return login_redirect()

        #modelo_registro = request.registry['rbs.documento.mercantil.'+k['tipo']]
        #registro_ids = registro.search(cr, uid, [('id','=',)], context=context)
        #registro = modelo_registro.browse(cr,uid,[1,],context = context)
        #data = registro.filedata
        #tiffstack = Image.open(BytesIO(base64.b64decode(data)))
        #tiffstack.load()
        

        #tiffstack.show()
        '''buffer = cStringIO.StringIO()
        
        tiffstack.seek(0)
        for l in range(tiffstack.n_frames):
            
            #tiffstack.show()
        
            tiffstack.save(buffer, format="JPEG")
            img_str = base64.b64encode(buffer.getvalue())
            init +="document.getElementById('img').setAttribute( 'src', 'data:image/png;base64,"+img_str+"' );\n"
        '''
        
        
        #PosSession = request.registry['pos.session']
        #pos_session_ids = PosSession.search(cr, uid, [('state','=','opened'),('user_id','=',session.uid)], context=context)
        #if not pos_session_ids:
        #    return werkzeug.utils.redirect('/web#action=web_tiff_widget.action_pos_session_opening')
        #PosSession.login(cr,uid,pos_session_ids,context=context)
        
        modules =  simplejson.dumps(module_boot(request.db))
        print modules
        init ="var tiff = TifWIdget('"+tipo+"',"+binary+");"
        
        html = request.registry.get('ir.ui.view').render(cr, session.uid,'web_tiff_widget.TiffEditWidget',{
            'init': init,
            'modules': modules,
        })

        return html

    @http.route('/web_tiff_widget/web_separator', type='http', auth='user')
    def a_s(self, **k):
        cr, uid, context, session = request.cr, request.uid, request.context, request.session
        print str(k) + "---------------------------------------------------------------------------------------------------------------------\
        ---------------------------------------------------------------------------------------------------------------"
        if not session.uid:
            return login_redirect()

        
        modules =  simplejson.dumps(module_boot(request.db))
        print modules
        #init ="var tiff = TifWIdget('"+tipo+"',"+binary+");"
        
        html = request.registry.get('ir.ui.view').render(cr, session.uid,'web_tiff_widget.TiffSeparator',{
         #   'init': init,
            'modules': modules,
        })

        return html

class BinaryTiff(Binary):

    @http.route('/web_tiff_widget/BinaryTiff/tiff', type='http', auth="public")
    def tiff(self, model, id, field, **kw):
        last_update = '__last_update'
        Model = request.registry[model]
        cr, uid, context = request.cr, request.uid, request.context
        headers = [('Content-Type', 'image/tiff')]
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
                    image_base64 = openerp.tools.image_resize_image(base64_source=image_base64, size=(width, height), encoding='base64', filetype='TIFF')

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

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: