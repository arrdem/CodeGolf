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

import sexpr

prio = {'*' : 3,
        '+' : 2,
        '&' : 1}

def is_iterable(param): 
    try: 
        return type(param) == type([])
    except TypeError: 
        return False

def get_prio(itterable):
    p = []
    
    
    for foo in itterable:
        if is_iterable(foo):
            p.append(get_prio(foo))
        else:
            p.append(prio[itterable[0]])
    
    return p

def expand(foo):
    pass

if __name__ == '__main__':
    a = ["(* a (+ b c))",
         "(* (+ a b) ((+ c d)))",
         "(* (& (* (& a b) (& (+ c d) e))) (* f (+ g h i)))",
         "(+ (& a b) c)"]
    
    for foo in a:
        print foo, "\n\t", sexpr.str2sexpr(foo), "\n\t", get_prio(sexpr.str2sexpr(foo))
    
