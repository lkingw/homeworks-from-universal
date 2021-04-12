# the A and B matrices as dictionaries
A = {'N': {'N': 0.54, 'V': 0.23, 'R': 0.08, '#': 0.15}, 'V': {'N': 0.62, 'V': 0.17, 'R': 0.11, '#': 0.10},
     'R': {'N': 0.17, 'V': 0.68, 'R': 0.10, '#': 0.05}, '#': {'N': 0.7, 'V': 0.2, 'R': 0.1, '#': 0.0}}
B = {'N': {'time': 0.98, 'flies': 0.015, 'quickly': 0.005, '#': 0.0}, 'V': {'time': 0.33, 'flies': 0.64, 'quickly': 0.03, '#': 0.0},
     'R': {'time': 0.01, 'flies': 0.01, 'quickly': 0.98, '#': 0.0}, '#': {'time': 0.0, 'flies': 0.0, 'quickly': 0.0, '#': 1.0}}
# Define a new emission matrix B2 for Question 4
# V N R swat flies quickly
B2 = {
    'N': {'swat': 0.0, 'time': 0.3,  'flies': 0.68, 'quickly': 0.02, '#': 0.0}, 
    'V': {'swat': 0.7, 'time': 0.1,  'flies': 0.20, 'quickly': 0.00, '#': 0.0},
    'R': {'swat': 0.0, 'time': 0.01,  'flies': 0.02, 'quickly': 0.98, '#': 0.0}, 
    '#': {'swat': 0.0, 'time': 0.00,  'flies': 0.00, 'quickly': 0.00, '#': 1.0}
}
tagnum = {"N": 0, "V": 1, "R": 2, "#": 3}  # gives index for a given tag
# two data structures you may find useful for mapping between tags and their (arbitrary) indices
numtag = ['N', 'V', 'R', '#']  # gives tag for a given index


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
        v.append({})
        newpath = {}
        for j in range(len(numtag)):
            tag = numtag[j]
            # find the  maximum of the current forward probability for the tag j
            (prob, state) = max((v[t-1][y0] * A[y0][tag]
                                 * B[tag][ws[t]], y0) for y0 in tagnum)
            v[t][tag] = prob
            # add state to the path table
            newpath[tag] = path[state] + [tag]
        path = newpath
    n = t
    # find the best taging result for sentence
    (prob, state) = max((v[n][y], y) for y in tagnum)
    return (prob, path[state])


### MAIN CODE GOES HERE ###
seq1 = ('time', 'flies', 'quickly')
seq2 = ('quickly', 'time', 'flies')
print("calculating forward probability of", seq1, ":\n", forward(seq1, A, B))
print("calculating most likely tags for", seq1, ":\n", viterbi(seq1, A, B))
seq3 = ('swat', 'flies', 'quickly')
print("calculating forward probability of", seq3, ":\n", forward(seq3, A, B2))
#print("calculating most likely tags for", seq3, ":\n", viterbi(seq3, A, B2))
print("calculating forward probability of", seq1, ":\n", forward(seq1, A, B2))
