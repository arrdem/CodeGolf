#! /usr/bin/python
#
# Iterated prisoner's dilemma King of Hill Script.
# Argument is a directory.
# We find all the executables therein, and run all possible
# binary combinations (including self-plays (which only count once!)).
#
# Author: rmckenzie (http://codegolf.stackexchange.com/users/1370/rmckenzie)
# Credit for base code goes to
#   dmckee (http://codegolf.stackexchange.com/users/78/dmckee)
#   casey (http://codegolf.stackexchange.com/users/1375/casey)
#   Josh Caswell (http://codegolf.stackexchange.com/users/1384/josh-caswell)

####    DEPENDS
import subprocess 
import os
import sys
import random
import py_compile
import itertools
import multiprocessing
import string

############## CRITICAL IMPORT ############
from bot import *

####    CONFIG
WARRIORS_DIR    = "./warriors/"     # path to the final executable bots
SRC_DIR         = "./src"           # path to the bot source code

NUM_ROUNDS = 100

####    FUNCTIONS

def scoreRound(r1,r2):
    #TODO
    @TODO

def runGame(rounds,p1,p2, printing = False):
    @TODO
    
def runPairs(pairs):
    pool = multiprocessing.Pool(None) # None = use cpu_count processes
    results = pool.map(runGameLoader, pairs)
    
    for (s1,s2),(p1,p2) in zip(results,pairs):
        if (p1 == p2):
            scores[p1] += (s1 + s2)/2
        else:
            scores[p1] += s1
            scores[p2] += s2

    return sorted(scores,key=scores.get)


def challenger(player, players, rounds = NUM_ROUNDS, v = False):

    print "Running %s tournament iterations of %s matches" % (num_iters, rounds)
    scores={}
    pointsFor = 0
    pointsAgainst = 0
    pairs = []
    
    for foo in players:
        pairs.append((player, foo))
        scores[foo] = 0
    
    players_sorted = runPairs(pairs)

    print "\n"
    for p in players_sorted:
        print p.nicename(), scores[p]

    print "\n\tTotal points for %s: %i" %(player.nicename(pad = False), pointsFor)
    print "\tTotal points against %s: %i" %(player.nicename(pad = False), pointsAgainst)

if __name__ == "__main__":
    if(('-?' in sys.argv) or ('--help' in sys.argv)):
        print """\nscore.py\nAuthor: dmckee (http://codegolf.stackexchange.com/users/78/dmckee)
Improved by : casey (http://codegolf.stackexchange.com/users/1375/casey)
        and : Josh Caswell (http://codegolf.stackexchange.com/users/1384/josh-caswell)
Major edits and CLI by: rmckenzie (http://codegolf.stackexchange.com/users/1370/rmckenzie)\n
Usage: score [[rounds] [games/round] [-i]]\n"""
    
    else:
        players = buildBots(WARRIORS_DIR, SRC_DIR)

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
            tourney(num_iters, NUM_ROUNDS, players)
