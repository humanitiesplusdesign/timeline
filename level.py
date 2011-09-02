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
from util import foo

class utils(object):
    @staticmethod
    def lon2x(lon):
        return lon * -0.125
    @staticmethod
    def lat2z(lat):
        return lat * 0.125
    @staticmethod
    def ms2y(ms):
        return 0

def application(environ, start_response):
    colors = [
        "#ff0000",
        "#00ff00",
        "#0000ff",
        ]
    events = []
    output = api.mongoApi(environ)
    evs = json.loads(output)['result']
    if not evs:
        events = [
            foo(lat=40.715, lon=-74, ms=0, color=0),
            foo(lat=0, lon=0, ms=0, color=0),
            foo(lat=0, lon=44, ms=0, color=1),
            foo(lat=50, lon=0, ms=0, color=2),
        ]
    print >> sys.stderr, "DEBUG evs:", evs
    for ev in evs:
        lat = None
        ms = None
        if ev['Type'] == "Arrival":
            if "MPlace" in ev and ev['MPlace']:
                place = mong.MPlace.find_one({"_id":ev['MPlace']})
                if place and "Coords" in place:
                    lat, lon = place['Coords'].split(",")
                    lat = float(lat)
                    lon = float(lon)
            if "Date" in ev and ev['Date']:
                ms = ev['Date']['ms']

        if lat and ms:
            nu = foo()
            nu.lat = lat
            nu.lon = lon
            nu.ms = ms
            nu.color = 0
            events.append(nu)
            print >> sys.stderr, "EVENT:", events[-1]

    template = "/template/level.xml"
    f = open(DOCROOT + template)
    tmpl = MarkupTemplate(f)
    f.close()
    stream = tmpl.generate(colors=colors, events=events, utils=utils)
    output = stream.render('xhtml')

    status = '200 OK'
    response_headers = [('Content-type', 'text/html'),
                        ('Content-Length', str(len(output)))]
    start_response(status, response_headers)
    return [output]
