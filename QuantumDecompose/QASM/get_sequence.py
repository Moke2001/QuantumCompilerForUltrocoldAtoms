##将qasm对象转换为SEQUENCE对象##
import pyqpanda as pq
from scipy.stats import unitary_group
import numpy as np
from Panda.panda_decompose import panda_decompose

## 主函数
def get_sequence(qasm):

    ## 预处理
    s=str()
    sequence=[]
    L=len(qasm)
    flag=0

    ## 遍历qasm对象
    for i in qasm:
        if i != '\n' and flag!=L-1:
            s = s + i
        else:
            if s[0:2] == 'cx':
                sequence.append(cu_get(s,'cx'))
            elif s[0:2] == 'cz':
                sequence.append(cu_get(s,'cz'))
            elif s[0:2] == 'u3':
                sequence.append(u_get(s,'u3'))
            s = str()
        flag=flag+1

    ## 返回结果
    return sequence

## 得到双量子比特门SEQUENCE形式
def cu_get(s,type):

    ## 预处理
    flag=0
    num_control=-1
    num_target=-1
    count_i=0
    count_j=0

    ## 分析语句
    for i in s:
        if i=='[':
            count_j=count_i
            for j in s[count_i:]:
                if j==']':
                    if flag==0:
                        num_control=int(s[count_i+1:count_j])
                        flag=1
                    else:
                        num_target=int(s[count_i+1:count_j])
                    break
                count_j=count_j+1
        count_i=count_i+1

    ## 返回SEQUENCE子对象
    return [type,num_control,num_target]

## 得到单量子比特门SEQUENCE形式
def u_get(s,type):

    ## 预处理
    global flag_0, flag_1, flag_2, flag_3, flag_4, flag_5
    flag=0
    count=0

    ## 分析语句
    for i in s:
        if i=='(':
            flag_0=count
        elif i==',' and flag==0:
            flag_1=count
            flag=1
        elif i==',' and flag==1:
            flag_2=count
        elif i==')':
            flag_3=count
        elif i=='[':
            flag_4=count
        elif i==']':
            flag_5=count
        count=count+1
    theta_0=float(s[flag_0+1:flag_1])
    theta_1=float(s[flag_1+1:flag_2])
    theta_2 = float(s[flag_2 + 1:flag_3])
    num_target=int(s[flag_4+1:flag_5])

    ## 返回SEQUENCE子对象
    return [type,num_target,theta_0,theta_1,theta_2]