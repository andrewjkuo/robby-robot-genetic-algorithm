# robby-robot-genetic-algorithm
Implementation of the Robby Robot genetic algorithm described in Melanie Mitchell's "Complexity: A Guided Tour"

### Changes
This Implementation differs slightly from the one described in Mitchell's book in the following ways:
* while mating probabilities are still linked to fitness, the evolutionary process is accelerated by dropping the least fit individuals from each generation altogether
* for similar reasons (faster convergence) the fitness scores of the population are squared before converting to probabilities
* rather than creating child dna from the two parents with a random splice and join, each individual gene is chosen randomly from the parents

### To Do
* documentation (including demo notebook with visualisation)
* save results and best model from experiments
