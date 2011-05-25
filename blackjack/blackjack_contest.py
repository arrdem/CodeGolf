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
HOUSE_SCORE = 17
global VERBOSE
VERBOSE = 0 # VARBOSE an integer range 0,2
            # 0 - basic printing
            # 1 - reasonable debugging
            # 2 - blow-by-blow

####    FUNCTIONS
def doShit(player, d, c, isFirstMove, v = 0):
    try:
        if player.__score__() > 21:
            raise Exception
        if v>1:
            print "    ||",player.nicename(pad = False),"has: ",
            for a in range(len(player.hand)):
                print player.hand[a],
                if(0 <= a < len(player.hand)-1):
                    print " "*(20-len(str(player.hand[a-1]))),
        
            print "\n    ||      chose to :",
        
        s = player.run(c).strip("\n").split(" ")
        
        if "b" in s:
            # then s should be of the format ['b', '50'] or something like
            b = abs(int(s[1])) # just in case bots try to make negative bets... >:-)
            player.dChips(-1*b)
            players.stake += b
            if v>1: print "Bet $",b
        
        elif "h" in s:
            d,c = deal(player, d, c)
            if v>1: print "Draw, got:", c[-1]
        
        elif ("d" in s) and isFirstMove:
            d, c = deal(player, d, c)
            player.stand = True
            player.dChips(player.stake)
            player.stake *= 2
            if v>1: print "DoubleDown, got:", c[-1]
            
        elif ("d" in s) and not isFirstMove:
            player.stand = True
            
        elif "s" in s:
            if v>1: print "Stand"
            player.stand = True
            
        elif "p" in s:
            # UNSUPPPORTED
            player.__die__()
        
        else:
            if True: print "[!] WARNING - NO ACTION TAKEN\n\n     ORIGINAL OUTPUT WAS:",s,"\n\n[!] CONTINUING\n\n"
             
    except Exception:
        player.stand = True
    finally:
        return d, c

def deal(player, d, c):
    while True:
        try:
            c.append(d.draw())
            player.append(c[-1])
            break
        except IndexError:
            # the deck is empty....
            # deal from a new deck or something...
            d = deck()
            continue
    return d, c

def runTable(players, hands = NUM_ROUNDS):
    global VERBOSE
    v = VERBOSE
    for hand in range(hands):
        print "\n\n","*"*80
        print "#### Deck number: "+str(hand)
        print "*"*80
        d = deck()
        c = []
        dealer=[]
        s=list(players)
        
        for j in range(5):

            # subtract the buy-in cost, deal
            for i in range(len(players)):
                player = players[i]
                if player.hasDough:
                    player.dChips(-10)
                    d, c = deal(player, d, c)
                    player.stake = 10                    
                else:
                    player.stand = True
            isFirstMove = False
                    
            d,c = deal(dealer, d, c)
            
            # now let them play....   
            while (False in map(lambda x: x.stand, players)): # while SOMEONE is still up,
                for player in players:
                    if not player.stand:
                        d,c = doShit(player, d, c, isFirstMove, v = VERBOSE)
                isFirstMove = False
                        
            while sum(map(lambda x: x.score(), dealer)) < 17:
                d,c = deal(dealer, d, c)
            if sum(map(lambda x: x.score(), dealer)) > 21:
                dealer = []
            try:
                print "\n[DEALER] "+20*"-"+"> ",sum(map(lambda x: x.score(), dealer))
            except Exception:
                print 0
            
            for p in players:
                if p.__score__() > sum(map(lambda x: x.score(), dealer)):
                    print "[+]"+" "*4, 
                    p.chips += (2*p.stake)
                else:
                    print "[-]"+" "*4,
                l=len(p.nicename())
                print p.nicename()," "*2, p.__score__(), " "*(8-len(str(p.__score__()))), p.chips,
                
                print " "*(12-len(str(p.__score__())+str(p.chips))),
                for a in range(len(p.hand)):
                    print p.hand[a].letter(),
                
                print ""
                p.hand = []
                p.stake = 0
                p.stand = False
                
            dealer = []
    
    for player in s:
        if player != dealer:
            print player.nicename(), player.chips
        player.__reset__()
        
def scores(players):
    a=[]
    for i in players: a.append((i.chips, i))
    return a
    
def trimBrokes(players):
    l=[]
    for i in players:
        if i.hasDough:
            l.append(i)
    return l
        
def tourney(players, NUM_ROUNDS = 1, NUM_HANDS = 3):
    for i in range(NUM_ROUNDS):
        print "-"*80, "\n", "ROUND NUMBER", (i+1), "\n", "-"*80
        sets = list(itertools.combinations(players, 4))
        
        for f in sets:
            f=trimBrokes(f)
            if f != []:
                runTable(f, hands = NUM_HANDS)

    #### FORMAL RESULTS PRINTING
    print "\n","-"*80
    for p in players:
        print p.nicename(pad = False), p.chips
        
    winner = max(scores(players))
    print "\tWinner is %s" %(winner[1].nicename(pad = False))

if __name__ == "__main__":
    if(('-?' in sys.argv) or ('--help' in sys.argv)):
        print """\nblackjack_contest.py\nAuthor: rmckenzie (http://codegolf.stackexchange.com/users/1370/rmckenzie)\n
Usage: ./blackjack_contest.py [[matches to run] [-i] [-v|-vv]]\n\t-i specifies interactive mode via a simple cli\n\t-v enables a very verbose printing of players' moves\n-vv makes the scoring code print EVERYTHING\n"""
    
    else:
        players = buildBots(WARRIORS_DIR, SRC_DIR, botType=cardshark)
        num_iters = 1
        
        if "-v" in sys.argv:
            VERBOSE = 1
        elif "-vv" in sys.argv:
            VERBOSE = 2
        else:
            VERBOSE = 0
        
        try:
            num_iters = int(sys.argv[1])
        except Exception:
            pass
        
        if not ("-i" in sys.argv):
            tourney(players, NUM_ROUNDS = num_iters)
        
        else:
            print \
"""
########################################################################
## \\\\/\\\\/ELCOME to the BlackJack Contest CLI                          ##
##  Use quit, ctrl-d or ctr-c to exit the interpreter                 ##
##  Use help to list commands, Help [command] for more information    ##
##                                                                    ##
##  WARNING:                                                          ##
##      DO NOT CTRL+C OR CTRL+D WHILE THE CONTEST IS RUNNING.         ##
##      AT PRESENT, THIS SOFTWARE DOESN'T HAVE SUPPORT FOR THOSE      ##
##      ERRORS WHILE RUNNING CONTESTS AND THE SCORING CODE WILL CRASH ##
########################################################################
"""
            # CLI implimentation here
            champ_dict = {}
            for foo in players:
                champ_dict[foo.nicename(pad = False)] = foo
            
            pop_dict = { 'default' : players}
            help_dict = {
                         'list'     : "usage: list [population]\n\twith argument lists the contents of the population.\n\telse lists populations.",
                         'match'    : "usage: match [champ] [[rounds] [-v]]\n\tpits one champ against the dealer.\n\t -v causes the match's play-by play to be printed too.'",
                         #'challenge': "usage: challenge [champ] [population] [[rounds] [-v]]\n\tpits one champ against the others\n\t -v causes the match's play-by play to be printed too.'",
                         'run'      : "usage: run [population] [[hands]]\n\truns all champs against the house.",
                         'quit'     : "exits this CLI",
                         'del'      : "usage: del [champion] [population] [[count] [-a]]\n\tdeletes count (default 1) instance of champion from the population.\n\t-a deletes all.",
                         'add'      : "usage: add [champion] [population] [[instances]]\n\tadds the specified number of instances of the champion to a given population",
                         'new'      : "usage: new [population name]\n\tcreates an empty list of champions",
                         ''         : "avalable commands:\nlist, match, run, new, add, quit"
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
                                runTable(dealer, champ_dict[cmd[1]])
                            except Exception:                            
                                print "[!] BAD COMMAND ERROR - TRY THIS COMMAND: help match"
                                continue
                    
                        if(cmd[0] == "run"):
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
                    
                            tourney(pop, NUM_ROUNDS = itters)
                        
                        if("quit" in cmd):
                            print "Bye.\n"
                            break
                        
                        else:
                            continue
                        
                except EOFError:
                        print "\n\nBye.\n"
                        exit(0)
                
                except KeyboardInterrupt:
                        print "\n\nBye.\n"
                        exit(0)
                        
                except Exception:
                        print "[!] ERROR IN REPL LOOP - TOP LEVEL"
                        continue
