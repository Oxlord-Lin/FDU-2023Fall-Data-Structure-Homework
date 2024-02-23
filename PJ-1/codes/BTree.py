from random import randint, randrange
from binarySearchTree import less, larger

class word:
    def __init__(self, key, value):
        self.key = key
        self.value = value

class Node:
    def __init__(self, leaf=False):
        self.leaf = leaf
        self.words = []
        self.children = []

    def preorder_print(self,lvl,index):
        results = []
        results.append( (lvl, index, self.words) )  # words is a list of word，every word has key and value
        lvl += 1
        if len(self.children) > 0: # 当前节点不是leaf，还有子节点，则继续遍历子节点
            for childIndex, child in enumerate(self.children):
                results.extend(child.preorder_print(lvl,childIndex))
        return results
    
    def get(self, k):
        """
        Search for key 'k', beginning from self
        :param k: The key to search for.
        :return: None and None if 'k' is not found. 
        Otherwise returns the index of the word in node.words and the node it belongs to.
        """
        node = self
        i = 0
        while i < len(node.words) and larger(k,node.words[i].key):
            i += 1
        if i < len(node.words) and k == node.words[i].key: # 若在当前节点找到了
            return i, node
        elif node.leaf:
            return None, None
        else:
            # Search its children
            node = node.children[i]
            return node.get(k)


class BTree:
    def __init__(self, t=10):
        """
        Initializing the B-Tree
        :param t: Order, default 10(suggested)
        """
        self.root = Node(True)
        self.t = t

    def B_preorder(self):
        """
        Prints the complete B-Tree in a preorder traversal
        :return a list contain tuple with level,child and the words in this node, i.e (level, child, [words])
        where child is the index of the node, and [words] is a list.
        """
        results = self.root.preorder_print(0,0)
        return results

    def get(self, k):
        """
        Search for key 'k', beginning from the root
        :param k: The key to search for.
        :return: None and None if 'k' is not found. 
        Otherwise returns the index of the word in node.words and the node it belongs to.
        """
        node = self.root
        return node.get(k)


    def findSuccessor(self, i:int, node:Node):
        """Find the successor of a word in the B-tree
        :param: i is the index of the word in node.words
        :param: node is where the word belong to
        :return: index and node of the successor"""
        if node.leaf is False:
            return self.findMin(node.children[i+1])
        # if node is leaf
        if i < len(node.words) -1:  # not the last one
            return i+1, node

        # if node 【is leaf】 and if the word is 
        # the 【last one】 of node.words, then search from the root
        k = node.words[i].key
        node = self.root
        index = 0
        successorNode = None
        while not node.leaf:
            i = 0
            while i < len(node.words) and larger(k, node.words[i].key):
                i += 1
            # if i < len(node.words) and k == node.words[i].key: # 若找到了
            #     break
            else:
                if i != len(node.words):
                    index = i
                    successorNode = node # 这样做，会记录下最后一次遇到的比node大的“父节点”
                node = node.children[i]
        return index, successorNode


    def findMin(self,node:Node):
        """Find the index of the minimum word and the node that the word belong to 
        within the subtree rooted at node
        :return: the index and the node"""
        if node.leaf:
            return 0, node
        else:
            return self.findMin(node.children[0])
        

    def findMax(self,node:Node):
        """Find the index of the maxium word and the node that the word belong to 
        within the subtree rooted at node
        :return: the index and the node"""
        if node.leaf:
            return len(node.words)-1, node
        else:
            return self.findMin(node.children[-1])


    def rangeSearch(self, b1:str, b2:str):
        """
        Search for words within the range [b1,b2]
        :param b1: the left bound
        :param b2: the right bound
        :return: a list containing the words(some instances, with key and value) within [b1,b2]
        """
        if len(self.root.words) == 0: # 空树
            print('B树中没有单词，请先插入单词！')
            return [] 
        index, node = self.get(b1)
        if index is not None:
            startIndex = index
            startNode = node 
        else: # index is None, the word cannot be found, need to find the start
            node = self.root
            k = b1
            # i = 0
            while True:
                i = 0
                while i < len(node.words) and larger(k, node.words[i].key):
                    # print(k, node.words[i].key)
                    i += 1
                # if i < len(node.words) and k == node.words[i].key: # 若在当前节点找到了
                #     return i, node
                if node.leaf:
                    break # 退出while循环时，i恰好是b1“适合插入”的那个位置
                else:
                    # Search its children
                    node = node.children[i]
            if i < len(node.words):
                startIndex = i
                startNode = node
            else: # 在node的最后一个word的右边
                startIndex, startNode = self.findSuccessor(i-1, node)

        results = []
        while startNode and ( less(startNode.words[startIndex].key, b2) or startNode.words[startIndex].key == b2):
            results.append(startNode.words[startIndex])
            startIndex,startNode = self.findSuccessor(startIndex,startNode)
        
        return results



    def _splitChild(self, x:Node, i:int):
        """
        Splits the child of node at 'x' from index 'i'
        :param x: Parent node of the node to be split.
        :param i: Index value of the child.
        """
        t = self.t
        y :Node = x.children[i]
        z = Node(y.leaf)
        x.children.insert(i + 1, z)
        x.words.insert(i, y.words[t - 1])
        z.words = y.words[t:]
        y.words = y.words[0:t-1]
        if not y.leaf:
            z.children = y.children[t:]
            y.children = y.children[0:t]


    def put(self, key, value):
        """
        Calls the respective helper functions for insertion into B-Tree
        :param key: the key of the word
        :param value: the value of the word 
        """
        newWord = word(key,value)
        temp, node = self.get(key)
        if node is not None:
            print('请勿重复插入已经存在的单词：',key)
            return -1
        root = self.root
        # If the root is full, split the root's child
        # Spliting the root is the only way to increase the height of a B-tree
        if len(root.words) == (2 * self.t) - 1:
            newRoot = Node()
            self.root = newRoot
            # Former root becomes 0'th child of newRoot
            newRoot.children.insert(0, root)
            self._splitChild(newRoot, 0)
            self._insertNonFull(newRoot, newWord)
        else:
            self._insertNonFull(root, newWord)

    def _insertNonFull(self, x, newWord):
        """
        Inserts a word in a non-full node
        :param x: the node to begin from
        :param newWord: the new word(an instance) to be inserted
        """
        i = len(x.words) - 1
        if x.leaf: # for a B-Tree, insertion only happen in the leaf!
            x.words.append((None, None))
            while i >= 0 and less(newWord.key, x.words[i].key):
                x.words[i + 1] = x.words[i]
                i -= 1
            x.words[i + 1] = newWord
        else:
            while i >= 0 and less(newWord.key, x.words[i].key):
                i -= 1
            i += 1
            if len(x.children[i].words) == (2 * self.t) - 1:
                self._splitChild(x, i)
                if larger(newWord.key, x.words[i].key):
                    i += 1
            self._insertNonFull(x.children[i], newWord)

    def delete(self,key:str):
        """Delete the word with the provided key from B-tree
        :param key: the key of the word to be deleted"""
        tempIndex, tempNode = self.get(key)
        if tempNode is None: #如果是None
            print('错误！试图删除不存在的单词：',key)
            return -1
        
        self._delete(self.root,key)

    def _delete(self, x, key:str):
        """
        Just a private function! need to provide the node to begin from
        Calls the respective helper functions for deletion from B-Tree
        :param x: The node, according to whose relative position, helper functions are called.
        :param key: The key to be deleted.
        """
        # if key == 'criminalistics':
        #     temp = 0
        #     if x.words[0].key == 'countless':
        #         temp = 1
        
        t = self.t
        i = 0
        while i < len(x.words) and larger(key , x.words[i].key):
            i += 1
        # Deleting the key if the node is a leaf
        if x.leaf:
            if i < len(x.words) and x.words[i].key == key:
                x.words.pop(i)
                return
            return

        # Calling '_deleteInternalNode' when x is an internal node and contains the key 'k'
        if i < len(x.words) and x.words[i].key == key:
            return self._deleteInternalNode(x, key, i)
        # Recursively calling 'delete' on x's children
        elif len(x.children[i].words) >= t: # the i-th child has at least t words 
            self._delete(x.children[i], key)
        # Ensuring that a child always has at least 't' words
        
        else:
            # print('original_len',len(x.children[i].words))
            if i != 0 and i + 1 < len(x.children): # 要在中间的child中删除
                if len(x.children[i - 1].words) >= t:
                    self._deleteSibling(x, i, i - 1)
                elif len(x.children[i + 1].words) >= t:
                    self._deleteSibling(x, i, i + 1)
                else:
                    self._deleteMerge(x, i, i + 1)
            elif i == 0: # 要在最左边的child中删除
                if len(x.children[i + 1].words) >= t:
                    self._deleteSibling(x, i, i + 1)
                else:
                    self._deleteMerge(x, i, i + 1)
            elif i + 1 == len(x.children): # 要在最右边的child中删除
                if len(x.children[i - 1].words) >= t:
                    self._deleteSibling(x, i, i - 1)
                else:
                    self._deleteMerge(x, i-1, i)
                    i = -1 # 要删除的单词在最右边的一棵子树里，但由于发生了merge，则children减少，这里直接取最后一个child
            # print('after_len',len(x.children[i].words))
            self._delete(x.children[i], key)

    def _deleteInternalNode(self, x:Node, k:str, i:int):
        """
        Deletes internal node
        :param x: The internal node in which word is present.
        :param k: The key to be deleted.
        :param i: The index position of the word(with key=k) in the self.words
        """
        t = self.t
        # Deleting the key if the node is a leaf
        if x.leaf:
            if x.words[i].key == k:
                x.words.pop(i)
                return
            return

        # Replacing the key with its predecessor and deleting predecessor
        if len(x.children[i].words) >= t: # 前提是left Child至少有t个words
            x.words[i] = self._deletePredecessor(x.children[i])
            return
        # Replacing the key with its successor and deleting successor
        elif len(x.children[i + 1].words) >= t: # 前提是right Child至少有t个words
            x.words[i] = self._deleteSuccessor(x.children[i + 1])
            return
        # Merging the child, its left sibling and the key 'k'
        else: # 此时merge后的节点的words数量为2t-1
            self._deleteMerge(x, i, i + 1)
            self._deleteInternalNode(x.children[i], k, self.t - 1)

    def _deletePredecessor(self, x:Node) -> word:  
        """
        Deletes predecessor of key 'k' which is to be deleted
        :param x: Node
        :return: Predecessor of key 'k' which is to be deleted
        """
        if x.leaf:
            return x.words.pop()  # 返回key最大的word
        
        n = len(x.words) - 1
        if len(x.children[-1].words) == self.t-1:  # predecessor必在最右边的child里，看一下这个child的words是否为t-1
            if len(x.children[-2].words) >= self.t:  # immediate sibling has at least t words
                self._deleteSibling(x, n + 1, n)
            else: # immediate sibling has only t-1 words
                self._deleteMerge(x, n, n + 1)
        return self._deletePredecessor(x.children[-1]) 

    def _deleteSuccessor(self, x:Node) -> word:
        """
        Deletes successor of key 'k' which is to be deleted
        :param x: Node
        :return: Successor of key 'k' which is to be deleted
        """
        if x.leaf:
            return x.words.pop(0) # 返回key最小的word
        
        if len(x.children[0].words) == self.t - 1: 
            if len(x.children[1].words) >= self.t: # immediate sibling has at least t words
                self._deleteSibling(x, 0, 1)
            else: # immediate sibling has only t-1 words
                self._deleteMerge(x, 0, 1)
        return self._deleteSuccessor(x.children[0])

    def _deleteMerge(self, x, i, j):
        """
        Merges the children of x and one of its own words
        :param x: Parent node
        :param i: The index of one of the children
        :param j: The index of one of the children, j should be larger than i
        """
        cNode = x.children[i]

        # Merging the x.children[i], x.children[j] and x.words[i]
        # if j > i:
        rsNode = x.children[j]
        cNode.words.append(x.words[i])
        # Assigning words of right sibling node to child node
        for k in range(len(rsNode.words)):
            cNode.words.append(rsNode.words[k])
            if len(rsNode.children) > 0:
                cNode.children.append(rsNode.children[k])
        if len(rsNode.children) > 0: # rsNode的key最大的一个word
            cNode.children.append(rsNode.children.pop())
        new = cNode
        x.words.pop(i)
        x.children.pop(j)
        # Merging the x.children[i], x.children[j] and x.words[i]
        # else:  # j<i
        #     lsNode = x.children[j]
        #     lsNode.words.append(x.words[j])
        #     # Assigning words of left sibling node to child node
        #     for i in range(len(cNode.words)):
        #         lsNode.words.append(cNode.words[i])
        #         if len(lsNode.children) > 0:
        #             lsNode.children.append(cNode.children[i])
        #     if len(lsNode.children) > 0:
        #         lsNode.children.append(cNode.children.pop())
        #     new = lsNode
        #     x.words.pop(j)
        #     x.children.pop(i)

        # If x is root and is empty, then re-assign root
        if x == self.root and len(x.words) == 0:  # 树高下降
            self.root = new


    def _deleteSibling(self, x, i, j):
        """
        Borrows a key from j'th child of x and appends it to i'th child of x
        :param x: Parent node
        :param i: The index of one of the children
        :param j: The index of one of the children
        """
        cNode = x.children[i]
        if i < j:
            # Borrowing key from right sibling of the child
            rsNode = x.children[j]
            cNode.words.append(x.words[i])  # 把父节点的word拿下来
            x.words[i] = rsNode.words[0] # 把右侧子节点的最小word拿上去
            if len(rsNode.children) > 0: # 不是子节点
                cNode.children.append(rsNode.children[0])
                rsNode.children.pop(0)
            rsNode.words.pop(0)
        else:
            # Borrowing key from left sibling of the child
            lsNode = x.children[j]
            cNode.words.insert(0, x.words[i - 1])
            x.words[i - 1] = lsNode.words.pop()
            if len(lsNode.children) > 0:
                cNode.children.insert(0, lsNode.children.pop())




# The main function
def main():
    BT = BTree(t=2)
    while True:
        command = input('请输入您的要求：')
        if command=='q':
            break
        if command=='put':
            key = input('请输入key，要求为英文单词：')
            # val = input('请输入value，要求为中文：')
            val = None
            BT.put(key,val)
            results = BT.B_preorder()
            for item in results:
                lvl = item[0]
                words = item[1]
                print('level=',lvl)
                for w in words:
                    print(w.key,end=' ')
                print()
        # if command=='show':
        #     BT.inorder_walk()
        if command == 'delete':
            key = input('请输入要删除的单词')
            BT.delete(key)
            results = BT.B_preorder()
            for item in results:
                lvl = item[0]
                words = item[1]
                print('level=',lvl)
                for w in words:
                    print(w.key,end=' ')
                print()
        if command == 'search':
            key = input('请输入key，要求为英文单词：')
            index, node = BT.get(key)
            if index is None: # 如果是None
                print('词典中无该单词！')
            else:
                print(node.words[index].key)
        if command == 'pre':
            results = BT.B_preorder()
            for item in results:
                lvl = item[0]
                words = item[1]
                print('level=',lvl)
                for w in words:
                    print(w.key,end=' ')
                print()
        if command == 'rangesearch':
            bd1 = input('请输入bd1: ')
            bd2 = input('请输入bd2: ')
            words = BT.rangeSearch(bd1,bd2)
            for w in words:
                print(w.key)

        

if __name__ == '__main__':
    main()