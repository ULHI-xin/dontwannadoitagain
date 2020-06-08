#!/usr/bin/python
# coding: utf-8

import os
import sys
import subprocess
from datetime import datetime

from utils import cd


root = sys.argv[1]
for r, d, f in os.walk(root):
    for _d in d:
        if not _d or _d == 'bak':
            continue
        zipname = _d.decode("utf-8")
        zipname = zipname.replace(" ", "_").replace("/", "-")
        # if not _d.startswith(datelabel):
        #     zipname = datelabel + "_" + zipname
        zipname = zipname + ".zip"

        with cd(root):
            args = ["zip", "-r", zipname, _d]
            print(args)
            subprocess.call(args)
