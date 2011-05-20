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
    print range(hands/numHandsPerDeck)
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
                print p.nicename(), p.__score__()
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
Usage: ./blackjack_contest.py [[rounds] [games/round] [-i]]\n"""
    
    else:
        players = buildBots(WARRIORS_DIR, SRC_DIR, botType=cardshark)
        num_iters = 1
        
        try:
            num_iters = int(sys.argv[1])
        except Exception:
            pass
            
        try:
            NUM_ROUNDS = int(sys.argv[2])
        except Exception:
            pass
        
        if('-i' in sys.argv):
            # a crude CLI for special testing etc.
            champ_dict = {}
            for foo in players:
                champ_dict[foo.nicename(pad = False)] = foo
            
            pop_dict = { 'default' : players}
            help_dict = {
                         'list'     : "usage: list [population]\n\twith argument lists the contentsof the population.\n\telse lists populations.",
                         'match'    : "usage: match [champ] [champ] [[rounds] [-v]]\n\tpits two champs against each-other\n\t -v causes the match's play-by play to be printed too.'",
                         'challenge': "usage: challenge [champ] [population] [[rounds] [-v]]\n\tpits one champ against the others\n\t -v causes the match's play-by play to be printed too.'",
                         'tourney'  : "usage: tourney [population] [[itterations] [rounds]]\n\tplays off all champs against each-other.",
                         'quit'     : "exits this CLI",
                         'del'      : "usage: del [champion] [population] [[count] [-a]]\n\tdeletes count (default 1) instance of champion from the population.\n\t-a deletes all.",
                         'add'      : "usage: add [champion] [population] [[instances]]\n\tadds the specified number of instances of the champion to a given population",
                         'new'      : "usage: new [population name]\n\tcreates an empty list of champions",
                         ''         : "avalable commands:\nlist, match, challenge, tourney, new, add, quit"
                        }
            
            for champ in players:
                champ_dict[champ.nicename(pad = False)] = champ
            
            while 1:
                try:
                    foo = raw_input("\n[]> ")
                    if(foo == ""):
                        continue
                    else:
                        if(" " in foo):
                            cmd = foo.split(" ")
                        else:
                            cmd = [foo]
                        
                        if(cmd[0] == ("help" or "?")):
                            try:
                                print help_dict[cmd[1]]
                            except Exception:
                                print help_dict['']
                        
                        if(cmd[0] == "add"):
                            try:
                                i = 1
                                if cmd[3]: i = int(cmd[3])
                                for foo in xrange(i):
                                    pop_dict[cmd[2]].append(champ_dict[cmd[1]])
                            except Exception:
                                print "[!] BAD COMMAND ERROR - TRY THIS COMMAND: help add"
                                
                        if(cmd[0] == 'new'):
                            try:
                                if cmd[1] in pop_dict:
                                    print "[!] *WARNING* - POPULATION EXISTS"
                                    if not ('y' == raw_input("(y/n) > ")):
                                        continue
                                pop_dict[cmd[1]] = []
                            except Exception:
                                print "[!] BAD COMMAND ERROR - TRY THIS COMMAND: help new"
                                
                        if(cmd[0] == 'del'):
                            try:
                                if(cmd[3]):
                                    try:
                                        count = int(cmd[3])
                                    except Exception:
                                        print "[*] EXTERMINATE! EXTERMINATE! EXTERMINATE!"
                                        count = int(1e300000)
                                for c in range(0, len(pop_dict[cmd[2]])):
                                    if (pop_dict[cmd[2]][c] == champ_dict[cmd[1]]):
                                        if(count > 0):
                                            pop_dict[cmd[2]][c].pop()
                            except Exception:
                                print "[!] BAD COMMAND ERROR - TRY THIS COMMAND: help del OR MAYBE: list default"
                        
                        if(cmd[0] == "list"):
                            try:
                                if(cmd[1]):
                                    print "Avalible champs in " + cmd[1] + ":"
                                    for c in pop_dict[cmd[1]]:
                                        print "\t", c.nicename(pad = False)
                                else:
                                    print "Avalible populations:"
                                    for c in pop_dict:
                                        print "\t", c
                            except Exception:
                                print "Avalible populations:"
                                for c in pop_dict:
                                    print "\t", c

                        if(cmd[0] == "match"):
                            flag = ('-v' in cmd)
                            try:
                                runGame(int(cmd[3]), champ_dict[cmd[1]], champ_dict[cmd[2]], printing = flag)
                            except Exception:
                                try:
                                    runGame(50, champ_dict[cmd[1]], champ_dict[cmd[2]], printing = flag)
                                except Exception:
                                    print "[!] BAD COMMAND ERROR - TRY THIS COMMAND: help match"
                                    continue
                        
                        if(cmd[0] == "challenge"):
                            rounds = 100
                            flag = ('-v' in cmd)
                            chuck_norris = None
                            pop = []
                            try:
                                chuck_norris = champ_dict[cmd[1]]
                            except Exception:
                                print "[!] BAD CHAMPION PROVIDED - TRY THIS COMMAND: help challenge OR: list default"
                                continue
                            
                            try:
                                pop = pop_dict[cmd[2]]
                            except Exception:
                                print "[!] BAD POPULATION PROVIDED - TRY THIS COMMAND: help challenge OR: list"
                                continue
                                
                            try:
                                rounds = int(cmd[3])
                            except Exception:
                                pass
                            
                            challenger(chuck_norris, pop, rounds = rounds, v = flag)
                        
                        if(cmd[0] == "tourney"):
                            itters = 5
                            rounds = 100
                            pop = []
                            try:
                                pop = pop_dict[cmd[1]]
                            except Exception:
                                print "[!] BAD POPULATION PROVIDED - TRY THIS COMMAND: help tourney OR: list"
                                continue
                            
                            try:
                                itters = int(cmd[2])
                            except Exception:
                                pass
                                
                            try:
                                rounds = int(cmd[3])
                            except Exception:
                                pass
                    
                            tourney(itters, rounds, pop)
                        
                        if("quit" in cmd):
                            print "Bye.\n"
                            break
                        
                        else:
                            continue
                        
                except Exception:
                    if Exception in (EOFError or KeyboardInterrupt):
                        print "Bye."
                        exit(0)
                    else:
                        print "[!] ERROR IN REPL LOOP - TOP LEVEL"
                        continue
        
        else:
            tourney(players, NUM_ROUNDS = num_iters)
