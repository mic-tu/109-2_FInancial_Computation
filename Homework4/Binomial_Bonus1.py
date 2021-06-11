import numpy as np
import copy

def Binomial_Tree_Bonus(S_t, r, q, sigma, t1, T2, S_max_t, n, option_type="European"):
    # 1. 計算u, d, p
    delta_t = (T2 - t1) / n
    u = np.exp(sigma * (delta_t ** 0.5))
    d = 1 / u
    p = (np.exp((r - q) * delta_t)- d) / (u - d)

    # 3. 建立每個點的股價
    # 2-1. 計算 Tree 所有出現的股價: 若有n期，則有2n+1個可能股價
    prices = np.concatenate(([S_t * (u ** x) for x in range(n, -1, -1)],
                            [S_t * (d ** x) for x in range(1, n + 1)]), axis=None)
    # 2-2. 建立每個點的股價: 兩層list，第一層是第幾期、第二層是那一期每個node的股價
    S_t_list = []
    for period in range(n + 1):
        S_t_list.append([prices[x] for x in range(n - period, n + period + 1, 2)])
    
    # 3. 建立每個點的S_max_list
    S_max_list = []  # 三層list，第一層S_max_list是第幾期、第二層period_max_list是那一期每個node、第三層node_max_list是每個node的S_max
    price_value = np.where(prices <= S_max_t, S_max_t, prices)
    for period in range(n + 1):  # 第幾期
        period_max_list = []
        for node in range(period + 1):  # 第幾個node
            if node > period // 2:
                node_max_list = price_value[(n - period + node):n + 1].tolist()
            else:
                node_max_list = price_value[(n - period + node):n - period + node * 2 + 1].tolist()
            period_max_list.append(node_max_list)
        S_max_list.append(period_max_list)
        
    # 4. 計算最後一期價格、每一期Early exercise的價格
    S_value_list = copy.deepcopy(S_max_list)
    for period in range(n + 1):  # 第幾期
        for node in range(period + 1):  # 第幾個node
            for x in range(len(S_value_list[period][node])):
                S_value_list[period][node][x] = S_value_list[period][node][x] - S_t_list[period][node]

    # 5. 計算選擇權價值：使用函數count_option_value(option_type)，option_type='American'/'European'
    def count_option_value(option_type):
        option_value = copy.deepcopy(S_value_list)
        for period in range(n - 1, -1, -1):  # 第幾期(Backward)
            for node in range(period + 1):  # 第幾個node
                for x in range(len(S_max_list[period][node])):  # 第x個max_value
                    price_without_discount = 0
                    # u
                    if S_max_list[period][node][x] in S_max_list[period + 1][node]:  # If there is a Smax equal to Smax1, find the put value for that Smax.
                        index = S_max_list[period + 1][node].index(S_max_list[period][node][x])
                        price_without_discount += option_value[period + 1][node][index] * p
                    else:  # If there is not, find the put value for Smax equal to Stu.
                        index = S_max_list[period + 1][node].index(S_t_list[period + 1][node])
                        price_without_discount += option_value[period + 1][node][index] * p
                    # d
                    if S_max_list[period][node][x] in S_max_list[period + 1][node + 1]:  # If there is a Smax equal to Smax1, find the put value for that Smax.
                        index = S_max_list[period + 1][node + 1].index(S_max_list[period][node][x])
                        price_without_discount += option_value[period + 1][node + 1][index] * (1 - p)
                    else:  # If there is not, find the put value for Smax equal to Stu.
                        index = S_max_list[period + 1][node + 1].index(S_t_list[period + 1][node])
                        price_without_discount += option_value[period + 1][node + 1][index] * (1 - p)
                    if option_type == 'American':
                        option_value[period][node][x] = max(price_without_discount * np.exp(-r * delta_t), option_value[period][node][x])
                    else:
                        option_value[period][node][x] = price_without_discount * np.exp(-r * delta_t)
        return option_value
    
    return count_option_value(option_type)[0][0][0]