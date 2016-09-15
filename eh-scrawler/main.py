import re
from httplib2 import Http

h = Http()
hc = Http('.cache')


def _html_from_url(url, cookie):
    print "visit url", url
    for _ in xrange(10):
        print "_try ", _
        try:
            headers = {'Set-Cookie': cookie}
            resp, ctnt = h.request(url, headers=headers)
            if '200' == resp.get('status'):
                return ctnt, resp['set-cookie']
        except:
            continue


def _next_urls_from_html(html):
    print "find urls"
    # print html
    pat = '<a [^>]+><img src="[^"]+\.[a-z][a-z][a-z]" style="[^"]+"[^/]+ ?/></a>'
    try:
        spliteds = re.findall(
            pat,
            html)[0].split('"')
    except IndexError as e:
        print html
        raise e
    next_page = spliteds[1]
    img_url = spliteds[3]
    return next_page, img_url


def _download_img(url, dst, idx):
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

    # print ctnt
    if ctnt is None:
        print "Failed img:", url
        return
    extname = url[url.rfind('.'):]
    filename = str(idx) + extname
    if not dst.endswith('/'):
        dst += "/"
    with open(dst + filename, 'wb') as f:
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


def run_args(url, dst):
    ck = cfg['snh'][2]
    for _ in xrange(500):
        page, cookie = _html_from_url(url, ck)
        next_page, img_url = _next_urls_from_html(page)
        _download_img(img_url, dst, url[url.rfind('-')+1:])
        if next_page == url:
            print "FINISHED!"
            break
        url = next_page


def run(name):
    url, dst, ck = cfg[name]
    for _ in xrange(500):
        page, cookie = _html_from_url(url, ck)
        next_page, img_url = _next_urls_from_html(page)
        _download_img(img_url, dst, url[url.rfind('-')+1:])
        if next_page == url:
            print "FINISHED!"
            break
        url = next_page


import sys

if len(sys.argv) == 2:
    run(sys.argv[1])
else:
    run_args(sys.argv[1], sys.argv[2])
