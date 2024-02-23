from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout
import sys 
import Ui_ui_matplotlib_pyqt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import numpy as np 
import cv2 as cv

class MatplotlibWidget(QWidget):
    def __init__(self,parent=None):
        super(MatplotlibWidget,self).__init__(parent)
        self.figure = Figure()
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.axis = self.figure.add_subplot(111)

        self.layoutvertical = QVBoxLayout(self)
        self.layoutvertical.addWidget(self.canvas)


class MainWidget(QWidget, Ui_ui_matplotlib_pyqt.Ui_Form):
    def __init__(self):
        super(MainWidget,self).__init__()
        self.setupUi(self)
        self.init_widget()
        self.pushButton.clicked.connect(self.plot_widget)

    def init_widget(self):
        self.matplotlibwidget = MatplotlibWidget()
        self.layoutvertical = QVBoxLayout(self.widget)
        self.layoutvertical.addWidget(self.matplotlibwidget)

    def plot_widget(self):
        self.matplotlibwidget.axis.clear()


        im = cv.imread('tagged.png')
        self.matplotlibwidget.axis.imshow(im)
        x = 1000*np.random.random(8)
        y = 1000*np.random.random(8)
        txts = ['1','2','3','4','5','6','7','8']
        self.matplotlibwidget.axis.scatter(x,y)

        for index ,txt in enumerate(txts):
            self.matplotlibwidget.axis.annotate(txt,(x[index],y[index]))
        self.matplotlibwidget.canvas.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWidget()
    w.show()
    sys.exit(app.exec_())