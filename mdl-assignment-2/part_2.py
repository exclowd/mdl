from collections import OrderedDict

import numpy as np

actions = ['UP', 'LEFT', 'DOWN', 'RIGHT', 'STAY', 'SHOOT', 'HIT', 'CRAFT', 'GATHER', 'NONE']
step_cost = -20
gamma = 0.999
delta = 0.001


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
                (getid((pos, mat, arrow - 1, ms, max(0, mh - 25))), 0.5, (step_cost + 50) if mh == 25 else step_cost),
                (getid((pos, mat, arrow - 1, ms, mh)), 0.5, step_cost)
            ]
        elif action == 'HIT':
            res = [
                (getid((pos, mat, arrow, ms, max(0, mh - 50))), 0.1, (step_cost + 50) if 0 < mh <= 50 else step_cost),
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
                (getid((pos, mat, arrow - 1, ms, max(0, mh - 25))), 0.9, (step_cost + 50) if mh == 25 else step_cost),
                (getid((pos, mat, arrow - 1, ms, mh)), 0.1, step_cost)
            ]
        elif action == 'HIT':
            res = [
                (getid((pos, mat, arrow, ms, max(0, mh - 50))), 0.2, (step_cost + 50) if 0 < mh <= 50 else step_cost),
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
                (getid((pos, mat, arrow - 1, ms, max(0, mh - 25))), 0.25, (step_cost + 50) if mh == 25 else step_cost),
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
                temp.append((getid((pos, mat, 0, 'D', min(mh + 25, 100))), r[1] * 0.5, step_cost - 40))
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


# Actions = {
#     3 :{
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
# }

if __name__ == '__main__':
    initStates()
    Actions = []
    V = np.zeros(len(States))
    for i in range(len(States)):
        Actions.append(OrderedDict())
        for act in get_actions(States[i]):
            Actions[i][act] = resolve_action(act, States[i])

    # Set dictionary containing monster health zero to empty
    for i in range(len(States)):
        if States[i][-1] == 0:
            Actions[i] = {"NONE": []}

    iteration = 0
    while True:
        temp = np.full(len(States), -np.inf)  # for new V(t + 1)
        for i in range(len(States)):
            if States[i][-1] == 0:
                temp[i] = 0
                continue
            for action in Actions[i]:  # key=action value=[tuple(s`, P, R)]
                sm = 0
                for next_state in Actions[i][action]:
                    s, P, R = next_state
                    sm += P * (R + gamma * V[s])
                temp[i] = max(temp[i], sm)

        print(f"iteration={iteration}")
        for i in range(len(States)):
            maxUtility = -np.inf
            chosen = "NONE"
            for action in Actions[i]:
                sm = 0
                for next_state in Actions[i][action]:
                    s, P, R = next_state
                    sm += P * (R + gamma * V[s])
                if sm > maxUtility:
                    maxUtility = sm
                    chosen = action
            print(f"({States[i][1]},{States[i][2]},{States[i][3]},{States[i][4]},{States[i][5]}):{chosen}=[{temp[i]:.3f}]")
        iteration += 1

        maxDiff = 0
        for i in range(len(States)):
            maxDiff = max(abs(V[i] - (temp[i])), maxDiff)
        if maxDiff < delta:
            break
        V = temp

    # print(States[np.argmax(np.where(V == 0, -np.inf, V))])
