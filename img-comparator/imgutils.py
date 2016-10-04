import re
import subprocess as sub
from contextlib import closing
from PIL import Image

import requests
from httplib2 import Http


hc = Http('.cache')


def img_size_from_url(url):
    print "img size from url:", url
    for _ in xrange(3):
        try:
            with closing(requests.get(url, stream=True)) as r:
                size = r.headers.get('content-length')
                if not size:
                    size = r.headers.get('Content-Length')
                if not size:
                    return None
                else:
                    return int(size)
        except:
            return None


def shunk_gif(infile, outfile, **kwargs):
    print "shunk_gif:", infile
    DEFAULTS = {
        'colors': '64',
        'scale': '0.4',
    }
    args = {k: v for k, v in DEFAULTS.iteritems()}
    for k in DEFAULTS:
        if k in kwargs:
            args[k] = kwargs[k]
    p = sub.Popen(['gifsicle', ] + \
                  sum([["--" + k, v] for k, v in args.iteritems()], []) +\
                  [infile, '-o', outfile],
                  stdout=sub.PIPE, stderr=sub.PIPE)
    output, errors = p.communicate()
    if errors:
        print errors


def shunk_img(im, infile, out, bound, **kwargs):
    print "shunk_img:", infile
    if im.format.lower() == "gif":
        shunk_gif(infile, out)
    else:
        factor = min(float(bound[0]) / im.size[0],
                     float(bound[1]) / im.size[1])
        resized = im.resize((int(im.size[0] * factor),
                             int(im.size[1] * factor)))
        resized.save(out, quality=85)
        return True


def download_img_from_url(url, tofile):
    print "download ", url
    ctnt = None
    for _ in xrange(5):
        print "_try ", _
        try:
            resp, ctnt = hc.request(url)
            if '200' == resp.get('status'):
                break
        except Exception as e:
            print "Download failed: ", e
            continue

    if ctnt is None:
        print "Failed img:", url
        return None
    with open(tofile, 'wb') as f:
        f.write(ctnt)
        return tofile
