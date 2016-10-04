import csv
import os

from imgutils import *

BASE_DIR = '/Users/xinzhao/Desktop/gems/'


def prepare():
    r = []
    with open(BASE_DIR + 'local.csv') as fr:
        cr = csv.reader(fr)
        keys = ['id', 'size', 'url', 'local']
        for l in cr:
            r.append(dict(zip(keys, l)))
    return r


def process(imgs):
    for img in imgs:
        url = img['url']
        if url == None or not url:
            continue

        tofile = BASE_DIR + str(img['id'])
        local_exist = False
        try:
            open(tofile)
            local_exist = True
        except IOError:
            local_exist = False
        if local_exist:
            img['local'] = tofile
            if 'None' == img['size']:
                img['size'] = os.path.getsize(tofile)
            continue

        try:
            size = int(img['size'])
        except:
            size = -1
        if size < 0:
            _size = img_size_from_url(img['url'])
            if _size:
                img['size'] = _size
                size = _size
        if size <= 500000:
            continue

        downloaded = download_img_from_url(url, tofile)
        img['local'] = downloaded

    return imgs





