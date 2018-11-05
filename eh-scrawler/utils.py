#!/usr/bin/python

import re
import httplib2
import subprocess as sub
from httplib2 import Http

proxy_info = httplib2.ProxyInfo(httplib2.socks.PROXY_TYPE_SOCKS5, '127.0.0.1', 1086)
h = Http(proxy_info=proxy_info)
hc = Http('.cache')


def html_from_url(url, cookie):
    print("visit url", url)
    for _ in xrange(5):
        print("_try ", _)
        try:
            if cookie is not None:
                headers = {'Cookie': cookie}
                resp, ctnt = h.request(url, headers=headers)
            else:
                resp, ctnt = h.request(url)
            if '200' == resp.get('status'):
                return ctnt, resp.get('set-cookie', cookie)
        except Exception as e:
            print '%r' % e
            continue
    return None, None


def download_img(url, dst, idx):
    print("download ", url)
    ctnt = None
    for _ in xrange(3):
        print "_try ", _
        try:
            resp, ctnt = hc.request(url)
            if '200' == resp.get('status'):
                break
        except Exception as e:
            print "Download failed: ", e
            continue

    # print ctnt
    if ctnt is None:
        print "Failed img:", url
        return
    extname = url[url.rfind('.'):]
    filename = str(idx) + extname
    dst = "/Users/xinzhao/.hehe/" + dst if '/' not in dst else dst
    if not dst.endswith('/'):
        dst += "/"
    try:
        with open(dst + filename, 'wb') as f:
            f.write(ctnt)
    except IOError:
        p = sub.Popen(['mkdir', '-p', dst], stdout=sub.PIPE,
                      stderr=sub.PIPE)
        output, errors = p.communicate()
        with open(dst + filename, 'wb') as f:
            f.write(ctnt)

