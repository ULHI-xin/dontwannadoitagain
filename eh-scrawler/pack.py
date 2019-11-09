#!/usr/bin/python
# coding: utf-8

import os
import sys
import subprocess
from datetime import datetime


root = sys.argv[1]
for r, d, f in os.walk(root):
    datelabel = datetime.now().strftime('%Y%m%d')
    for _d in d:
        if not _d or _d == 'bak':
            continue
        zipname = _d.decode("utf-8")
        zipname = zipname.replace(" ", "_").replace("/", "-")
        if not _d.startswith(datelabel):
            zipname = datelabel + "_" + zipname
        zipname = zipname + ".zip"

        args = ["zip", "-r", root + "/" + zipname, root + "/" + _d]
        print(args)
        subprocess.call(args)