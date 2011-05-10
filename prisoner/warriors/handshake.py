#!/usr/bin/python
#tcctcttttt
import sys
import random

def main():
    if len(sys.argv) == 1:
        hist = ""
    else:
        hist = sys.argv[1]
    if len(hist) <= len(TAG) and hist == TAGMATCH[len(TAG) - len(hist):]:
        print TAG[len(TAG) - len(hist) - 1]
        return
    if hist[-len(TAG):] == TAGMATCH:
        print 'c'
        return
    print "t"

def getTag():
    global TAG
    filename = sys.argv[0]
    filename = filename.replace(".pyc", ".py")
    f = open(filename, 'r')
    code = f.read().split('\n')
    f.close()
    if len(code[1]) == 0 or code[1][0] != '#':
        random.seed()
        newtag = 't' * 10
        cs = 0
        while cs < 3:
            pos = random.randint(0, 8)
            if newtag[pos] == 't':
                newtag = newtag[:pos] + 'c' + newtag[pos+1:]
                cs += 1
        code.insert(1, '#%s' % newtag)
        f = open(filename, 'w')
        f.write('\n'.join(code))
        f.close()
        TAG = newtag
    else:
        TAG = code[1][1:]
    global TAGMATCH
    TAGMATCH = TAG.replace('c', 'K').replace('t', 'E')

if __name__ == "__main__":
    getTag()
    main()
