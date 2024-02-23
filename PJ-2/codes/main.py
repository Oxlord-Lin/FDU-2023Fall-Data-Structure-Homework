from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout
import sys 
import Ui_navigator
# import Ui_navigator_v2 as Ui_navigator
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import numpy as np 
import matplotlib.image as image
im = image.imread('tagged.png')
from Dijkstra import oneToAllShortestPath
from Floyd_Warshall import shortedPathBetweenTwoPoints_by_FW
from Johnson import shortedPathBetweenTwoPoints_by_Johnson
from Krustal import kruskal
from Prim import prim
from utils import *


class MatplotlibWidget(QWidget):
    def __init__(self,parent=None):
        super(MatplotlibWidget,self).__init__(parent)
        self.figure = Figure()
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.axis = self.figure.add_subplot(111)
        self.layoutvertical = QVBoxLayout(self)
        self.layoutvertical.addWidget(self.canvas)


class MainWidget(QWidget, Ui_navigator.Ui_Form):
    global im
    def __init__(self):
        super(MainWidget,self).__init__()
        self.setupUi(self)
        self.init_widget()

        self.pushButton.clicked.connect(self.oneToOne)
        self.pushButton_2.clicked.connect(self.oneToAll)
        self.pushButton_3.clicked.connect(self.subwayRoute_1)
        self.pushButton_5.clicked.connect(self.subwayRoute_2)

        self.pushButton_4.clicked.connect(self.busRoute)

        self.tab = 1 # the tab we are using
        self.radioButton.setChecked(True)

        self.radioButton_4.setChecked(True)

        self.radioButton_5.setChecked(True)
        self.radioButton_5.clicked.connect(self.disableSubwayRoute_2)
        self.radioButton_6.clicked.connect(self.enableSubwayRoute_2)
        self.init_operation_3()
        self.G = createGraph()
        self.tabWidget.currentChanged.connect(self.tabChanged)

    def tabChanged(self):
        if self.tabWidget.currentIndex() == 0:
            self.init_operation_1()
        elif self.tabWidget.currentIndex() == 1:
            self.init_operation_2()
        elif self.tabWidget.currentIndex() == 2:
            self.init_operation_3()
        elif self.tabWidget.currentIndex() == 3:
            self.init_operation_4()

    def init_operation_1(self):
        # self.matplotlibwidget.axis.clear()
        # self.matplotlibwidget.axis.imshow(im)
        # self.matplotlibwidget.canvas.draw()
        self.clearMap()
        self.lineEdit.clear()
        self.lineEdit_2.clear()
        self.textBrowser.clear()
        self.myPrint('操作一能够提供从起点到终点的最短路线以及路线长度！可以选择Johnson或Floyd-Warshall算法完成！\n')

    def init_operation_2(self):
        self.clearMap()
        self.lineEdit_3.clear()
        self.textBrowser.clear()
        self.myPrint('操作二能够提供从起点到所有其他点的最短路线以及路线长度！可以选择Johnson或Floyd-Warshall算法完成！\n')

    def init_operation_3(self):
        # self.init_widget()
        self.clearMap()
        self.textBrowser.clear()
        if self.radioButton_5.isChecked():
            self.pushButton_5.setEnabled(False)
        self.myPrint('操作三能够提供最优的地铁线路，也即最小生成树，并返回最小生成树的路径长度！可以选择Krustal或者Prim算法完成！\n')

    def init_operation_4(self):
        # self.init_widget()
        self.clearMap()
        self.lineEdit_4.clear()
        self.textBrowser.clear()
        self.myPrint('操作四能够提供从起点出发的最优的公交车路线！基于Dijkstra算法！\n')

    def init_widget(self):
        self.matplotlibwidget = MatplotlibWidget()
        self.matplotlibwidget.canvas.mpl_connect('button_press_event',self.on_canvas_click)
        self.layoutvertical = QVBoxLayout(self.widget)
        self.layoutvertical.addWidget(self.matplotlibwidget)
        self.matplotlibwidget.axis.imshow(im)

    def disableSubwayRoute_2(self):
        # self.myPrint('disable!')
        self.pushButton_5.setEnabled(False)

    def enableSubwayRoute_2(self):
        # self.myPrint('enable!')
        self.pushButton_5.setEnabled(True)

    def on_canvas_click(self,event):
        if event.inaxes is not None:
            x, y = event.xdata, event.ydata
            pointName = findClosestPoints(x,y)
            if self.tabWidget.currentIndex() == 0:
                start = self.lineEdit.text()
                terminal = self.lineEdit_2.text()
                if len(start) !=0 and len(terminal) != 0: # reset
                    self.lineEdit.clear()
                    self.lineEdit_2.clear()
                    self.clearMap()

                start = self.lineEdit.text()
                terminal = self.lineEdit_2.text()
                if len(start) == 0:  # if lineEdit has no input
                    self.lineEdit.setText(pointName)
                elif len(terminal) == 0: # if the lineEdit_2 has no input:
                    self.lineEdit_2.setText(pointName)

            elif self.tabWidget.currentIndex() == 1:
                self.lineEdit_3.setText(pointName)

            elif self.tabWidget.currentIndex() == 3:
                self.clearMap()
                self.lineEdit_4.setText(pointName)
                
    def clearMap(self):
        self.matplotlibwidget.axis.clear()
        self.matplotlibwidget.axis.plot((0),(0),linewidth=0.0001)
        self.matplotlibwidget.axis.imshow(im)
        self.matplotlibwidget.canvas.draw()

    def myPrint(self,mes):
        self.textBrowser.insertPlainText(str(mes))

    def myPlot(self,f,t):
        xx,yy = pointsToCoordinates(f,t)
        self.matplotlibwidget.axis.plot(xx,yy,'gold',linewidth=7)
        # self.matplotlibwidget.axis.imshow(im)
        self.matplotlibwidget.canvas.draw()


    def oneToOne(self):
        """对应操作一"""
        start = self.lineEdit.text()
        terminal = self.lineEdit_2.text()
        valid = checkValidPoint(start) and checkValidPoint(terminal)
        if not valid:
            self.textBrowser.clear()
            self.myPrint('请输入正确的起点与终点！\n\n')
            return
        J = self.radioButton.isChecked()
        if J: # using Johnson's algorithm
            path, distance = shortedPathBetweenTwoPoints_by_Johnson(self.G,start,terminal)
        else: # using Floyd-Warshall algorithm
            path, distance = shortedPathBetweenTwoPoints_by_FW(self.G,start,terminal)

        self.matplotlibwidget.axis.clear()
        self.matplotlibwidget.axis.imshow(im)
        self.textBrowser.clear()
        self.myPrint('路线为：\n')
        n = len(path)
        for index, v in enumerate(path):
            if index == n-1:
                self.myPrint(v)
                self.myPrint('\n')
                break
            f = v
            t = path[index+1]
            self.myPlot(f,t)
            self.myPrint(v)
            self.myPrint(' --> ')
        self.myPrint('路线长度为：')
        self.myPrint(round(distance,ndigits=1))


    def oneToAll(self):
        """对应操作二"""
        start = self.lineEdit_3.text()
        valid = checkValidPoint(start)
        if not valid:
            self.textBrowser.clear()
            self.myPrint('请输入正确的起点！\n')
            return
        J = self.radioButton_4.isChecked()
        vertices = self.G.getVertices()
        vertices = list(sorted(vertices))
        if J:
            results = []
            for v in vertices:
                results.append(shortedPathBetweenTwoPoints_by_Johnson(self.G,start,v))
        else:
            results = []
            for v in vertices:
                results.append(shortedPathBetweenTwoPoints_by_FW(self.G,start,v))

        self.textBrowser.clear()
        for item in results:
            path, distance = item
            terminal = path[-1]
            self.myPrint('\n终点为：\n')
            self.myPrint(terminal)
            self.myPrint('\n路线为：\n')
            n = len(path)
            for index, v in enumerate(path):
                if index == n-1:
                    self.myPrint(v)
                    self.myPrint('\n')
                    break
                self.myPrint(v)
                self.myPrint(' --> ')
            self.myPrint('路线长度为：')
            self.myPrint(round(distance,ndigits=1))
            self.myPrint('\n\n')

    def subwayRoute_1(self):
        """对应操作三，绘制出用Krustal算法找到的最小生成树"""
        MST_edges, distance = kruskal(self.G)

        # show and plot
        self.textBrowser.clear()
        self.clearMap()
        self.myPrint('最佳地铁线路（最小生成树）的总长度为：\n')
        self.myPrint(round(distance,ndigits=1))
        self.myPrint('\n地铁线路包含以下的边：\n')
        for e in MST_edges:
            u,v = e
            self.myPlot(u,v)
            self.myPrint('(' + u + ',' + v + ')\n')

    def subwayRoute_2(self):
        """对应操作三，绘制出用Prim算法找到的第二棵最小生成树"""
        start = 'H'
        # start = 'I'
        MST_edges, distance = prim(self.G,start)

        # show and plot
        self.textBrowser.clear()
        self.clearMap()
        self.myPrint('最佳地铁线路（最小生成树）的总长度为：\n')
        self.myPrint(round(distance,ndigits=1))
        self.myPrint('\n地铁线路包含以下的边：\n')
        for e in MST_edges:
            u,v = e
            self.myPlot(u,v)
            self.myPrint('(' + u + ',' + v + ')\n')

    
    def busRoute(self):
        """对应操作四，给定一个起点，基于Dijkstra算法，找到所有其他点到起点的最短路径"""
        start = self.lineEdit_4.text()
        valid = checkValidPoint(start)
        if not valid:
            self.textBrowser.clear()
            self.myPrint('请输入正确的起点！\n\n')
            return
        
        loc_path_dist = oneToAllShortestPath(self.G,start)
        G_edges = self.G.getEdges()
        edges, distance = pathsToEdges(loc_path_dist,G_edges)

        self.textBrowser.clear()
        self.clearMap()
        self.myPrint(f'以{start}为起点的最佳公交线路总长度为：\n')
        self.myPrint(round(distance,ndigits=1))
        self.myPrint('\n公交线路包含以下的边：\n')
        for e in edges:
            u,v = e
            self.myPlot(u,v)
            self.myPrint('(' + u + ',' + v + ')\n')



if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWidget()
    w.show()
    sys.exit(app.exec_())