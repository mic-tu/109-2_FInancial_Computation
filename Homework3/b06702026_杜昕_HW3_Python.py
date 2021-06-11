import numpy as np

def cholesky(matrix_C, n):
    matrix_ = np.zeros([n, n])
    # Step 1
    matrix_[0, 0] = np.sqrt(matrix_C[0, 0])
    for j in range(1, n):
        matrix_[0, j] = matrix_C[0, j] / matrix_[0, 0]
    # Step 2 ~ 4
    for i in range(1, n):
        matrix_[i, i] = np.sqrt(matrix_C[i, i] - sum([matrix_[j, i] ** 2 for j in range(i)]))
        for j in range(i+1, n):
            matrix_[i, j] = (matrix_C[i, j] - sum([matrix_[k, i] * matrix_[k, j] for k in range(i)])) / matrix_[i, i]
    return matrix_

def count_payoff():
    payoff = np.max(Si_T, axis=1) - K
    payoff = np.where(payoff<0, 0, payoff)  # 負數取0
    payoff = np.array(payoff * np.exp(-r * T))
    return np.mean(payoff.flatten())

def print_result(Payoff):
    mean = np.mean(Payoff)
    std = np.std(Payoff)
    print("Option Value = {}, Std = {}".format(round(mean, 4), round(std, 4)))
    print('95% Confidence Interval = {} ~ {}'.format(round(mean - 2 * std, 4), round(mean + 2 * std, 4)))

# 1. 設定參數
K = 100
r = 0.1
T = 0.5
Sim_n = 10000
Rep_n = 20

input_question = True
while input_question:
    question = input("要看的測資是？(輸入1/2/3)：")
    if question == "1":
        n = 2
        cov_matrix = np.matrix([[1, 1], [1, 1]])
        input_question = False
    elif question == "2":
        n = 2
        cov_matrix = np.matrix([[1, -1], [-1, 1]])
        input_question = False
    elif question == "3":
        n = 5
        cov_matrix = np.matrix([[1, 0.5, 0.5, 0.5, 0.5],
                                [0.5, 1, 0.5, 0.5, 0.5],
                                [0.5, 0.5, 1, 0.5, 0.5],
                                [0.5, 0.5, 0.5, 1, 0.5],
                                [0.5, 0.5, 0.5, 0.5, 1]
                                ])
        input_question = False
    else:
        print("輸入有誤，", end='')

S_i0 = np.array([95 for i in range(n)])  # 起始價格
q_i = np.array([0.05 for i in range(n)])  # 股利率
sigma_i = np.array([0.5 for i in range(n)])  # sigma

# 2. 計算矩陣C
matrix_C = np.zeros([n, n])
for i in range(n):
    for j in range(n):
        matrix_C[i, j] = cov_matrix[i, j] * sigma_i[i] * sigma_i[j] * T

# 3. 計算矩陣A
matrix_A = cholesky(matrix_C, n)

 # 4. 抽樣並算出Payoff
# 測資1、2印出Basic Requirement；測資3印出Basic Requirement跟Bonus
if question == "1" or question == "2":
    # 測資1: 11.9759
    # 測資2: 23.9518
    mean_lnSi_T = np.log(S_i0) + (r - q_i - sigma_i ** 2 / 2) * T
    Rep_payoff_Basic = []
    for num in range(Rep_n):
        zi_b = np.matrix(np.random.normal(0, 1, size=(Sim_n, n)))
        # 4-1. Basic Requirement
        ri_b = np.dot(zi_b, matrix_A)
        Si_T = np.exp(ri_b + mean_lnSi_T)
        Rep_payoff_Basic.append(count_payoff())
    Rep_payoff_Basic = np.array(Rep_payoff_Basic)
    print("測資{} Basic Requirement".format(question))
    print_result(Rep_payoff_Basic)
else:
    # 測資3: 30.3852
    mean_lnSi_T = np.log(S_i0) + (r - q_i - sigma_i ** 2 / 2) * T
    Rep_payoff_Basic = []
    Rep_payoff_Bonus1 = []
    Rep_payoff_Bonus2 = []
    for num in range(Rep_n):

        # 4-1. Basic Requirement
        zi_b = np.matrix(np.random.normal(0, 1, size=(Sim_n, n)))
        ri_b = np.dot(zi_b, matrix_A)
        Si_T = np.exp(ri_b + mean_lnSi_T)
        Rep_payoff_Basic.append(count_payoff())

        zi = np.array(np.random.normal(0, 1, size=(Sim_n//2, n)))
        # 4-2. Bonus 1
        zi_1 = np.matrix(np.append(zi, -zi, axis=0))
        zi_1 /= np.std(zi_1)
        ri_1 = np.dot(zi_1, matrix_A)
        Si_T = np.exp(ri_1 + mean_lnSi_T)
        Rep_payoff_Bonus1.append(count_payoff())

        # 4-3. Bonus 2
        zi_2 = np.array(np.append(zi, -zi, axis=0))
        zi_2 /= np.std(zi_2)
        zi_coff = np.corrcoef([zi_2[:, a] for a in range(n)])
        matrix_B = cholesky(zi_coff, n)
        ri_2 = np.dot(np.matrix(zi_2), np.dot(np.linalg.inv(matrix_B), matrix_A))
        Si_T = np.exp(ri_2 + mean_lnSi_T)
        Rep_payoff_Bonus2.append(count_payoff())

    Rep_payoff_Basic = np.array(Rep_payoff_Basic)
    Rep_payoff_Bonus1 = np.array(Rep_payoff_Bonus1)
    Rep_payoff_Bonus2 = np.array(Rep_payoff_Bonus2)

    print("測資{} Basic Requirement".format(question))
    print_result(Rep_payoff_Basic)

    print("測資{} Bonus 1".format(question))
    print_result(Rep_payoff_Bonus1)

    print("測資{} Bonus 2".format(question))
    print_result(Rep_payoff_Bonus2)