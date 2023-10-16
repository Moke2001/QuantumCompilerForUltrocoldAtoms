import numpy as np

from Compiler.SingleDecompose.Tool.global_arctan import global_arctan


def normal(x):
    if np.abs(x) > 1:
        if x > 0:
            x = 1
        else:
            x = -1
    return x

def single_decompose_0(U, num):
    ## 将量子门元素记录下来
    a = U[0][0]
    c = U[1][0]
    d = U[1][1]
    a1 = normal(np.real(U[0][0]))
    a2 = normal(np.imag(U[0][0]))
    b1 = normal(np.real(U[0][1]))
    b2 = normal(np.imag(U[0][1]))
    c1 = normal(np.real(U[1][0]))
    c2 = normal(np.imag(U[1][0]))
    d1 = normal(np.real(U[1][1]))
    d2 = normal(np.imag(U[1][1]))

    ## 如果第一个元素为0
    if np.abs(a) < 0.0001:
        theta = np.pi

        ## c2=0的情况需要单独讨论
        if c2 == 0:
            if c1 >= 0:
                wc = 0
            elif c1 < 0:
                wc = np.pi
        else:
            wc = np.arcsin(c2)

        ## b2=0的情况需要单独讨论
        if b2 == 0:
            if b1 > 0:
                wb = np.pi
            elif b1 <= 0:
                wb = 0
        else:
            wb = np.arcsin(-b2)

        ## 计算结果
        delta = (wc + wb) / 2
        beta = 0
        alpha = wc - wb

    ## 如果第三个元素为0
    elif np.abs(c) < 0.0001:
        theta = 0

        wa=global_arctan(a1,a2)

        ## d2=0需要单独考虑
        wd=global_arctan(d1,d2)

        ## 计算结果
        delta = (wa + wd) / 2
        beta = 0
        alpha = wd - wa

    ## 正常情况
    else:
        theta = 2 * np.arctan(np.abs(c) / np.abs(a))

        ## a的分类讨论：
        wa = np.arcsin(np.abs(a2) / np.abs(a))
        if a1 >= 0 and a2 >= 0:
            wa = wa
        elif a1 <= 0 and a2 >= 0:
            wa = np.pi-wa
        elif a1 <= 0 and a2 <= 0:
            wa = wa + np.pi
        elif a1 >= 0 and a2 <= 0:
            wa = 2*np.pi-wa

        ## c的分类讨论：
        wc = np.arcsin(np.abs(c2) / np.abs(c))
        if c1 >= 0 and c2 >= 0:
            wc = wc
        elif c1 <= 0 and c2 >= 0:
            wc = np.pi-wc
        elif c1 <= 0 and c2 <= 0:
            wc = wc + np.pi
        elif c1 >= 0 and c2 <= 0:
            wc = 2*np.pi-wc

        ## d的分类讨论：
        wd = np.arcsin(np.abs(d2) / np.abs(d))
        if d1 >= 0 and d2 >= 0:
            wd = wd
        elif d1 <= 0 and d2 >= 0:
            wd = np.pi-wd
        elif d1 <= 0 and d2 <= 0:
            wd = wd + np.pi
        elif d1 >= 0 and d2 <= 0:
            wd = 2*np.pi-wd

        ## 计算结果
        alpha = wc - wa
        beta = wd - wc
        delta = (wd + wa) / 2

    delta = delta - alpha / 2 - beta / 2

    return [['RZ', [num, beta]], ['RY', [num, theta]], ['RZ', [num, alpha]], ['I', [num, delta]]]  # 返回分解的结果