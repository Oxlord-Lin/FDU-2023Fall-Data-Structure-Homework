def insertiong_sort(seq):
    """插入排序，返回从小到大的升序数组"""
    n = len(seq)
    for j in range(1,n):
        key = seq[j]
        i = j - 1
        while (i >= 0) and (seq[i] > key):
            seq[i+1] = seq[i]
            i = i - 1
        seq[i+1] = key
    return seq