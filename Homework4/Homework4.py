import time
from Monte_Carlo import Monte_Carlo_Simulation
from Binomial import Binomial_Tree
from Binomial_Bonus1 import Binomial_Tree_Bonus
from Bonus2 import Bonus2

S_t = 50
r = 0.1
q = 0
sigma = 0.4
t = 0
T = 0.25
Sim_n = 10000
Rep_n = 20


for n in [100, 300]:
    for S_max_t in [50, 60, 70]:
        
        print("-" * 39)
        print("         n = {}, S_max_t = {}         ".format(n, S_max_t))
        print("-" * 39)
        
        # 1. Monte Carlo
        time1 = time.time()
        Monte_Carlo_mean, Monte_Carlo_std = Monte_Carlo_Simulation(S_t, r, q, sigma, t, T, S_max_t, n, Sim_n, Rep_n)
        time2 = time.time()

        print('1. Monte Carlo Simulation for European     Spend Time: {}'.format(round(time2 - time1, 6)))
        print('Mean: {}       Std: {}'.format(round(Monte_Carlo_mean, 4), round(Monte_Carlo_std, 4)))
        print('95% Confidence Interval: {} ~ {}'.format(round(Monte_Carlo_mean - 2 * Monte_Carlo_std, 4), round(Monte_Carlo_mean + 2 * Monte_Carlo_std, 4)))
        print()

        # 2. CRR Binomial Basic Requirement
        time3 = time.time()
        Binomial_European_value = Binomial_Tree(S_t, r, q, sigma, t, T, S_max_t, n, "European")
        Binomial_American_value = Binomial_Tree(S_t, r, q, sigma, t, T, S_max_t, n, "American")
        time4 = time.time()

        print('2. CRR Binomial Tree      Spend Time: {}'.format(round(time4 - time3, 6)))
        print('European Option: {}'.format(round(Binomial_European_value, 4)))
        print('American Option: {}'.format(round(Binomial_American_value, 4)))
        print()

        # 3. Bonus 1
        time5 = time.time()
        Bonus1_European_value = Binomial_Tree_Bonus(S_t, r, q, sigma, t, T, S_max_t, n, "European")
        Bonus1_American_value = Binomial_Tree_Bonus(S_t, r, q, sigma, t, T, S_max_t, n, "American")
        time6 = time.time()

        print('3. Bonus 1      Spend Time: {}'.format(round(time6 - time5, 6)))
        print('European Option: {}'.format(round(Bonus1_European_value, 4)))
        print('American Option: {}'.format(round(Bonus1_American_value, 4)))

# 4. Bonus 2
n = 1000
S_max_t = 50

print("-" * 39)
print("         n = {}, S_max_t = {}         ".format(n, S_max_t))
print("-" * 39)

time7 = time.time()
Bonus2_European_value, Bonus2_American_value = Bonus2(S_t, r, q, sigma, t, T, n)
time8 = time.time()

print('4. Bonus 2      Spend Time: {}'.format(round(time8 - time7, 6)))
print('European Option: {}'.format(round(Bonus2_European_value, 4)))
print('American Option: {}'.format(round(Bonus2_American_value, 4)))