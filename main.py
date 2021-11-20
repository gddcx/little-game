import sys
import random
import time
import numpy as np
from PyQt5.QtWidgets import QWidget, QApplication, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QThread, pyqtSignal
from queue import Queue


class myThread(QThread):
    finish_signal = pyqtSignal(int)
    def __init__(self, handle):
        super().__init__()
        self.handle = handle
        self.handle.setVisible(True)
        random.seed(time.time())
        mid = random.randint(500, 1100)
        self.x = np.linspace(mid-300, mid+300, 30)
        self.y = 0.005 * (self.x - mid) ** 2

    def run(self):
        for idx in range(len(self.x)):
            self.handle.move(self.x[idx], self.y[idx])
            time.sleep(0.05)
        self.handle.setVisible(False)
        self.finish_signal.emit(0)

class myLabel(QLabel):
    def __init__(self, parent, Qpixmap=None, idx=0):
        super().__init__(parent)
        self.p = parent
        self.idx = idx
        self.setVisible(False)
        self.setPixmap(Qpixmap)

    def timerEvent(self, event):
        self.killTimer(self.p.id_list[self.idx].get())
        self.thread = myThread(self)
        self.thread.finish_signal.connect(self.receiveSignal)
        self.thread.start()

    def receiveSignal(self, ins):
        pass

class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.widget = offerWinget(self)
        self.widget.setGeometry(-100, -150, 1600, 1200)
        self.setWindowTitle("Offer收割机")
        self.baidu = QPixmap("D:\\文件\\OneDrive - University of Macau\\20211122\\百度.jpg")
        self.zijie = QPixmap("D:\\文件\\OneDrive - University of Macau\\20211122\\字节跳动.jpg")
        self.weiruan = QPixmap("D:\\文件\\OneDrive - University of Macau\\20211122\\微软.jpg")
        self.weilai = QPixmap("D:\\文件\\OneDrive - University of Macau\\20211122\\蔚来.jpg")
        self.xiapi = QPixmap("D:\\文件\\OneDrive - University of Macau\\20211122\\虾皮.png")
        self.xiaohongshu = QPixmap("D:\\文件\\OneDrive - University of Macau\\20211122\\小红书.png")
        self.xiaomi = QPixmap("D:\\文件\\OneDrive - University of Macau\\20211122\\小米.png")

        self.label_list = [myLabel(self, self.baidu, 0), myLabel(self, self.zijie, 1), myLabel(self, self.weiruan, 2),
                           myLabel(self, self.weilai, 3), myLabel(self, self.xiapi, 4), myLabel(self, self.xiaohongshu, 5),
                           myLabel(self, self.xiaomi, 6)]
        self.id_list = [Queue(), Queue(), Queue(), Queue(), Queue(), Queue(), Queue()]
        self.setMouseTracking(True)

    def timerEvent(self, event):
        idx = random.randint(0, 6)
        id_ = self.label_list[idx].startTimer(1000) #TODO 连续两个相同的，上一个没执行完下一个就开始？
        self.id_list[idx].put(id_)

    def mouseMoveEvent(self, event):
        print(event.x(), event.y())


class offerWinget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setMouseTracking(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = Main()
    myWin.startTimer(2000)
    myWin.show()
    sys.exit(app.exec_())

