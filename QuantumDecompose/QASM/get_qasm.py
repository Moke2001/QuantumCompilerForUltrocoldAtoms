##给定SEQUENCE对象，返回qasm对象##
import pyqpanda as pq
from scipy.stats import unitary_group
from Panda.panda_decompose import panda_decompose
from QASM.get_sequence import get_sequence


def get_qasm(sequence, num_qubit):

    ## 构造量子虚拟机
    machine = pq.CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(num_qubit)
    circuit = pq.QCircuit()
    prog = pq.QProg()

    ## 遍历SEQUENCE对象
    for gate in sequence:
        if gate is None:
            continue
        if gate[0] == 'cx':
            circuit << pq.CNOT(q[gate[1]], q[gate[2]])
        elif gate[0] == 'cz':
            circuit << pq.CZ(q[gate[1]], q[gate[2]])
        elif gate[0] == 'u3':
            circuit << pq.U3(q[gate[1]], gate[2], gate[3], gate[4])
        elif gate[0] == 'h':
            circuit << pq.H(q[gate[1]])
        elif gate[0] == 'c':
            circuit<<pq.U4(q[gate[1]], 0, -gate[2], gate[1] , gate[2])

    ## 将结果转化为qasm并输出
    prog << circuit
    qasm = pq.convert_qprog_to_qasm(prog, machine)
    return qasm


if __name__ == "__main__":
    unitary_matrix = unitary_group.rvs(2 ** 3, random_state=169384)  # 生成任意酉矩阵
    qasm = panda_decompose(unitary_matrix)[0]
    sequence = get_sequence(qasm)
    qasm_out = get_qasm(sequence, 3)
    pass
