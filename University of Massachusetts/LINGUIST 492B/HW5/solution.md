## Solution for assignment 5

1. Why does the stub generate so many long sentences? Specifically, what grammar rule is responsible and why? What is special about this rule?

    > The rules (NP -> NP PP) and (PP -> Prep NP) will continuous extent the sentence with high probability.

2. The grammar allows multiple adjectives, as in ”the fine perplexed pickle.” Why do your program’s sentences do this so rarely?

    > The symbol 'Noun' can be converted to new rule (Noun -> Adj Noun) and serveral noun term, however, the probability of rule (Noun -> Adj Noun) is selected is only 1/6.

3. Which numbers must you modify to fix the problems in (1) and (2) above, making the sentences shorter and the adjectives more frequent? (Check your answer by running your new generator!)

    > We increase the weight of rule (NP -> Det Noun) that will make the sentences shorter. We also increase the weight of rule (Noun -> Adj Noun) will make the adjectives more frequent.

4. What other numeric adjustments can you make to the grammar in order to favor more natural sets of sentences? Experiment. Discuss at least two adjustments you made -why are they necessary and what is their effect?

    > We increase the weight of declarative sentence (S .), because it is more common used in daily life, and also increase the weights of determiners 'the' and 'a', which are more frequent in natural sentences.

    #### Briefly discuss your modifications to the grammar. 

    > a. Add new word 'Sally' as a Noun term.
    > b. Add new word 'and' as a coujunction term and add a new grammar rule (NP -> NP Conj NP).
    > c. Add new word 'signed' as a Verb term.
    > d. Add new word 'thought' as a Verb term and add a new 'that' as Conjunction term.
    > e. Assign the word 'that' to determiner class and add rule (S -> S VP) to the grammar.
    > f. Add words 'proposal' and 'desk' as Noun terms to grammar.

    #### Generate about 5 more random sentences, in bracketed format.

    * (ROOT (S (S (NP (Det the) (Noun (Adj fine) (Noun chief of staff))) (VP (Verb ate) (NP (Noun chief of staff)))) (VP (Verb thought) (NP (Noun Sally)))) .)
    * (ROOT (S (S (NP (NP (Det a) (Noun Sally)) (Conj that) (NP (Noun president))) (VP (Verb ate) (NP (Det the) (Noun desk)))) (VP (Verb sighed) (NP (Noun desk)))) !)
    * (ROOT is it true that (S (S (S (S (NP (Det that) (Noun (Adj fine) (Noun Sally))) (VP (Verb wanted) (NP (NP (Det the) (Noun Sally)) (PP (Prep in) (NP (NP (Det that) (Noun president)) (PP (Prep on) (NP (NP (NP (Det the) (Noun president)) (PP (Prep with) (NP (Det every) (Noun (Adj perplexed) (Noun floor))))) (Conj that) (NP (Det the) (Noun Sally))))))))) (VP (Verb pickled) (NP (Det that) (Noun sandwich)))) (VP (Verb sighed) (NP (Noun sandwich)))) (VP (Verb wanted) (NP (Noun pickle)))) ?)
    * (ROOT (S (S (S (NP (Noun (Adj fine) (Noun Sally))) (VP (Verb sighed) (NP (Det the) (Noun chief of staff)))) (VP (Verb perplexed) (NP (NP (Noun Sally)) (Conj that) (NP (Noun (Adj fine) (Noun pickle)))))) (VP (Verb ate) (NP (Det that) (Noun pickle)))) .)
    * (ROOT (S (S (S (S (NP (NP (Det that) (Noun (Adj fine) (Noun Sally))) (Conj that) (NP (Noun Sally))) (VP (Verb sighed) (NP (Noun (Adj delicious) (Noun Sally))))) (VP (Verb pickled) (NP (NP (Noun pickle)) (Conj that) (NP (Det the) (Noun president))))) (VP (Verb ate) (NP (Det the) (Noun president)))) (VP (Verb sighed) (NP (NP (Noun proposal)) (Conj that) (NP (Det a) (Noun Sally))))) .)

5. One derivation is as follows; what is the other(give your answer as a bracketed string or draw a tree)?

    <img src="./syntax tree.png" width="80%">