#!/usr/bin/env python

import os
import subprocess 
import re
import sys

for foo in os.listdir("./lispers/"):
    print foo,
    os.system(str("cp ./lispers/"+foo+" ./warriors/"))
    os.system(str("./score.py ./warriors/ 1 50 | tee ./log_"+foo+".log"))
    os.system(str("rm ./warriors/"+foo))
    if os.path.isfile(str("./log_"+foo+".log")):
        print "\tDone!"
    else:
        print "\n\nFAILURE"
        exit(1)
