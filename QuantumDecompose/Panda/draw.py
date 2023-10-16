##给定qasm绘制对应的量子线路图##
import pyqpanda as pq


def draw(qasm,path):

    ## 构造量子虚拟机
    machine = pq.CPUQVM()
    machine.init_qvm()
    prog=pq.convert_qasm_string_to_qprog(qasm,machine)[0]

    ## 绘制图像
    pq.draw_qprog(prog,'pic',filename=path)