import numpy as np
import yaml

# import settings
with open("config.yaml", "r") as yamlfile:
    config = yaml.safe_load(yamlfile)

rubbish_prob = config['rubbish_probability']
grid_size = config['grid_size']
wall_penalty = config['wall_penalty']
no_rub_penalty = config['no_rub_penalty']
rubbish_score = config['rubbish_score']
mutation_rate = config['mutation_rate']

# generate dict to lookup gene index from situation string
con = ['w','o','x'] #wall, empty, rubbish
situ_dict = dict()
count = 0

for up in con:
    for right in con:
        for down in con:
            for left in con:
                for pos in con:
                    situ_dict[up+right+down+left+pos] = count
                    count += 1

class Environment:
    def __init__(self, p=rubbish_prob, g_size=grid_size):
        self.p = p
        self.g_size = g_size

        # initialise grid
        self.grid = np.random.choice(['o','x'], size=(self.g_size+2,self.g_size+2), p=(1 - self.p, self.p))
        self.grid[:,[0,self.g_size+1]] = 'w'
        self.grid[[0,self.g_size+1], :] = 'w'

    def show_grid(self):
        print(self.grid)

    def remove_rubbish(self,i,j):
        if self.grid[i,j] == 'o':
            return False
        else:
            self.grid[i,j] = 'o'
            return True

    def get_pos_string(self,i,j):
        return self.grid[i-1,j] + self.grid[i,j+1] + self.grid[i+1,j] + self.grid[i,j-1] + self.grid[i,j]

class Robot:
    def __init__(self, p1_dna=None, p2_dna=None, m_rate=mutation_rate, w_pen=wall_penalty, nr_pen=no_rub_penalty, r_score=rubbish_score):
        self.m_rate = m_rate
        self.wall_penalty = w_pen
        self.no_rub_penalty = nr_pen
        self.rubbish_score = r_score
        self.p1_dna = p1_dna
        self.p2_dna = p2_dna

        self.get_dna()

    def get_dna(self):
        if self.p1_dna is None:
            self.dna = ''.join([str(x) for x in np.random.randint(7,size=243)])
        else:
            self.dna = self.mix_dna()

    def mix_dna(self):
        mix_dna = ''.join([np.random.choice([self.p1_dna,self.p2_dna])[i] for i in range(243)])

        #add mutations
        for i in range(243):
            if np.random.rand() > 1 - self.m_rate:
                mix_dna = mix_dna[:i] + str(np.random.randint(7)) + mix_dna[i+1:]

        return mix_dna

    def simulate(self, n_iterations, n_moves, debug=False):
        tot_score = 0
        for it in range(n_iterations):
            self.score = 0
            self.envir = Environment()
            self.i, self.j = np.random.randint(1,self.envir.g_size+1, size=2)
            if debug:
                print('before')
                print('start position:',self.i, self.j)
                self.envir.show_grid()
            for move in range(n_moves):
                self.act()
            tot_score += self.score
            if debug:
                print('after')
                print('end position:',self.i, self.j)
                self.envir.show_grid()
                print('score:',self.score)
        return tot_score / n_iterations

    def act(self):
        post_str = self.envir.get_pos_string(self.i, self.j)
        gene_idx = situ_dict[post_str]
        act_key = self.dna[gene_idx]
        if act_key == '5':
            act_key = np.random.choice(['0','1','2','3'])

        if act_key == '0':
            self.mv_up()
        elif act_key == '1':
            self.mv_right()
        elif act_key == '2':
            self.mv_down()
        elif act_key == '3':
            self.mv_left()
        elif act_key == '6':
            self.pickup()

    def mv_up(self):
        if self.i == 1:
            self.score += self.wall_penalty
        else:
            self.i -= 1

    def mv_right(self):
        if self.j == self.envir.g_size:
            self.score += self.wall_penalty
        else:
            self.j += 1

    def mv_down(self):
        if self.i == self.envir.g_size:
            self.score += self.wall_penalty
        else:
            self.i += 1

    def mv_left(self):
        if self.j == 1:
            self.score += self.wall_penalty
        else:
            self.j -= 1

    def pickup(self):
        success = self.envir.remove_rubbish(self.i, self.j)
        if success:
            self.score += self.rubbish_score
        else:
            self.score += self.no_rub_penalty

def robot_from_dna(dna):
    return Robot(p1_dna=dna, p2_dna=dna, m_rate=0)
