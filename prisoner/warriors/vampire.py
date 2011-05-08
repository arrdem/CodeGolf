#!/usr/bin/env python

"""
Help Vampire, entry to 1P5 Iterated Prisoner's Dilemma,
by Josh Caswell.

1. Appear Cooperative 2. Acknowledge Chastisement 
3. Act contritely 4. Abuse charity 5. Continual affliction
"""

import sys
from os import urandom

LEN_ABASHMENT = 5

try:
    history = sys.argv[1]
except IndexError:
    print 'c'    # Appear cooperative
    sys.exit(0)

# Acknowledge chastisement
if history[0] in "RE":
    print 'c'
# Act contritely
elif set(history[:LEN_ABASHMENT]).intersection(set("RE")):
    print 'c'
# Abuse charity
elif history[0] == 'S':
    print 't'
# Continual affliction
else:
    print 't' if ord(urandom(1)) % 3 else 'c'

