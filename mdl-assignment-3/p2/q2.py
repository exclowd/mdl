import numpy as np

roll_no = 2019101006
discount = 0.5
N = 8 * 8 * 2
p = 1 - (((roll_no % 10000) % 30) + 1) / 100
start_state = (1, 0)
R = roll_no % 90 + 10

actions = ['UP', 'DOWN', 'LEFT', 'RIGHT', 'STAY']
# call = ['ON', 'NOOP', 'OFF']

# agent, target, call
# actions = [(x, y, z) for z in call for y in action for x in action]
action_str = ' '.join(actions)

positions = [(x, y) for x in range(2) for y in range(4)]

observations = ['', 'o1', 'o2', 'o3', 'o4', 'o5', 'o6']

init = f"""discount: {discount}
values: reward
states: {N}
actions: {action_str}
observations: {' '.join(observations[1:])}
"""

# agent_pos, target_pos, call
states = [(x, y, z) for x in positions for y in positions for z in range(2)]


def get_obs(pos_a, pos_t):
    if pos_a == pos_t:
        return 1
    elif (pos_a[0], pos_a[1] + 1) == pos_t:
        return 2
    elif (pos_a[0], pos_a[1] - 1) == pos_t:
        return 4
    elif (pos_a[0] + 1, pos_a[1]) == pos_t:
        return 3
    elif (pos_a[0] - 1, pos_a[1]) == pos_t:
        return 5
    return 6


def resolve_action(state, act):
    pos, pos_t, call = state
    agent_states = []  # (pos, prob, rew)
    if act == 'UP':
        agent_states.append(((max(0, pos[0] - 1), pos[1]), p, -1))
        agent_states.append(((min(1, pos[0] + 1), pos[1]), 1 - p, -1))
    elif act == 'DOWN':
        agent_states.append(((min(1, pos[0] + 1), pos[1]), p, -1))
        agent_states.append(((max(0, pos[0] - 1), pos[1]), 1 - p, -1))
    elif act == 'RIGHT':
        agent_states.append(((pos[0], min(3, pos[1] + 1)), p, -1))
        agent_states.append(((pos[0], max(0, pos[1] - 1)), 1 - p, -1))
    elif act == 'LEFT':
        agent_states.append(((pos[0], max(0, pos[1] - 1)), p, -1))
        agent_states.append(((pos[0], min(3, pos[1] + 1)), 1 - p, -1))
    else:
        agent_states.append((pos, 1, 0))

    target_states = [((max(0, pos_t[0] - 1), pos_t[1]), .1),
                     ((min(1, pos_t[0] + 1), pos_t[1]), .1),
                     ((pos_t[0], min(3, pos_t[1] + 1)), .1),
                     ((pos_t[0], max(0, pos_t[1] - 1)), .1),
                     (pos_t, .6)]  # (pos, prob)
    temp = []

    for t in target_states:
        if call:
            temp.append((t[0], 0, t[1] * 0.1))
            temp.append((t[0], 1, t[1] * 0.9))
        else:
            temp.append((t[0], 0, t[1] * 0.5))
            temp.append((t[0], 1, t[1] * 0.5))
    target_states = temp  # (pos, call, prob)

    res = []  # (agent_pos, target_pos, call), reward, prob, obs
    # state -> [next_state, reward, probability, obs]

    for s1 in agent_states:
        for s2 in target_states:
            res.append((
                (s1[0], s2[0], 0 if pos == pos_t and call else s2[1]),
                (R + s1[2]) if (s1[0] == s2[0] and not (pos == pos_t and call) and s2[1] == 1) else s1[2],  # ?
                s1[1] * s2[2],
                get_obs(s1[0], s2[0])
            ))
    # print('xxxxxxxxxxxxxxxxx')
    # print(state)
    # print(act)
    # print(res)
    # print('xxxxxxxxxxxxxxxxx')
    return res


def get_id(s):
    for i, ss in enumerate(states):
        if ss == s:
            return i


if __name__ == '__main__':
    transitions = {}
    rewards = {}
    observe = []
    start = np.zeros(len(states))
    # print(p, R)
    for it, s in enumerate(states):
        if s[1] == start_state and get_obs(s[0], s[1]) == 6:
            start[it] = 1
        for ia, a in enumerate(actions):
            for nxt in resolve_action(s, a):
                ns, rew, prob, obs = nxt
                # print(s, a, ns)
                # curr = s
                curr = it
                ns = get_id(ns)
                obs = observations[obs]

                if (a, curr, ns) in transitions:
                    transitions[(a, curr, ns)] += prob
                else:
                    transitions[(a, curr, ns)] = prob

                # if (a, curr, ns, obs) in rewards:
                #     rewards[(a, curr, ns, obs)] += rew
                # else:
                rewards[(a, curr, ns, obs)] = rew

                # rewards.append((a, curr, ns, obs, rew))
                observe.append((a, ns, obs, 1.0))

    start = start / np.sum(start)

    print(init)
    print('start:')
    print(' '.join([str(float(x)) for i, x in enumerate(start)]))
    print('')
    for x, y in transitions.items():
        print(
            f"T: {' : '.join([str(z) for z in x])} {str(round(y, 7))}")

    for x in observe:
        print(
            f"O: {' : '.join([str(y) for y in x[:-1]])} {str(round(x[-1], 7))}")

    for x, y in rewards.items():
        print(
            f"R: {' : '.join([str(z) for z in x])} {str(round(y, 7))}")

    # for x in rewards:
    #     print(f"R: {' : '.join([str(z) for z in x[:-1]])} {str(round(x[-1], 7))}")
    #
    # print(len(rewards), len(set(rewards)))

    # with open('q2.pomdp', 'w+') as f:
    #     init += f"start:\n{' '.join([str(float(x)) for x in start])}\n"
    #     for x in transitions:
    #         init += f"T: {' : '.join([str(y) for y in x[:-1]])} {str(round(x[-1], 3))}\n"

    #     for x in observe:
    #         init += f"O: {' : '.join([str(y) for y in x[:-1]])} {str(round(x[-1], 3))}\n"

    #     for x in rewards:
    #         init += f"R: {' : '.join([str(y) for y in x[:-1]])} {str(round(x[-1], 3))}\n"

    #     f.write(init)
