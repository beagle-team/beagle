import random
import string
import re
import pylev
import multiprocessing

from deap import base, creator, tools, algorithms

creator.create('RegFitnessMin', base.Fitness, weights=(-1.0,))
creator.create('RegIndividual', list, fitness=creator.RegFitnessMin)

all_char = string.ascii_letters + string.punctuation + string.digits


def initIndividual(icls, content):
    return icls(content)


def initPopulation(pcls, ind_init, number, individuals):
    pop = []

    for i in individuals:
        pop.append(ind_init(i))

    return pcls(pop)


def evaluate(individual, target, domain):
    keys = ['username', 'firstname', 'lastname', 'password', 'passconfirm']

    individual.append(individual[-1])
    i = dict(zip(keys, individual))

    match = []

    for k in keys:
        if k == 'passconfirm':
            match.append(re.match(domain['password'], i['passconfirm']))
        else:
            match.append(re.match(domain[k], i[k]))

    if not (all(match)):
        return 1000,

    d = [pylev.levenshtein(i['username'], target['username']),
         pylev.levenshtein(i['firstname'], target['firstname']),
         pylev.levenshtein(i['lastname'], target['lastname']),
         pylev.levenshtein(i['password'], target['password']),
         pylev.levenshtein(target['password'], target['passconfirm'])]

    if target['username'] == '':
        d[0] = 60.0
    if target['firstname'] == '':
        d[1] = 60.0
    if target['lastname'] == '':
        d[2] = 60.0
    if target['password'] == '':
        d[3] = 60.0
    if target['passconfirm'] == '':
        d[4] = 60.0

    if re.match(domain['username'], target['username']):
        d[0] = 0.0
    if re.match(domain['firstname'], target['firstname']):
        d[1] = 0.0
    if re.match(domain['lastname'], target['lastname']):
        d[2] = 0.0
    if re.match(domain['password'], target['password']):
        d[3] = 0.0
    if target['passconfirm'] == target['password']:
        d[4] = 0.0

    del individual[-1]

    return sum(d),


def mutateRandomChar(individual):
    r = random.random()

    n = random.randint(0, len(individual) - 1)

    i = list(random.choice(individual[n]))
    if r < 0.33:
        i[random.randint(0, len(i) - 1)] = random.choice(all_char)
    elif r < 0.66:
        i.insert(random.randint(0, len(i)), random.choice(all_char))
    else:
        if len(i) > 2:
            del i[random.randint(0, len(i) - 1)]

    individual[n] = "".join(i)

    return individual,


def main(target, domain, population):
    # target = payload{ fields }
    # target = reg_domain{ fields }

    toolbox = base.Toolbox()
    toolbox.register("RegIndividual", initIndividual, creator.RegIndividual)
    toolbox.register("population", initPopulation, list, toolbox.RegIndividual,
                     individuals=population, number=10)

    toolbox.register('evaluate', evaluate, target=target, domain=domain)
    toolbox.register('mate', tools.cxOnePoint)
    toolbox.register('mutate', mutateRandomChar)
    toolbox.register('select', tools.selTournament, tournsize=3)

    # print("Target: {} ".format(target), end='')

    match = []

    match.append(re.match(domain['username'], target['username']))
    match.append(re.match(domain['firstname'], target['firstname']))
    match.append(re.match(domain['lastname'], target['lastname']))
    match.append(re.match(domain['password'], target['password']))
    match.append(re.match(domain['password'], target['passconfirm']))
    match.append(target['password'] == target['passconfirm'])

    if all(match):
        best = toolbox.RegIndividual(target)
        best.fitness.values = 0,
        print(" [*]Found[*]")

        return population, best

    import numpy

    # Distributed Algorithm
    # pool = multiprocessing.Pool(8)
    # toolbox.register("map", pool.map)

    pop = toolbox.population()

    CXPB, MUTPB = 0.95, 0.1
    # print("Start of evolution")
    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit
    # print("  Evaluated {} individuals".format(len(pop)))
    fits = [ind.fitness.values[0] for ind in pop]
    g = 0
    while min(fits) > 0 and g < 1:
        g = g + 1
        # print("-- Generation {} --".format(g))
        offspring = toolbox.select(pop, len(pop))
        offspring = list(map(toolbox.clone, offspring))
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < CXPB:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values
        for mutant in offspring:
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
        pop[:] = offspring
        fits = [ind.fitness.values[0] for ind in pop]
        # print("fitness-- ", min(fits))
    # print("-- End of (successful) evolution --")
    best_ind = toolbox.select(pop, k=len(pop))[0]
    # print(best_ind.fitness.values[0])

    # pop_list = ["".join(i) for i in pop]

    return pop, best_ind
