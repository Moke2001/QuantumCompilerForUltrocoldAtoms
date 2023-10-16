##统计程序，统计qasm格式量子线路中各种量子门的数量##
def count(qasm):

    ## 预处理
    s = str()
    num_cx = 0
    num_cz = 0
    num_single = 0

    ## 遍历线路
    for i in qasm:
        if i != '\n' and i != '\'':
            s = s + i
        else:
            if s[0:2] == 'cx':
                num_cx = num_cx + 1
            elif s[0:2] == 'cz':
                num_cz = num_cz + 1
            elif s[0] == 'u':
                num_single = num_single + 1
            s = str()

    ## 返回结果
    return [num_cx, num_cz, num_single]
