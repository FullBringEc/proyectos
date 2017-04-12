#
# jQuery File Tree
# Python/Django connector script
# By Martin Skou
#
import os
import urllib

def dirlist(request):
   r=['<ul class="jqueryFileTree" style="display: none;">']
   try:
       r=['<ul class="jqueryFileTree" style="display: none;">']
       d=urllib.unquote(request.POST.get('dir','c:\\temp'))
       for f in os.listdir(d):
            
            ff=os.path.join(d,f)

            print ff+"    -  "+f+"\n\n\n"
            if os.path.isdir(ff):
               r.append('<li class="directory collapsed"><a href="#" rel="%s/">%s</a></li>' % (ff,f))
            else:
               e=os.path.splitext(f)[1][1:] # get .ext and remove dot
               r.append('<li class="file ext_%s"><a href="#" rel="%s">%s</a></li>' % (e,ff,f))
       r.append('</ul>')
   except Exception,e:
       r.append('Could not load directory: %s' % str(e))
   r.append('</ul>')
   print r
   return HttpResponse(''.join(r))

from ftplib import FTP
ftp = FTP('ftp.debian.org')
ftp.login()
for name in ftp.nlst():
    print "listing: " + name
    ftp.cwd(name)
    ftp.retrlines('LIST')
    ftp.cwd('../')
