# MDL Assignment 2 Part 3
## Linear Programming

### Procedure of creating A matrix
Matrix A is a matrix of order `number of states` x `number of total actions`, where `A[i][j]` = net flow of probabilities to take action `j` from state `i`
* Starting with a null matrix. For for each action `a` originating from state `s`, we set the entry in `A[s][a]` = 1. This ensures that the outflow from each state is 1 since summing up the probabilities for all transitions for action equates to one.
* Now for each transition in action `a` leading the agent to state `s'`, we decrease the value of `A[s'][a]` by the probability of transition accounting for inflow in the state.
* If there exists a self loop, then eventually the outflow from a state `s` reduces from one since the transition itself leads to same state accounting an inflow.
* This procedure generates the matrix A.

### Procedure of creating policy
* We convert the problem into a Linear Programming problem with the constraint that `A*X = alpha`(flow is preserved) and `X > 0`. 
* After solving the `LP` to maximise `sum(x @ R)`. Out of the possible actions out of the state `s` one with the maximum value of `x` is chosen as the policy for `s`.

### Analysis of policy
**Note: The analysis is based on current policy obtained and may be susceptible to precision errors.**

* When the agent is at the center position and the monster is in `R` state it prefers to go to either `N` or `S` depending on the amount of material that the agent possesses. In other cases it tries to do damage to the monster.

* Whenever the agent is present at `E` state , then he always prefer to either shoot if he has arrows or hit the monster with blade. No movement action is ever taken.

* When ever the agent has material it decides to craft at `N`.

* The agent also decides to gather material at `S`.

* If we run a simulation for current situation , the agent is present only on `N` , `C` or `E` positions. He never travels to either `S` or `W`. The actions taken include that firstly he travels to `N` state and stays up there. If incase he fails to stay , he is teleported to `E` state where he continuously attacks and never moves which will eventually end the game. If he fails to move `N`, then too he lands on `E` state.

### Do multiple policies exist?

LP has a constraint: AX = alpha , X >= 0
LP has objective: Maximize (R'X) where R' represents the transpose of R

* The calculated policy depends on the alpha vector which describes the probabilities of starting from a particular state.
Here the alpha chosen is all zeroes vector except at state (C, 2, 3, R, 100) where the value is 1.
If we change the values in the alpha vector, such that sum of all values is the vector is one and each entry is greater than zero, then we might end up in getting a different policy.

* Similarly, another way is change the probabilities and rewards of transitions in an action. The change in probabilities will affect the A matrix which changes the constraints to the problem. 
* The change in rewards will affect theR matrix which changes the objective function and thereby resulting in different policy.
* There seem to be some inherent precision error in the solver. This can be shown by the fact that we could generate multiple policies by just scaling R. This meant that the objective was also scaled by the same amount by we would get entirely different policies.

All these methods will affect the solution of the problem , which may result in change in policy. Therefore, these kind of problems can have different policies.