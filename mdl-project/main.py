import math
import random

from request import do_request
from save import *

overfit_vector = np.array(
    [-0.08368223959845181, -0.000000000002237270470239752, -0.00000000000031272951418616673,
     0.00000000004431767299933582, -0.00000000016010404392407493, -0.000000000000000904338582732779,
     0.0000000000000008369616535547681, 0.000039641814107156555, -0.0000017813543172198783,
     -0.00000002927448577060052, 0.0000000009838476913002091
     ]
)

start_vector = [
    get_from_id(4038)[0],
    get_from_id(4040)[0],
    get_from_id(4117)[0],
    get_from_id(3964)[0],
    get_from_id(3981)[0],
    get_from_id(4069)[0],
    get_from_id(3885)[0],
    get_from_id(3984)[0],
    get_from_id(3775)[0],
    get_from_id(3871)[0],
    # np.zeros(11)
]

N = 40
ITERATIONS = 40


def get_closest_power10(num, pow):
    if num == 0.0:
        return -1
    return math.floor(math.log10(abs(num))) - pow


def get_closest_random(num, pow=0):
    return num + np.random.choice([-1, 1]) * np.random.uniform(0, 1) * (
            10 ** get_closest_power10(num, pow))


def get_closest_random_m(vector: np.array):
    ret = np.zeros(len(vector))
    for i in range(len(vector)):
        ret[i] = get_closest_random(vector[i], int(np.random.choice([1, 0], p=[0.5, 0.5])))
    assert len(ret) == len(vector)
    return ret


def get_closest_random1(num):
    return get_closest_random(num, 1)


def gen_pop(vector: np.array, num):
    print("Generating Population from", vector)
    return np.array([np.array(list(map(get_closest_random1, vector))) for x in range(num // 2)] +
                    [np.array(list(map(get_closest_random, vector))) for x in
                     range(num - 1 - num // 2)] +
                    [vector])


def gen_pop_multiple(vectors: list, num):
    population = []
    sz = len(vectors)
    assert num % sz == 0
    num //= sz
    print("Generating Population from")
    for vector in vectors:
        print(vector),
        population = population + [get_closest_random_m(vector) for x in range(num - 1)] + [vector]

    return np.array(population)


def get_mse(vector: np.array):
    if exists(vector):
        return score(vector)
    else:
        mse = do_request(vector)
        add(vector, mse)
        return mse


def fitness_func(mse: np.array):
    return math.log10(0.9 * mse[1] + 0.2 * mse[0])


def sort_pop_by_fitness(population):
    errors = np.array(list(map(get_mse, population)))
    fitness_arr = np.array(list(map(fitness_func, errors)))
    idx = fitness_arr.argsort()
    to_print = "\n".join(
        str(get_id(population[it])) + ":" + str(errors[it]) + ":" + str(population[it]) + ":" + str(
            fitness_arr[it]) for
        it in idx
    )
    print('Population scores:', to_print, sep='\n')
    return population[idx], fitness_arr[idx]


def select_fittest(pp, fit):
    idx = fit.argsort()
    pp = pp[idx]
    fit = fit[idx]
    fit = np.exp(-fit)
    cum = np.cumsum(fit) / np.sum(fit)
    cnt = np.zeros(cum.shape, dtype=int)
    for x in range(100):
        r = np.random.uniform()
        cnt[np.searchsorted(cum, r)] += 1
    idx = cnt.argsort()[-2:]
    print("Selected:", idx)
    return pp[idx]


def get_children(parents):
    c = crossover(parents)
    c = do_mutation(c)
    return c


def crossover(parents):
    p1, p2 = parents
    c = np.zeros((2, 11))
    print("***************")
    print("***CROSSOVER***")
    print("***************")
    for j in range(11):
        c[0][j], c[1][j] = (p1[j], p2[j]) if random.randint(0, 2) == 0 else (p2[j], p1[j])
    return c


def crossover_blx(parents):
    children = 2
    c = np.zeros((children, 11))
    print("*******************")
    print("***CROSSOVER BLX***")
    print("*******************")
    p1, p2 = parents
    ALPHA = 0.2
    for j in range(11):
        old = abs(p2[j] - p1[j])
        for i in range(children):
            c[i][j] = np.random.uniform(min(p1[j], p2[j]) - ALPHA * old,
                                        max(p1[j], p2[j]) + ALPHA * old)
    return c


def do_mutation(children):
    print("before mutation")
    print("children:", "\n".join(str(x) for x in children), sep='\n')
    print("***************")
    print("***MUTATION***")
    print("***************")
    for c in children:
        for i in range(len(c)):
            p = np.random.randint(0, 10)
            if p < 3:
                v = get_closest_random(c[i], pow=0 if np.random.randint(0, 10) < 3 else 1)
                c[i] = v
    print("children:", "\n".join(str(x) for x in children), sep='\n')
    return children


def tournament_selection(parents, children):
    population = np.concatenate((parents, children), axis=0)
    return sort_pop_by_fitness(population)[0][:2]


np.set_printoptions(linewidth=np.inf)

if __name__ == '__main__':
    pop = gen_pop_multiple(start_vector, N)
    for i in range(ITERATIONS * N // 2):
        # pop = get_fitness(pop)
        new = np.zeros((N, 11))
        print("*******************************")
        print("***iteration:", i, "Population is***")
        print("*******************************")
        pop, fitness = sort_pop_by_fitness(pop)

        par = select_fittest(pop, fitness)
        child = get_children(par)
        print("&&&&&&&&&&&&&&&&&&&&&&&&")
        print("&&TOURNAMENT SELECTION&&")
        print("&&&&&&&&&&&&&&&&&&&&&&&&")
        print("parents:", "\n".join(str(get_id(x)) + str(x) for x in par), "children:",
              "\n".join(str(x) for x in child), sep='\n')
        selected = tournament_selection(par, child)
        print("To be Selected for the new population:",
              "\n".join(str(get_id(x)) + str(x) for x in selected), sep='\n')
        pop = np.unique(np.concatenate((pop, selected), axis=0), axis=0)
        pop = sort_pop_by_fitness(pop)[0][:N]

    pop, fitness = sort_pop_by_fitness(pop)
    print("%%%%%%%%%%%%%%%%%%%%%%%%%")
    print("%%%final - population%%%%")
    print("%%%%%%%%%%%%%%%%%%%%%%%%%")
    print("\n".join(str(get_id(x)) + ":" + str(get_mse(x)) + ":" + str(x) for x in pop))
