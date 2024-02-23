import numpy as np
import time
import matplotlib.pyplot as plt

def Strassen_matrix_multiplication(A,B):
    """只考虑方阵, 且矩阵维度为2的整数幂次的ing情况"""
    n = np.size(A,1)
    # 若大小为1则直接返回，这是递归的基础情况
    if n == 1: 
        return np.multiply(A,B)
    
    # 首先进行分块
    temp = int(n/2)
    A11 = A[0:temp, 0:temp]
    A12 = A[0:temp, temp:]
    A21 = A[temp:, 0:temp]
    A22 = A[temp:, temp:]
    B11 = A[0:temp, 0:temp]
    B12 = A[0:temp, temp:]
    B21 = A[temp:, 0:temp]
    B22 = A[temp:, temp:]

    # 然后做十个矩阵加法或减法，生成中间的辅助矩阵S1~S10
    S1 = B12 - B22
    S2 = A11 + A12
    S3 = A21 + A22
    S4 = B21 - B11
    S5 = A11 + A22
    S6 = B11 + B22
    S7 = A12 - A22
    S8 = B21 + B22
    S9 = A11 - A21
    S10 = B11 + B12

    # 再做7个矩阵乘法，使用递归算法，生成中间的辅助矩阵P1~P7
    P1 = Strassen_matrix_multiplication(A11,S1)
    P2 = Strassen_matrix_multiplication(S2,B22)
    P3 = Strassen_matrix_multiplication(S3,B11)
    P4 = Strassen_matrix_multiplication(A22,S4)
    P5 = Strassen_matrix_multiplication(S5,S6)
    P6 = Strassen_matrix_multiplication(S7,S8)
    P7 = Strassen_matrix_multiplication(S9,S10)
    
    # 生成分块矩阵C1~C4
    C11 = P5 + P4 - P2 + P6
    C12 = P1 + P2
    C21 = P3 + P4
    C22 = P5 + P1 - P3 - P7

    C1_ = np.hstack((C11, C12)) # 横向拼接
    C2_ = np.hstack((C21, C22)) # 横向拼接
    return np.vstack((C1_, C2_)) # 垂直拼接


def main():
    time_store = []
    start_power = 3
    end_power = 9
    np.random.seed(123)
    for power in range(start_power,end_power):
        n = 2**power # n为矩阵维度
        A = np.random.randn(n,n)
        B = np.random.randn(n,n)
        start_time = time.time()
        for _ in range(9-power): # 多次计算求平均值，更准确，但维数太大时，少算几轮
            Strassen_matrix_multiplication(A,B)
        end_time = time.time()
        print("完成一轮矩阵乘法！",power)
        time_store.append((end_time - start_time)/(9-power))
    print("耗时：", time_store)
    print("log2(耗时) :", np.log2(time_store))
    # fig, ax = plt.subplots(figsize=(8,8))
    plt.loglog(np.exp2(list(range(start_power,end_power))), time_store)
    plt.xscale("log", base=2)
    plt.yscale("log", base=2)
    plt.xlabel("the dimension of matrix")
    plt.ylabel("running time")
    plt.title("the loglog plot of running time vs dimension by Strassen's algorithm")
    # plt.show()
    plt.savefig("Strassen.png")
    return

if __name__=='__main__':
    main()