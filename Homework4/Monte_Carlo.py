import numpy as np

def Monte_Carlo_Simulation(S_t, r, q, sigma, t, T, S_max_t, n, Sim_n = 10000, Rep_n = 20):
    delta_t = (T - t) / n
    Rep_payoff = []
    for time in range(Rep_n):  # 第幾次模擬
        Sim_rand = np.random.normal(0, 1, size=(Sim_n, n))
        Sim_value = np.zeros((Sim_n, n + 2))
        Sim_value[:, 0] = S_max_t
        Sim_value[:, 1] = S_t
        for i in range(n):  # 第幾行
            Sim_value[:, i + 2] = np.exp(np.log(Sim_value[:, i + 1]) + (r - q - (sigma ** 2) / 2) * delta_t + Sim_rand[:, i] * (delta_t ** 0.5) * sigma)
        Rep_payoff.append(np.mean(np.max(Sim_value, axis=1) - Sim_value[:, -1]) * np.exp(-r * (T - t)))
    Rep_payoff = np.array(Rep_payoff)
    return np.mean(Rep_payoff), np.std(Rep_payoff)
