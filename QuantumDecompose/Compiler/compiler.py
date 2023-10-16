##编译程序，将一个酉操作编译为可以在冷原子量子计算平台上执行的量子线路##
import numpy as np
from Compiler.get_c import get_c
from Panda.panda_decompose import panda_decompose
from QASM.get_sequence import get_sequence
from QASM.get_qasm import get_qasm


def compiler(unitary_matrix):

    ## 预处理
    num_qubit = int(np.log2(unitary_matrix.shape[0]))
    [qasm, info] = panda_decompose(unitary_matrix)
    sequence = get_sequence(qasm)
    sequence_new = []
    count = 0

    ## 将cx门替换为cz门
    for gate in sequence:
        if gate[0] == 'cx':
            sequence_new.append(['h', gate[2]])
            sequence_new.append(['cz', gate[1], gate[2]])
            sequence_new.append(['h', gate[2]])
        else:
            sequence_new.append(gate)

    ## 交换两个量子线路
    sequence = sequence_new.copy()
    sequence_new = []

    ## 将单量子比特门替换为C门
    moment_sequence = []
    for i in range(num_qubit):
        moment_sequence.append([])
    for gate in sequence:
        if gate[0] == 'cz':
            sequence_sub_0 = moment_sequence[gate[1]]
            sequence_sub_1 = moment_sequence[gate[2]]
            result_0 = get_c(sequence_sub_0, gate[1])
            result_1 = get_c(sequence_sub_1, gate[2])
            sequence_new.append(result_0[0])
            sequence_new.append(result_0[1])
            sequence_new.append(result_1[0])
            sequence_new.append(result_1[1])
            sequence_new.append(gate)
            moment_sequence[gate[1]] = []
            moment_sequence[gate[2]] = []
        else:
            moment_sequence[gate[1]].append(gate)

    ## 将结果转换为qasm格式并输出
    qasm = get_qasm(sequence_new, num_qubit)
    return qasm
