import sys, os, json
from genshi.template import MarkupTemplate
DOCROOT = os.path.dirname(__file__)
sys.path[:0] = [os.path.join(DOCROOT, "../data")]
import pymongo as pm
con = pm.Connection()
mong = con.mong
import api
from pprint import PrettyPrinter
pprint = PrettyPrinter(indent=3, width=100)

seqTypes = (type([]), type(()))
stringTypes = (type(''), type(u''))

def application(environ, start_response):
    template = "/template/timeline.html"
    f = open(DOCROOT + template)
    tmpl = MarkupTemplate(f)
    f.close()
    stream = tmpl.generate()
    output = stream.render('xhtml')

    status = '200 OK'
    response_headers = [('Content-type', 'text/html'),
                        ('Content-Length', str(len(output)))]
    start_response(status, response_headers)
    return [output]
