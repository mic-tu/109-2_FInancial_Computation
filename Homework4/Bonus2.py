import numpy as np

def Bonus2(S_t, r, q, sigma, t1, T2, n):
    delta_t = (T2 - t1) / n
    u = np.exp(sigma * (delta_t ** 0.5))
    d = 1 / u
    mu =  np.exp((r - q) * delta_t)
    p = 1 - ((mu * u - 1) / (mu * u - mu * d))

    eur = np.zeros((n + 1, n + 1))  # European
    ame = np.zeros((n + 1, n + 1))  # American
    for i in range(n + 1):
        for j in range(n + 1 - i):
            eur[i][j] = (u ** j - 1)
            ame[i][j] = (u ** j - 1)

    for i in range(1, n + 1):
        for j in range(n + 1 - i):
            if j == 0:
                eur[i][j] = ((1 - p) * eur[i - 1][0] + p * eur[i - 1][1])
                ame[i][j] = max(((1 - p) * ame[i - 1][0] + p * ame[i - 1][1]), ame[i][j])
            else:
                eur[i][j] = ((1 - p) * eur[i - 1][j - 1] + p * eur[i - 1][j + 1])
                ame[i][j] = max(((1 - p) * ame[i - 1][j - 1] + p * ame[i - 1][j + 1]), ame[i][j])
    return eur[n][0] * S_t, ame[n][0] * S_t