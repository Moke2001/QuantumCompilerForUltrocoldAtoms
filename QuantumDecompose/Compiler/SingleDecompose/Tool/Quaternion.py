import numpy as np

from Compiler.SingleDecompose.Tool.global_arctan import global_arctan


class Quaternion:

    def __init__(self,q):
        self.q=[0,0,0,0]
        self.q[0]=q[0]
        self.q[1] = q[1]
        self.q[2] = q[2]
        self.q[3] = q[3]

    ## 重载乘法运算符
    def __mul__(self,q):
        moment_1=np.array([[self.q[0],-self.q[1],-self.q[2],-self.q[3]],
                         [self.q[1],self.q[0],-self.q[3],self.q[2]],
                         [self.q[2],self.q[3],self.q[0],-self.q[1]],
                         [self.q[3],-self.q[2],self.q[1],self.q[0]]])
        moment_2=np.array([[q.q[0]],[q.q[1]],[q.q[2]],[q.q[3]]])
        moment=moment_1@moment_2  # 四元数来源于矩阵乘法
        q_moment=[moment[0][0],moment[1][0],moment[2][0],moment[3][0]]  # 四元数的定义list
        return Quaternion(q_moment)  # 返回一个四元数对象

    ## 返回四元数的旋转角与旋转轴
    def get_value(self):
        theta= 2 * global_arctan(self.q[0], np.sqrt(self.q[1] ** 2 + self.q[2] ** 2 + self.q[3] ** 2))
        n=[self.q[1]/np.sin(theta/2),self.q[2]/np.sin(theta/2),self.q[3]/np.sin(theta/2)]
        return [theta,n.copy()]