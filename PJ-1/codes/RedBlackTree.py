"""基于basic_structure.py(包含了基本的树结构和节点，以及基本的增删查操作)
构建红黑树"""

from binarySearchTree import BinarySearchTree, TreeNode, less

class rbTree(BinarySearchTree):
    """红黑树，从二叉树继承而来"""
    # def __init__(self,root=None,size=0):
    #    super(rbTree, self).__init__(root,size)  # 继承父类
    
    def __init_subclass__(cls) -> None:
        return super().__init_subclass__()


    def put(self,key,val):
        """对父类的插入函数put进行重构。put实现节点的插入，并且能够自动维护红黑树"""
        node = self.get(key)
        if node:
            print('不能重复插入已经存在的单词：',key)
            return -1
        if self.root:
            node = self._put(key,val,self.root)  # 不是空树时，调用私有函数_put；node是插入的节点
            self.RB_insert_fixup(node) # 进行红黑树的维护，注意，由于原树不是空树，则node一定有parent
        else: # 如果是空树，就放到根节点上，并把颜色设为black
            self.root = rbNode(key,val,'b')
            node = self.root
        self.size = self.size + 1
        return node
    # 私有函数，通过while循环的方式插入新的节点，并返回插入的node
    def _put(self,key,val,currentNode):
        if less(key, currentNode.key):
            if currentNode.hasLeftChild():
                node = self._put(key,val,currentNode.leftChild)
            else:
                currentNode.leftChild = rbNode(key,val,'r',parent=currentNode) # 初始为红色
                node = currentNode.leftChild
        else: # key >= currentNode.key
            if currentNode.hasRightChild():
                node = self._put(key,val,currentNode.rightChild)
            else:
                currentNode.rightChild = rbNode(key,val,color='r',parent=currentNode) # 初始为红色
                node = currentNode.rightChild
        return node
    
    def RB_insert_fixup(self,node):
        """定义在Tree上的维护红黑树插入的函数"""
        while (not node.isRoot())  and  node.parent.isRed():
            # 在伪代码的基础上加了下面这个if判断
            # if node.parent.isRoot(): # 如果parent已经到根节点了，就直接改root颜色为black，然后结束
            #     self.root.color = 'b'
            #     break

            # 在伪代码的基础上加了下面这个if判断
            # if node.isRoot():
            #     self.root.color = 'b'
            #     break

            if node.parent.isLeftChild(): # 父亲是左孩子
                uncle = node.parent.parent.rightChild
                if uncle and uncle.isRed(): # case 1, where uncle is also Red
                    node.parent.color = 'b'
                    uncle.color = 'b'
                    node.parent.parent.color = 'r'
                    node = node.parent.parent # 现在变成祖父可能是问题节点，进入下一轮循环
                else: # uncle.color == 'b' ，包括虚拟节点的情况
                    if node.isRightChild(): # case 2, 问题节点和parent在异侧，先需要进行预旋转，和父亲一起变到左边，变成case 3
                        node = node.parent
                        self.left_rotation(node)
                    # 现在出问题的节点和父亲都在左侧,case 3 
                    node.parent.color = 'b'
                    node.parent.parent.color = 'r' # 交换父子关系，更改颜色
                    self.right_rotation(node.parent.parent) # 以祖父为轴右旋
                    break
            else: # self.parent.isRightChild() 父亲是右孩子
                uncle = node.parent.parent.leftChild
                if uncle and uncle.isRed(): # case 1
                    node.parent.color = 'b'
                    uncle.color = 'b'
                    node.parent.parent.color = 'r'
                    node = node.parent.parent # 现在祖父是可能是问题节点，进入下一轮循环
                else: # uncle.color = 'b'， 包括虚拟节点的情况
                    if node.isLeftChild(): #case 2变成case3，问题节点和parent在异侧，先进行预旋转，和父亲一起变到右边
                        node = node.parent
                        self.right_rotation(node)
                    # case3 问题节点和父节点都在右侧
                    node.parent.color = 'b'
                    node.parent.parent.color = 'r'
                    self.left_rotation(node.parent.parent)
                    break
        self.root.color = 'b'
    
    def delete(self, key):
        """对父类delete进行重构。delete实现对节点的删除，并且自动维护红黑树"""
        node = self.get(key)
        if not node:
            print('错误！试图删除不存在的节点:',key)
            return -1
        if not node.hasBothChildren(): # 是可以直接删的节点
            y = node
        else: # 要删后继者或者前驱，可作优化
            # y1 = node.findPredecessor()
            # y2 = node.findSuccessor()
            # if y1.isRed(): # 能走到这一步，说明有两个子节点，则一定有前驱或者后继 
                # y = y1
            # else: # y2可能是red，也可能是black，不确定，但显然y1是black，所以不要y1
                # y = y2
            y = node.findSuccessor()
        if y.hasLeftChild(): # y最多有一个孩子
            x = y.leftChild
        elif y.hasRightChild():
            x = y.rightChild
        else:
            x = rbNode(None,None,'b',parent=y) # 虚拟的黑色叶子节点？【这里可能会有bug，小心】
        
        # 删除y
        x.parent = y.parent
        if y.isRoot(): # 如果y已经是根节点
            self.root=x
        else:
            if y.isLeftChild():
                y.parent.leftChild = x
            else: # y.isRightChild()
                y.parent.rightChild = x
        if node != y: # 如果实际删除的是前驱或者后继
            node.key = y.key
        if y.isBlack(): # 如果y是red可以直接删除
            self.RB_delete_fixup(x)  # 注意，传进去的是黑色的x，因为y经脱离了红黑树
        
        # 最后，将之前引入的虚拟黑色节点删除：
        if not x.key:
            if x.isLeftChild():
                x.parent.leftChild = None
            elif x.isRightChild():
                x.parent.rightChild = None
            else: # x is root
                self.root = None
        return y # 返回被删的节点

    def RB_delete_fixup(self,node):
        """定义在Tree上的维护红黑树删除的函数，其中node是删除后补上去的节点"""
        while node != self.root and node.isBlack():
            
            if node.isLeftChild():
                sibling = node.parent.rightChild # 在第一次循环时，node一定有sibling，否则原本就不是红黑树
                if sibling.isRed(): # case 1
                    sibling.color = 'b'
                    node.parent.color = 'r' # 换颜色
                    self.left_rotation(node.parent)
                    sibling = node.parent.rightChild # 现在node和sibling都是黑色，变成case 2 / case 3 / case 4
                if sibling.hasBlackLeftChild() and sibling.hasBlackRightChild() :  # case 2
                    # 注意，由于我没有引入虚拟的黑色叶子节点，因此遇到没有child的情况视为有黑色的child
                    sibling.color = 'r'
                    node = node.parent # 重新开始循环
                    continue
                else: # case 3 / case 4
                    if sibling.hasBlackRightChild(): # case 3 
                        # 能走到这一步，说明sibling的leftChild是red
                        sibling.leftChild.color = 'b' # 交换父子关系，交换颜色；注意，此时sibling一定有真正的leftChild
                        sibling.color = 'r'
                        self.right_rotation(sibling)
                        sibling = node.parent.rightChild
                    sibling.color = node.parent.color # case 4
                    node.parent.color = 'b'
                    sibling.rightChild.color = 'b'
                    self.left_rotation(node.parent)
                    node = self.root
                    break
            

            else: # node.isRightChild
                sibling = node.parent.leftChild # 在第一次循环时，node一定有sibling，否则原本就不是红黑树
                if sibling.isRed(): # case 1
                    sibling.color = 'b'
                    node.parent.color = 'r' # 换颜色
                    self.right_rotation(node.parent)
                    sibling = node.parent.leftChild # 现在node和sibling都是黑色，变成case 2 / case 3 / case 4
                if sibling.hasBlackLeftChild() and sibling.hasBlackRightChild() :  # case 2
                    # 注意，由于我没有引入虚拟的黑色叶子节点，因此遇到没有child的情况视为有黑色的child
                    sibling.color = 'r'
                    node = node.parent # 重新开始循环
                else: # case 3 / case 4
                    if sibling.hasBlackLeftChild(): # case 3 
                        # 能走到这一步，说明sibling的rightChild是red
                        sibling.rightChild.color = 'b' # 交换父子关系，交换颜色；注意，此时sibling一定有真正的rightChild
                        sibling.color = 'r'
                        self.left_rotation(sibling)
                        sibling = node.parent.leftChild
                    sibling.color = node.parent.color # case 4
                    node.parent.color = 'b'
                    sibling.leftChild.color = 'b'
                    self.right_rotation(node.parent)
                    node = self.root
                    break
        node.color = 'b'

    def RB_preorder(self):
        return self.root.RB_preorder(0)


class rbNode(TreeNode): 
    """红黑树的节点，从二叉树的节点继承而来"""
    # def __init__(self,key,val,color,left=None,right=None,parent=None):
    #    super(rbNode, self).__init__(key,val,left,right,parent)  # 继承父类
    #    rbNode.color = color
    def __init__(self,key,val, color = None, left=None,right=None,parent=None):
        super().__init__(key=key, payload = val, left = left, right = right,parent = parent) # 继承父类属性
        self.color = color # 子类自己的属性
    
    def isRed(self):
        return self.color == 'r'
    
    def isBlack(self):
        return self.color == 'b'
    
    def hasBlackLeftChild(self):
        """如果没有LeftChild，则视为拥有黑色的LeftChild"""
        return (not self.hasLeftChild())   or  self.leftChild.isBlack()
    
    def hasBlackRightChild(self):
        """如果没有RightChild，则视为拥有黑色的RightChild"""
        return (not self.hasRightChild())  or  self.rightChild.isBlack()
    

  
    def RB_preorder(self,level) -> list: 
        """对红黑树进行先序遍历，同打印出层数以及节点颜色，
        格式为：
        level=0 child=0 5(BLACK)
        level=1 child=0 3(BLACK)
        level=2 child=0 1(RED)
        level=3 child=0 null
        """
        lines = []
        if self.isRoot() or self.isLeftChild():
            child = 0
        else:
            child = 1
        line = (level,child,self.key,self.color)
        
        lines.append(line)
        
        # 左子树
        if self.hasLeftChild():
            line_left = self.leftChild.RB_preorder(level+1)
        else:
            line_left = [ (level+1,0,'null',None),]
        lines.extend(line_left)

        # 右子树
        if self.hasRightChild():
            line_right = self.rightChild.RB_preorder(level+1)
        else:
            line_right = [(level+1,1,'null',None),]
        lines.extend(line_right)

        return lines




def main():
    RBT = rbTree()
    while True:
        command = input('请输入您的要求：')
        if command=='q':
            break
        if command=='insert':
            key = input('请输入key，要求为英文单词：')
            val = input('请输入value，要求为中文：')
            RBT.put(key,val)
        if command=='show':
            RBT.inorder_walk()
        if command == 'delete':
            key = input('请输入要删除的单词')
            RBT.delete(key)
        if command == 'search':
            key = input('请输入key，要求为英文单词：')
            result = RBT.get(key)
            if not result: # 如果是None
                print('词典中无该单词！')
            else:
                print(result.key)
        if command == 'preorder':
            RBT.RB_preorder()
        if command == 'rangesearch':
            bd1 = input('请输入bd1: ')
            bd2 = input('请输入bd2: ')
            words = RBT.rangeSearch(bd1,bd2)
            for w in words:
                print(w.key)

        

if __name__ == '__main__':
    main()

        
    
    