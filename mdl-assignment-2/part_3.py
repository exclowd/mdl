import json
import sys
from collections import OrderedDict
import cvxpy as cp
import numpy as np

actions = ['UP', 'LEFT', 'DOWN', 'RIGHT', 'STAY', 'SHOOT', 'HIT', 'CRAFT', 'GATHER', 'NONE']
step_cost = -20
gamma = 0.999
delta = 0.001


def init_actions():
    for s in States:
        id, pos, material, arrow, ms, mh = s


def get_actions(state):
    res = []
    id, pos, mat, arrow, ms, mh = state
    if mh == 0:
        return ['NONE']
    if pos == 'C':
        res.append('LEFT')
        res.append('RIGHT')
        res.append('UP')
        res.append('DOWN')
        res.append('STAY')
        if arrow > 0:
            res.append('SHOOT')
        res.append('HIT')
    elif pos == 'N':
        res.append('DOWN')
        res.append('STAY')
        if mat > 0:
            res.append('CRAFT')
    elif pos == 'W':
        res.append('RIGHT')
        res.append('STAY')
        if arrow > 0:
            res.append('SHOOT')
    elif pos == 'S':
        res.append('UP')
        res.append('STAY')
        res.append('GATHER')
    elif pos == 'E':
        res.append('LEFT')
        res.append('STAY')
        if arrow > 0:
            res.append('SHOOT')
        res.append('HIT')
    return res


def resolve_action(action: str, state):
    res = []
    id, pos, mat, arrow, ms, mh = state
    if action == 'NONE':
        return []
    if pos == 'C':
        if action == 'UP':
            res = [
                (getid(('N',) + state[2:]), 0.85, step_cost),
                (getid(('E',) + state[2:]), 0.15, step_cost),
            ]
        elif action == 'DOWN':
            res = [
                (getid(('S',) + state[2:]), 0.85, step_cost),
                (getid(('E',) + state[2:]), 0.15, step_cost),
            ]
        elif action == 'LEFT':
            res = [
                (getid(('W',) + state[2:]), 0.85, step_cost),
                (getid(('E',) + state[2:]), 0.15, step_cost),
            ]
        elif action == 'RIGHT':
            res = [
                (getid(('E',) + state[2:]), 1, step_cost),
            ]
        elif action == 'STAY':
            res = [
                (id, 0.85, step_cost),
                (getid(('E',) + state[2:]), 0.15, step_cost),
            ]
        elif action == 'SHOOT':
            res = [
                (getid((pos, mat, arrow - 1, ms, max(0, mh - 25))), 0.5, step_cost),
                (getid((pos, mat, arrow - 1, ms, mh)), 0.5, step_cost)
            ]
        elif action == 'HIT':
            res = [
                (getid((pos, mat, arrow, ms, max(0, mh - 50))), 0.1, step_cost),
                (id, 0.9, step_cost)
            ]
    elif pos == 'N':
        if action == 'DOWN':
            res = [
                (getid(('C',) + state[2:]), 0.85, step_cost),
                (getid(('E',) + state[2:]), 0.15, step_cost),
            ]
        elif action == 'STAY':
            res = [
                (id, 0.85, step_cost),
                (getid(('E',) + state[2:]), 0.15, step_cost),
            ]
        elif action == 'CRAFT':
            res = [
                (getid((pos, mat - 1, min(3, arrow + 1), ms, mh)), 0.5, step_cost),
                (getid((pos, mat - 1, min(3, arrow + 2), ms, mh)), 0.35, step_cost),
                (getid((pos, mat - 1, min(3, arrow + 3), ms, mh)), 0.15, step_cost)
            ]
    elif pos == 'S':
        if action == 'UP':
            res = [
                (getid(('C',) + state[2:]), 0.85, step_cost),
                (getid(('E',) + state[2:]), 0.15, step_cost),
            ]
        elif action == 'STAY':
            res = [
                (id, 0.85, step_cost),
                (getid(('E',) + state[2:]), 0.15, step_cost),
            ]
        elif action == 'GATHER':
            res = [
                (getid((pos, min(2, mat + 1), arrow, ms, mh)), 0.75, step_cost),
                (id, 0.25, step_cost),
            ]
    elif pos == 'E':
        if action == 'LEFT':
            res = [
                (getid(('C',) + state[2:]), 1, step_cost),
            ]
        elif action == 'STAY':
            res = [
                (id, 1, step_cost),
            ]
        elif action == 'SHOOT':
            # if mh == 25:
            #     print(id, "yoo")
            res = [
                (getid((pos, mat, arrow - 1, ms, max(0, mh - 25))), 0.9, step_cost),
                (getid((pos, mat, arrow - 1, ms, mh)), 0.1, step_cost)
            ]
        elif action == 'HIT':
            res = [
                (getid((pos, mat, arrow, ms, max(0, mh - 50))), 0.2, step_cost),
                (id, 0.8, step_cost)
            ]
    elif pos == 'W':
        if action == 'RIGHT':
            res = [
                (getid(('C',) + state[2:]), 1, step_cost),
            ]
        elif action == 'STAY':
            res = [
                (id, 1, step_cost),
            ]
        elif action == 'SHOOT':
            res = [
                (getid((pos, mat, arrow - 1, ms, max(0, mh - 25))), 0.25, step_cost),
                (getid((pos, mat, arrow - 1, ms, mh)), 0.75, step_cost)
            ]

    if ms == 'D':
        temp = []
        for r in res:
            id2, pos2, mat2, arrow2, ms2, mh2 = States[r[0]]
            temp.append((getid((pos2, mat2, arrow2, 'R', mh2)), r[1] * 0.2, r[2]))
            temp.append((id2, r[1] * 0.8, r[2]))
        res = temp
    elif ms == 'R':
        temp = []
        for r in res:
            id2, pos2, mat2, arrow2, ms2, mh2 = States[r[0]]
            temp.append((id2, r[1] * 0.5, r[2]))
            if pos in ['C', 'E']:  # check TODO
                temp.append(
                    (getid((pos, mat, 0, 'D', min(mh + 25, 100))), r[1] * 0.5, step_cost - 40))
            else:
                temp.append((getid((pos2, mat2, arrow2, 'D', mh2)), r[1] * 0.5, r[2]))
        res = temp
    return res


def getid(state):
    for s in States:
        if s[1:] == state:
            return s[0]


States = []  # list of tuples  state = ("C", 0, 0, "D", 100)   id, pos , material, arrow, monster-state, monster-health


def initStates():
    id = 0
    positions = ['C', 'N', 'S', 'W', 'E']
    for pos in positions:
        for material in range(3):
            for arrow in range(4):
                for ms in ['R', 'D']:
                    for mh in range(0, 101, 25):
                        States.append((id, pos, material, arrow, ms, mh))
                        id += 1


# Actions =[
#     {
#         'STAY':[
#             (id, 0.85, -20),
#             (id, 0.15, -30),
#         ],
#         "GATHER":[
#             ('C', 1, 0.4, -20)
#             ('C',2, 0.3, -20),
#             ('C', 3)
#         ],
#        'CRAFT': [
#
#        ]
#     }
# ]

np.set_printoptions(threshold=np.inf)
if __name__ == '__main__':
    initStates()
    Actions = []
    V = np.zeros(len(States))
    for i in range(len(States)):
        Actions.append(OrderedDict())
        for act in get_actions(States[i]):
            Actions[i][act] = resolve_action(act, States[i])
        # print(States[i] , "->", Actions[i])
    # Set dictionary containing monster health zero to empty
    for i in range(len(States)):
        if States[i][-1] == 0:
            Actions[i] = {"NONE": []}
        # print(Actions[i].keys())
    ans = {}
    tot_actions = sum(len(Actions[i].keys()) for i in range(len(States)))
    # print(tot_actions)
    A = np.zeros((len(States), tot_actions))
    RR = np.zeros(tot_actions)
    alpha = np.zeros(len(States))
    alpha[getid(('C', 2, 3, 'R', 100))] = 1
    ac_no = 0
    for i in range(len(States)):
        for action in Actions[i]:
            A[i][ac_no] = 1
            for next_state in Actions[i][action]:
                s, P, R = next_state
                A[s][ac_no] -= P
            if States[i][-1] == 0:
                RR[ac_no] = 0
            elif States[i][-2] == 'R':
                RR[ac_no] = step_cost + (-20 if States[i][1] in ['C', 'E'] else 0)
            else:
                RR[ac_no] = step_cost
            ac_no += 1
    ans['a'] = [list(x) for x in A]
    ans['r'] = list(RR)
    ans['alpha'] = list(alpha)
    # pp.pprint(Actions)
    X = cp.Variable(tot_actions, name='X')
    # a = np.array([[1, 0], [0, 1]])
    # b = cp.Variable(2)
    # x = np.array([1,1])
    # constraint = [cp.matmul(a, b) == x, b >= 0]
    # objective = cp.Maximize(b[0])
    # problem = cp.Problem(objective, constraint)
    # print(problem.solve())
    constraints = [A @ X == alpha, X >= np.zeros(tot_actions)]  # sx 1
    objective = cp.Maximize(cp.sum(RR @ X))
    problem = cp.Problem(objective, constraints)
    solution = problem.solve()
    # for i in A:
    #     t = ' '.join([str(j) for j in i])
    #     sys.stdout.write(t + "\n")

    # print(RR)
    # print(X)
    # print(solution)
    val = X.value
    ans['x'] = list(val)
    ans['objective'] = solution
    ans['policy'] = []

    cur_act = 0
    for i in range(len(States)):
        # for act in Actions[i]:
        chosen = np.argmax(val[cur_act:cur_act + len(Actions[i].keys())])
        # s = "(" + ",".join([str(x) for x in States[i][1:]]) + ")"
        ans['policy'].append([States[i][1:], list(Actions[i].keys())[chosen]])
        # print(States[i], '=>', list(Actions[i].keys())[chosen])
        cur_act += len(Actions[i].keys())
    json_object = json.dumps(ans)
    print(json_object)
    #
    # x = cp.Variable(2, name="x")  # [x, y]
    # A = np.array([[4, 3], [-3, 4]])
    #
    # constraints = [cp.matmul(A, x)[0] <= 12, cp.matmul(A, x)[1] <= 5, x[0] <= 2, x[1] >= 0]
    # # all inequalities >=
    # objective = cp.Maximize(x[1])
    # problem = cp.Problem(objective, constraints)
    #
    # solution = problem.solve()
    # print(solution)

    # print(x.value)
