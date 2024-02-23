from math import *
def merge_sort(seq):
    """merge排序，返回从小到大的升序数组"""
    n = len(seq)
    if n == 1:
        return seq
    if n//2 == 0:
        A1 = merge_sort(seq[0:int(n/2)])
        A2 = merge_sort(seq[int(n/2):])
    else: # 如果是奇数
        A1 = merge_sort(seq[0:ceil(n/2)]) # 元素升序排列
        A2 = merge_sort(seq[ceil(n/2):]) # 元素升序排列
    # 以下是merge过程，使用双指针思想
    i = 0
    j = 0
    sorted_seq = []
    while i < len(A1) and j < len(A2):
        if A1[i] <= A2[j]:
            sorted_seq.append(A1[i])
            i += 1
        else: # if A1[i] > A2[j]
            sorted_seq.append(A2[j])
            j += 1
    sorted_seq.extend(A1[i:])
    sorted_seq.extend(A2[j:])
    return sorted_seq