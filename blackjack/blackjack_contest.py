#! /usr/bin/python

####    DEPENDS
from __future__ import division
import os
import sys
import itertools

############## CRITICAL IMPORTS ############
from bot import *
from cardshark import *
from deck import *

####    CONFIG
global VERBOSE, WARRIORS_DIR, SRC_DIR, NUM_ROUNDS, NUM_HANDS, HOUSE_SCORE, DEALER

WARRIORS_DIR    = "./warriors/"
SRC_DIR         = "./src"
NUM_ROUNDS      = 1
NUM_HANDS       = 5
HOUSE_SCORE     = 17
VERBOSE         = 1

DEALER = cardshark("./dealer.py")

def scores(players):
    return [ ((sum(i.__history__)/len(i.__history__)), i) for i in players ]
    
def trimBrokes(players, v=VERBOSE):
    return [i for i in players if i.hasDough]

def doShit(player, d, c, isFirstMove):
    s = player.run(c).strip("\n").split(" ")

    if "b" in s:
        b = abs(int(s[1]))
        if player.chips >= b:
            player.dChips(-1*b)
            player.stake += b
        else:
            player.stand = True

    elif "h" in s:
        d,c = deal(player, d, c)

    elif ("d" in s) and isFirstMove:
        d, c = deal(player, d, c)
        player.stand = True
        player.dChips(-1*player.stake)
        player.stake *= 2
        
    elif ("d" in s) and not isFirstMove:
        player.stand = True
    
    elif "s" in s:
        player.stand = True

    elif s != "":
        player.stand = True

    return d, c

def deal(player, d, c, v=VERBOSE):
    while True:
        try:
            c.append(d.draw())
            player.append(c[-1])
            break
        except IndexError:
            d = deck()
            continue

    return d, c

def runTable(players, hands = NUM_HANDS, dealer=DEALER, v=VERBOSE):
    __players__ = players
    d = deck()
    c = []

    for j in range(hands):
        players=list(__players__)
        
        d,c = deal(dealer, d, c)
        d,c = deal(dealer, d, c)
        c[-1].hidden = True
        
        for jj in [0,1]:
            for i in players:
                if i.hasDough and (jj == 0):
                    i.dChips(-10)
                    i.stake = 10
                    
                if i.hasDough:
                    d, c = deal(i, d, c)
                    
                else:
                    i.stand = True

        isFirstMove = True
        
        while (False in map(lambda x: x.stand, players)):
            for player in players:
                if not player.stand:
                    d,c = doShit(player, d, c, isFirstMove)
            isFirstMove = False
                    
        while not dealer.stand:
            d,c = doShit(dealer, d, c, False) 
                    
        for p in __players__:
            if p.__score__() > dealer.__score__():
                p.chips += (2*p.stake)

            p.hand = []
            p.stake = 0
            p.stand = False
            
        dealer.hand = []
        dealer.stand = False  
        for l in c: 
            l.hidden = False

    for player in __players__:
        player.rounds += 1
        
        player.__reset__()
        
def tourney(players, NUM_TOURNEYS = 25, NUM_ROUNDS = 5, NUM_HANDS = 5, v=VERBOSE):
    
    __players__ = list(players)
    
    del players
    
    for i in range(NUM_TOURNEYS):
        players = list(__players__)
        
        while False in map(lambda x: x.rounds == NUM_ROUNDS, players):
            players=trimBrokes(players)
            random.shuffle(players)
            
            if players != []:
                r_min = min(map(lambda x: x.rounds, players))
                s = [t for t in players if t.rounds == r_min]
                random.shuffle(s)
                s=s[0:4]
                runTable(s, hands = NUM_HANDS)
        
        for p in __players__:
            p.__history__.append(p.chips or 0)
            p.chips = 200
            p.rounds = 0
            p.__reset__()
            
        del players

    for p in __players__:
        print "   ",p.nicename(), (sum(p.__history__)/len(p.__history__))
        
    winner = max(scores(__players__))
    print "\tWinner is %s" %(winner[1].nicename(pad = False))

if __name__ == "__main__":
    if(('-?' in sys.argv) or ('--help' in sys.argv)):
        print """\nblackjack_contest.py\nAuthor: rmckenzie (http://codegolf.stackexchange.com/users/1370/rmckenzie)\n
Usage: ./blackjack_contest.py [[matches to run] [-i] [-v|-q]]\n\t-i specifies interactive mode via a simple cli\n\t-v enables a blow-by-blow output of hands, draws, bets and moves\n-q silences most output aside from the final results\n"""
    
    else:
        players = buildBots(WARRIORS_DIR, SRC_DIR, botType=cardshark)
        num_iters = 1
        
        try:
            num_iters = int(sys.argv[1])
        except Exception:
            pass
        
        tourney(players)
