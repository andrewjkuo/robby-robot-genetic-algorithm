import numpy as np
import yaml
from tqdm import tqdm

from components import Robot, robot_from_dna

# import settings
with open("config.yaml", "r") as yamlfile:
    config = yaml.safe_load(yamlfile)

pop_size = config['pop_size'] # number of robots per generation
num_breeders = config['num_breeders'] # number of robots who can mate in each generation
num_gen = config['num_generations'] # total number of generations
iter_per_sim = config['iterations_per_simulation'] # number of rubbish-collection simulations per robot
moves_per_iter = config['moves_per_iteration'] # number of moves robot can make per simulation

# initial population
pop = [Robot() for x in range(pop_size)]
results = []

# run evolution
for i in tqdm(range(num_gen)):
    scores = np.zeros(pop_size)

    # iterate through all robots
    for idx, rob in enumerate(pop):
    # run rubbish collection simulation and calculate fitness
        score = rob.simulate(iter_per_sim, moves_per_iter)
        scores[idx] = score

    results.append([scores.mean(),scores.max()]) # save mean and max scores for each generation

    best_robot = pop[scores.argmax()] # save the best robot

    # limit robots who are able to mate to top num_breeders
    inds = np.argpartition(scores, -num_breeders)[-num_breeders:] # get indices of top robots based on fitness
    subpop = []
    for idx in inds:
        subpop.append(pop[idx])
    scores = scores[inds]

    # square and normalise fitness scores
    norm_scores = (scores - scores.min()) ** 2
    norm_scores = norm_scores / norm_scores.sum()

    # create next generation of robots
    new_pop = []
    for child in range(pop_size):
        p1, p2 = np.random.choice(subpop, p=norm_scores, size=2, replace=False)
        new_pop.append(Robot(p1.dna, p2.dna))

    pop = new_pop

best_robot.simulate(1,200,debug=True)
