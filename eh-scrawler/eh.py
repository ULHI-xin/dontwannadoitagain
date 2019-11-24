#!/usr/bin/python
# coding: utf-8

import re
import httplib2
import subprocess as sub
from httplib2 import Http

from utils import download_numbered_img
from platform.eh import parse_index_page_info

proxy_info = httplib2.ProxyInfo(httplib2.socks.PROXY_TYPE_SOCKS5, '127.0.0.1', 1082)
h = Http(proxy_info=proxy_info)
hc = Http('.cache')


def _html_from_url(url, cookie):
    print "visit url", url
    for _ in xrange(5):
        print "_try ", _
        try:
            headers = {'Cookie': cookie}
            resp, ctnt = h.request(url, headers=headers)
            if '200' == resp.get('status'):
                return ctnt, resp.get('set-cookie', cookie)
            ## print resp, ctnt
        except Exception as e:
            print '%r' % e
            continue


def _next_urls_from_html(html):
    html = html.replace(' id="img"', '')
    html = re.sub(' onclick="[^"]+"', '', html)
    print "find urls"
    # print html
    # pat = '<a [^>]+><img src="[^"]+\.[a-z][a-z][a-z]" style="[^"]+"[^/]+ ?/></a>'
    pat = '<a [^>]+><img id="img" [^>]+></a>'
    try:
        tag = re.findall(
            pat,
            html)[0]
        # print tag
        next_page = re.findall('href="[^"]+"', tag)[0][6:-1]
        img_url = re.findall('src="[^"]+"', tag)[0][5:-1]

    except IndexError as e:
        pat = '<a [^>]+><img src="[^"]+\.[a-z][a-z][a-z]" style="[^"]+"[^/]+ ?/></a>'
        try:
            tag = re.findall(
                pat,
                html)[0]
            # print tag
            next_page = re.findall('href="[^"]+"', tag)[0][6:-1]
            img_url = re.findall('src="[^"]+"', tag)[0][5:-1]
        except IndexError as e:
            print html
            raise e
    # next_page = spliteds[1]
    # img_url = spliteds[3]
    print "next page:", next_page
    return next_page, img_url


def _download_misc(url, dst, cookie):
    print "download ", url
    ctnt = None
    for _ in xrange(3):
        print "_try ", _
        try:
            headers = {'Cookie': cookie}
            resp, ctnt = hc.request(url, headers=headers)
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
    dst = "/Users/xinzhao/.hehe/" + dst if '/' not in dst else dst
    if not dst.endswith('/'):
        dst += "/"
    try:
        with open(dst, 'wb') as f:
            f.write(ctnt)
    except IOError:
        p = sub.Popen(['mkdir', '-p', dst], stdout=sub.PIPE,
                      stderr=sub.PIPE)
        output, errors = p.communicate()
        with open(dst, 'wb') as f:
            f.write(ctnt)


cfg = {
    'snh':
        ['http://g.e-hentai.org/s/a8b8843de1/2049-52',
         '/Users/xinzhao/HEHE/snh',
         'uconfig=uh_y-lt_m-rc_0-tl_r-cats_0-xns_0-ts_m-tr_2-prn_y-dm_l-ar_0-rx_0-ry_0-ms_n-mt_n-cs_a-fs_p-to_a-pn_0-sc_0-ru_rrggb-xr_a-sa_y-oi_n-qb_n-tf_n-hh_-hp_-hk_-xl_; expires=Sun, 13-Aug-2017 09:42:35 GMT; Max-Age=31536000; path=/; domain=.e-hentai.org'],
    'hnk':
        ['http://g.e-hentai.org/s/0791c1dd8e/418959-3',
         '/Users/xinzhao/HEHE/haitoku_no_kanata',
         'uconfig=uh_y-lt_m-rc_0-tl_r-cats_0-xns_0-ts_m-tr_2-prn_y-dm_l-ar_0-rx_0-ry_0-ms_n-mt_n-cs_a-fs_p-to_a-pn_0-sc_0-ru_rrggb-xr_a-sa_y-oi_n-qb_n-tf_n-hh_-hp_-hk_-xl_; expires=Sun, 13-Aug-2017 09:42:35 GMT; Max-Age=31536000; path=/; domain=.e-hentai.org'],
    'pm':
        ['http://g.e-hentai.org/s/0b1f472a29/642078-161',
         '/Users/xinzhao/HEHE/physical_message',
         'uconfig=uh_y-lt_m-rc_0-tl_r-cats_0-xns_0-ts_m-tr_2-prn_y-dm_l-ar_0'
         '-rx_0-ry_0-ms_n-mt_n-cs_a-fs_p-to_a-pn_0-sc_0-ru_rrggb-xr_a-sa_y-oi_n-qb_n-tf_n-hh_-hp_-hk_-xl_; expires=Sun, 13-Aug-2017 09:53:16 GMT; Max-Age=31536000; path=/; domain=.e-hentai.org'],
    'sc1':
        [
            'http://g.e-hentai.org/s/c423e61f7f/852436-1',
            '/Users/xinzhao/HEHE/sc1',
            'uconfig=uh_y-lt_m-rc_0-tl_r-cats_0-xns_0-ts_m-tr_2-prn_y-dm_l-ar_0-rx_0-ry_0-ms_n-mt_n-cs_a-fs_p-to_a-pn_0-sc_0-ru_rrggb-xr_a-sa_y-oi_n-qb_n-tf_n-hh_-hp_-hk_-xl_; expires=Sun, 13-Aug-2017 09:42:35 GMT; Max-Age=31536000; path=/; domain=.e-hentai.org',
        ],
}


def run_args(url, dst, stop=1500):
    ck = "__cfduid=d0d4f1422f7ed0333fb6106bf992f3e441488450044"
    ck = " skipserver=29192-17643_23626-17643; __cfduid=d8c49442195dc4df6d0a47179b2fb273f1523767719"
    ck = "__cfduid=d8c49442195dc4df6d0a47179b2fb273f1523767719"
    for _ in xrange(stop):
        page, cookie = _html_from_url(url, ck)
        next_page, img_url = _next_urls_from_html(page)
        download_numbered_img(img_url, dst, url[url.rfind('-') + 1:])
        if next_page == url:
            print "FINISHED!"
            break
        url = next_page


def run(name, stop_arg=1500):
    url, dst, ck = cfg[name]
    for _ in xrange(stop_arg):
        page, cookie = _html_from_url(url, ck)
        next_page, img_url = _next_urls_from_html(page)
        download_numbered_img(img_url, dst, url[url.rfind('-') + 1:])
        if next_page == url:
            print "FINISHED!"
            break
        url = next_page


def run_img_url_only(dst, start_url):
    p = sub.Popen(['mkdir', '-p', dst.replace('.', '_')], stdout=sub.PIPE,
                  stderr=sub.PIPE)
    ck = "tips=1; __utma=185428086.1372950640.1477723685.1478415126.1480141868.5; __utmc=185428086; __utmz=185428086.1477723685.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); eap_45442=1"
    ck = "skipserver=18683-17302_14188-17301_17879-17301; __cfduid=d0acb48934e768c96bb08275951098e0c1494255264; nw=1; eap_45442=1"
    with open(dst, 'a') as fa:
        for _ in xrange(1500):
            page, cookie = _html_from_url(start_url, ck)
            next_page, img_url = _next_urls_from_html(page)
            fa.write('%s\n' % img_url)
            if next_page == start_url:
                print "FINISHED!"
                break
            start_url = next_page


if __name__ == "__main__":
    import sys

    if len(sys.argv) == 2:
        ck = "nw=1; __cfduid=d8c49442195dc4df6d0a47179b2fb273f1523767719"
        page, cookie = _html_from_url(sys.argv[1], ck)
        start_url, title = parse_index_page_info(page)
        run_args(start_url, title)

    elif len(sys.argv) == 3 and sys.argv[2].startswith('start='):
        ck = "__cfduid=d8c49442195dc4df6d0a47179b2fb273f1523767719"
        start_url = sys.argv[2][6:]
        page, cookie = _html_from_url(sys.argv[1], ck)
        _, title = parse_index_page_info(page)
        run_args(start_url, title)

    elif len(sys.argv) == 4 and sys.argv[1] == 'no-dl':
        run_img_url_only(sys.argv[3], sys.argv[2])
    elif len(sys.argv) == 2:
        run(sys.argv[1])
    elif len(sys.argv) == 4 and sys.argv[3].startswith('stop='):
        stop_arg = sys.argv[3]
        stop_arg = int(stop_arg[5:])
        print('stop=', stop_arg)
        run_args(sys.argv[1], sys.argv[2], stop_arg)
    else:
        run_args(sys.argv[1], sys.argv[2])

