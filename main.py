import sys
import random
import time
import numpy as np
from PyQt5.QtWidgets import QWidget, QApplication, QLabel
from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtCore import QThread, pyqtSignal
from queue import Queue

# for throw logo
class myThread(QThread):
    finish_signal = pyqtSignal(int)
    def __init__(self, handle, mouse_loc, idx):
        super().__init__()
        self.handle = handle
        self.mouse_loc = mouse_loc
        self.idx = idx
        random.seed(time.time())
        mid = random.randint(500, 1100)
        self.x = np.linspace(mid-300, mid+300, 30)
        self.y = 0.005 * (self.x - mid) ** 2 + random.randint(0, 400)
        self.handle.move(self.x[0], self.y[0])
        self.handle.setVisible(True)

    def run(self):
        count = 0
        flag = False
        for idx in range(len(self.x)):
            if flag:
                time.sleep(0.05)
                count += 1
                if count == 5:
                    self.handle.success.setVisible(False)
                    self.handle.success.move(-1, -1)
                    break
                self.handle.move(self.x[idx], self.y[idx])
                continue
            self.handle.move(self.x[idx], self.y[idx])
            now_loc = self.mouse_loc[self.idx]
            if now_loc[0] < self.x[idx]+150 and now_loc[0] > self.x[idx] and now_loc[1] < self.y[idx] + 70 and now_loc[1] > self.y[idx]:
                self.handle.success.move(self.x[idx], self.y[idx])
                self.handle.success.setVisible(True)
                flag = True
            time.sleep(0.05)
        self.handle.setVisible(False)
        self.handle.move(-1, -1)
        self.finish_signal.emit(0)


class myLabel(QLabel):
    def __init__(self, parent, Qpixmap=None, idx=0):
        super().__init__(parent)
        self.p = parent
        self.idx = idx
        self.setVisible(False)
        self.setPixmap(Qpixmap)
        # self.setObjectName("LOGO" + str(idx))
        self.success = QLabel(parent)
        self.success.setPixmap(QPixmap("D:\\文件\\OneDrive - University of Macau\\20211122\\5points.jpg"))
        self.success.setVisible(False)

    def timerEvent(self, event):
        self.killTimer(self.p.id_list[self.idx].get())
        self.thread = myThread(self, self.p.loc_list, self.idx)
        self.thread.finish_signal.connect(self.receiveSignal)
        self.thread.start()
        self.p.now_squeue.put(self.idx)

    def receiveSignal(self, ins):
        pass


class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.widget = offerWinget(self)
        self.widget.setGeometry(-100, -150, 1600, 1200)
        self.setObjectName("MainWindow")
        self.setStyleSheet("#MainWindow{background-color: white}")
        self.setWindowTitle("Offer收割机")
        # 实验室电脑
        # self.baidu = QPixmap("D:\\onedrive\\OneDrive - University of Macau\\20211122\\百度.jpg")
        # self.zijie = QPixmap("D:\\onedrive\\OneDrive - University of Macau\\20211122\\字节跳动.jpg")
        # self.weiruan = QPixmap("D:\\onedrive\\OneDrive - University of Macau\\20211122\\微软.jpg")
        # self.weilai = QPixmap("D:\\onedrive\\OneDrive - University of Macau\\20211122\\蔚来.jpg")
        # self.xiapi = QPixmap("D:\\onedrive\\OneDrive - University of Macau\\20211122\\虾皮.png")
        # self.xiaohongshu = QPixmap("D:\\onedrive\\OneDrive - University of Macau\\20211122\\小红书.png")
        # self.xiaomi = QPixmap("D:\\onedrive\\OneDrive - University of Macau\\20211122\\小米.png")
        # Laptop
        self.baidu = QPixmap("D:\\文件\\OneDrive - University of Macau\\20211122\\百度.jpg")
        self.zijie = QPixmap("D:\\文件\\OneDrive - University of Macau\\20211122\\字节跳动.jpg")
        self.weiruan = QPixmap("D:\\文件\\OneDrive - University of Macau\\20211122\\微软.jpg")
        self.weilai = QPixmap("D:\\文件\\OneDrive - University of Macau\\20211122\\蔚来.jpg")
        self.xiapi = QPixmap("D:\\文件\\OneDrive - University of Macau\\20211122\\虾皮.png")
        self.xiaohongshu = QPixmap("D:\\文件\\OneDrive - University of Macau\\20211122\\小红书.png")
        self.xiaomi = QPixmap("D:\\文件\\OneDrive - University of Macau\\20211122\\小米.png")

        self.label1 = myLabel(self, self.baidu, 0)
        self.label2 = myLabel(self, self.zijie, 1)
        self.label3 = myLabel(self, self.weiruan, 2)
        self.label4 = myLabel(self, self.weilai, 3)
        self.label5 = myLabel(self, self.xiapi, 4)
        self.label6 = myLabel(self, self.xiaohongshu, 5)
        self.label7 = myLabel(self, self.xiaomi, 6)
        self.label_list = [self.label1, self.label2, self.label3, self.label4, self.label5, self.label6, self.label7]
        self.id_list = [Queue(), Queue(), Queue(), Queue(), Queue(), Queue(), Queue()]
        self.setMouseTracking(True)
        self.now_squeue = Queue()
        self.loc_list = [(-1, -1), (-1, -1), (-1, -1), (-1, -1), (-1, -1), (-1, -1), (-1, -1)]

    def timerEvent(self, event):
        idx = random.randint(0, 6)
        id_ = self.label_list[idx].startTimer(1000) #TODO 连续两个相同的，上一个没执行完下一个就开始？
        self.id_list[idx].put(id_)

    def mouseMoveEvent(self, event):
        # logo_obj = self.findChild(QLabel, "LOGO0")
        for idx in range(7):
            self.loc_list[idx] = (event.x(), event.y())


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

