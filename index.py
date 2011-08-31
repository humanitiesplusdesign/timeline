import sys, os, json
from genshi.template import MarkupTemplate
DOCROOT = os.path.dirname(__file__)

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
