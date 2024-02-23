from math import *
import numpy as np
import time
import matplotlib.pyplot as plt

def insertion_sort(seq):
    """插入排序，返回从小到大的升序数组"""
    n = len(seq)
    if n == 1:
        return seq
    for j in range(1,n):
        key = seq[j]
        i = j - 1
        while (i >= 0) and (seq[i] > key):
            seq[i+1] = seq[i]
            i = i - 1
        seq[i+1] = key
    return seq


def combined_sort(seq,k):
    """主体为merge排序，当数组长度小于k时，不再递归，直接使用插入排序。
    输入：seq为待排序的数组，k为两种排序方式的临界值
    输出：该函数返回从小到大的升序数组。"""
    n = len(seq)
    # 如果数组太短，不再递归，直接调用插入排序的函数
    if n <= k:  
        return insertion_sort(seq)
    if n//2 == 0:
        A1 = combined_sort(seq[0:int(n/2)],k)
        A2 = combined_sort(seq[int(n/2):],k)
    else: # 如果是奇数
        A1 = combined_sort(seq[0:ceil(n/2)],k) # 元素升序排列
        A2 = combined_sort(seq[ceil(n/2):],k)  # 元素升序排列
    # 以下是merge过程，使用双指针思想
    i = 0
    j = 0
    sorted_seq = []
    while i < len(A1) and j < len(A2):
        if A1[i] <= A2[j]:
            sorted_seq.append(A1[i])
            i += 1
        else: # A1[i] > A2[j]
            sorted_seq.append(A2[j])
            j += 1
    sorted_seq.extend(A1[i:])
    sorted_seq.extend(A2[j:])
    return sorted_seq


def worst_find_k(n,step,ending):
    """输入n和k，寻找n固定时，最坏条件下的最优分界点k，k按步长step增加，增加到ending为止"""
    seq = list(range(n,0,-1))  # seq降序排列，为最坏情况
    Ts = []
    Ks = []
    for i in range(floor(ending/step)):
        k = step + i*step
        Ks.append(k)
        start_time = time.time()
        for _ in range(10): # 重复多次求平均值更准确
            combined_sort(seq,k)
        end_time = time.time()
        Ts.append((end_time - start_time)/10)
    best_k = Ks[Ts.index(min(Ts))]
    fig, ax = plt.subplots(figsize=(8,6))
    ax.plot(Ks,Ts)
    ax.set_xlabel('k')
    ax.set_ylabel('time')
    ax.set_title('running time against k in worst case with n=%d and best k=%d' %(n,best_k))
    # plt.show
    fig.savefig('worst case with n='+str(n)+'.png')
    return best_k

def rand_find_k(n,step,ending):
    """输入n和k，寻找n固定时，随机条件下的最优分界点k，k按步长step增加，增加到engding为止"""
    Ts = []
    Ks = []
    for i in range(floor(ending/step)):
        k = step + i*step
        print(k)
        Ks.append(k)
        t = 0
        for _ in range(20): # 重复多次求平均值
            seq = np.random.randint(1,2*n,size=n)
            start_time = time.time()
            combined_sort(seq,k)
            end_time = time.time()
            t += (end_time - start_time)
        Ts.append(t/20)
    best_k = Ks[Ts.index(min(Ts))]
    fig, ax = plt.subplots(figsize=(8,6))
    ax.plot(Ks,Ts)
    ax.set_xlabel('k')
    ax.set_ylabel('time')
    ax.set_title('running time against k in random case with n=%d and best k=%d' %(n,best_k))
    # plt.show
    fig.savefig('random case n='+str(n)+'.png')
    return best_k


def main():
    kw1 = worst_find_k(100,1,100)
    print(kw1)
    kw2 = worst_find_k(250,2,250)
    print(kw2)
    kw3 = worst_find_k(500,2,350)
    print(kw3)
    kw4 = worst_find_k(1000,2,350)
    print(kw4)

    np.random.seed(1)
    kr1 = rand_find_k(100,1,100)
    print(kr1)
    kr2 = rand_find_k(250,2,250)
    print(kr2)
    kr3 = rand_find_k(500,2,350)
    print(kr3)
    kr4 = rand_find_k(1000,2,350)
    print(kr4)
    
    return


if __name__=='__main__':
    main()

