##将一个单量子比特操作转换为一个C量子门##
import pyqpanda as pq
import numpy as np
from Compiler.SingleDecompose.single_decompose import single_decompose
from QASM.get_qasm import get_qasm


def get_c(sequence_sub,target):

    ## 非空线路得到一个单量子比特的量子线路
    if sequence_sub:
        sequence_new=sequence_sub.copy()
        for i in range(len(sequence_new)):
            sequence_new[i][1]=0
        qasm=get_qasm(sequence_new,1)
        machine = pq.CPUQVM()
        machine.init_qvm()
        prog=pq.convert_qasm_string_to_qprog(qasm,machine)[0]

        ## 执行转换
        U=pq.get_matrix(prog)
        matrix=np.array([[U[0],U[1]],[U[2],U[3]]])
        result=single_decompose(matrix, target)

        ## 返回结果
        return [result[0],result[1]]

    ## 空线路不执行操作
    else:
        return [None,None]