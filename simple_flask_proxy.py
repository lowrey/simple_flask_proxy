# -*- coding: utf-8 -*-
from flask import Flask, request, make_response  # jsonify, render_template,
import requests
from urlparse import urlparse

app = Flask(__name__)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    #dest = url.geturl().replace(url.hostname, 'secure.authorize.net')
    FORWARD_HEADER = 'Forwarding-Address'
    # prepare header for foward request
    hdr = header_to_dict(request.headers)
    hdr['X-Forwarded-For'] = request.remote_addr
    fwd_addr = None
    if FORWARD_HEADER in hdr:
        fwd_addr = hdr[FORWARD_HEADER]
        hdr.pop(FORWARD_HEADER, None)
    if not fwd_addr:
        fwd_addr = 'lowrey.me'
        # return "Fowarding Address not set", 400
    # change destination url
    url = urlparse(request.url)
    dest = url.geturl().replace(url.netloc, fwd_addr)
    #print 'Dest: {}, {}, {}'.format(dest, request.method, str(hdr))
    r = requests.request(request.method, dest,
                         data=request.data,
                         headers=hdr)
    # prepare response headers
    resp = make_response(r.content, r.status_code)
    resp.mimetype = r.headers['content-type']
    return resp


def header_to_dict(headers):
    ret = {}
    IGNORE = ['Content-Length', 'Host']
    for k, v in headers:
        if not k in IGNORE:
            ret[k] = v
    return ret


def print_request(req):
    print "REQUEST"
    print "======="
    print "url = " + str(req.url)
    print "json = " + str(req.json)
    print "args = " + str(req.args)
    print "data = " + str(req.data)
    print "values = " + str(req.values)
    print "headers = " + str(req.headers)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
