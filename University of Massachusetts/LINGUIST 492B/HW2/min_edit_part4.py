import sys
import re

# this regexp will match any vowel symbol
V = r"[0123456789$@EI{VQUiu#cq]"

def ins_cost(c):
    return 1

def del_cost(c):
    return 1

def sub_cost(c, d):
    if c == d: return 0
    else: return 2

# PART4 compute the additional similarity at sound
def pheontic_sim(source, target):

    # remove the vowel symbol
    p_source = re.sub(V, "", source)
    p_target = re.sub(V, "", target)
    if p_source == p_target:
        #print(p_source)
        return 1
    else: return 0

def min_edit(source='', target='', verbose=False):
    m = len(source)
    n = len(target)

    dist = [[0]*(n+1) for i in range(m+1)]

    ## PART 1 - fill in the values of dist using the min_edit algorithm here##

    for i in range(m + 1):
        for j in range(n + 1):

            if i == 0:
                dist[i][j] = j    # Min. operations = j
 
            elif j == 0:
                dist[i][j] = i    # Min. operations = i
 
            elif source[i-1] == target[j-1]:
                dist[i][j] = dist[i-1][j-1]
 
            else:

                # add special cost for each operation portation
                delPortion = dist[i][j-1] + del_cost(source[i-1])
                insPortion = dist[i-1][j] + ins_cost(source[i-1])
                subPortion = dist[i-1][j-1] + sub_cost(source[i-1], target[j-1])
                
                dist[i][j] = 1 + min(delPortion, insPortion, subPortion)

    ## if verbose is set to True, will print out the min_edit table
    if verbose:
        #print the matrix
        for i in range(m+1)[::-1]:
            if i > 0: print(source[i-1], end='')
            else: print('#', end='')
            for j in range(n+1):
                print('\t' + str(dist[i][j]), end='')
            print()
        print('#\t#\t' + '\t'.join(list(target)) + '\n')

    # returns the cost for the full transformation
    # PART4 weighted the cost with the sentence length
    return dist[m][n] / max(n, m)

def main():
    s = sys.argv[1]
    t = sys.argv[2]
    print(min_edit(source=s, target=t, verbose=True))

if __name__ == "__main__":
    main()
