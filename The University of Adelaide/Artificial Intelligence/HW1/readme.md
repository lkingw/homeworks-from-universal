* For the ordinary minimax-based AI, just run 
<code>python tictac.py <your-board> visited.txt </code>

* For the AI based on minimax with prune, run
<code>python tictac.py <your-board> visited.txt prune</code>

* For the AI equipped with early termination function (i.e. a heuristic function), run
<code>python tictac.py <your-board> visited.txt prune <max-step></code>
Note that the max step must be a number in range 0 to 9.

* As for the question 1.3, you can write
  
> In the first two cases, we can see the try number of our algorithm got big decreased after the minimax search tree pruned as well as the the search early terminated benifited by the heuristic function. In the third case, because we already consider the emplty board condition, our machine can randomly do the next move, otherwise the algorithm will be stucked in an endless loop.
