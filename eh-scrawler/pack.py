#!/usr/bin/env python
# coding: utf-8

import os
import re
import sys
import subprocess
from datetime import datetime

from utils import cd


root = sys.argv[1]
for r, d, f in os.walk(root):
    for _d in d:
        if not _d or _d == 'bak':
            continue
        zipname = _d.strip()
        zipname = re.sub(r'^\([^)]+\)', '', zipname).strip()
        author_name = re.findall(r'^\[[^]]+]', zipname)
        if author_name:
            zipname = (zipname.replace(author_name[0], '') + author_name[0]).strip()
        zipname = zipname.replace(" ", "_").replace("/", "-").replace("/", "-").replace('?', '')
        # if not _d.startswith(datelabel):
        #     zipname = datelabel + "_" + zipname
        zipname = zipname + ".zip"

        with cd(root):
            args = ["zip", "-r", zipname, _d]
            print(args)
            subprocess.call(args)
