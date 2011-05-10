#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       deck.py
#
#   LICENSE      
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
#
#   ABOUT
#       This file was created for the code-golf BlackJack challenge, and
#       serves to abstract a deck of paper cards into an easily
#       manipulated object, complete with a shuffle and deal function.

import cards
import itertools
import random

class deck:
    def __init__(self, jokers = False):
        self.__deck__ = []
        self.__clean__ = self.__cleandeck__()
        self.shuffle()
    
    def __cleandeck__(self):
        d = []
        for a in cards.SUITS:
            for b in cards.CARDS:
                d.append(cards.card(a, b))
        return d
    
    def shuffle(self):
        self.__deck__ = self.__clean__
        for i in range(3000):
            a=random.randint(0,51)
            b=random.randint(0,51)
            c=None
            
            c = self.__deck__[a]
            self.__deck__[a] = self.__deck__[b] 
            self.__deck__[b] = c 
        
    def draw(self):
        return self.__deck__.pop()
    
    def __str__(self):
        s = "A 52-card deck, from which "+str(52-len(self.__deck__))+" cards have been drawn\n"
        for c in self.__deck__:
            s += "\t"
            s += c.__str__()
            s += "\n"
        return s
            
if __name__ == "__main__":
    d = deck()
    print d
    print "\n\n\n"
    for i in range(5):
        d.draw()
    print d
