# 重新定义大于和小于
alphabets = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz'
d = dict()
count = 0
for letter in alphabets:
    d[letter] = count
    count = count + 1

def less(w1,w2): 
    l1 = len(w1)
    l2 = len(w2)
    l = min(l1,l2)
    for i in range(l):
        if d[w1[i]] < d[w2[i]]:
            return True
        if d[w1[i]] == d[w2[i]]:
            continue
        if d[w1[i]] > d[w2[i]]:
            return False
    # 如果两个单词的开头都相同，则短的单词更小，比如AbCd小于AbCd***
    return l1 < l2

def larger(w1,w2):
    l1 = len(w1)
    l2 = len(w2)
    l = min(l1,l2)
    for i in range(l):
        if d[w1[i]] < d[w2[i]]:
            return False
        if d[w1[i]] == d[w2[i]]:
            continue
        if d[w1[i]] > d[w2[i]]:
            return True
    # 如果两个单词的开头都相同，则长的单词更大，比如AbCd***大于AbCd
    return l1 > l2


class BinarySearchTree:
    # 以下是BinarySearchTree的基本函数
    def __init__(self):
        self.root = None
        self.size = 0
    
    def length(self):
        return self.size
    
    def __len__(self):
        return self.size
    
    def __iter__(self):
        return self.root.__iter__()
    
    def preorder_walk(self):
        self.root.preorder()

    def inorder_walk(self):
        self.root.inorder()
    
    # put函数实现插入，并且返回插入的node
    def put(self,key,val):
        """ put函数实现插入，并且返回插入的node"""
        if self.root:
            node = self._put(key,val,self.root)  # 不是空树时，调用私有函数_put
        else: # 如果是空树，就放到根节点上
            self.root = TreeNode(key,val)
            node = self.root
        self.size = self.size + 1
        return node
    # 私有函数，通过递归的方式插入新的节点
    def _put(self,key,val,currentNode):
        if less(key , currentNode.key):
            if currentNode.hasLeftChild():
                node = self._put(key,val,currentNode.leftChild)
            else:
                currentNode.leftChild = TreeNode(key,val,parent=currentNode)
                node = currentNode.leftChild
        else: # key >= currentNode.key
            if currentNode.hasRightChild():
                node = self._put(key,val,currentNode.rightChild)
            else:
                currentNode.rightChild = TreeNode(key,val,parent=currentNode)
                node = currentNode.rightChild
        return node
    
    
    # 重载[]运算符，用于插入
    def __setitem__(self,k,v):
        self.put(k,v)

    # get用于查询
    def get(self,key):
        """get返回查询到的节点，而不仅仅是key或payload"""
        if self.root:
            res = self._get(key,self.root)
            if res:
                return res
            else:
                return None
        else:
            return None
        
    def _get(self,key,currentNode):
        # if currentNode and currentNode.key == 'customarily':
        #     k = 1
        if not currentNode: # 递归的基础情况
            return None
        elif currentNode.key == key:
            return currentNode
        elif less(key , currentNode.key):
            return self._get(key,currentNode.leftChild)
        else:
            return self._get(key,currentNode.rightChild)
    
    # 重载[]运算符用于查询，返回的是node
    def __getitem__(self,key):
        return self.get(key)
    
    # 重载in，判断key是否在树中
    def __contains__(self,key):
        if self._get(key,self.root):
            return True
        else:
            return False

    # 删除节点的函数
    def remove(self,currentNode):
        if currentNode.isLeaf():
            if currentNode.isLeftChild():
                currentNode.parent.leftChild = None
            else:
                currentNode.parent.rightChild = None
        elif currentNode.hasBothChildren(): # 有两个节点
            succ = currentNode.findSuccessor()
            succ.spliceOut()
            currentNode.key = succ.key
            currentNode.payload = succ.payload
        else: # 只有一个子节点
            if currentNode.hasLeftChild():
                if currentNode.isLeftChild():
                    currentNode.leftChild.parent = currentNode.parent
                    currentNode.parent.leftChild = currentNode.leftChild
                elif currentNode.isRightChild():
                    currentNode.leftChild.parent = currentNode.parent
                    currentNode.parent.rightChild = currentNode.leftChild
                else:
                    currentNode.replaceNodeData(currentNode.leftChild.key,
                                            currentNode.leftChild.payload,
                                            currentNode.leftChild.leftChild,
                                            currentNode.leftChild.rightChild)

            else: # currentNode has Right child
                if currentNode.isLeftChild():
                    currentNode.rightChild.parent = currentNode.parent
                    currentNode.parent.leftChild = currentNode.rightChild
                elif currentNode.isRightChild():
                    currentNode.rightChild.parent = currentNode.parent
                    currentNode.parent.rightChild = currentNode.rightChild
                else:
                    currentNode.replaceNodeData(currentNode.rightChild.key,
                                            currentNode.rightChild.payload,
                                            currentNode.rightChild.leftChild,
                                            currentNode.rightChild.rightChild)


        

    # 删除函数，带有防错检查机制
    def delete(self,key):
        """定义在TreeNode上的删除函数，删除成功则返回True，删除失败则返回False"""
        if self.size>1:
            nodeToRemove = self._get(key,self.root)
            if nodeToRemove:
                self.remove(nodeToRemove)
                self.size = self.size-1
                return True
            else:
                # raise KeyError('Error ,key not in tree')
                return False
        elif self.size == 1 and self.root.key == key:
            self.root = None
            self.size = self.size - 1
            return True
        else:
            # raise KeyError('Error, key not in tree')
            return False
    
    # 重载删除
    def __delitem__(self,key):
        self.delete(key)

    ## 进行按范围查询的操作，比较冗杂的方法
    # def range_search(self,bd1,bd2):
    #     if bd1 > bd2:
    #         return None
    #     if not self.root: # 如果是空树
    #         return None
        
    #     currentNode = self.root
    #     start = None

    #     while not currentNode.isLeaf():
    #         if bd1 < currentNode.key:
    #             currentNode = currentNode.leftChild
    #         elif bd1 == currentNode.key:
    #             start = currentNode
    #             break
    #         else: # bd1 > currentNode.key
    #             currentNode = currentNode.rightChild
        
    #     # 结束循环后有两种可能，一是找到了start，二是到达了leaf，只需要处理后者
    #     if not start: # 如果是因为到达叶子节点而停止循环，那么就要根据叶子节点的key与bd1的关系进行判断
    #         if bd1 < currentNode.key:
    #             start = currentNode
    #         elif bd1 == currentNode.key:
    #             start = currentNode
    #         else: # bd1>currentNode.key
    #             start = currentNode.parent.findSuccessor()
    
    # 范围内搜索，基于get和put函数
    def rangeSearch(self,bd1,bd2):
        """范围内搜索，基于get和put函数，返回范围内的nodes"""
        if larger(bd1,bd2):
            return []
        if not self.root: # 如果是空树
            return []
        start = self.get(bd1)
        if not start:
            temp_node = self.put(bd1,None)
            start = temp_node.findSuccessor()
            temp_node.spliceOut()
        end = self.get(bd2)
        if end is None:
            temp_node = self.put(bd2,None)
            
            # test = self.get(bd2)
            # print(test.key)

            end = temp_node.findPredecessor()

            # print(end.key)

            temp_node.spliceOut()
        
        if (not start) or (not end): # bd1和bd2的范围内没有覆盖到任何节点
            return [] 
        
        words = [] # 存储的是node
        while start and ( less(start.key , end.key) or start.key == end.key) :
            words.append(start)
            start = start.findSuccessor()
            # print(start.key)
        return words
    
    def left_rotation(self,node):
        """定义在Tree上的左旋，其中node是轴"""
        x = node
        y = x.rightChild
        x.rightChild = y.leftChild
        if y.hasLeftChild():
            y.leftChild.parent = x
        y.parent = x.parent
        if x.isRoot():
            self.root = y
        elif x.isLeftChild():
            x.parent.leftChild = y
        else:
            x.parent.rightChild = y
        y.leftChild = x
        x.parent = y
   

    def right_rotation(self,node):
        """定义在Tree上的右旋，其中node是轴"""
        x = node
        y = x.leftChild
        x.leftChild = y.rightChild
        if y.hasRightChild():
            y.rightChild.parent = x
        y.parent = x.parent
        if x.isRoot():
            self.root = y
        elif x.isLeftChild():
            x.parent.leftChild = y
        else:
            x.parent.rightChild = y
        y.rightChild = x
        x.parent = y
        

        


class TreeNode:
    # 以下是TreeNode的基本函数
    def __init__(self,key,payload,left=None,right=None,parent=None):
        self.key = key
        self.payload = payload
        self.leftChild = left
        self.rightChild = right
        self.parent = parent

    def hasLeftChild(self):
        return self.leftChild
    
    def hasRightChild(self):
        return self.rightChild
    
    def isLeftChild(self):
        return self.parent and self.parent.leftChild == self
    
    def isRightChild(self):
        return self.parent and self.parent.rightChild == self

    def isRoot(self):
        return not self.parent
    
    def isLeaf(self):
        return not (self.leftChild or self.rightChild)
    
    def hasAnyChildren(self):
        return self.leftChild or self.rightChild
    
    def hasBothChildren(self):
        return self.leftChild and self.rightChild
    
    def replaceNodeData(self,key,value,lc,rc):
        self.key = key
        self.payload = value
        self.leftChild = lc
        self.rightChild = rc
        if self.hasLeftChild(): # 当传入的lc不是None时，需要让lc指向self
            self.leftChild.parent = self
        if self.hasRightChild():  # 当传入的rc不是None时，需要让lc指向self
            self.rightChild.parent = self
    
    def findMin(self):
        current = self
        while current.hasLeftChild():
            current = current.leftChild
        return current
    
    def findMax(self):
        current = self
        while current.hasRightChild():
            current = current.rightChild
        return current
    
    # 找到后继者
    def findSuccessor(self):
        """找到后继"""
        succ = None
        if self.hasRightChild():
            succ = self.rightChild.findMin()
        else:
            if self.parent:
                if self.isLeftChild():
                    succ = self.parent
                else: # self is rightChild
                    self.parent.rightChild = None # 由于接下来要递归调用，则要让父节点暂时先失去右子节点
                    succ = self.parent.findSuccessor()
                    self.parent.rightChild = self
        return succ
    
    def findPredecessor(self):
        """找到前驱"""
        pred  = None
        if self.hasLeftChild():
            pred = self.rightChild.findMax()
        else:
            if self.parent:
                if self.isRightChild():
                    pred = self.parent
                else: # self is leftChild
                    self.parent.leftChild = None
                    pred = self.parent.findPredecessor()
                    self.parent.leftChild = self
        return pred
    
    # 删除successor专用函数
    # 注意，作为后继者，要么是叶子，要么只有一个孩子
    def spliceOut(self):
        """删除successor专用函数，successor作为后继者，要么是叶子，要么只有一个孩子"""
        if self.isLeaf(): # 已经是叶子，直接删除
            if self.isLeftChild():
                self.parent.leftChild = None
            else:
                self.parent.rightChild = None
        elif self.hasAnyChildren():
            if self.hasLeftChild():
                if self.isLeftChild():
                    self.parent.leftChild = self.leftChild
                else:
                    self.parent.rightChild = self.leftChild
                self.leftChild.parent = self.parent
            else: # self.hasRightChild():
                if self.isLeftChild():
                    self.parent.leftChild = self.rightChild
                else:
                    self.parent.rightChild = self.rightChild
                self.rightChild.parent = self.parent



    # # 重载循环，实现中序遍历（从小到大）
    # def __iter__(self):
    #     if self:
    #         if self.hasLeftChild():
    #             for elem in self.leftChild:
    #                 yield elem
    #         yield self.key
    #         if self.hasRightChild():
    #             for elem in self.rightChild:
    #                 yield elem
    
    # 先序遍历
    def preorder(self): 
        if self.isLeaf():
            print(self.key,self.payload,sep=' ')
            return
        else:
            print(self.key,self.payload,sep=' ')
            if self.hasLeftChild():
                self.leftChild.preorder()
            if self.hasRightChild():
                self.rightChild.preorder()

    # 中序遍历
    def inorder(self): 
        if self.isLeaf():
            print(self.key, self.payload, sep=' ')
            # input()
            return
        else:
            if self.hasLeftChild():
                self.leftChild.inorder()
            print(self.key, self.payload, sep=' ')
            # input()
            if self.hasRightChild():
                self.rightChild.inorder()



def main():
    BST = BinarySearchTree()
    while True:
        command = input('请输入您的要求：')
        if command=='q':
            break
        if command=='insert':
            key = input('请输入key，要求为英文单词：')
            # val = input('请输入value，要求为中文：')
            BST[key] = None
        if command=='show':
            for item in BST:
                print(item)
        if command == 'delete':
            key = input('请输入要删除的单词')
            del BST[key]
        if command == 'search':
            key = input('请输入key，要求为英文单词：')
            result = BST[key]
            if not result: # 如果是None
                print('词典中无该单词！')
            else:
                print(result)
        if command == 'preorder':
            BST.preorder_walk()
        if command == 'rangesearch':
            bd1 = input('请输入bd1: ')
            bd2 = input('请输入bd2: ')
            words = BST.rangeSearch(bd1,bd2)
            for w in words:
                print(w.key)
        

if __name__ == '__main__':
    main()