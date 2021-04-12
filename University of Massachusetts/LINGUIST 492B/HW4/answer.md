Q1. What is probability of ‘time flies quickly’? How many tag sequences are contributing to this probability (that is, how many non-zero ways of tagging ‘time flies quickly’ are there according to this HMM)?

> The sentence's probability is 0.004276, there are six tag sequences contribute to this probability.

Q2. What is the best tag sequence for ‘time flies quickly’? What meaning does this tag sequence correspond to?

> The best tag sequence is ‘N V R’, it is means the best tagging result for ‘time flies quickly’ is 'Noun Verb and Adverb'

Q3. What’s the probability of ‘quickly time flies’? What parameters would you need to change to make ‘quickly time flies’ more likely than ‘time flies quickly’ (don’t actually change the parameters in your code)? Be specific!

> 0.0004721 is the probability of ‘quickly time flies’, our solution is increase the weight value of transfer rules '# -> R', 'R -> N', 'N -> V' and 'V -> #' in transition matrix, and then decrease the other weight values.

Q4. Modify matrix B to add a new word ‘swat’ to the lexicon. Assume that ‘swat’ can only be a verb, and be sure your matrix defines proper conditional probability distributions. Set your probabilities so that the most likely tag sequence for ‘swat flies quickly’ is ‘V N R’. (hint: you will need to change probabilities in multiple rows). Show this matrix in your question write-up, and also encode it into the script as a dictionary ‘B2’.

> Our new emission matrix B2 is
> | | swat   | time | flies  | quickly | # |
> |----|---- |----  |---- |----  |----  |----|
> | N  | 0.0 |  0.3 |0.68 | 0.02 | 0.0 |
> | V  | 0.7 |  0.1 |0.20 | 0.0  | 0.0 |
> | R  | 0.0 | 0.01 |0.02 | 0.98 | 0.0 |
> | #  | 0.0 |  0.0 |0.0  | 0.0  | 1.0 |


Q5. In your new HMM from Q4, ‘V N R’ is the most likely tag sequence for ‘swat flies quickly’. How is this probability different from the probability of the same tag sequence for ‘time flies quickly’ (i.e. what parameters are relevant to this comparison)? Which is higher? Explain why the answer to this question determines the answer to the following question:
- Which is higher P(‘N V’, ‘flies time’) or P(‘N V’, ‘flies swat’)

> 1. Related to the result of under the condition of V, which word's (time or swat) probability is higher.
> 2. ‘time flies quickly’ is higher
> 3. For the comparison between P(‘N V’, ‘flies time’) or P(‘N V’, ‘flies swat’), it is also only related the result of under the condition of V, which word's (time or swat) probability is higher.
