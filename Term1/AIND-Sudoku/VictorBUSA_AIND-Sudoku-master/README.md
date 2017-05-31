# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: 
Let's say we have to Sudoku Grid :

  1    237    4   | 2357   9    257  |  27    6     8
  9     5     6   |  27    1     8   |  27    3     4
  23   237    8   |  4     37    6   |  9     5     1
------------------+------------------+------------------
  5     1    2379 | 237   347   279  |  34    8     6
  8     37   379  |  6    347   579  | 345    1     2
  6     4     23  |12 35   8    125  |  35    9     7
------------------+------------------+------------------
  7     8     1   |  9     2     3   |  6     4     5
  4     9     5   |  17    6     17  |  8     2     3
  23    6     23  |  8     5     4   |  1     7     9

we can see that we can either put a 2 or a 3 in both F3 and I3.
So if we choose to put 2 in F3, as 2 is already in the column (in a unit)
we don't have the choice but to put 3 in I3 and hence as 2 and 3 are placed
in the column we know there will not be in D3 or E3. By a symmetric argument,
if we put a 3 in I3, we won't have the choice but to but 2 in F3 and hence
again, as 2 and 3 are already placed in the columns we cannot place in the
column (unit) we know we cannot place 2 or 3 in D3 or E3.

So we use this technique for each unit (column, row, square) to reduce the
dimension of the problem to solve. we applied this technique at each recursive
step allowing us to reduce the space of the possible path to take in the tree.
So in a nutshell, it allows us to trim the tree and hence avoiding DFS to search
in a path we already know it won't get us anywhere.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: Seemingly, we constraint the problem to satisfy one more condition : each
number from 1 to 9 must appear only once on each major diagonals. So it reduces
the dimension of the problem and allow the algorithm to eliminate number we can
put in each diagonal before applying DFS. Hence again, Constraint propagation
allows to trim the tree at each recursive step of DFS, avoiding unecessary path
to be tried. So Constraint Propagation allows use to trim a tree here and by
avoiding to use uncessary path the algorithm converges faster.

Note : 
	- Naked Twins is not necessary to solve a Grid Sudoku but it surely boosts
	the speed of the algorithm.
	- Diagonal Sudoku is necessary because it constraints the final solution of
	the problem. If we didn't use this constraint, we would still have find a
	solution to our Sudoku Grid, but this solution don't necessarily respect the
	diagonal constraint.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.