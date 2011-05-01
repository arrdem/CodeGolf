#! /usr/bin/python
#
# Iterated prisoner's dilemma King of Hill Script Argument is a
# directory. We find all the executables therein, and run all possible
# binary combinations (including self-plays (which only count once!)).
#
# Author: dmckee (http://codegolf.stackexchange.com/users/78/dmckee)
#
import subprocess 
import os
import sys
import random
import py_compile
import itertools
import multiprocessing
import string
###
# config
PYTHON_PATH = '/usr/bin/python' #path to python executable
CLISP_PATH = '/usr/bin/clisp'   #path to clisp executable

RESULTS = {"cc":(2,"K"), "ct":(-1,"R"), "tc":(4,"S"), "tt":(1,"E")}

class warrior:
    def __init__(self, filename):
        print "[!] CREATED WARRIOR -", filename
        self.filename = filename
        self.exec_code = self.__build__(os.path.splitext(filename))
        print "\t", self.exec_code
        
    def __build__(self, a):
        base, ext = a
        if ext == '.py':
            py_compile.compile(self.filename)
            print 'compiled python: ' + self.filename
            return ('%s %sc' %( PYTHON_PATH, self.filename))
        
        elif ext =='.lsp':
            
            # we mess with stdout/err here to suprress
            # the noisy output of clisp
            if subprocess.call([CLISP_PATH, '-c --silent', self.filename],stdout=subprocess.PIPE,stderr=subprocess.PIPE) == 0:
                print 'compiled lisp: ' + self.filename
                return CLISP_PATH + " " + self.filename
        else:
            return self.filename
        
    def run(self, history):
        process = subprocess.Popen(self.exec_code+" "+history,stdout=subprocess.PIPE,shell=True)
        return process.communicate()[0].strip().lower()
        
    def nicename(self, pad = True):
        if pad:
            return string.center(os.path.splitext(os.path.split(self.filename)[1])[0], 16)
        else:
            return os.path.splitext(os.path.split(self.filename)[1])[0]

def scoreRound(r1,r2):
    return RESULTS.get(r1[0]+r2[0],0)

def runRound(p1,p2,h1,h2):
    """Run both processes, and score the results"""
    r1 = p1.run(h1)
    r2 = p2.run(h2)
    (s1, L1), (s2, L2) = scoreRound(r1,r2), scoreRound(r2,r1)
    return (s1, L1+h1),  (s2, L2+h1)

def runGameWork( pair, rounds = 100 ):
    try:
        foo = runGame(rounds,*pair)
        return foo
    except Exception:
        print "FATAL ERROR IN CONTEST"
        return
        

def runGame(rounds,p1,p2):
    print p1.nicename(),"Vs.", p2.nicename(),"\t",
    sa, sd = 0, 0
    ha, hd = '', ''
    for a in range(0,rounds):
        (na, ha), (nd, hd) = runRound(p1,p2,ha,hd)
        sa += na
        sd += nd
    print "Score: ", (sa, sd)
    return sa, sd


def processPlayers(players):
    for i,p in enumerate(players):
        players[i] = warrior(p)
        
    print "\n"
    return players

def tourney(num_iters, num_rounds, players):
    total_scores={}
    
    for p in players:
        total_scores[p] = 0
    
    print "Running %s tournament iterations" % (num_iters)
    
    for i in range(1,num_iters+1):
        print "\nTournament", i, "\n", "-"*80
        scores={}
        
        for p in players:
            scores[p] = 0
        
        # create the round robin pairs
        pairs = list( itertools.combinations( players, 2) )
        pairs.extend( list( itertools.izip( players, players ) ) ) # adds the self pairs
        pool = multiprocessing.Pool(None) # None = use cpu_count processes
        results = pool.map(runGameWork, pairs)
        
        for (s1,s2),(p1,p2) in zip(results,pairs):
            if (p1 == p2):
                scores[p1] += (s1 + s2)/2
            else:
                scores[p1] += s1
                scores[p2] += s2

        players_sorted = sorted(scores,key=scores.get)
        
        print "\n"
        for p in players_sorted:
            print p.nicename(pad = False), scores[p]
        
        winner = max(scores, key=scores.get)
        print "\tWinner is %s" %(winner)
        total_scores[p] += 1

    print '-'*80, "\n", "Final Results:"
    
    players_sorted = sorted(total_scores,key=total_scores.get)
    
    for p in players_sorted:
        print p.nicename(pad = False), total_scores[p]
    
    winner = max(total_scores, key=total_scores.get)
    print "Final Winner is " + winner.nicename(pad = False) + "!"

if __name__ == "__main__":
    if(len(sys.argv) < 2):
        print """score - by dmckee (http://codegolf.stackexchange.com/users/78/dmckee)
Usage score [warriors dir] [[rounds] [games/round] [-i]]"""
    
    else:
        print "Finding warriors in " + sys.argv[1]
        players = [sys.argv[1]+exe for exe in os.listdir(sys.argv[1]) if os.access(sys.argv[1]+exe,os.X_OK)]
        players = processPlayers(players)

        num_iters = 1
        try:
            num_iters = int(sys.argv[2])
        except Exception:
            pass
            
        num_games = 100
        try:
            num_games = int(sys.argv[3])
        except Exception:
            pass
        
        if('-i' in sys.argv):
            #TODO - ADD A CLI/SHELL
            pass
        
        else:
            tourney(num_iters, num_games, players)
