#!/usr/bin/python

from platform.pic177 import all_img_url_for_manga


# all_img_url_for_manga('http://www.177piczz.info/html/2018/06/2149124.html', 39)


if __name__ == "__main__":
    import sys
    all_img_url_for_manga(sys.argv[1], sys.argv[2], int(sys.argv[3]))
