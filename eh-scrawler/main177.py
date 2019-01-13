#!/usr/bin/python

import re
import httplib2
import subprocess as sub
from datetime import datetime
from httplib2 import Http

from utils import (html_from_url, )

BASEDIR = '/Users/xinzhao/.hehe'


def img_url_from_html(html_str):
    found = re.findall(r'<img src="http://img.177piczz.info/uploads/[^"]+"', html_str)
    if found:
        return [x[x.find('"') + 1:-1] for x in found]
    found = re.findall(r'<img src="http://img.177pic.info/uploads/[^"]+"', html_str)
    if found:
        return [x[x.find('"') + 1:-1] for x in found]
    return found


def all_img_url_for_manga(manga_url, name, end):
    img_url_file = '{}/{}_{}.txt'.format(BASEDIR, name, httplib2.urllib.quote_plus(manga_url))
    with open(img_url_file, 'w') as fw:
        for i in range(1, end + 1):
            idx_url = '{}/{}'.format(manga_url, i)
            html, setcookie = html_from_url(idx_url, cookie=None)
            if not html:
                raise ValueError('Fail to download index html {}'.format(idx_url))
            img_urls = img_url_from_html(html)
            for iu in img_urls:
                fw.write(iu + '\n')
    print('All img url scrawled. cmd: `open "{}"`'.format(img_url_file))
    target_dir = BASEDIR + '/' + datetime.now().strftime('%Y%m%d') + '_' + name
    p = sub.Popen(['mkdir', '-p', target_dir], stdout=sub.PIPE,
                  stderr=sub.PIPE)
    output, errors = p.communicate()
    print('Target dir created: `{}`'.format(target_dir))


# all_img_url_for_manga('http://www.177piczz.info/html/2018/06/2149124.html', 39)


import sys
all_img_url_for_manga(sys.argv[1], sys.argv[2], int(sys.argv[3]))
