import random
import string
import re
import pylev
import multiprocessing

from deap import base, creator, tools, algorithms

creator.create('InnerFitnessMin', base.Fitness, weights=(-1.0,))
creator.create('InnerIndividual', list, fitness=creator.InnerFitnessMin)

all_char = string.ascii_letters + string.punctuation + string.digits


def initIndividual(icls, content):
    content = str(content).strip('"')
    return icls(str(content))


def initPopulation(pcls, ind_init, number, individuals):
    pop = []

    for i in individuals:
        pop.append(ind_init(i))

    return pcls(pop)


def evaluate(individual, target, domain):
    s = "".join(individual)
    if not (all(re.match(r, s, flags=re.IGNORECASE) for r in domain)):
        return 1000,

    return pylev.levenshtein("".join(individual), "".join(target)),


def mutateRandomChar(individual):

    r = random.random()
    if r < 0.33:
        individual[random.randint(0, len(individual) - 1)] = random.choice(all_char)
    elif r < 0.66:
        individual.insert(random.randint(0, len(individual)), random.choice(all_char))
    else:
        if len(individual) > 2:
            del individual[random.randint(0, len(individual) - 1)]
    
    return individual,



def main(target, domain, population):

    toolbox = base.Toolbox()
    toolbox.register("InnerIndividual", initIndividual, creator.InnerIndividual)
    toolbox.register("population", initPopulation, list, toolbox.InnerIndividual,
            individuals=population, number=10)

    toolbox.register('evaluate', evaluate, target=target, domain=domain)
    toolbox.register('mate', tools.cxOnePoint)
    toolbox.register('mutate', mutateRandomChar)
    toolbox.register('select', tools.selTournament, tournsize=3)

    # print("Target: {} ".format(target), end='')

    if all(re.match(r, target, re.IGNORECASE) for r in domain):
        best = toolbox.InnerIndividual(target)
        best.fitness.values = 0,
        print(" [*]Found[*]")

        return population, best


    import numpy

    # Distributed Algorithm
    # pool = multiprocessing.Pool(8)
    # toolbox.register("map", pool.map)

    pop = toolbox.population()

    # pop, logbook = algorithms.eaSimple(pop, toolbox, cxpb=0.95, mutpb=0.1, ngen=1000,
            # stats=stats, halloffame=hof, verbose=True)

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

    pop_list = ["".join(i) for i in pop]

    return pop_list, best_ind


if __name__ == "__main__":

    # Se TARGET soddisfa domain, distanza 0 senza fare i test
    # TARGET = "<script>alert(12037219803210938123123213</script>"
    # TARGET = "<script>alert(120372198032109381231232ab</script>"
    TARGET = "<script>alert(120372198032109381231232xy</script>"

    
    domain = [ ".{6,}", ".*\d.*" ]
    # domain = "(<script>alert\('.*'\)</script>)|(<script>alert\(\d+\)</script>)"

    """
    individuals = [
        "<script>alert(1)</script>",
        "<script>alert(741212)</script>",
        "<script>alert(4)</script>",
        "<script>alert('')</script>",
        "<script>alert('basd')</script>",
        "<script>alert(1)</script>",
        "<script>alert(74382)</script>",
        "<script>alert(3)</script>",
        "<script>alert('a')</script>",
        "<script>alert('bnyA')</script>",
    ]
    """

    individuals = [
        "asd4as",
        "bi2ads",
        "sdb82a",
        "sad123",
        "92dsad",
        "sd9asd",
        "9sad13",
        "7ga78d",
        "7fg23h",
        "sa7d20",
    ]
    
    pop, best_ind = main(target=TARGET, domain=domain, population=individuals)
    print("Best individual is: %s\nwith fitness: %s" % ("".join(best_ind), best_ind.fitness))
