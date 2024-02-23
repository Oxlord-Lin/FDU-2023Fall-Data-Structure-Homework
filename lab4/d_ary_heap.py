from math import *

class d_ary_heap:
    def __init__ (self,d): 
        self.heapList = [0]
        self.d_factor = d
        self.currentSize = 0
    
    def show_heap(self):
        d = self.d_factor
        print('\n',str(d),'叉堆如下\n')
        count = 1
        for level in range(ceil(log(self.currentSize, d))):
            for _ in range(d**level):
                if count > self.currentSize:
                    print('\n')
                    return
                else:
                    print(self.heapList[count],end=' ')
                    count += 1
            print('\n')

                


    def childs(self,i):
        temp = i * self.d_factor
        return tuple(range(temp - (self.d_factor - 2), temp + 1 + 1))
        
    def parent(self,i):
        return (i + (self.d_factor-2))//self.d_factor
    
    def extra_max(self):
        if self.currentSize < 1:
            print('错误：heap已经空的！')
            return
        max_item = self.heapList[1]
        self.heapList[1] = self.heapList[self.currentSize]
        self.currentSize -= 1
        self.heapify(1)
        print('弹出最大元素！最大元素是：',max_item)
        return max_item
    
    def heapify(self,i):
        child_range = self.childs(i)
        temp = None
        largest = i
        for k in child_range:
            if k <=self.currentSize and self.heapList[k] > self.heapList[i]:
                largest = k
        if largest != i:
            temp = self.heapList[i]
            self.heapList[i] = self.heapList[largest]
            self.heapList[largest] = temp
            self.heapify(largest)

    def insert(self, key):
        self.currentSize += 1
        self.heapList.append(None)
        self.increase_key(self.currentSize, key)

    def increase_key(self, i, key):
        if i > self.currentSize:
            print('错误：下标已经超出数组范围！')
        if not self.heapList[i]:  # if None
            self.heapList[i] = key
            # print(self.heapList)
            while i > 1 and self.heapList[self.parent(i)] < self.heapList[i]:
                temp = self.heapList[i]
                self.heapList[i] = self.heapList[self.parent(i)]
                self.heapList[self.parent(i)] = temp
                i = self.parent(i)
                # print(self.heapList)
            return 
        elif key >= self.heapList[i]:
            self.heapList[i] = key
            while i > 1 and self.heapList[self.parent(i)] < self.heapList[i]:
                temp = self.heapList[i]
                self.heapList[i] = self.heapList[self.parent(i)]
                self.heapList[self.parent(i)] = temp
            return
        elif key < self.heapList[i]:
            print('错误：输入的key值比原有的数值小！')
            print('当前heap的情况为',self.heapList)
            print('key=',key)
            print('position=',i)



def main():
    myHeap = d_ary_heap(3)
    for i in range(1,31):
        myHeap.insert(i)
    print('1~30插入完成')
    myHeap.show_heap()
    myHeap.extra_max()
    myHeap.show_heap()
    myHeap.increase_key(10,28)
    print('将第10个元素的权重增加到28！')
    myHeap.show_heap()

if __name__ == '__main__':
    main()
    