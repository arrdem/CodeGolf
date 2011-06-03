#!/usr/bin/env python
from __future__ import division
import sys
s = sys.argv

c=150
f=15

if int(s[1]) < f:
    print "H"
else:
    if int(s[4]) == 10:
        print "B", int((int(s[1])/21)*c)
    else:
        print "S"

