import sys, os, json
from genshi.template import MarkupTemplate
DOCROOT = os.path.dirname(__file__)

events = [
    [0,0,0],
    [4,0,0],
    [0,4,0],
    [4,4,4]
    ]

def application(environ, start_response):
    template = "/template/level.xml"
    f = open(DOCROOT + template)
    tmpl = MarkupTemplate(f)
    f.close()
    stream = tmpl.generate(special_color="#ff0000", events=events)
    output = stream.render('xhtml')

    status = '200 OK'
    response_headers = [('Content-type', 'text/html'),
                        ('Content-Length', str(len(output)))]
    start_response(status, response_headers)
    return [output]
