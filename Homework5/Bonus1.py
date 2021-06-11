import numpy as np

def Binomial_Tree_Bonus1(S_t, K, r, q, sigma, t, T_minus_t, M, n, S_ave_t):
    delta_t = T_minus_t / n
    T = T_minus_t + t
    u = np.exp(sigma * (delta_t ** 0.5))
    d = 1 / u
    p = (np.exp((r - q) * delta_t) - d) / (u - d)

    # Step 1 & Step 2
    A = np.zeros((n + 1, n + 1, M + 1))
    eur_C = np.zeros((n + 1, n + 1, M + 1))  # European call
    ame_C = np.zeros((n + 1, n + 1, M + 1))  # American call
    for i in range(n + 1):
        for j in range(i + 1):
            A_max = (S_ave_t * (t * n / T_minus_t + 1) + (S_t * u) * (1 - u ** (i - j)) / (1 - u) + (S_t * (u ** (i - j)) * d) * (1 - d ** j) / (1 - d)) / (i + t * n / T_minus_t + 1)
            A_min = (S_ave_t * (t * n / T_minus_t + 1) + (S_t * d) * (1 - d ** j) / (1 - d) + (S_t * u * d ** j) * (1 - u ** (i - j)) / (1 - u)) / (i + t * n / T_minus_t + 1)
            for k in range(M + 1):
                A[i][j][k] = np.exp(((M - k) / M) * np.log(A_max) + (k / M) * np.log(A_min))

    # Step 3
    for j in range(n + 1):
        for k in range(M + 1):
            eur_C[n][j][k] = max(A[n][j][k] - K, 0)
            ame_C[n][j][k] = max(A[n][j][k] - K, 0)
    
    # Step 4
    for i in range(n - 1, -1, -1):
        for j in range(i + 1):
            for k in range(M + 1):
                A_u = (A[i][j][k] * (i + t * n / T_minus_t + 1) + S_t * (u ** (i + 1 - j)) * (d ** j)) / (i + t * n / T_minus_t + 2)
                if A[i + 1][j][0] == A[i + 1][j][M]:  # 最上面或最下面
                    eur_C_u = eur_C[i + 1][j][0]
                    ame_C_u = ame_C[i + 1][j][0]
                elif A[i + 1][j][M] > A_u:  # 跟最後一個一樣
                    eur_C_u = eur_C[i + 1][j][M]
                    ame_C_u = ame_C[i + 1][j][M]
                else:
                    k_u = list(A[i + 1][j]).index(A[i + 1][j][A[i + 1][j] <= A_u][0])
                    w_u = (A[i + 1][j][k_u - 1] - A_u) / (A[i + 1][j][k_u - 1] - A[i + 1][j][k_u])
                    eur_C_u = w_u * eur_C[i + 1][j][k_u] + (1 - w_u) * eur_C[i + 1][j][k_u - 1]
                    ame_C_u = w_u * ame_C[i + 1][j][k_u] + (1 - w_u) * ame_C[i + 1][j][k_u - 1]
                
                A_d = (A[i][j][k] * (i + t * n / T_minus_t + 1) + S_t * (u ** (i - j)) * (d ** (j + 1))) / (i + t * n / T_minus_t + 2)
                if A[i + 1][j + 1][0] == A[i + 1][j + 1][M]:
                    eur_C_d = eur_C[i + 1][j + 1][0]
                    ame_C_d = ame_C[i + 1][j + 1][0]
                elif A[i + 1][j + 1][M] > A_d:
                    eur_C_d = eur_C[i + 1][j + 1][M]
                    ame_C_d = ame_C[i + 1][j + 1][M]
                else:
                    k_d = list(A[i + 1][j + 1]).index(A[i + 1][j + 1][A[i + 1][j + 1] <= A_d][0])
                    w_d = (A[i + 1][j + 1][k_d - 1] - A_d) / (A[i + 1][j + 1][k_d - 1] - A[i + 1][j + 1][k_d])
                    eur_C_d = w_d * eur_C[i + 1][j + 1][k_d] + (1 - w_d) * eur_C[i + 1][j + 1][k_d - 1]
                    ame_C_d = w_d * ame_C[i + 1][j + 1][k_d] + (1 - w_d) * ame_C[i + 1][j + 1][k_d - 1]
                eur_C[i][j][k] = (p * eur_C_u + (1 - p) * eur_C_d) * np.exp(-r * delta_t)
                ame_C[i][j][k] = max(A[i][j][k] - K, (p * ame_C_u + (1 - p) * ame_C_d) * np.exp(-r * delta_t))
    
    return eur_C[0][0][0], ame_C[0][0][0]

if __name__ == '__main__':
    S_t = 50
    K = 50
    r = 0.1
    q = 0.05
    sigma = 0.4
    t = 0.25
    T_minus_t = 0.25
    M = 100
    n = 100
    S_ave_t = 50
    Sim_n = 10000
    Rep_n = 20
    result = Binomial_Tree_Bonus1(S_t, K, r, q, sigma, t, T_minus_t, M, n, S_ave_t)
    print(result)

