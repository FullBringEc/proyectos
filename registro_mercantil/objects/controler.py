from openerp import http
from openerp.http import request
from openerp.addons.web.controllers.main import serialize_exception,content_disposition
import base64

class Binary(http.Controller):
 @http.route('/web/binary/download_document', type='http', auth="public")
 @serialize_exception
 def download_document(self,model,field,id,filename=None, **kw):
     Model = request.registry[model]
     cr, uid, context = request.cr, request.uid, request.context
     fields = [field]
     res = Model.read(cr, uid, [int(id)], fields, context)[0]
     #print res
     filecontent = base64.b64decode(res.get(field) or '')
     if not filecontent:
         return request.not_found()
         print "holaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
     else:
        print "Chaoooooooooooooooooooooooooooooooooooooooooooooooooo"
        if not filename:
             filename = '%s_%s' % (model.replace('.', '_'), id)
             return request.make_response(filecontent,
                            [('Content-Type', 'application/msword'),
                             ('Content-Disposition', content_disposition(filename))])
        else:
            return request.make_response(filecontent,
                            [('Content-Type', 'application/msword'),
                             ('Content-Disposition', content_disposition(filename))])



