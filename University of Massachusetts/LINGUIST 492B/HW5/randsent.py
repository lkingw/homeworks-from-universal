import sys
import math
import random
from collections import defaultdict
from nltk.tree import Tree
tree_string = ''

# convertor for symbol to id numbers
CONVERTER = {
        'S': 0, 'NP': 1, 'VP': 2, 'PP': 3, 'Det': 4, 'Prep': 5, 
        'Adj': 6, 'Conj': 7, 'Noun': 8, 'Verb': 9
    }

# convertor for id numbers to corresponding symbol
ANTI_CONVERTER = {
        '0': 'S', '1': 'NP', '2': 'VP', '3': 'PP', '4': 'Det', '5': 'Prep', 
        '6': 'Adj', '7': 'Conj', '8': 'Noun', '9': 'Verb'
    }


def readGrammarFile(fn):

    f = open(fn, "r")
    rules = defaultdict(lambda:[])

    for line in f:
        # strip out comments and whitespace
        line = line.split('#')[0].strip() 
        if line == '': continue
        fields = line.split()
        weight = int(fields[0])
        lhs = fields[1]
        # a list of RHS symbols
        rhs = fields[2:]
        # adds a list of the list of RHS symbols
        rules[lhs].extend( [{'key':rhs, 'w':weight}] )  

    return rules


def genNonTerminal_advanced(nonterm, rules):

    # grab a random RHS for this nonterminal from the grammar
    global tree_string
    tot_weight = 0
    for rule in rules[nonterm]: tot_weight += rule['w']
    index = random.randint(0, tot_weight)

    # select a child by their weights
    acc_weight = 0
    for rule in rules[nonterm]:
        acc_weight += rule['w']
        if acc_weight >= index:
            selected = rule
            break
    
    result = ""

    # construct the tree string
    if nonterm == 'ROOT':
        tree_string = '(ROOT ' + ' '.join(selected['key']) + ')'
    else:
        tree_string = tree_string.replace(nonterm, '(' + str(CONVERTER[nonterm]) + ' ' 
            + ' '.join(selected['key']) + ')', 1)

    # go through each symbol in the chosen RHS
    for symbol in selected['key']:
        if not symbol in rules:
            # this is a terminal symbol so write it out
            result += symbol + " "
        else:
            # this is a non-terminal symbol so recurse
            result += genNonTerminal_advanced(symbol, rules)

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

for i in range(n):
    if T: 
        string = genNonTerminal_advanced("ROOT", grammar)

        # convert symbol ids to correponding symbols
        for index in ANTI_CONVERTER:
            word = ANTI_CONVERTER[index]
            tree_string = tree_string.replace(index, word)
        
        print (tree_string)
        t = Tree.fromstring(tree_string)
        t.draw()
    else: 
        string = genNonTerminal_advanced("ROOT", grammar)
        print (string)


