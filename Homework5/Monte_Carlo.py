import numpy as np

def Monte_Carlo_Simulation(S_t, K, r, q, sigma, t, T_minus_t, n, S_ave_t,  Sim_n = 10000, Rep_n = 20):
    delta_t = T_minus_t / n
    T = t + T_minus_t
    Rep_payoff = []
    for time in range(Rep_n):  # 第幾次模擬
        Sim_rand = np.random.normal(0, 1, size=(Sim_n, n))
        Sim_value = np.ones((Sim_n, int((n * T) / T_minus_t) + 1)) * S_ave_t
        Sim_value[:, 0] = S_t
        for i in range(n):  # 第幾行
            Sim_value[:, i + 1] = np.exp(np.log(Sim_value[:, i]) + (r - q - (sigma ** 2) / 2) * delta_t + Sim_rand[:, i] * (delta_t ** 0.5) * sigma)
        mean = np.mean(Sim_value, axis = 1) - K
        mean[mean < 0] = 0
        Rep_payoff.append(mean * np.exp(- r * T_minus_t))
    Rep_payoff = np.mean(np.array(Rep_payoff), axis = 1)
    return np.mean(Rep_payoff), np.std(Rep_payoff)

if __name__ == '__main__':
    import time

    S_t = 50
    K = 50
    r = 0.1
    q = 0.05
    sigma = 0.4
    t = 0.25
    T_minus_t = 0.25
    n = 100
    S_ave_t = 50
    Sim_n = 10000
    Rep_n = 20
    
    time1 = time.time()
    result = Monte_Carlo_Simulation(S_t, K, r, q, sigma, t, T_minus_t, n, S_ave_t, Sim_n, Rep_n)
    time2 = time.time()

    print(result[0] - 2 * result[1], result[0] + 2 * result[1])
    print(time2 - time1)