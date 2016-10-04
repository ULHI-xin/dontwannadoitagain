import random

from base import (html_from_url, mkdir_with_autocreate,
                  download_img, cp)
from bs4 import BeautifulSoup

def get_img_urls(url):
    html, next_cookie = \
        html_from_url(url,
                      "__cfduid=dd108d037222bfc1db916c925c5688ba21475306839; "
                      "PHPSESSID=ffj8s94pqst14b7acu9gh09es6; "
                      "bdshare_firstime=1475306840899; CNZZDATA1259688398=1254372273-1475301461-null%7C1475306863")
    # print html
    bs = BeautifulSoup(html, "html.parser")
    imgs = bs.findAll('img')
    # print imgs
    # for img in imgs:
    #     print img['src']
    return [img['src'] for img in imgs
            if img['src'] and img['src'].startswith("http")]


def extract_all_img_urls(index_urls):
    all_img_urls = []
    for i_u in index_urls:
        imgs = []
        for r in range(5):
            try:
                imgs = get_img_urls(i_u)
                break
            except:
                pass
        if not imgs:
            print "NO img extracted from ", i_u
        all_img_urls += imgs
    return all_img_urls


def all_urls(start_url, index):
    return [start_url] +\
        [start_url + ("index%s.html" % i) for i in range(2, index + 1)]

import sys

cmd = sys.argv[1]

print cmd

if cmd == "pages":
    u = sys.argv[4]
    vol = sys.argv[2]
    index_count = int(sys.argv[3])

    output = "/Users/xinzhao/HEHE/xynlqy/"
    index_urls = all_urls(u, index_count)
    # print index_urls
    all_img_urls = extract_all_img_urls(index_urls)
    # print all_img_urls
    mkdir_with_autocreate(output + vol)
    with open(output + vol + "/urls", 'w') as fw:
        for aiu in all_img_urls:
            fw.write("%s\n" % aiu)
    for idx, aiu in enumerate(all_img_urls):
        filename = "%s/%s_%s.%s" % (output + vol,
                                    vol, idx, aiu[aiu.rfind('.')+1:])
        aiu = aiu.replace('s51', 's' + str(31 + 2 * random.randint(0, 4)))
        print "%s/%s" % (idx, len(all_img_urls))
        download_img(aiu, filename)
elif "files" == cmd:
    f = sys.argv[4]
    vol = sys.argv[2]
    start = int(sys.argv[3])
    output = "/Users/xinzhao/HEHE/xynlqy/"
    with open(f, 'r') as fr:
        all_img_urls = []
        for l in fr.readlines():
            all_img_urls.append(l)
        all_img_urls = [a[:-1] for a in all_img_urls]
    for idx, aiu in enumerate(all_img_urls):
        if idx < start:
            continue
        filename = "%s/%s_%s.%s" % (output + vol,
                                    vol, idx, aiu[aiu.rfind('.')+1:])
        aiu = aiu.replace('s51', 's' + str(31 + 2 * random.randint(0, 4)))
        print "%s/%s" % (idx, len(all_img_urls))
        download_img(aiu, filename)
elif "rename" == cmd:
    f = sys.argv[3]
    vol = sys.argv[2]
    with open(f + "/urls", 'r') as fr:
        all_img_urls = []
        for l in fr.readlines():
            all_img_urls.append(l)
        all_img_urls = [a[:-1] for a in all_img_urls]
    for idx, aiu in enumerate(all_img_urls):
        old_name = aiu[aiu.rfind('/')+1:]
        new_name = vol + "_" + str(idx) + ".jpg"
        print "rename", old_name, "->", new_name
        cp(f + "/" + old_name, f + "/" + new_name)
