# 这是一个示例脚本。
import numpy as np
from Compiler.compiler import compiler


def main():
    U_test=np.array([[1,0],[0,1]])
    result=compiler(U_test)
    return result


if __name__ == '__main__':
    print(main())

