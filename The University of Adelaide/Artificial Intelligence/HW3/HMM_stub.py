# the A and B matrices as dictionaries

A = {
     'NNP': {'#': 0.2767, 'NNP': 0.3777, 'MD': 0.0008, 'VB': 0.0322, 'JJ': 0.0366, 'NN': 0.0096, 'RB': 0.0068, 'DT': 0.1147}, 
     'MD': {'#': 0.0006, 'NNP': 0.0110, 'MD': 0.0002, 'VB': 0.0005, 'JJ': 0.0004, 'NN': 0.0176, 'RB': 0.0102, 'DT': 0.0021},
     'VB': {'#': 0.0031, 'NNP': 0.0009, 'MD': 0.7968, 'VB': 0.0050, 'JJ': 0.0001, 'NN': 0.0014, 'RB': 0.1011, 'DT': 0.0002},
     'JJ': {'#': 0.0453, 'NNP': 0.0084, 'MD': 0.0005, 'VB': 0.0837, 'JJ': 0.0733, 'NN': 0.0086, 'RB': 0.1012, 'DT': 0.2157},
     'NN': {'#': 0.0449, 'NNP': 0.0584, 'MD': 0.0008, 'VB': 0.0615, 'JJ': 0.4509, 'NN': 0.1216, 'RB': 0.0120, 'DT': 0.4744},
     'RB': {'#': 0.0510, 'NNP': 0.0090, 'MD': 0.1698, 'VB': 0.0514, 'JJ': 0.0036, 'NN': 0.0177, 'RB': 0.0728, 'DT': 0.0102},
     'DT': {'#': 0.2026, 'NNP': 0.0025, 'MD': 0.0041, 'VB': 0.2231, 'JJ': 0.0036, 'NN': 0.0068, 'RB': 0.0479, 'DT': 0.0017},
    }

A2 = {
     '#': {'NNP': 0.2767, 'MD': 0.0006, 'VB': 0.0031, 'JJ': 0.0453, 'NN': 0.0449, 'RB': 0.0510, 'DT': 0.2026, '#': 0}, 
     'NNP': {'NNP': 0.3777, 'MD': 0.0110, 'VB': 0.0009, 'JJ': 0.0084, 'NN': 0.0584, 'RB': 0.0090, 'DT': 0.0025, '#': 0}, 
     'MD': {'NNP': 0.0008, 'MD': 0.0002, 'VB': 0.7968, 'JJ': 0.0005, 'NN': 0.0008, 'RB': 0.1698, 'DT': 0.0041, '#': 0},
     'VB': {'NNP': 0.0322, 'MD': 0.0005, 'VB': 0.0050, 'JJ': 0.0837, 'NN': 0.0615, 'RB': 0.0514, 'DT': 0.2231, '#': 0},
     'JJ': {'NNP': 0.0366, 'MD': 0.0004, 'VB': 0.0001, 'JJ': 0.0733, 'NN': 0.4509, 'RB': 0.0036, 'DT': 0.0036, '#': 0},
     'NN': {'NNP': 0.0096, 'MD': 0.0176, 'VB': 0.0014, 'JJ': 0.0086, 'NN': 0.1216, 'RB': 0.0177, 'DT': 0.0068, '#': 0},
     'RB': {'NNP': 0.0068, 'MD': 0.0102, 'VB': 0.1011, 'JJ': 0.1012, 'NN': 0.0120, 'RB': 0.0728, 'DT': 0.0479, '#': 0},
     'DT': {'NNP': 0.1147, 'MD': 0.0021, 'VB': 0.0002, 'JJ': 0.2157, 'NN': 0.4744, 'RB': 0.0102, 'DT': 0.0017, '#': 0},
    }

B = {
    'NNP': {'Janet': 0.0000032, 'will': 0,  'back': 0, 'the': 0.000048, 'bill': 0, '#':0}, 
    'MD': {'Janet': 0, 'will': 0.308431,  'back': 0, 'the': 0, 'bill': 0, '#':0}, 
    'VB': {'Janet': 0, 'will': 0.000028,  'back': 0.000672, 'the': 0, 'bill': 0.000028, '#':0},  
    'JJ': {'Janet': 0, 'will': 0,  'back': 0.000340, 'the': 0, 'bill': 0, '#':0}, 
    'NN': {'Janet': 0, 'will': 0.000200,  'back': 0.000223, 'the': 0, 'bill': 0.002337, '#':0}, 
    'RB': {'Janet': 0, 'will': 0,  'back': 0.010446, 'the': 0, 'bill': 0, '#':0}, 
    'DT': {'Janet': 0, 'will': 0,  'back': 0, 'the': 0.506099, 'bill': 0, '#':0}, 
    '#': {'Janet': 0, 'will': 0,  'back': 0, 'the': 0, 'bill': 0, '#': 1.0}, 
    }

tagnum = {"NNP": 0, "MD": 1, "VB": 2, "JJ": 3, 'NN': 4, 'RB': 5, 'DT': 6, '#': 7}  # gives index for a given tag
tagnum2 = {"NNP": 0, "MD": 1, "VB": 2, "JJ": 3, 'NN': 4, 'RB': 5, 'DT': 6}  # gives index for a given tag
# two data structures you may find useful for mapping between tags and their (arbitrary) indices
numtag = list(tagnum.keys())  # gives tag for a given index


def print_table(table, words, ef='%.4f', colwidth=12):
    tags = A.keys()
    print(''.ljust(colwidth), end='')
    for w in words:
        print(str(w).ljust(colwidth), end='')
    print()
    for n in range(len(A.keys())):
        print(str(numtag[n]).ljust(colwidth), end='')
        for t in range(len(words)):
            out = str(table[t][n])
            if type(table[t][n]) == tuple:
                form = ef+",%s"
                out = form % (table[t][n][0], table[t][n][1])
            elif type(table[t][n]) == float:
                out = str(ef % table[t][n])
            print(out.ljust(colwidth), end='')
        print()


def forward(ws, A, B):

    # prepend and postpend ‘#’ to test_sequence
    ws = ['#'] + list(ws) + ['#'] 
    # create table to store results
    alpha = [[0 for i in range(len(A))] for j in range(len(ws))]
    # initialize the table 
    alpha[0][len(A) - 1] = 1
    for t in range(1, len(ws)):
        for j in range(len(numtag)):
            tag = numtag[j]
            # compute the current forward probability for the tag j
            sum = 0
            for k in range(len(A)):
                val = list(A[tag].values())[k] * alpha[t - 1][k]
                sum += val
            alpha[t][j] = sum * B[tag][ws[t]]
            
    print_table(alpha, ws)
    return alpha[len(ws) - 1][len(A) - 1]


def viterbi(ws, A, B):

    # prepend and postpend ‘#’ to test_sequence
    ws = ['#'] + list(ws) + ['#'] 
    # create table to store results
    path = {}
    v = [{}]
    # initialize the table 
    for y in tagnum:
        if y == '#':
            v[0][y] = 1 
        else:
            v[0][y] = 0
        path[y] = [y]

    for t in range(1, len(ws)):

        print(t, ws[t])
        if ws[t] == '#': 
            break
        v.append({})
        newpath = {}
        for j in range(len(numtag)):
            tag = numtag[j]
            #print(t, j, tag)
            # find the  maximum of the current forward probability for the tag j
            (prob, state) = max((v[t-1][y0] * A[y0][tag] * B[tag][ws[t]], y0) for y0 in tagnum)
            if t == 4 and j == 6:
                for y0 in tagnum:
                    print(tag, v[t-1][y0] * A[y0][tag] * B[tag][ws[t]])
            v[t][tag] = prob
            # add state to the path table
            newpath[tag] = path[state] + [tag]
        path = newpath
    n = t - 1
    print(v)
    # find the best taging result for sentence
    (prob, state) = max((v[n][y], y) for y in tagnum)
    return (prob, path[state])


### MAIN CODE GOES HERE ###
seq1 = ('Janet', 'will', 'back', 'the', 'bill')
#print("calculating forward probability of", seq1, ":\n", forward(seq1, A, B))
print("calculating most likely tags for", seq1, ":\n", viterbi(seq1, A2, B))
