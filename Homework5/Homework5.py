import pandas as pd
import time
from Monte_Carlo import Monte_Carlo_Simulation
from Binomial import Binomial_Tree
from Bonus1 import Binomial_Tree_Bonus1
from Bonus2 import Binomial_Tree_Interpolation, Binomial_Tree_Binary

# Basic Requirement 1.
S_t = 50
K = 50
r = 0.1
q = 0.05
sigma = 0.2
t = 0.25
T_minus_t = 0.25  # T = 0.5
M = 100
n = 100
S_ave_t = 60
Sim_n = 10000
Rep_n = 20

print("Basic Requirement")
t1 = time.time()
monte_carlo_mean, monte_carlo_std = Monte_Carlo_Simulation(S_t, K, r, q, sigma, t, T_minus_t, n, S_ave_t,  Sim_n, Rep_n)
t2 = time.time()
print("1. Monte Carlo             Spend Time = {}".format(round(t2 - t1, 6)))
print("95% Confidence Interval: {} ~ {}".format(round(monte_carlo_mean - 2 * monte_carlo_std, 4), round(monte_carlo_mean + 2 * monte_carlo_std, 4)))
print("-" * 40)

t3 = time.time()
eur_binomial, ame_binomial = Binomial_Tree(S_t, K, r, q, sigma, t, T_minus_t, M, n, S_ave_t)
t4 = time.time()
print("2. Binomial Tree           Spend Time = {}".format(round(t4 - t3, 6)))
print("European Call: {}".format(round(eur_binomial, 4)))
print("American Call: {}".format(round(ame_binomial, 4)))
print("-" * 40)

print("Bonus 2")
# Bonus 2 Binary
t5 = time.time()
eur_binary, ame_binary = Binomial_Tree_Binary(S_t, K, r, q, sigma, t, T_minus_t, M, n, S_ave_t)
t6 = time.time()
print("3. Binomial Binary         Spend Time = {}".format(round(t6 - t5, 6)))
print("European Call: {}".format(round(eur_binary, 4)))
print("American Call: {}".format(round(ame_binary, 4)))
print("-" * 40)

# Bonus 2 Interpolation
t7 = time.time()
eur_interpolation, ame_interpolation = Binomial_Tree_Interpolation(S_t, K, r, q, sigma, t, T_minus_t, M, n, S_ave_t)
t8 = time.time()
print("4. Binomial Interpolation  Spend Time = {}".format(round(t8 - t7, 6)))
print("European Call: {}".format(round(eur_interpolation, 4)))
print("American Call: {}".format(round(ame_interpolation, 4)))
print("-" * 40)

# 印出時間
spend_time = pd.DataFrame([["Sequential search", t4 - t3], ["Binary search", t6 - t5], ["Linear interpolation method", t8 - t7]], columns = ["Method", "Spend Time"]).set_index("Method")
print("Bonus 2")
print(spend_time.sort_values("Spend Time"))
print("-" * 40)
'''
# Bonus 1
print("Bonus 1")
Ms = [50, 100, 150, 200, 250, 300, 350, 400]
result = []
for M in Ms:
    t9 = time.time()
    linearly_eur = round(Binomial_Tree_Interpolation(S_t, K, r, q, sigma, t, T_minus_t, M, n, S_ave_t)[0], 4)
    linearly_ame = round(Binomial_Tree_Interpolation(S_t, K, r, q, sigma, t, T_minus_t, M, n, S_ave_t)[1], 4)
    t10 = time.time()
    print("Finish linearly         M = {}, Spend Time: {}".format(M, round(t10 - t9, 6)))
    logarithmically_eur = round(Binomial_Tree_Bonus1(S_t, K, r, q, sigma, t, T_minus_t, M, n, S_ave_t)[0], 4)
    logarithmically_ame = round(Binomial_Tree_Bonus1(S_t, K, r, q, sigma, t, T_minus_t, M, n, S_ave_t)[1], 4)
    t11 = time.time()
    print("Finish logarithmically  M = {}, Spend Time: {}".format(M, round(t11 - t10, 6)))
    result.append([linearly_eur, logarithmically_eur, linearly_ame, logarithmically_ame])

# 印出結果
comparion = pd.DataFrame(result).T
comparion.index = ["European(linearly)", "European(logarithmically)", "American(linearly)", "American(logarithmically)"]
comparion.columns = ["M = {}".format(M) for M in Ms]
print(comparion)
'''