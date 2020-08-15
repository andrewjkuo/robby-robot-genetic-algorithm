# robby-robot-genetic-algorithm
Implementation of the Robby Robot genetic algorithm described in Melanie Mitchell's "Complexity: A Guided Tour"

### Approach
A robot named Robby lives in a two-dimensional grid world full of rubbish and surrounded by 4 walls. The aim of this project is to evolve an optimal control strategy for Robby that will allow him to pick up rubbish efficiently and not crash into walls. Robby can only see the four squares NESW of himself as well as the square he is in. There are 3 options for each square; it can be empty, have rubbish in it or be a wall. Therefore there are 3⁵ = 243 different scenarios Robby can be in. Robby can perform 7 different actions; move NESW, move randomly, pickup rubbish or stay still. Robby's control strategy can therefore be encoded as a "DNA" string of 243 digits between 0 and 6 (corresponding to the action Robby should take in each of the 243 possible situations).

To solve this problem, you create a first generation of Robbys initialised to random DNA strings. You then simulate letting these robots run around in randomly assigned grid worlds and see how they perform. A robot's fitness is a function of how many pieces of rubbish it picked up in n moves and how many times it crashed into a wall. The robots then "mate" with probabilities linked to their fitness (i.e. robots that picked up lots of rubbish are more likely to mate) and a new generation is created. Iterate through this process until the robots are incredible rubbish-collecting geniuses.

### Changes
This Implementation differs slightly from the one described in Mitchell's book in the following ways:
* while mating probabilities are still linked to fitness, the evolutionary process is accelerated by dropping the least fit individuals from each generation altogether
* for similar reasons (faster convergence) the fitness scores of the population are squared before converting to probabilities
* rather than creating child dna from the two parents with a random splice and join, each individual gene is chosen randomly from the parents

### To Do
* documentation (including demo notebook with visualisation)
* save results and best model from experiments
