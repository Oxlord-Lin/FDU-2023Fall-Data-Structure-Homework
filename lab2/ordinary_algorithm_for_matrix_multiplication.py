import numpy as np
import time
import matplotlib.pyplot as plt



def ord_matrix_multiplication(A,B):
    """只考虑两个矩阵均为方阵的情况"""
    n = np.size(A,1)
    C = np.zeros((n,n))
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i,j] = C[i,j] + A[i,k] * B[k,j]  # 生成C中每个元素需要大约n次乘法和n次加法
    return C

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
            ord_matrix_multiplication(A,B)
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
    plt.title("the loglog plot of running time vs dimension by ordinary algorithm")
    # plt.show()
    plt.savefig("ord.png")
    return

if __name__=='__main__':
    main()