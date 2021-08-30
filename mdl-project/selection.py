# 541
# 21

import numpy as np

from main import *
from save import get_from_id

np.set_printoptions(linewidth=np.inf)

I = 541
J = 439

if __name__ == '__main__':
    print(f"Using {I} {J}")
    a, erra = get_from_id(I)
    b, errb = get_from_id(J)
    print(a, erra)
    print(b, errb)
    par = np.array([a, b])
    chld = do_mutation(crossover_blx(par))
    sort_pop_by_fitness(chld)
