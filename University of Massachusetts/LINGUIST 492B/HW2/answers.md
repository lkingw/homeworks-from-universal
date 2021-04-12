## LINGUIST 492
### HOMEWORK 2

<script type="text/javascript" src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=default"></script>

#### Part 2

* Try different values of $s$ and find one that works best. What is this value?
   >$s = 1$ is the best choice.

* What’s the best correlation you get?
   >5.1721

* What are two words where the predictions of the model and the human ratings are particularly divergent? Why do you think the model may have trouble with these cases?
   >The words are trisk and nung, that is mainly because there is no similar verbs in our dataset for the two words.

#### Part 3

* What’s the accuracy of the model on the forced choice task?
  >0.5854

* Which words does the model get wrong (list them all)? For each one, indicate what the model predicts and what it should have predicted instead.

  | Wug   |  Predicted  | Expected  | Wug | Predicted  | Expected  |
  | ----  |   ----   |  ----  |  ---- |   ----  |   ----   |
  |  b2z  | NULL->d  | 2->I   | kwid  | i->E    | NULL->Id |
  |  dr2s | NULL->t  | 2->5   | tip   | NULL->t | iX->EXt  |
  |  flI_ | NULL->d  | 2->I   | gud   | NULL    | NULL->Id |
  |  r2f  | NULL->t  | 2->5   | prik  | NULL->t | 1->5     |
  |  blIg | NULL->d  | IN->$t | bl1f  | NULL->t | NULL->d  |
  |  J1k  | NULL->t  | 1->U   | d1p   | NULL->t | NULL->d  |
  |  drIt | NULL     | NULL->Id | gEz | NULL->d | E->Q     |
  |  glIt | NULL     | NULL->Id | tES | NULL->t | NULL->Id |
  |  n5ld | NULL     | 5->E   |

* Examining the close neighbors of five of the wugs it gets wrong, which words seem to lead it astray? In other words, are there particular words the model ‘thinks’ are close neighbors, but it really shouldn’t count themas close for purposes of applying the past tense transformation?

  | Orth  |  Neighbor  | Distance | Expected |
  | ----  |  ----      | ----     | ----     |
  | bize  |  bite      | 1        | Yes      |
  | bize  |  size      | 1        | No       |
  | bize  |  bide      | 1        | Yes      |
  | drice  |  drive    | 1        | Yes      |
  | drice  |  price    | 1        | No       |
  | drice  |  dice     | 1        | No       |

  > From the above table, we can clearly find that the similarity of orth's front part is more important than the back part.

* Do you notice any general problems with the model? That is, is it failing to capture something general about how you think humans actually seem to perform this task.
 
  >The model not consider the phonetic similarity between wug and actual English verbs, that is very useful to detect wug's past tense.

#### Part 4

* Were you able to improve the model’s accuracy? What accuracy were you able to achieve?
  >Yes, we did it, we got a 0.7317 accuracy in our modified model.

* What did you try? Why did you think it might help?
  > (1) The edit distance is weighted by the length of comparing sentences. (2) The model additional take phonetic similarity into consideration for prediction.

* Why do you think it did(or didn’t, as appropriate) work?
  >The similarity should not influenced by the sentence length. In addition, the pronunciation of a word affects the transformation of its past tense.
