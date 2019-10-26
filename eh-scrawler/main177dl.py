#!/usr/bin/python
# coding: utf-8

# from main import download_img
from utils import download_numbered_img
import pic177


def download_from_imgurlfile(imgurlfile, dst):
    # type: (str, str) -> None
    with open(imgurlfile) as fr:
        lines = fr.readlines()
    for idx, url in enumerate(lines):
        url = url.strip('\n').strip(' ')
        download_numbered_img(url, dst, idx)


if __name__ == "__main__":
    import sys
    img_url_file, target_dir = all_img_url_for_manga(sys.argv[1], sys.argv[2], int(sys.argv[3]))

