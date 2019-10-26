#!/usr/bin/python

from platform.pic177 import all_img_url_for_manga, download_from_imgurlfile
from utils import (html_from_url, )


# all_img_url_for_manga('http://www.177piczz.info/html/2018/06/2149124.html', 39)


if __name__ == "__main__":
    import sys

    img_url_file, target_dir = all_img_url_for_manga(sys.argv[1])
    download_from_imgurlfile(img_url_file, target_dir)
