#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       card-shark.py
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
#       This is an extension of the bot class developed for the
#       code-golf blackjack challenge.
#
#   DOCUMENTATION
#       INPUT SPECIFICATION
#          $ ./foo.bar <hand-score> <hand> <visible cards> <stake> <chips>
#          <hand-score>     is the present integer value of the player's hand.
#          <hand>           is a space-free string of the characters [1-9],A,J,Q,K
#          <visible cards>  every dealt card on the table
#          <stake>          the  number of chips which the bot has bet this hand
#          <chips>          the number of chips which the bot has
#       SAMPLE INPUT
#          $ ./foo.bar KJA KQKJA3592A 25 145
#
#       OUTPUT SPECIFICATION
#          "H"|"S"|"D"      (no quotes in output)
#          "H"              HIT - deal a card
#          "S"              STAND - the dealer's turn
#          "D"              DOUBLEDOWN - double the bet, take one card. FIRST MOVE ONLY

import subprocess 
from cards import card
from bot import *
import errors

DEFAULT_CHIPS = 200
TEST_CASE = "21 KJA KQKJA3592A 25 145"

class cardshark(bot):
    def __init__(self, filename, chips = DEFAULT_CHIPS, hand = ""):
        bot.__init__(self, filename)
        self.filename = filename
        self.hand = []
        self.stand = False
        self.chips = chips
        self.stake = 0
        self.wins = 0
        self.hasDough = True
        
    def __reset__(self):
        self.hand = []
        self.stand = False
        self.stake = 0

    def __test__(self):
        process = subprocess.Popen(self.exec_code+" "+TEST_CASE,stdout=subprocess.PIPE,shell=True)
        if (process.communicate()[0].strip().lower() not in ("h", "s", "d")):
            self.__die__()
            
    def __score__(self):
        s = sum(map(lambda x: x.score(), self.hand))
        if True in map(lambda x: x.isAce(), self.hand):
            if s > 21:
                s = sum(map(lambda x: x.score(aceEleven = False), self.hand))
        if s > 21:
            self.stand = True
            self.hand = []
        return s
        
    def __hand__(self, cards):
        s = ""
        for c in cards:
            s += c.letter()
        return s
        
    def dChips(self, s):
        self.chips += s
        self.hasDough = (self.chips > 0)
        
    def run(self, cards_dealt):
        if self.hasDough:
            process = subprocess.Popen(self.exec_code+" "+\
                                       str(self.__score__())+" "+\
                                       self.__hand__(self.hand)+" "+\
                                       self.__hand__(cards_dealt)+" "+\
                                       str(self.stake)+" "+\
                                       str(self.chips),stdout=subprocess.PIPE,shell=True)
            o = process.communicate()[0].strip().lower()
            
            if o=="s":
                self.stand = True
            
            return o
    
    def append(self, c):
        if type(c) == type(card("Clubs", "Nine")):
            self.hand.append(c)
        else:
            raise Exception
