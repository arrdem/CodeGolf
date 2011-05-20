#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       cards.py
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
#       This code was developed for the code-golf BlackJack KOTH game.
#       This file serves to do two things.
#       1 - it serves as a wrapper for the CARDS, SUITS and SCORES dicts
#       2 - it serves to hold the card class, from which I base deck.py
#
#   DOCUMENTATION
#       class CARD
#           card is a container for representing paper playing cards in
#           otherwise fairly functional programming.
#           __init__()
#               sets up the card
#           __str__()
#               builds the card into a pretty string for printing
#           score()
#               gets the integer value of the card
#           TODO:
#               THERE IS NO ERROR CHECKING IN THIS CLASS. YOU CAN MAKE A
#               CARD OF SUIT "BANANA" IF YOU WANT TO.

__CARDS =  [ "Ace",
           "One",
           "Two",
           "Three",
           "Four",
           "Five",
           "Six",
           "Seven",
           "Eight",
           "Nine",
           "Ten",
           "Jack",
           "Queen",
           "King"
         ]

__SUITS = [ "Clubs",
          "Spades",
          "Hearts",
          "Diamonds" ]

__SCORES = { "Ace"    :(1,11),
           "One"    :1,
           "Two"    :2,
           "Three"  :3,
           "Four"   :4,
           "Five"   :5,
           "Six"    :6,
           "Seven"  :7,
           "Eight"  :8,
           "Nine"   :9,
           "Ten"    :10,
           "Jack"   :10,
           "Queen"  :10,
           "King"   :10
         }

# some error protection, so that stupid devs can override defaults
SCORES = __SCORES
SUITS = __SUITS
CARDS = __CARDS


class card:
    def __init__(self, suit, face):
        self.suit = suit
        self.type = face
        self.value = self.score()
    
    def isAce(self):
        global __CARDS
        return (self.type == "Ace")
    
    def score(self, aceEleven = False):
        if not self.type == "Ace":
            return SCORES[self.type]
        else:
            if aceEleven:
                return SCORES[self.type][1]
        return SCORES[self.type][0]
        
    def letter(self):
        if 1 < self.score() < 10:
            return str(self.score())
        return str(self)[0].lower()
    
    def __call__(self):
        return self
        
    def __str__(self):
        return str(self.type) + " of " + self.suit
