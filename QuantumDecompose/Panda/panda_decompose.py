##利用pyQPanda中的分解程序得到量子线路的初步分解##
import pyqpanda as pq
import numpy as np
from Panda.count import count


def panda_decompose(unitary_matrix):

        ## 预处理
        num_qubit=int(np.log2(unitary_matrix.shape[0]))
        machine = pq.CPUQVM()
        machine.init_qvm()
        q = machine.qAlloc_many(num_qubit)

        # 输入需要被分解的线路，输出结果
        prog = pq.QProg()
        prog << pq.matrix_decompose(pq.QVec(q), unitary_matrix,mode=pq.DecompositionMode.QSDecomposition)
        qasm = pq.convert_qprog_to_qasm(prog, machine)  # 输出的qasm
        info=count(qasm)  # 输出的统计信息
        return [qasm,info]

