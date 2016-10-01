
from base import html_from_url
from BeautifulSoup import BeautifulSoup

def get_img_urls(url):
    html, next_cookie = \
        html_from_url(url,
                      "__cfduid=dd108d037222bfc1db916c925c5688ba21475306839; "
                      "PHPSESSID=ffj8s94pqst14b7acu9gh09es6; "
                      "bdshare_firstime=1475306840899; CNZZDATA1259688398=1254372273-1475301461-null%7C1475306863")
    print html
    bs = BeautifulSoup(html)
    imgs = bs.findAll('img')
    print imgs
    for img in imgs:
        print img['src']

u = "http://www.qiaokk.com/artkt/zhongwencaimanxiaoyuannuliqiyuesishiyilunxian130P/index3.html"
get_img_urls(u)