import sys
import random
import time
import numpy as np
from PyQt5.QtWidgets import QWidget, QApplication, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer, QThread, pyqtSignal


class myThread(QThread):
    finish_signal = pyqtSignal(int)
    def __init__(self, handle):
        super().__init__()
        self.handle = handle
        length = 300
        step = 10
        start = np.random.uniform(0, 800)
        self.x = np.linspace(start, start+length, step)
        mid = np.random.uniform(200, 1400)
        a = -0.001
        b = -1 * mid * 2 * a
        self.y = a * self.x ** 2 + b * self.x + np.random.uniform(300, 400)

    def run(self):
        for idx in range(len(self.x)):
            print(self.x[idx], self.y[idx])
            self.handle.move(self.x[idx], self.y[idx])
            time.sleep(0.3)
        self.finish_signal.emit(0)

class myLabel(QLabel):
    def __init__(self, parent, Qpixmap=None):
        super().__init__(parent)
        self.p = parent
        self.setPixmap(Qpixmap)

    def timerEvent(self, event):
        self.killTimer(self.p.id_)
        self.thread = myThread(self)
        self.thread.finish_signal.connect(self.receiveSignal)
        self.thread.start()

    def receiveSignal(self, ins):
        pass

class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.widget = offerWinget(self)
        self.widget.setGeometry(10, 10, 1600, 1200)
        self.setWindowTitle("Offer收割机")
        self.baidu = QPixmap("D:\\文件\\OneDrive - University of Macau\\图片资料\\百度.jpg")
        self.zijie = QPixmap("D:\\文件\\OneDrive - University of Macau\\图片资料\\字节跳动.jpg")
        self.weiruan = QPixmap("D:\\文件\\OneDrive - University of Macau\\图片资料\\微软.jpg")
        self.weilai = QPixmap("D:\\文件\\OneDrive - University of Macau\\图片资料\\蔚来.jpg")
        self.xiapi = QPixmap("D:\\文件\\OneDrive - University of Macau\\图片资料\\虾皮.png")
        self.xiaohongshu = QPixmap("D:\\文件\\OneDrive - University of Macau\\图片资料\\小红书.png")
        self.xiaomi = QPixmap("D:\\文件\\OneDrive - University of Macau\\图片资料\\小米.png")

        self.myLabel1 = myLabel(self, self.baidu)
        self.label2 = QLabel(self)
        self.label3 = QLabel(self)
        self.label4 = QLabel(self)
        self.label5 = QLabel(self)
        self.label6 = QLabel(self)
        self.label7 = QLabel(self)
        self.label8 = QLabel(self)

        self.id_ = self.myLabel1.startTimer(1000)

        self.setMouseTracking(True)



class offerWinget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setMouseTracking(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = Main()
    myWin.show()
    sys.exit(app.exec_())

