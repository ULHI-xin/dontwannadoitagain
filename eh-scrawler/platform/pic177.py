# coding: utf-8

import re
import httplib2
import subprocess as sub
from datetime import datetime
from httplib2 import Http

from utils import (html_from_url, download_numbered_img)

BASEDIR = '/Users/xinzhao/.hehe'


def parse_index_page_info(html_str):
    found = re.findall('<h1[^>]*>([^<]+)</h1>', html_str)
    title = found[0]
    print(title)
    found = re.findall(r'<span>(\d+)</span>', html_str)
    length = found[-1]
    print(length)
    return title, length


def img_url_from_html(html_str):
    # print(html_str)
    found = re.findall(r'<img src="http://img.177piczz.info/uploads/[^"]+"', html_str)
    if found:
        return [x[x.find('"') + 1:-1] for x in found]
    found = re.findall(r'<img src="http://img.177pic.info/uploads/[^"]+"', html_str)
    if found:
        return [x[x.find('"') + 1:-1] for x in found]
    found = re.findall(r' data-lazy-src="http://img.177pic.pw/uploads/[^"]+"', html_str)
    if found:
        return [x[x.find('"') + 1:-1] for x in found]
    # print(found)
    return found


def all_img_url_for_manga(manga_url):
    name, end = parse_index_page_info(html_from_url(manga_url, None)[0])
    end = int(end)

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
    target_dir = BASEDIR + '/' + name
    p = sub.Popen(['mkdir', '-p', target_dir], stdout=sub.PIPE,
                  stderr=sub.PIPE)
    output, errors = p.communicate()
    print('Target dir created: `{}`'.format(target_dir))
    return img_url_file, target_dir


def download_from_imgurlfile(imgurlfile, dst):
    # type: (str, str) -> None
    with open(imgurlfile) as fr:
        lines = fr.readlines()
    for idx, url in enumerate(lines):
        url = url.strip('\n').strip(' ')
        download_numbered_img(url, dst, idx)
