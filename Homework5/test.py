import numpy as np
import math

def Binomial_Tree_Binary(S_t, K, r, q, sigma, t, T_minus_t, M, n, S_ave_t):
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
                A[i][j][k] = ((M - k) / M) * A_max + (k / M) * A_min

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
                    k_u = M // 2
                    times = 1
                    while True:
                        if A[i + 1][j][k_u - 1] >= A_u and A_u >= A[i + 1][j][k_u]:
                            break
                        elif A[i + 1][j][k_u - 1] < A_u:
                            k_u -= math.ceil(M * 2 ** -times)
                        else:
                            k_u += math.ceil(M * 2 ** -times)
                        times += 1
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
                    k_d1 = math.ceil((A[i + 1][j + 1][0] - A_d) / (A[i + 1][j + 1][0] - A[i + 1][j + 1][-1]) * M)
                    print(k_d1, A[i + 1][j + 1][k_d1 - 1], A[i + 1][j + 1][k_d1], A_d)
                    k_d = M // 2
                    times = 1
                    if abs(A[i + 1][j + 1][0] - A_d) <= 10 ** -8 :
                        k_d = 0
                    elif A[i + 1][j + 1][M] == A_d:
                        k_d = M
                    else:
                        while True:
                            if A[i + 1][j + 1][k_d - 1] >= A_d and A_d >= A[i + 1][j + 1][k_d]:
                                break
                            elif A[i + 1][j + 1][k_d] <= A_d:
                                k_d -= math.ceil(M * 2 ** -times)
                            else:
                                k_d += math.ceil(M * 2 ** -times)
                            times += 1
                    print(k_d, A[i + 1][j + 1][k_d - 1], A[i + 1][j + 1][k_d], A_d)
                    print()

                    


if __name__ == '__main__':
    S_t = 50
    K = 50
    r = 0.1
    q = 0.05
    sigma = 0.8
    t = 0.25
    T_minus_t = 0.25
    M = 10
    n = 4
    S_ave_t = 50
    result = Binomial_Tree_Binary(S_t, K, r, q, sigma, t, T_minus_t, M, n, S_ave_t)

