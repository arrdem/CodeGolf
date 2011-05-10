#! /usr/bin/python
#
# Iterated prisoner's dilemma King of Hill Script.
# Argument is a directory.
# We find all the executables therein, and run all possible
# binary combinations (including self-plays (which only count once!)).
#
# Author: dmckee (http://codegolf.stackexchange.com/users/78/dmckee)
# Improved by : casey (http://codegolf.stackexchange.com/users/1375/casey)
#         and : Josh Caswell (http://codegolf.stackexchange.com/users/1384/josh-caswell)
# Major edits and CLI by: rmckenzie (http://codegolf.stackexchange.com/users/1370/rmckenzie)

####    DEPENDS
import subprocess 
import os
import sys
import random
import py_compile
import itertools
import multiprocessing
import string
import re

############## CRITICAL IMPORT ############
from bot import *

####    CONFIG
WARRIORS_DIR    = "./warriors/"     # path to the final executable bots
SRC_DIR         = "./src"           # path to the bot source code

NUM_ROUNDS = 100

RESULTS = {"cc":(2,"K"), "ct":(-1,"R"), "tc":(4,"S"), "tt":(1,"E")}

####    FUNCTIONS
def runGame(rounds,p1,p2, printing = (False, False)):
    print p1.nicename(),"Vs.", p2.nicename(),"\t",
    sa, sd = 0, 0
    ha, hd = '', ''
    for a in range(0,rounds):
        (na, ha), (nd, hd) = runRound(p1,p2,ha,hd)
        sa += na
        sd += nd
    print "Score: ", (sa, sd)
    if(printing[0]):
        print p1.nicename(),"Vs.", p2.nicename(),"\t", "Score: ", (sa, sd)
        if(printing[1]):
            print p1.nicename(pad = False), ha, "\n", p2.nicename(pad = False), hd
    return sa, sd

def runGameLoader(pair):
    global NUM_ROUNDS
    try:
        return runGame(NUM_ROUNDS,*pair)
    except Exception:
        print "[!] FATAL ERROR IN CONTEST"
        exit(1)

def runRound(p1,p2,h1,h2):
    """Run both processes, and score the results"""
    r1 = p1.run(h1)
    r2 = p2.run(h2)
    (s1, L1), (s2, L2) = scoreRound(r1,r2), scoreRound(r2,r1)
    return (s1, L1+h1),  (s2, L2+h2)

def scoreRound(r1,r2):
    return RESULTS.get(r1[0]+r2[0],0)

def runPairs(pairs, scores):
    pool = multiprocessing.Pool(None) # None = use cpu_count processes
    results = pool.map(runGameLoader, pairs)
    
    for (s1,s2),(p1,p2) in zip(results,pairs):
        if (p1 == p2):
            scores[p1] += (s1 + s2)/2
        else:
            scores[p1] += s1
            scores[p2] += s2

    return sorted(scores,key=scores.get), scores


def challenger(player, players, rounds = NUM_ROUNDS, v = False):

    print "Running %s tournament iterations of %s matches" % (num_iters, rounds)
    scores={}
    pointsFor = 0
    pointsAgainst = 0
    pairs = []
    
    for foo in players:
        pairs.append((player, foo))
        scores[foo] = 0
    
    players_sorted, scores = runPairs(pairs, scores)

    print "\n"
    for p in players_sorted:
        print p.nicename(), scores[p]

    print "\n\tTotal points for %s: %i" %(player.nicename(pad = False), pointsFor)
    print "\tTotal points against %s: %i" %(player.nicename(pad = False), pointsAgainst)

def tourney(num_iters, num_rounds, players, play_self = True):
    total_scores={}
    global NUM_ROUNDS
    NUM_ROUNDS = num_rounds   
    
    for p in players:
        total_scores[p] = 0
    
    print "Running %s tournament iterations of %s matches" % (num_iters, NUM_ROUNDS)
    
    for i in range(1,num_iters+1):
        print "\nTournament", i, "\n", "-"*80
        scores={}
        
        for p in players:
            scores[p] = 0
        
        # create the round robin pairs
        pairs = list( itertools.combinations( players, 2) )
        if(play_self):
            for foo in players:
                pairs.append([foo, foo])
        
        players_sorted, scores = runPairs(pairs, scores)
        
        print "\n"
        for p in players_sorted:
            print p.nicename(pad = False), scores[p]
        
        winner = max(scores, key=scores.get)
        print "\tWinner is %s" %(winner.nicename(pad = False))
        total_scores[p] += 1

    print '-'*80, "\n", "Final Results:"
    
    players_sorted = sorted(total_scores,key=total_scores.get)
    
    for p in players_sorted:
        print p.nicename(pad = False), total_scores[p]
    
    winner = max(total_scores, key=total_scores.get)
    print "Final Winner is " + winner.nicename(pad = False) + "!"

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
