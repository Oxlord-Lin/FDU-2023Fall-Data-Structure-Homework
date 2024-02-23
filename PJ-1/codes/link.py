from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog
# import os

from Ui_dic import Ui_Form
from RedBlackTree import rbTree
from BTree import BTree



def preorder_print_tree(tree, treeType, outFileName):
    """将树打印到对应的文件中"""
    if treeType == 'rb':
        result = tree.RB_preorder()
        try:
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
        except Exception:
            return
        
    elif treeType == 'b':
        result = tree.B_preorder()
        try:
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
        except Exception:
            return


global tree
tree = None # 初始化全局变量一下，可以用于防错检查

def checkTree():
    global tree
    if tree is None:
        myPrint('请先选择要建立的树！')
        return False


def myPrint(mes):
    ui.textBrowser.append(mes)


def openFile():
    check = checkTree()
    if check is False:
        return
    fname = QFileDialog.getOpenFileName(None,'打开文件','./')
    if fname[0]: # fname[0]是文件路径
        ui.textBrowser_2.clear()
        ui.textBrowser_2.append(fname[0])
        # 截取文件名
        fileName = fname[0].split('/')[-1]  
        myPrint('正在执行以下文件：'+fileName)
        print(fileName)
        with open(fname[0], 'r', encoding='utf-8') as f:
            for i, line in enumerate(f):
                if i == 0:
                    operation = line.strip()
                    continue

                if operation == 'INSERT':
                    word, meaning = line.split()
                    tree.put(word,meaning)
                    
                elif operation == 'DELETE':
                    word = line.split()[0]
                    tree.delete(word)

        if isinstance(tree,rbTree):
            if tree.root is None:
                return
            treeType = 'rb'
            outFileName = 'rbTree print result/'+'rbt_'+fileName+'.txt'
        else: # tree is a BTree
            if len(tree.root.words) == 0:
                return
            treeType = 'b'
            outFileName = 'BTree print result/'+'bt_t='+str(tree.t)+"_"+fileName+'.txt'
        # 先序遍历，打印到对应的文件中 
        preorder_print_tree(tree,treeType,outFileName)
        myPrint('执行完毕！')
        if treeType == 'rb':
            myPrint('已经将红黑树打印到"rbTree print result"文件夹下')
        elif treeType == 'b':
            myPrint('已经将B树打印到"BTree print result"文件夹下')


def set_rb():
    global tree
    if tree is None or isinstance(tree,BTree):
        tree = rbTree()
        # 重新建树时清空textbrwoser
        ui.textBrowser.clear()
        myPrint('重新建立一棵红黑树！')
    else:
        return



def set_b():
    global tree
    if tree is None or isinstance(tree,rbTree):
        try:
            t = int(ui.lineEdit_4.text())
            if t < 2:
                myPrint('t值需要大于等于2')
                return
        except Exception:
            myPrint('请指定B树的t值')
            return
        tree = BTree(t)
        # 重新建树时清空textbrwoser
        ui.textBrowser.clear()
        myPrint('重新建立一棵B树！t='+str(t))
    else:
        return

def insert():
    check = checkTree()
    if check is False:
        return
    ui.textBrowser.clear()
    global tree
    key = ui.lineEdit_6.text()
    value = ui.lineEdit_7.text()
    flg = tree.put(key,value)
    if flg == -1:
        myPrint('错误！不能重复插入单词：'+key)
    else:
        myPrint('成功插入单词：'+key)


def delete():
    check = checkTree()
    if check is False:
        return
    ui.textBrowser.clear()
    global tree
    key = ui.lineEdit_6.text()
    flg = tree.delete(key)
    if flg == -1:
        myPrint('错误！试图删除不存在的单词：'+key)
    else:
        myPrint('成功删除单词：'+key)


def translate():
    check = checkTree()
    if check is False:
        return
    ui.textBrowser.clear()
    global tree
    key = ui.lineEdit.text()
    if isinstance(tree,rbTree):
        result = tree.get(key)
        if result is None:
            myPrint('词典中不存在该单词！')
        else:
            meaning = result.payload
            myPrint('English: '+key+'\t 中文：'+meaning)

    elif isinstance(tree,BTree):
        index,node = tree.get(key)
        if index is None:
            myPrint('词典中不存在该单词！')
        else:
            meaning = node.words[index].value
            myPrint('English: '+key+'\t 中文：'+meaning)
    

def rangeSearch():
    check = checkTree()
    if check is False:
        return
    ui.textBrowser.clear()
    bd1 = ui.lineEdit_2.text()
    bd2 = ui.lineEdit_3.text()
    if isinstance(tree,rbTree):
        words = tree.rangeSearch(bd1,bd2)
        for w in words:
            myPrint('English: '+w.key+'\t\t'+'中文：'+w.payload)
    elif isinstance(tree,BTree):
        words = tree.rangeSearch(bd1,bd2)
        for w in words:
            myPrint('English: '+w.key+'\t\t'+'中文：'+w.value)

if __name__ == '__main__':
    app = QApplication([])

    window = QWidget()
    ui = Ui_Form()
    ui.setupUi(window)

    ui.pushButton_5.clicked.connect(openFile)
    ui.radioButton.clicked.connect(set_rb)
    ui.radioButton_2.clicked.connect(set_b)
    ui.pushButton_3.clicked.connect(insert)
    ui.pushButton_4.clicked.connect(delete)
    ui.pushButton.clicked.connect(translate)
    ui.pushButton_2.clicked.connect(rangeSearch)

    window.show()

    app.exec()