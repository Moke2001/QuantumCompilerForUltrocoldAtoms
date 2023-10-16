import numpy as np


def judge_phase(g1, g2):
    moment = []
    g = g1 / g2
    for i in range(len(g)):  # 遍历行
        for j in range(len(g[i])):  # 遍历列
            if not np.isinf(g[i][j]) and abs(g[i][j])>0.00001:
                moment.append(g[i][j])

    result = 0
    for i in range(len(moment)):
        for j in range(len(moment)):
            result = result+abs(moment[i] - moment[j])

    if result < 0.0001:
        return True
    else:
        return False