from multiprocessing import Pool
import random
import string
from seleniumdriver import SeleniumDriverMock
from fitnessevaluator import FitnessEvaluator
import csv
# import numpy as np

from deap import base, creator, tools, algorithms

creator.create('FitnessMin', base.Fitness, weights=(-1.0,))
creator.create('Individual', list, fitness=creator.FitnessMin)
toolbox = base.Toolbox()


def initIndividual(icls, length=6):
    individual = []
    for i in range(length - 1):
        individual.append(('click', [random.randint(0, 256), random.randint(0, 256)]))

    chars = string.ascii_letters + string.digits + string.punctuation
    random_string = "".join([random.choice(chars) for _ in range(40)])
    individual.insert(random.randint(0, len(individual)), ('type', random_string))

    return icls(individual)


def initPopulation(pcls, ind_init, length, number):
    pop = []

    pop.append(ind_init(length))

    for i in range(number - 1):  # The first one is already done
        pop.append(ind_init(length))

    return pcls(pop)


# def random_action():
# if random.random() < 0.99:
# return 'type', random.choice(string.ascii_letters + string.digits + string.punctuation)
# else:
# return 'click', [random.randint(0, 256), random.randint(0, 256)]


# toolbox.register('random_action', random_action)


def test(individual, individuals):
    target = '<script>alert(1)</script>'

    selenium_mock = SeleniumDriverMock()

    for action in individual:
        selenium_mock.perform(action)

    individuals, best = FitnessEvaluator().evaluate(selenium_mock, individuals)

    return individuals, best


def mutateRandomAction(individual, indpb):
    if random.random() < 0.5:
        i = random.randrange(0, len(individual))
    else:
        i = individual.index(('type', dict(individual)['type']))

    # if random.random() < indpb:
    if individual[i][0] == 'type':

        r = random.random()

        # Change char in random position
        if r < 0.97:

            content = list(individual[i][1])

            chars = string.ascii_letters + string.digits + string.punctuation
            random_char = random.choice(chars)
            random_pos = random.randrange(len(content))

            content[random_pos] = random_char

            # print("Mutate {} char from {} to {}".format(random_pos, individual[i][1][random_pos], random_char))

            individual[i] = ('type', "".join(content))

        # Remove char in random position
        elif r < 0.98:

            content = list(individual[i][1])

            random_pos = random.randrange(len(content))

            random_char = content[random_pos]

            del content[random_pos]

            # print("Remove {} char in position {}".format(random_char, random_pos))

            individual[i] = ('type', "".join(content))

        # Add random char in random position
        else:

            content = list(individual[i][1])
            chars = string.ascii_letters + string.digits + string.punctuation
            random_char = random.choice(chars)
            random_pos = random.randrange(len(content))

            # print("".join(content))
            content.insert(random_pos, random_char)
            # print("Add {} char in position {}".format(random_char, random_pos))
            individual[i] = ('type', "".join(content))
            # print("".join(content))


    elif individual[i][0] == 'click':
        individual[i] = ('click', [random.randint(0, 256), random.randint(0, 256)])

    return individual,


def customCrossover(ind1, ind2):
    if random.random() < 0.5:
        i = random.randrange(0, len(ind1))
    else:
        i = ind1.index(('type', dict(ind1)['type']))

    if ind1[i][0] == 'click':
        if ind2[i][0] == 'click':
            j = i
        else:
            j = (i + 1) % len(ind2)

        coord1, coord2 = ind1[i][1], ind2[j][1]

        coord1[0], coord2[0] = coord2[0], coord1[0]

        ind1[i] = ('click', coord1)
        ind2[j] = ('click', coord2)

    elif ind1[i][0] == 'type':
        # Find index trick
        type_value = dict(ind2)['type']
        j = ind2.index(('type', type_value))

        cut = random.randrange(1, len(type_value))
        prev_str1, prev_str2 = ind1[i][1], ind2[j][1]

        str1 = prev_str1[:cut] + prev_str2[cut:]
        str2 = prev_str2[:cut] + prev_str1[cut:]

        ind1[i] = ('type', prev_str1)
        ind2[j] = ('type', prev_str2)

    return ind1, ind2


toolbox = base.Toolbox()
toolbox.register('evaluate', test)


def eval_wrap(vals):
    return toolbox.evaluate(*vals)


def main(individuals):
    """
    pop = toolbox.population(length=8, number=10)
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    # stats.register("avg", numpy.mean)
    stats.register("min", numpy.min)
    # stats.register("max", numpy.max)

    pop, logbook = algorithms.eaSimple(pop, toolbox, cxpb=0.9, mutpb=0.1, ngen=50000, stats=stats, halloffame=hof, verbose=True)

    return pop, logbook, hof
    """

    CXPB, MUTPB = 0.95, 0.1

    toolbox.register('individual', initIndividual, creator.Individual)
    toolbox.register('population', initPopulation, list, toolbox.individual, length=6, number=20)

    toolbox.register('customCrossover', customCrossover)
    toolbox.register("mate", toolbox.customCrossover)
    toolbox.register("mutate", mutateRandomAction, indpb=0.5)
    toolbox.register("select", tools.selTournament, tournsize=3)

    pop = toolbox.population()

    p = Pool(20)

    fitnesses = []
    for i in pop:
        individuals, fitness = toolbox.evaluate(i, individuals)
        fitnesses.append((fitness,))

    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit
    # print("  Evaluated {} individuals".format(len(pop)))
    fits = [ind.fitness.values[0] for ind in pop]
    g = 0
    min_ = []
    while min(fits) > 0 and g < 50000:
        print("[+] Generation {}".format(g))
        g = g + 1
        # print("-- Generation {} --".format(g))
        offspring = toolbox.select(pop, len(pop))
        offspring = list(p.map(toolbox.clone, offspring))
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

        t_pop = list(p.map(eval_wrap, map((lambda x: (x, individuals)), invalid_ind)))
        individuals = t_pop[0][0]
        fitnesses = list(map((lambda x: (x[1],)), t_pop))
        # print(individuals)

        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
        pop[:] = offspring
        fits = [ind.fitness.values[0] for ind in pop]

        min_.append(min(fits))
        # print("fitness-- ", min(fits))
    # print("-- End of (successful) evolution --")


    best = min(pop, key= lambda ind: ind.fitness.values[0])

    return pop, best, min_



if __name__ == "__main__":

    individuals = [
        "<script>alert(1)</script>",
        "<script>alert(741212)</script>",
        "<script>alert(4)</script>",
        "script>alert('')</script>",
        "<script>alert('basd')</script>",
        "<script>alert(1)</script>",
        "script>alert(74382)</script>",
        "<script>alert(3)</script>",
        "<script>alert('a')</script>",
        "<script>alert('bnyA')</script>",
    ]

    for i in range(10):
        pop, best_ind, min_ = main(individuals)

        print("Best individual is: \n%s\nwith fitness: %s" % (best_ind, best_ind.fitness))

        with open('winners.csv', 'a') as f:
            f.write("{}\n".format(best_ind))

        with open('test_{:02d}.csv'.format(i), 'w') as f:
            for t in min_:
                f.write("{}\n".format(t))
