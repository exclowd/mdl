from fractions import Fraction as f
from decimal import Decimal as d


C = ['r', 'g', 'r', 'g', 'g', 'r']
O = {
    'r': {  # state color
        'r': f('0.85'),
        'g': f('0.15')
    },
    'g': {  # state color
        'r': f('0.1'),
        'g': f('0.9')
    }
}

p = f('0.83')

A = [(),('R', 'g'), ('L', 'r'), ('L', 'g')]

B = [[f(1, 3), 0, f(1, 3), 0, 0, f(1, 3)]]
B += [[f('0') for x in range(6)] for z in range(3)]

for i in range(1, 4):
    for j in range(6):
        # update values using all the left moves
        frm_right = min(j + 1, 5)
        # update values using all the right moves
        frm_left = max(j-1, 0)
        # print(j, frm_left, frm_right)
        # print(B[i][j])
        if 0<= j <= 4:
            B[i][j] += O[C[j]][A[i][1]] * B[i - 1][frm_right] * \
                (p if A[i][0] == 'L' else (1-p))
        elif j == 5:
            B[i][j] += O[C[j]][A[i][1]] * B[i - 1][j] * \
                (p if A[i][0] == 'R' else (1-p))

        if 1 <= j <= 5:
            B[i][j] += O[C[j]][A[i][1]] * B[i - 1][frm_left] * \
                (p if A[i][0] == 'R' else (1-p))
        elif j == 0:
            B[i][j] += O[C[j]][A[i][1]] * B[i - 1][j] * \
                (p if A[i][0] == 'L' else (1-p))

        # print(B[i][j])

    print(B[i])
    s = sum(B[i])
    print(f(s))
    B[i] = [f(x , s) for x in B[i]]
    print(B[i])
    print('-------------------')
    print('*******************') 
    print(list(map(lambda x: x.numerator / x.denominator, B[i])))
    print('*******************')