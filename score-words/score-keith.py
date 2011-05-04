#!/usr/bin/env python
from itertools import permutations
import time

S={'A':0,'E':0,'I':0,'O':0,'U':0,
   'L':1,'T':1,'N':1,
   'R':2,'D':2,'S':2,
   'G':3,'B':3,'M':3,
   'C':4,'H':4,'P':4,
   'F':5,'W':5,'V':5,
   'Y':6,'K':6,'J':6,
   'Q':7,'X':7,'Z':7,
   }

def best_word(min, s):
    global score_to_words
    best_score = 0
    best_word = ''
    for i in xrange(min, 100):
        for w in score_to_words[i]:
            score = (-2*len(w)+2*(w.count('A')+w.count('E')+w.count('I')+w.count('O')+w.count('U')) +
                      3*w.count(s[0])+4*w.count(s[1])+5*w.count(s[2])+6*w.count(s[3])+7*w.count(s[4])+
                      8*w.count(s[5])+9*w.count(s[6]))
            if score > best_score:
                best_score = score
                best_word = w
    return (best_score, best_word)

def load_words():
    global score_to_words
    wlist = [l.strip().upper() for l in open('/usr/share/dict/words') if l[0].lower() == l[0]]
    score_to_words = [[] for i in xrange(100)]
    for w in wlist: score_to_words[sum(S[c] for c in w)].append(w)
    for i in xrange(100):
        if score_to_words[i]: print i, len(score_to_words[i])

def find_best_words():
    load_words()
    best = 0
    bestwords = ()
    for c1 in permutations('LTN'):
        for c2 in permutations('RDS'):
            for c3 in permutations('GBM'):
                print time.ctime(),c1,c2,c3
                for c4 in permutations('CHP'):
                    for c5 in permutations('FWV'):
                        for c6 in permutations('YJK'):
                            for c7 in permutations('QZX'):
                                sets = zip(c1, c2, c3, c4, c5, c6, c7)
                                (s1, w1) = best_word((best + 3) / 3, sets[0])
                                (s2, w2) = best_word((best - s1 + 2) / 2, sets[1])
                                (s3, w3) = best_word(best - s1 - s2 + 1, sets[2])
                                score = s1 + s2 + s3
                                if score > best:
                                    best = score
                                    bestwords = (w1, w2, w3)
                                    print score, w1, w2, w3
    return bestwords, best


if __name__ == '__main__':
    import timeit
    print timeit.timeit('print find_best_words()', 'from __main__ import find_best_words', number=1)
