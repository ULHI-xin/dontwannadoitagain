import re
import subprocess as sub
from contextlib import closing
from PIL import Image
import os

import requests
from httplib2 import Http


hc = Http('.cache')


def img_size_from_url(url):
    print("img size from url:", url)
    for _ in range(3):
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


def shunk_gif(infile, outfile, target_size, **kwargs):
    print "shunk_gif:", infile
    if kwargs:
        print "  shrunk with args", kwargs
        args = {k: v for k, v in kwargs.iteritems()}
        p = sub.Popen(['gifsicle', ] + \
                  sum([["--" + k, v] for k, v in args.iteritems()], []) +\
                  [infile, '-o', outfile],
                  stdout=sub.PIPE, stderr=sub.PIPE)
        output, errors = p.communicate()
        if errors:
            print errors
    else:
        print "  auto shrunk"
        target_size = 2000000 if target_size is None else target_size
        ARGS = [
            {'colors': '256', },
            {'colors': '256', 'scale': '0.75'},
            {'colors': '256', 'scale': '0.6'},
            {'colors': '256', 'scale': '0.4'},
            {'colors': '128', },
            {'colors': '128', 'scale': '0.75'},
            {'colors': '128', 'scale': '0.6'},
            {'colors': '128', 'scale': '0.4'},
            {'colors': '64', },
            {'colors': '64', 'scale': '0.75'},
            {'colors': '64', 'scale': '0.6'},
            {'colors': '64', 'scale': '0.4'},
            {'colors': '32', 'scale': '0.3'},
        ]
        for args in ARGS:
            p = sub.Popen(['gifsicle', ] + \
                          sum([["--" + k, v] for k, v in args.iteritems()], []) +\
                          [infile, '-o', outfile],
                          stdout=sub.PIPE, stderr=sub.PIPE)
            output, errors = p.communicate()
            if errors:
                print errors
            _size = os.path.getsize(outfile)
            if _size <= target_size:
                print "succeed in", args, 'size:', _size
                break


def shunk_img(im, infile, out, bound, **kwargs):
    print "shunk_img:", infile
    if im.format.lower() == "gif":
        shunk_gif(infile, out, target_size=None, **kwargs)
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
