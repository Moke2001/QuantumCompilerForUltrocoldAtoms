import numpy as np


def global_arctan(a, b):

    ## 对a==0的情况特殊处理
    global x
    if a == 0:
        x_0 = np.pi / 2
    else:
        x_0 = np.arctan(abs(b / a))

    ## 分类讨论角度所在的区间
    if a >= 0 and b >= 0:
        x = x_0
    elif a < 0 and b >= 0:
        x = np.pi - x_0
    elif a < 0 and b < 0:
        x = np.pi + x_0
    elif a >= 0 and b < 0:
        x = 2 * np.pi - x_0

    ## 返回结果
    return x