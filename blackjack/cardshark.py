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
#          <visible cards>  every dealt card on the table. when new shoes are brought
#                           into play, cards drawn therefrom are simply added to this list
#                           NOTE: the first TWO (2) cards in this list belong to the dealer.
#                             one however will be "hidden" by a "#". the other is visible.
#                           !!! THE LIST IS CLEARED AT THE END OF HANDS, NOT SHOES !!!
#          <stake>          the  number of chips which the bot has bet this hand
#          <chips>          the number of chips which the bot has
#       SAMPLE INPUT
#          $ ./foo.bar 21 KJA KQKJA3592A 25 145
#
#       OUTPUT SPECIFICATION
#          "H"|"S"|"D"|"B"  (no quotes in output)
#          "H"              HIT - deal a card
#          "S"              STAND - the dealer's turn
#          "D"              DOUBLEDOWN - double the bet, take one card. FIRST MOVE ONLY
#          "B 15"           BET - raises the bot's stakes by $15.

import subprocess 
from cards import card
from bot import *
import sys

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
        self.rounds = 0
        self.__history__ = []
        self.bad = 0
        self.hands = 0
        
    def __reset__(self):
        self.hand = []
        self.stand = False
        self.stake = 0
        self.hasDough =(self.chips >= 10)

    def __test__(self):
        process = subprocess.Popen(self.exec_code+" "+TEST_CASE,stdout=subprocess.PIPE,shell=True)
        if (process.communicate()[0].strip().lower() not in ("h", "s", "d")):
            self.__die__()
            
    def __score__(self):
        s = sum(map(lambda x: x.score(aceEleven = True), self.hand))
        if True in map(lambda x: x.isAce(), self.hand):
            aces = [a for a in self.hand if a.isAce()]
            nonaces = [c for c in self.hand if not (c in aces)]
            
            for m in range(len(aces)):                
                sb = sum(map(lambda x: x.score(aceEleven = False), nonaces))
                for i in range(len(aces)):
                    s = sb + sum(map(lambda x: x.score(aceEleven = False), aces[0:i])) +sum(map(lambda x: x.score(aceEleven = False), aces[i-1::]))
                    if s <= 21:
                        break
                        
        if s > 21:
            self.stand = True
            s = 0
        return s
        
    def __hand__(self, cards):
        s = ""
        for c in cards:
            s += c.letter()
        return s
        
    def dChips(self, s):
        self.chips += s
        self.hasDough = ((self.chips > 10) or (self.stake > 0))
        
    def __execstr__(self, cards_dealt):
        s= self.exec_code+" "+\
           str(self.__score__())+" "+\
           self.__hand__(self.hand)+" "+\
           self.__hand__(cards_dealt)+" "+\
           str(self.stake)+" "+\
           str(self.chips)
        if not (s==""):
            return s
        print "[!]",s
        print "[!]",s
        print "[!]",
        for c in cards_dealt:
            print str(c),
        print ""
        sys.exit(1, msg="BAD EXECSTRING GENERATED")
        
    def run(self, cards_dealt):
        if (self.hasDough and (self.bad < 15)):
            process = subprocess.Popen(self.__execstr__(cards_dealt),stdout=subprocess.PIPE,shell=True)
            o = process.communicate()[0].strip().lower()
            
            if o=="s":
                self.stand = True
            
            return o
        else:
            print self.__execstr__(cards_dealt)
            sys.exit(1)
    
    def append(self, c):
        self.hand.append(c)
        self.__score__()
