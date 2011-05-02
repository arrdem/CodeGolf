#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#   For a given positive integer number N, write a complete program to
#   find the minimal natural M such that the product of digits of M is 
#   equal N. N is less than 1,000,000,000. If no M exists, print -1. 
#   Your code should not take more than 10 secs for any case.

import sys
s=""
for i in range(1,9):
    if(int(sys.argv[1])%i == 0):
        s += str(i);sys.argv[1]/=i
print s
