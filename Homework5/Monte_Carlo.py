import numpy as np

def Monte_Carlo_Simulation(S_t, K, r, q, sigma, t, T_minus_t, n, S_ave_t,  Sim_n = 10000, Rep_n = 20):
    delta_t = T_minus_t / n
    T = t + T_minus_t
    std = (delta_t ** 0.5) * sigma
    Rep_payoff = []
    for time in range(Rep_n):  # 第幾次模擬
        Sim_rand = np.random.normal(0, 1, size=(Sim_n, n))
        Sim_value = np.zeros((Sim_n, n + 1))
        Sim_value[:, 0] = S_t
        for i in range(n):  # 第幾期
            Sim_value[:, i + 1] = np.exp(np.log(Sim_value[:, i]) + (r - q - (sigma ** 2) / 2) * delta_t + Sim_rand[:, i] * std)
        Sim_value = (S_ave_t * ((n * t) / T_minus_t + 1) - S_t + np.sum(Sim_value, axis = 1)) / ((n * T) / T_minus_t + 1)
        Rep_payoff.append(np.exp(-r * T_minus_t) * np.mean(np.maximum(Sim_value - K, 0)))
    return np.mean(Rep_payoff), np.std(Rep_payoff)

if __name__ == '__main__':
    import time

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
    
    t1 = time.time()
    monte_carlo_mean, monte_carlo_std = Monte_Carlo_Simulation(S_t, K, r, q, sigma, 0, T_minus_t, n, S_ave_t,  Sim_n, Rep_n)
    t2 = time.time()
    print("1. t = 0      Spend Time = {:.6f}".format(t2 - t1))
    print("95% Confidence Interval: {:.4f} ~ {:.4f}".format(monte_carlo_mean - 2 * monte_carlo_std, monte_carlo_mean + 2 * monte_carlo_std))

    t3 = time.time()
    monte_carlo_mean, monte_carlo_std = Monte_Carlo_Simulation(S_t, K, r, q, sigma, 0.25, T_minus_t, n, S_ave_t,  Sim_n, Rep_n)
    t4 = time.time()
    print("2. t = 0.25   Spend Time = {:.6f}".format(t4 - t3))
    print("95% Confidence Interval: {:.4f} ~ {:.4f}".format(monte_carlo_mean - 2 * monte_carlo_std, monte_carlo_mean + 2 * monte_carlo_std))