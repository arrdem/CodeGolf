#! /usr/bin/python
#
# Iterated prisoner's dilemma King of Hill Script.
# Argument is a directory.
# We find all the executables therein, and run all possible
# binary combinations (including self-plays (which only count once!)).
#
# Author: rmckenzie (http://codegolf.stackexchange.com/users/1370/rmckenzie)

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

WARRIORS_DIR    = "./warriors/"     # path to the final executable bots
SRC_DIR         = "./src"           # path to the bot source code
NUM_ROUNDS      = 1
NUM_HANDS       = 5
HOUSE_SCORE     = 17
VERBOSE         = 1 # VERBOSE an integer range 0,2
                    # 0 - minimum printing
                    # 1 - reasonable debugging
                    # 2 - blow-by-blow

if "-q" in sys.argv:
    VERBOSE = 0
elif "-vv" in sys.argv:
    VERBOSE = 2
else:
    VERBOSE = 1

DEALER = cardshark("./dealer.py")

####    FUNCTIONS
def doShit(player, d, c, isFirstMove, v = VERBOSE):
    if v>1:
        sys.stdout.write("    ||\n    || "+player.nicename(pad = False)+" has: ")
        for a in range(len(player.hand)):
            sys.stdout.write(str(player.hand[a]))
            if(0 <= a < len(player.hand)-1):
                sys.stdout.write(" "*(20-len(str(player.hand[a-1]))))

        sys.stdout.write("\n    ||      chose to : ")

    s = player.run(c).strip("\n").split(" ")

    if "b" in s:
        # then s should be of the format ['b', '50'] or something like
        b = abs(int(s[1])) # just in case bots try to make negative bets... >:-)
        if player.chips >= b:
            player.dChips(-1*b)
            player.stake += b
        else:
            player.stand = True
        if v>1:
            sys.stdout.write("Bet $ "+str(b)+", had $"+str(player.chips))
            if player.chips < b:
                sys.stdout.write(", Forced to stand for a bad bet")

    elif "h" in s:
        d,c = deal(player, d, c)
        if v>1: 
            sys.stdout.write("Draw, got: "+str(c[-1]))
            if player.stand:
                sys.stdout.write("\n    ||      .....and busted.")

    elif ("d" in s) and isFirstMove:
        d, c = deal(player, d, c)
        player.stand = True
        player.dChips(-1*player.stake)
        player.stake *= 2
        if v>1:
            sys.stdout.write("DoubleDown, got: "+str(c[-1]))
        
    elif ("d" in s) and not isFirstMove:
        player.stand = True
        
    elif "p" in s:
        # UNSUPPPORTED
        player.__die__()
        
    # now deal with errors, standing as a block
    
    elif "s" in s:
        if v>1:
            sys.stdout.write("Stand")
        player.stand = True

    elif s != "":
        player.stand = True
        if v>0:
            print "\n[!] WARNING - NO ACTION TAKEN BY "+player.nicename(pad=False)+"\n[!]    ORIGINAL OUTPUT WAS:",repr(s)
            print "[!]    ",
            for m in c:
                print m.letter(),
            print "\n[!]    "+player.nicename(pad=False)+"\n[!]    INPUT WAS "+player.__execstr__(c)

    if v>1: sys.stdout.write("\n")
    return d, c

def deal(player, d, c, v=VERBOSE):
    while True:
        try:
            c.append(d.draw())
            player.append(c[-1])
            break
        except IndexError:
            # the deck is empty....
            # deal from a new deck or something...
            d = deck()
            if v>1: sys.stderr.write("\n[WARNING] - NEW DECK CREATED\n")
            continue
    return d, c

def runTable(players, hands = NUM_HANDS, dealer=DEALER, v=VERBOSE):
    __players__ = players
    d = deck()
    c = []
    
    # Outermost game loop
    for j in range(hands):
        players=list(__players__)
        
        d,c = deal(dealer, d, c)
        d,c = deal(dealer, d, c)
        c[-1].hidden = True
        
        for jj in [0,1]:            # do this twice..
            for i in players:       # for each player:
                if i.hasDough and (jj == 0):    # if this is the first pass
                    i.dChips(-10)               # charge 'em money
                    i.stake = 10
                    
                if i.hasDough:                  # if he's got the money
                    d, c = deal(i, d, c)        # deal him in
                    
                else:
                    i.stand = True         # gtfo broke

        isFirstMove = True
        
        # now let them play....   
        while (False in map(lambda x: x.stand, players)): # while SOMEONE is still up,
            for player in players:
                if not player.stand:
                    d,c = doShit(player, d, c, isFirstMove)
            isFirstMove = False
                    
        while not dealer.stand:
            d,c = doShit(dealer, d, c, False) 
            
        if v>0:
            print "\n\n[+/-]        Bot's Name         Score     Chips       Hand" 

            try:
                print "[DEALER] "+20*"-"+"> ",dealer.__score__()
            except Exception:
                print 0
        
        for p in players:
            if p.__score__() > dealer.__score__():
                if v>0: print "[+]"+" "*4, 
                p.chips += (2*p.stake)
            else:
                if v>0: print "[-]"+" "*4,
            if v>0:
                l=len(p.nicename())
                print p.nicename()," "*2, p.__score__(), " "*(8-len(str(p.__score__()))), p.chips,
                
                print " "*(12-len(str(p.__score__())+str(p.chips))),
                for a in range(len(p.hand)):
                    print p.hand[a].letter(),
                
                if v>0: print ""
            p.hand = []
            p.stake = 0
            p.stand = False
            
        dealer.hand = []
        dealer.stand = False  
        for l in c: 
            l.hidden = False        # unhide the dealer's old cards
        
    if v>0: print "\n\n Scores:"
    for player in __players__:
        if player != dealer:
            if v>0: print player.nicename(), player.chips
        player.rounds += 1
        
        player.__reset__()
    if v>0: print "\n"
        
def scores(players):
    a=[]
    for i in players: a.append( ((sum(i.__history__)/len(i.__history__)), i) )
    return a
    
def trimBrokes(players, v=VERBOSE):
    l=[]
    for i in players:
        if i.hasDough:
            l.append(i)
        else:
            if v>1: print "\n[!] "+i.nicename(pad=False)+" is broke\n"
    return l
        
def tourney(players, NUM_TOURNEYS = 25, NUM_ROUNDS = 5, NUM_HANDS = 5, v=VERBOSE):
    
    __players__ = list(players)
    del players
    
    for i in range(NUM_TOURNEYS):
        players = list(__players__)
        c=0    
        while False in map(lambda x: x.rounds == NUM_ROUNDS, players):  # while NOT all players have played NUM_ROUNDS rnds:
            players=trimBrokes(players)                                 # trim out the brokes...
            random.shuffle(players)                                     # shufle the list of players to try and mix up the tables
            if players != []:                                           # if there are still bots who can play
                r_min = min(map(lambda x: x.rounds, players))           # find the MINUMUM of the number of rounds played by all the bots
                s = [t for t in players if t.rounds == r_min][0:4]      # collect all bots with that many games played, slice to first four
                if v>0: print "#"*80, "\n", "ROUND NUMBER", (r_min+1), "\n", "#"*80
                runTable(s, hands = NUM_HANDS)                          # play'em off
                c+=1
        
        #print "\n", len(__players__), len(players)
        if v>1: sys.stderr.write("[!] END OF TOURNEY ROUND, PRINTING SCORES & RESETTING\n")
        for p in __players__:
            p.__history__.append(p.chips or 0)
            p.chips = 200
            p.rounds = 0
            p.__reset__()
            
        del players

    #### FORMAL RESULTS PRINTING
    if v>0: print "\n","-"*80, "\nFinal Tournament Scores:"
    for p in __players__:
        print "   ",p.nicename(pad = False), (sum(p.__history__)/len(p.__history__))
        
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
        
        if not ("-i" in sys.argv):
            tourney(players)
        
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
                            flag = 2 if ('-v' in cmd) else 0
                            try:
                                runTable(dealer, list(champ_dict[cmd[1]]), v=flag)
                            except Exception:                            
                                print "[!] BAD COMMAND ERROR - TRY THIS COMMAND: help match"
                                continue
                    
                        if(cmd[0] == "run"):
                            itters = 5
                            rounds = 100
                            try:
                                pop = pop_dict[cmd[1]]
                            except Exception:
                                print "[!] BAD POPULATION PROVIDED - using default"
                                pop = pop_dict["default"]
                            
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
