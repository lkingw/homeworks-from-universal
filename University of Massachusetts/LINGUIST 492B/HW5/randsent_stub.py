import sys
import math
import random
from collections import defaultdict
from nltk.tree import Tree

def readGrammarFile(fn):

    f = open(fn, "r")
    rules = defaultdict(lambda:[])

    for line in f:
        line = line.split('#')[0].strip()  # strip out comments and whitespace
        if line == '': continue
        fields = line.split()
        lhs = fields[1]
        rhs = fields[2:]            # a list of RHS symbols
        rules[lhs].extend( [rhs] )  # adds a list of the list of RHS symbols

    return rules

def genNonTerminal(nonterm, rules):

    # grab a random RHS for this nonterminal from the grammar
    numrules = len(rules[nonterm])
    rule = rules[nonterm][ random.randrange(0,numrules) ]

    result = ""

    # go through each symbol in the chosen RHS
    for symbol in rule:
        #print(symbol, list(rules.keys()))
        if not symbol in rules:
            # this is a terminal symbol so write it out
            result += symbol + " "
        else:
            # this is a non-terminal symbol so recurse
            result += genNonTerminal(symbol, rules)

    return result

T = False   # Should trees be drawn?

if len(sys.argv) < 2:
    print ("Usage: python randsent.py <grammar-file> [number-of-sentences]")
    exit(0)

file = sys.argv[1]
if len(sys.argv) >= 3:
    if sys.argv[1] == '-t': 
        file = sys.argv[2]
        T =True
        if len(sys.argv) >= 4: n = int(sys.argv[3])
        else: n = 1
    else: n = int(sys.argv[2])
else:
    n = 1

grammar = readGrammarFile(file)
print (grammar)
for i in range(n):
    if T: 
        bracketed = "( ROOT " + genNonTerminal("ROOT", grammar) + " )"
        print (bracketed)
        t = Tree.fromstring(bracketed)
        t.draw()
    else: print (genNonTerminal("ROOT", grammar))


