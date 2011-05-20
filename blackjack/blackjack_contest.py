#! /usr/bin/python
#
# Iterated prisoner's dilemma King of Hill Script.
# Argument is a directory.
# We find all the executables therein, and run all possible
# binary combinations (including self-plays (which only count once!)).
#
# Author: rmckenzie (http://codegolf.stackexchange.com/users/1370/rmckenzie)

####    DEPENDS
import os
import sys
import random
import py_compile
import itertools
import multiprocessing
import string

############## CRITICAL IMPORT ############
from bot import *
from cardshark import *
from deck import *
from errors import *

####    CONFIG
WARRIORS_DIR    = "./warriors/"     # path to the final executable bots
SRC_DIR         = "./src"           # path to the bot source code
NUM_ROUNDS = 1

DEALER = cardshark("./dealer.py")

####    FUNCTIONS

def doShit(player, d, c, isFirstMove):
    try:
        s = player.run(c).split(" ")
        if "b" in s:
            # then s should be of the format ['b', '50'] or something like
            b = abs(int(s[1])) # just in case
            player.dChips(-1*b)
            players.stake += b
        
        if "h" in s:
            c.append(d.draw())
            player.append(c[-1])
        
        if ("d" in s) and isFirstMove:
            c.append(d.draw())
            player.append(c[-1])
            player.stand = True
            player.dChips(player.stake)
            player.stake *= 2
            
        if "p" in s:
            # UNSUPPPORTED
            player.__die__()
    except AttributeError:
        player.stand = True

def runTable(players, dealer = DEALER, hands = NUM_ROUNDS):
    numHandsPerDeck = 52/(len(players)*4)
    for i in range(hands/numHandsPerDeck):
        d = deck()
        c = []
        
        for j in range(numHandsPerDeck):
            isFirstMove = True

            # subtract the buy-in cost, deal
            for i in range(len(players)):
                player = players[i]
                if player.hasDough:
                    player.dChips(-10)
                    c.append(d.draw())
                    player.append(c[-1])
                    player.stake = 10
                else:
                    player.stand = True
            
            c.append(d.draw())
            dealer.append(c[-1])
                
            # now let them play....   
            while (False in map(lambda x: x.stand, players)): # while SOMEONE is still up,
                for player in players:
                    if not player.stand:
                        doShit(player, d, c, isFirstMove)
                        
            while dealer.__score__() < 17:
                doShit(dealer, d, c, False)
            print "[DEALER]\t",dealer.__score__()
                
            for p in players:
                if p.__score__() > dealer.__score__():
                    print "[+]\t", 
                    p.chips += (2*p.stake)
                else:
                    print "[-]\t",
                print p.nicename(), p.__score__(), 
                
                print " "*(12-len(str(p.__score__()))),
                for a in range(len(p.hand)):
                    print p.hand[a],
                    if(0 <= a < len(p.hand)-1):
                        print " "*(20-len(str(p.hand[a-1]))),
                
                print ""
                p.hand = []
                p.stake = 0
                
            dealer.hand = []
                
    for player in players:
        print player.nicename(), player.chips
        player.__reset__()
        
def scores(players):
    a=[]
    for i in players: a.append((i.chips, i))
    return a
    
        
def tourney(players, NUM_ROUNDS = 1, NUM_HANDS = 3):
    for i in range(NUM_ROUNDS):
        print "-"*80, "\n", "ROUND NUMBER", i, "\n", "-"*80
        sets = list(itertools.combinations(players, 4))
        
        for f in sets:
            runTable(f, hands = NUM_HANDS)
        
        print "\n","-"*80
        for p in players:
            print p.nicename(pad = False), p.chips
        
        winner = max(scores(players))
        print "\tWinner is %s" %(winner[1].nicename(pad = False))

if __name__ == "__main__":
    if(('-?' in sys.argv) or ('--help' in sys.argv)):
        print """\nblackjack_contest.py\nAuthor: rmckenzie (http://codegolf.stackexchange.com/users/1370/rmckenzie)\n
Usage: ./blackjack_contest.py [[matches to run]]\n"""
    
    else:
        players = buildBots(WARRIORS_DIR, SRC_DIR, botType=cardshark)
        num_iters = 1
        try:
            num_iters = int(sys.argv[1])
        except Exception:
            pass
        
        tourney(players, NUM_ROUNDS = num_iters)
