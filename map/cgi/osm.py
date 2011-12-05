#!/usr/bin/env python

import cgitb;
cgitb.enable()

# Some hosts will need to have document_root appended
# to sys.path to be able to find user modules
import sys, os
sys.path.append(os.environ['DOCUMENT_ROOT'])

from cgi import FieldStorage
from session import Session
from osmoauth import OSMOAuth

sess = Session(expires=365*24*60*60, cookie_path='/')
api = OSMOAuth(sess)

args = FieldStorage()

if args.has_key('login'):
    # Just inisialyse the session to be shure that we are autorised.
    print
    print "OK"

elif args.has_key('oauth_token'):
    # auth callback.
    print
    print "logged OK"

elif args.has_key('new'):
    # create changeset
    empty_changeset = """<?xml version="1.0" encoding="UTF-8"?>
<osm>
  <changeset>
    <tag k="created_by" v="HTML editor 0.1 (courriel@stephane-brunner.ch)"/>
    <tag k="comment" v="%s"/>
  </changeset>
</osm>"""%args.getvalue('new')
    changeset_id = api.put("/api/0.6/changeset/create", empty_changeset)
    session['changeset_id'] = changeset_id

    print
    if args.has_key('cb'):
        print "function %s() {return '%s'} "%(args.getvalue('cb'), changeset_id)
    else:
        print result

elif args.has_key('close'):
    # close changeset
    result = api.put("/api/0.6/changeset/%s/close"%changeset_id)

    print
    if args.has_key('cb'):
        print "function %s() {return '%s'} "%(args.getvalue('cb'), result)
    else:
        print result

elif args.has_key('action'):
    result = api.put(args.getvalue('action'),  raw_input())

    print
    if args.has_key('cb'):
        print "function %s() {return '%s'} "%(args.getvalue('cb'), result)
    else:
        print result

elif args.has_key('test'):
    # create changeset
    empty_changeset = """<?xml version="1.0" encoding="UTF-8"?>
<osm>
  <changeset>
    <tag k="created_by" v="HTML editor 0.1 (courriel@stephane-brunner.ch)"/>
    <tag k="comment" v="First tests"/>
  </changeset>
</osm>"""
    changeset_id = api.put("/api/0.6/changeset/create", empty_changeset)
    session['changeset_id'] = changeset_id

    n1 = api.put("/api/0.6/node/create", """<?xml version="1.0" encoding="UTF-8"?>
<osm>
      <node lat="46.50588937346545" lon="6.674228713368014" changeset="%(changeset)s" />
</osm>"""%{'changeset': changeset_id})
    n2 = api.put("/api/0.6/node/create", """<?xml version="1.0" encoding="UTF-8"?>
<osm>
      <node lat="46.5058290657965" lon="6.674414951880432" changeset="%(changeset)s" />
</osm>"""%{'changeset': changeset_id})
    n3 = api.put("/api/0.6/node/create", """<?xml version="1.0" encoding="UTF-8"?>
<osm>
      <node lat="46.5059522910652" lon="6.674499182942514" changeset="%(changeset)s" />
</osm>"""%{'changeset': changeset_id})
    n4 = api.put("/api/0.6/node/create", """<?xml version="1.0" encoding="UTF-8"?>
<osm>
      <node lat="46.50601259859745" lon="6.674312944430097" changeset="%(changeset)s" />
</osm>"""%{'changeset': changeset_id})

    print api.put("/api/0.6/way/create", """<?xml version="1.0" encoding="UTF-8"?>
<osm>
      <way changeset="%(changeset)s">
        <nd ref="%(n1)s" />
        <nd ref="%(n2)s" />
        <nd ref="%(n3)s" />
        <nd ref="%(n4)s" />
        <nd ref="%(n1)s" />
        <tag k="test" v="test" />
      </way>
</osm>"""%{'changeset': changeset_id, 'n1': n1, 'n2': n2, 'n3': n3, 'n4': n4})

    # close changeset
    api.put("/api/0.6/changeset/%s/close"%changeset_id)

    print
    print "Writing changes to " + OSMOAuth.API_URL + "/browse/changeset/" + changeset_id

else:
    print
    print "No valid query."

sess.close()
