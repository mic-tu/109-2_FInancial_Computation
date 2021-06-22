import pandas as pd
import time
from Monte_Carlo import Monte_Carlo_Simulation
from Binomial import Binomial_Tree
from Bonus2 import Binomial_Tree_Interpolation, Binomial_Tree_Binary

def demo_result(S_t, K, r, q, sigma, t, T_minus_t, n, S_ave_t,  Sim_n, Rep_n):
    # Basic Requirement 1.
    print("Basic Requirement")
    t1 = time.time()
    monte_carlo_mean, monte_carlo_std = Monte_Carlo_Simulation(S_t, K, r, q, sigma, t, T_minus_t, n, S_ave_t,  Sim_n, Rep_n)
    t2 = time.time()
    print("1. Monte Carlo             Spend Time = {:.6f}".format(t2 - t1))
    print("95% Confidence Interval: {:.4f} ~ {:.4f}".format(monte_carlo_mean - 2 * monte_carlo_std, monte_carlo_mean + 2 * monte_carlo_std))
    print("-" * 40)

    t3 = time.time()
    eur_binomial, ame_binomial = Binomial_Tree(S_t, K, r, q, sigma, t, T_minus_t, M, n, S_ave_t)
    t4 = time.time()
    print("2. Binomial Tree           Spend Time = {:.6f}".format(t4 - t3))
    print("European Call: {:.4f}".format(eur_binomial))
    print("American Call: {:.4f}".format(ame_binomial))
    print("-" * 40)

    print("Bonus 2")
    # Bonus 2 Binary
    t5 = time.time()
    eur_binary, ame_binary = Binomial_Tree_Binary(S_t, K, r, q, sigma, t, T_minus_t, M, n, S_ave_t)
    t6 = time.time()
    print("3. Binomial Binary         Spend Time = {}".format(round(t6 - t5, 6)))
    print("European Call: {:.4f}".format(eur_binary))
    print("American Call: {:.4f}".format(ame_binary))
    print("-" * 40)

    # Bonus 2 Interpolation
    t7 = time.time()
    eur_interpolation, ame_interpolation = Binomial_Tree_Interpolation(S_t, K, r, q, sigma, t, T_minus_t, M, n, S_ave_t)
    t8 = time.time()
    print("4. Binomial Interpolation  Spend Time = {}".format(round(t8 - t7, 6)))
    print("European Call: {:.4f}".format(eur_interpolation))
    print("American Call: {:.4f}".format(ame_interpolation))
    print("-" * 40)

    # 印出時間
    spend_time = pd.DataFrame([["Sequential search", t4 - t3], ["Binary search", t6 - t5], ["Linear interpolation method", t8 - t7]], columns = ["Method", "Spend Time"]).set_index("Method")
    print("Bonus 2")
    print(spend_time.sort_values("Spend Time"))

S_t = 50
K = 50
r = 0.1
q = 0.05
sigma = 0.8
T_minus_t = 0.25  # T = 0.5
M = 100
n = 100
S_ave_t = 50
Sim_n = 10000
Rep_n = 20
print("t = 0")
demo_result(S_t, K, r, q, sigma, 0, T_minus_t, n, S_ave_t,  Sim_n, Rep_n)
print("-" * 40)
print("t = 0.25")
demo_result(S_t, K, r, q, sigma, 0.25, T_minus_t, n, S_ave_t,  Sim_n, Rep_n)
