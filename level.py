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


def latlon2xy(lat, lon):
    y = lat * 0.125
    x = lon * -0.125
    return x, y

def ms2z(ms):
    return (ms/1000000.0 + 6000.0) * .25

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
##        events = [
##            [40.71455000, -74.00712400,0,0],
##            [53.55, 13.27, 0, 1],
##            [31.07, 46.22, 0, 2],
##        ]
        events = [
            [40.715,-74,0,0],
            [0,0,0,0],
            [0,44,0,1],
            [50,0,0,2],
        ]
        for i in range(len(events)):
            x, z = latlon2xy(events[i][0], events[i][1])
            events[i][0] = x
            events[i][2] = z
            events[i][1] = 0
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
            x, z = latlon2xy(lat, lon)
            y = 0#ms2z(ms)
            print >> sys.stderr, "EVENT:", ev['MPlace'], x, y, z
            events.append([x, y, z, 2])

    template = "/template/level.xml"
    f = open(DOCROOT + template)
    tmpl = MarkupTemplate(f)
    f.close()
    stream = tmpl.generate(colors=colors, events=events)
    output = stream.render('xhtml')

    status = '200 OK'
    response_headers = [('Content-type', 'text/html'),
                        ('Content-Length', str(len(output)))]
    start_response(status, response_headers)
    return [output]
