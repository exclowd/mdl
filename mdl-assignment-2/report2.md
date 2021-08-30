# MDL Assignment 2

## Value Iteration

### Choice of Actions
Since the `step_cost` parameter was quite large for our case, the agent used
more aggressive play that would end the game quickly. This meant that
*  It would prefer hitting
with the blade more than using arrows. Since the gathering and crafting cycle would amount to a very 
large step cost. 
* However if the agent has materials the agent would prefer to craft those materials into arrows by reaching the `N` state. 
* Another interesting pattern that we saw that if the agent  had a large number of 
arrows and the monster was in the ready state, it would want to go to `N` or `S` and prefer to stay
there and wait for monster to become dormant, for there is a risk of loosing all the 
arrows collected.

* The agent considered shooting from the `C` position only when the 
monster's health was lowest i.e 25. In other cases it would prefer to go right towards `E` and then hit/shoot to maximise it's chances. 
* The agent also did not prefers to go to `W` state at all and tried to remain in `N`, `S`, `E`, `C`. The reason being that the agent considers the ability to attack at `W` to be insignificant as in the states `N` or `S` it might get teleported to `E`, in which it has excellent attacking probability.
* Another pattern that we observed was that it preferred to `HIT` when monster health is maximum and `SHOOT` whenever monster health is lower. The agent also does not move once it reaches `E` it stays put and does only damaging moves.
* The agent never tries to gather material (except one case, see below) even if he is present in `S` state because the cost to gather material and craft arrow is much higher than moving to east and hitting/shooting the monster. He prefers to  teleported to `E`, in which it has excellent attacking probability.

* One interesting case was when agent tries to gather material and then craft arrows. This only happened when the agent state was (S, 0, 0, R, 25). Here the agent tries to gather material and move `N` to craft them. If the monster remains in ready state, the agent thinks of staying in the `N` state since not staying may result in losing all arrows he crafted if monster attacked.

| no of iterations | gamma|
|------------------|------|
|       125        | 0.999|
|        9         | 0.25 |

### Sample simulations
*  Steps taken from ( C, 2, 0, R, 100)
```cobol
('C', 2, 0, 'R', 100)  ->  ('N', 2, 0, 'R', 100) :  UP =  -20
('N', 2, 0, 'R', 100)  ->  ('N', 1, 1, 'R', 100) :  CRAFT =  -40
('N', 1, 1, 'R', 100)  ->  ('N', 0, 2, 'D', 100) :  CRAFT =  -60
('N', 0, 2, 'D', 100)  ->  ('C', 0, 2, 'D', 100) :  DOWN =  -80
('C', 0, 2, 'D', 100)  ->  ('E', 0, 2, 'D', 100) :  RIGHT =  -100
('E', 0, 2, 'D', 100)  ->  ('E', 0, 2, 'D', 50) :  HIT =  -120
('E', 0, 2, 'D', 50)  ->  ('E', 0, 1, 'D', 25) :  SHOOT =  -140
('E', 0, 1, 'D', 25)  ->  ('E', 0, 0, 'D', 0) :  SHOOT =  -110
```

In order to defeat the monster, the agent initially goes to `N` state to craft arrows since he has 
2 pieces of material. He uses both the material to gain maximum arrows at once. Then he travels
to east so as to defeat the monster by attacking with the highest probability. Since the monster
was in dormant state and has high health, the agent prefers to hit him with blade rather than shooting 
arrows. Once the monster health drops below 100, he shoots to end the game fast enough by shooting
arrows and maximising the reward.

* Steps taken from ( W, 0, 0, R, 100)
```cobol
('W', 0, 0, 'R', 100)  ->  ('C', 0, 0, 'D', 100) :  RIGHT =  -20
('C', 0, 0, 'D', 100)  ->  ('E', 0, 0, 'R', 100) :  RIGHT =  -40
('E', 0, 0, 'R', 100)  ->  ('E', 0, 0, 'D', 100) :  HIT =  -100
('E', 0, 0, 'D', 100)  ->  ('E', 0, 0, 'D', 100) :  HIT =  -120
('E', 0, 0, 'D', 100)  ->  ('E', 0, 0, 'R', 100) :  HIT =  -140
('E', 0, 0, 'R', 100)  ->  ('E', 0, 0, 'D', 100) :  HIT =  -200
('E', 0, 0, 'D', 100)  ->  ('E', 0, 0, 'D', 100) :  HIT =  -220
('E', 0, 0, 'D', 100)  ->  ('E', 0, 0, 'D', 50) :  HIT =  -240
('E', 0, 0, 'D', 50)  ->  ('E', 0, 0, 'R', 0) :  HIT =  -210
```

Since, the agent doesn't have any arrows and materials and the total cost to gather material and then 
craft arrows will be highly negative, it chooses a path directly to go east and hits monster with
 his blade continuously until monster health reaches zero. In any case, the agent doesn't care if he gets
 hit by monster and gets a -40 reward.

### TASKS

#### CASE 1
* As we stated before the agent does not prefer the any movement action from `E` state and does only attacking actions. Therefore, on changing any kind of movement action from `E` state wouldn't result in any any change from original policy. Hence, now too, the agent does not move after coming to the `E` position and only performs attacking actions.

#### CASE 2
This was an interesting case, since the agent the had no step cost on staying.
* It preferred to move to `W` if it was at `C` at high monster health, The agent did not follow this only when the monster was at the lowest health and it had arrows left. The state of the monster had no effect on this decision.
* If the agent reached `W` it would stay there indefinitely.
* From `E` when the monster was at the lowest health and the agent had arrows left, it decided to shoot otherwise it preferred to move to `C`, in the hope to move towards `W` later on.  The state of the monster had no effect on this decision also.
* If the agent is located at `N` or `S`:
    * If the monster is `R` the agent stays there
    * Otherwise it has a choice to stay at `N` or `S` now and after being teleported to `E` move towards `W` or pay the price now by actively moving towards `W` via `C` and keep staying there.
    * The agent prefers the former action when monster's health is low as from east the killing chance is higher but on higher health it is better to take it safe at go to 'W'

#### CASE 3

* The agent is extremely short sighted in this case, since the value of gamma is low. the agent is not concerned about the step cost it would accumulate down the line.
* Therefore the agent does not differ between states that much and minute changes in the order of states in the program completely changes the policy.
* Since the agent does not get reward for decreasing the monster health, it only gets reward on completely killing the monster and that reward at monsters health 100 is so far away approximately equal to zero due to being multiplied by gamma. So if the agent were to start at the monster at high health, it would be akin to a game in which it just received -40 reward in some near time and +50 reward at some far time, therefore for an agent with gamma of 0.25, the objective of the game is to basically stay away from the negative reward which it does by moving to `N`, `S`, `W` and staying there.
* Examples which show above behaviour are (C, 1, 1, D, 100), (W, 1, 1, D, 100), (W, 1, 1, R, 75) etc.

* The agent only tries to shoot or hit from `C` when the health of monster is generally 25 (Some cases also contain 50 health.) This is because the agent thinks much only about present and he fears to attack from center on high monster health since monster may attack him and would face a much larger than the step cost. The gamma being low also means that the agent now hits more often from `C` as compared to the earlier version where if highly preferred `E` as it is more concerned about immediate reward. Another change is that at `W` it sometimes decides to hit for the reason mentioned above. 

* Since `E` has a higher probability for damaging monster, the agent chooses to attack upto 75 health.
* Even with maximum quantity of arrows , the agent never chooses to attack monster in center state (with health > 50) and in east state (with health > 75). The reason is same as stated above.

* Similar kind of behaviour is shown in `N` and `S`. Here agent only tries to stay away from monster as much as possible. He chooses to craft arrows and gather material since they would never teleport him to east. The agent only chooses to go for attack only if monster has low health between 25 to 50.
* Since west is the safest place for the agent (each action has 100% probability for reaching desired state), he chooses to attack the monster from that state if he has arrows or otherwise chooses to stay.

