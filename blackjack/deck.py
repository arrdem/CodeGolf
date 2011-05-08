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
#   DOCUMENTATION
#
#


import cards
import itertools
import random

class deck:
    def __init__(self, jokers = False):
        self.__deck__ = []
        self.__clean__ = __cleandeck__()
        self.deck = self.shuffle()
    
    def __cleandeck__(self):
        d = []
        for a in cards.SUITS:
            for b in cards.CARDS:
                d.append(cards.card(a, b))
        return d
    
    def shuffle(self):
        self.__deck__ = itertools.permutations(self.__clean__, len(self.__clean__))[random.randomint()%len(self.__clean__)]
        
    def draw(self):
        return self.__deck__.pop()
        
