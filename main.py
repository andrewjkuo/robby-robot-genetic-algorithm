import numpy as np
import yaml
from tqdm import tqdm

from components import Robot, robot_from_dna

# import settings
with open("config.yaml", "r") as yamlfile:
    config = yaml.safe_load(yamlfile)

pop_size = config['pop_size']
num_breeders = config['num_breeders']
num_gen = config['num_generations']
iter_per_sim = config['iterations_per_simulation']
moves_per_iter = config['moves_per_iteration']

# initial population
pop = [Robot() for x in range(pop_size)]
results = []

# run evolution
for i in tqdm(range(num_gen)):
    scores = np.zeros(pop_size)

    for idx, rob in enumerate(pop):
        score = rob.simulate(iter_per_sim, moves_per_iter)
        scores[idx] = score

    results.append([scores.mean(),scores.max()])

    best_robot = pop[scores.argmax()]

    inds = np.argpartition(scores, -num_breeders)[-num_breeders:]
    old_pop = pop
    pop = []

    for idx in inds:
        pop.append(old_pop[idx])

    scores = scores[inds]

    norm_scores = (scores - scores.min()) ** 2
    norm_scores = norm_scores / norm_scores.sum()

    new_pop = []

    for child in range(pop_size):
        p1, p2 = np.random.choice(pop, p=norm_scores, size=2, replace=False)
        new_pop.append(Robot(p1.dna, p2.dna))

    pop = new_pop

best_robot.simulate(1,200,debug=True)
