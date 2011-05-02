#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       expander.py
#       
#       Copyright 2011 Reid McKenzie <rmckenzie92@gmail.com>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

import re


def is_s_expression(foo):
    return ('(' in foo) and (')' in foo)
    
def check(a):
    print "CHECKING\t",a
    
    if re.search('\)\ [\&, \*, \+]\ \)$', a):
        print "TYPE 1 ERROR"
    
    b = re.search('\)\ [\&, \*, \+]\ *$', a)
    if b:
        print "TYPE 2 ERROR"
        a = a[0:len(a)-3]
        
    return a

def f(s):
    out = ""
    foo = 0
    
    s = s[1:(len(s)-1)]
    oper = s[0]
    s = s[1::]
    
    print oper
    scope = 0
    
    for c in range(1,len(s)):
        foo = c
        
        print c, "\t", s[c::], '\t', scope
        
        if s[c] == "(":
            scope += 1
        
        if s[c] == ")":
            scope -= 1
        
        if scope == 0:
            if s[c] == " ":
                continue
            
            elif s[c] == ')':
                out += (s[c] + ' ' + oper + ' ')
                continue
            
            else:
                out += (s[c] + oper)
                continue
        
        else:
            out += s[c]
            continue
    
    out = check(out)
    
    return out, s[foo::]

if __name__ == '__main__':
    a = "(& (* a (+ b c )) (* a (+ b c )))"
    a, b = f(a)
    a, b = f(a)
    a, b = f(a)
    
    
