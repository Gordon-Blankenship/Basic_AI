# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 08:37:08 2017

@author: xfang13, glblank

"""

# Genetic Algorithm to solve 8 Queens Problem
# generation() : returns list of size 8 randomly filled
# fitness() : tests how close to 28 the fitness is
# mutate() : changes a value in the list
# crossover() : creates a child from 2 parents, returns more fit option
# select() : chooses which parents to procreate
# solve() : main function to find solution

import numpy as np

def generation():

    # Create randomly filled chromosome
    chromosome = [np.random.randint(1, 8) for x in range(8)]
    return chromosome

def fitness(Input):
    #Input should be a list
    # assert(type(Input)==list)

    #Step1: make the state out of the Input
    state = np.zeros((8,8))
    for j in range(8):
        state[Input[j]-1][j] = 1
            

    #Step2: find the fitness of the state
    attacks = 0
    k = -1
    for j in range(8):
        k += 1
        #direction 1: the east
        for l in range(k+1,8):
            attacks += state[state[:,j].argmax()][l]
    
        #direction 2: the northeast
        row = state[:,j].argmax()
        column = j
        while row > 0 and column < 7:
            row -= 1
            column += 1
            attacks += state[row][column]
            
        #direction 3: the southeast
        row = state[:,j].argmax()
        column = j
        while row < 7 and column < 7:
            row += 1
            column += 1
            attacks += state[row][column]
            
    return 28 - attacks

def mutate(c):

    ind = np.random.randint(0, len(c)-1) # Determine random index
    mutation = np.random.randint(0, len(c)-1) # Determine new mutation

    c[ind] = mutation # Change the mutated value

    return c

# Breed chromosome 1 and chromosome 2
def crossover(c1, c2):
    # find a random crossover point
    cross = np.random.randint(2, 5)

    # move the genes around between chromosomes
    new_c1 = c1[:cross] + c2[cross:]
    new_c2 = c2[:cross] + c1[cross:]

    if fitness(new_c1) > fitness(new_c2):
        return new_c1
    else:
        return new_c2

# determine which chromosomes breed with which
def select(P, size):

    # random number of offspring to be generated
    offspring = size-1
    new_population = P

    while offspring > 0:

        r1 = np.random.randint(0, size // 2)
        c1 = P[r1]

        c2 = P[np.random.randint(r1, size-1)]
        # ^^ prevents the same parent from being picked 2x ^^

        new_population[offspring] = crossover(c1, c2)

        offspring -= 1

    return new_population

def solve_8_queens():

    # Constraints & Optimization
    max_generations = 10000
    size = 15

    # Initial random population
    population = [generation() for i in range(0, size)]

    # Sort based on best fitness
    population.sort(key=fitness, reverse=True)
    
    current_gen = 0
    
    while current_gen < max_generations:
        
        # Check if the most fit is max fit
        if fitness(population[0]) == 28:
            print("Gen # " + str(current_gen) + " found solution:")
            print("Chromosome #0 => " + str(population[0]) + " fit = " + str(fitness(population[0])))
            return

        # Which chromosome(s) to mutate
        mut_factor = np.random.randint(0, 7)

        # Breed the population
        population = select(population, size)

        # Mutate the population
        for x in range(0, size-1):
            population[x] = mutate(population[x])

        # Reorder them by most fit to least
        population.sort(key=fitness, reverse=True)

        # print_pop(population, current_gen)
        
        current_gen += 1
    
    print("Solution not found through " + str(max_generations) + " generations")
    

# print function prints all of the chromosomes in the population
# def print_pop(population, gen_num):

#     print("\t********Generation #" + str(gen_num) + "********")
#     count = 0
#     average = 0
#     for chromosome in population:
#         fit = fitness(chromosome)
#         average += fit
#         print("Chromosome #" + str(count) + " => " + str(chromosome) + " fit = " + str(fit))
#         count+=1
#     print("Average Fitness ==> " + str(round(average / count, 2)))
    
#     print("****************************************************")

if __name__=='__main__':

    # solve the 8 Queens problem with random initialization
    solve_8_queens()
