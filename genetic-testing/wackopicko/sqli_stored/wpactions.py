from multiprocessing import Pool
import random
import string
from wpmock import WackoPickoSqlStored
from wpfitnessevaluator import FitnessEvaluator
import csv

from deap import base, creator, tools, algorithms

creator.create('FitnessMin', base.Fitness, weights=(-1.0,))
creator.create('Individual', list, fitness=creator.FitnessMin)
toolbox = base.Toolbox()


def initIndividual(icls, length=30):
    clicks = []
    for i in range(length):
        clicks.append(('click', [random.randint(0, 256), random.randint(0, 256)]))

    chars = string.ascii_letters + string.digits + string.punctuation

    types = []
    for i in range(length):
        random_string = "".join([random.choice(chars) for _ in range(11)])
        types.append(('type', random_string))

    individual = []
    for c, t in zip(clicks, types):
        individual.append(c)
        individual.append(t)

    return icls(individual)


def initPopulation(pcls, ind_init, length, number):
    pop = []

    pop.append(ind_init(length))

    for i in range(number - 1):  # The first one is already done
        pop.append(ind_init(length))

    return pcls(pop)


def test(individual, reg_individuals, sim_individuals):
    mock = WackoPickoSqlStored()

    for action in individual:
        mock.perform(action)

    reg_individuals, sim_individuals, best = FitnessEvaluator().evaluate(mock, reg_individuals, sim_individuals)

    return reg_individuals, sim_individuals, best


def mutateRandomAction(individual, indpb):
    i = random.randrange(0, len(individual))

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
    i = random.randrange(0, len(ind1))

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


def main(reg_individuals, sim_individuals):
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
    toolbox.register('population', initPopulation, list, toolbox.individual, length=30, number=20)

    toolbox.register('customCrossover', customCrossover)
    toolbox.register("mate", toolbox.customCrossover)
    toolbox.register("mutate", mutateRandomAction, indpb=0.5)
    toolbox.register("select", tools.selTournament, tournsize=3)

    pop = toolbox.population()

    p = Pool(20)

    fitnesses = []
    for i in pop:
        reg_individuals, sim_individuals, fitness = toolbox.evaluate(i, reg_individuals, sim_individuals)
        fitnesses.append((fitness,))

    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit
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

        t_pop = list(p.map(eval_wrap, map((lambda x: (x, reg_individuals, sim_individuals)), invalid_ind)))

        # TODO: da recuperare (sbagliato quasi sicuro)
        reg_individuals = t_pop[0][0]
        sim_individuals = t_pop[0][1]
        fitnesses = list(map((lambda x: (x[2],)), t_pop))
        # print(fitnesses)

        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
        pop[:] = offspring
        fits = [ind.fitness.values[0] for ind in pop]

        min_.append(min(fits))

    best = min(pop, key=lambda ind: ind.fitness.values[0])

    return pop, best, min_


if __name__ == "__main__":

    reg_individuals = [
        ["a", "a", "a", "a"],
        ["b", "b", "b", "b"],
        ["c", "c", "c", "c"],
        ["d", "d", "d", "d"],
        ["aa", "aa", "aa", "aa"],
        ["ba", "ba", "ba", "ba"],
        ["ca", "ca", "ca", "ca"],
        ["da", "da", "da", "da"],
        ["da", "da", "da", "da"],
        ["da", "da", "da", "da"],
        ["da", "da", "da", "da"],
    ]

    sim_individuals = [
        "a' OR '1'='1",
        "b' OR '1'='1",
        "c' OR '1'='1",
        "d' OR '1'='1",
        "e' OR '1'='1",
        "f' OR '1'='1",
        "g' OR '1'='1",
        "h' OR '1'='1",
        "i' OR '1'='1",
        "l' OR '1'='1",
    ]

    for i in range(1):

        pop, best_ind, min_ = main(reg_individuals, sim_individuals)

        print("Best individual is: \n%s\nwith fitness: %s" % (best_ind, best_ind.fitness))

        with open('winners.csv', 'a') as f:
            f.write("{}\n".format(best_ind))

        with open('test_{}.csv'.format(i), 'w') as f:
            for t in min_:
                f.write("{}\n".format(t))
