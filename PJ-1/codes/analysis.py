"""本文件用于接受用户要求，并且根据用户要求对红黑树或B树进行增删改查的操作"""

from RedBlackTree import rbTree
from BTree import BTree
import time

def preorder_print_tree(tree, treeType, outFileName):
    if treeType == 'rb':
        result = tree.RB_preorder()
        with open(outFileName, 'w') as f:
            for line in result:
                color = None
                if line[3] == 'r':
                    color = 'RED'
                elif line[3] == 'b':
                    color = 'BLACK'
                if color: # 真正子节点，打印颜色
                    f.write('level={:<2d}  child={:<2d}  {:<14}({})\n'.format(line[0],line[1],line[2],color))
                else: # 虚拟子节点，不打印颜色
                    f.write('level={:<2d}  child={:<2d}  {:<14}\n'.format(line[0],line[1],line[2]))
    
    elif treeType == 'b':
        result = tree.B_preorder()
        with open(outFileName, 'w') as f:
            for line in result:
                level = line[0]
                index = line[1]
                words = line[2]
                f.write('level={:<3d}\tchild={:5<d}  '.format(level,index))
                for i in range(len(words)-1):
                    f.write('\t{:<14}\t/'.format(words[i].key))
                # 最后一个词
                f.write('\t{:<14}\n'.format(words[-1].key))




treeType = 'b' # 可以根据用户的要求进行更改，在'rb'/'b'之间修改

if treeType == 'rb':
    tree = rbTree()
if treeType == 'b':
    # global BTree_t
    BTree_t = 5
    tree = BTree(BTree_t)

# 初始化
print('\n\n')
fileNames = ['1_initial.txt','2_delete.txt','3_insert.txt']
for fileName in fileNames:
    usedTime = [fileName]
   
    with open(fileName, 'r', encoding='utf-8') as f:
        t_start = time.time() 
        for i, line in enumerate(f):
            if i == 0:
                operation = line.strip()
                continue
            if operation == 'INSERT':
                word, meaning = line.split()
                tree.put(word,meaning)
                
                # #for test
                # results = tree.B_preorder()
                # for item in results:
                #     lvl = item[0]
                #     words = item[1]
                #     print('level=',lvl)
                #     for w in words:
                #         print(w.key,end=' ')
                #         print()
                # print('\n====================')
                
            elif operation == 'DELETE':
                word = line.split()[0]
                # if word == 'criminalistics':
                #     temp = input()
                # print('I will delte:',word)
                tree.delete(word)

                #for test
                # results = tree.B_preorder()
                # for item in results:
                #     lvl = item[0]
                #     words = item[1]
                #     print('level=',lvl)
                #     for w in words:
                #         print(w.key,end=' ')
                #         print()
                #         if w.key == 'bachelordom':
                #             temp = input()
                #             break
                # print('\n====================')

            if i%100 == 0: # 每间隔100就要计时一下
                t_end = time.time()
                usedTime.append(t_end - t_start)
                t_start = time.time()

    if treeType == 'rb':
        outFileName = 'rbTree print result/'+'rbt_'+fileName+'.txt'
    else:
        outFileName = 'BTree print result/'+'bt_t='+str(BTree_t)+"_"+fileName+'.txt'
    preorder_print_tree(tree,treeType,outFileName)

    print(usedTime)

t_start = time.time()
for _ in range(1000):
    node = tree.get('concisely')
t_end = time.time()
print((t_end - t_start)/1000)

t_start = time.time()
for _ in range(100):
    nodes = tree.rangeSearch('afr','cu')
t_end = time.time()
# for w in nodes:
#     print(w.key)
print((t_end - t_start)/100)