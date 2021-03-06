# -*- coding: utf-8 -*-
# Author: Changxing DENG
# @Time: 2021/11/22 1:07


import sys
import random
import time
import numpy as np
from PyQt5.QtWidgets import QWidget, QApplication, QLabel
from PyQt5.QtGui import QPixmap, QColor, QPalette, QFont
from PyQt5.QtCore import QThread, pyqtSignal
from queue import Queue
from PyQt5.QtCore import Qt
from PyQt5.QtMultimedia import QSound

# for throw logo
class myThread(QThread):
    finish_signal = pyqtSignal(int)
    def __init__(self, handle, mouse_loc, idx):
        super().__init__()
        self.handle = handle
        self.mouse_loc = mouse_loc
        self.idx = idx
        random.seed(time.time())
        mid = random.randint(300, 1100)
        if random.choice([0, 1]) == 1:
            self.x = np.linspace(mid - 300, mid + 300, 30)
        else:
            self.x = np.linspace(mid + 300, mid - 300, 30)
        self.y = 0.005 * (self.x - mid) ** 2 + random.randint(0, 400)
        self.handle.move(self.x[0], self.y[0])
        self.handle.setVisible(True)

    def run(self):
        for idx in range(len(self.x)):
            self.handle.move(self.x[idx], self.y[idx])
            now_loc = self.mouse_loc[self.idx]
            width = self.handle.width()
            height = self.handle.height()
            if now_loc[0] < self.x[idx] + width + 10 and now_loc[0] > self.x[idx] - 10 and now_loc[1] < self.y[idx] + height + 10 and \
                    now_loc[1] > self.y[idx] - 10:
                money = int(self.handle.p.money_label.text())
                if self.idx < 6:
                    money += 5
                    self.handle.success.move(self.x[idx] - 50, self.y[idx] - 50)
                    self.handle.success.setVisible(True)
                else:
                    money -= 5
                    self.handle.fail.move(self.x[idx] - 50, self.y[idx] - 50)
                    self.handle.fail.setVisible(True)
                self.handle.p.money_label.setText(str(money))
                time.sleep(0.1)
                break
            time.sleep(0.05)

        self.handle.success.setVisible(False)
        self.handle.success.move(-1, -1)
        self.handle.fail.setVisible(False)
        self.handle.fail.move(-1, -1)
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
        self.success.setPixmap(QPixmap("D:\\onedrive\\OneDrive - University of Macau\\20211122\\5points.jpg"))
        # self.success.setPixmap(QPixmap("D:\\??????\\OneDrive - University of Macau\\20211122\\5points.jpg"))
        self.success.setVisible(False)

        self.fail = QLabel(parent)
        self.fail.setPixmap(QPixmap("D:\\onedrive\\OneDrive - University of Macau\\20211122\\minus5points.jpg"))
        # self.fail.setPixmap(QPixmap("D:\\??????\\OneDrive - University of Macau\\20211122\\minus5points.jpg"))
        self.fail.setVisible(False)

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
        self.setWindowTitle("Offer?????????")
        # self.sound = QSound("D:\\onedrive\\OneDrive - University of Macau\\20211122\\????????????.wav", self) # ?????????
        # self.sound = QSound("D:\\onedrive\\OneDrive - University of Macau\\20211122\\????????????.wav", self)  # ?????????
        # self.sound.play()
        # self.sound.setLoops(100)
        # self.sound = QSound("D:\\onedrive\\OneDrive - University of Macau\\20211122\\???.wav", self)

        # ???????????????
        self.logo_list = [QPixmap("D:\\onedrive\\OneDrive - University of Macau\\20211122\\??????.jpg"),
                          QPixmap("D:\\onedrive\\OneDrive - University of Macau\\20211122\\????????????.jpg"),
                          QPixmap("D:\\onedrive\\OneDrive - University of Macau\\20211122\\??????.jpg"),
                          QPixmap("D:\\onedrive\\OneDrive - University of Macau\\20211122\\??????.jpg"),
                          QPixmap("D:\\onedrive\\OneDrive - University of Macau\\20211122\\??????.png"),
                          QPixmap("D:\\onedrive\\OneDrive - University of Macau\\20211122\\?????????.png"),
                          QPixmap("D:\\onedrive\\OneDrive - University of Macau\\20211122\\??????.png"),
                          QPixmap("D:\\onedrive\\OneDrive - University of Macau\\20211122\\oppo.jpg"),
                          QPixmap("D:\\onedrive\\OneDrive - University of Macau\\20211122\\??????.jpg"),
                          QPixmap("D:\\onedrive\\OneDrive - University of Macau\\20211122\\??????.jpg")]
        # Laptop
        # self.logo_list = [QPixmap("D:\\??????\\OneDrive - University of Macau\\20211122\\??????.jpg"),
        #                   QPixmap("D:\\??????\\OneDrive - University of Macau\\20211122\\????????????.jpg"),
        #                   QPixmap("D:\\??????\\OneDrive - University of Macau\\20211122\\??????.jpg"),
        #                   QPixmap("D:\\??????\\OneDrive - University of Macau\\20211122\\??????.jpg"),
        #                   QPixmap("D:\\??????\\OneDrive - University of Macau\\20211122\\??????.png"),
        #                   QPixmap("D:\\??????\\OneDrive - University of Macau\\20211122\\?????????.png"),
        #                   QPixmap("D:\\??????\\OneDrive - University of Macau\\20211122\\??????.png"),
        #                   QPixmap("D:\\??????\\OneDrive - University of Macau\\20211122\\oppo.jpg")
        #                   QPixmap("D:\\??????\\OneDrive - University of Macau\\20211122\\??????.jpg")
        #                   QPixmap("D:\\??????\\OneDrive - University of Macau\\20211122\\??????.jpg")]
        self.label_list = []
        self.id_list = []
        self.loc_list = []
        for idx, logo in enumerate(self.logo_list):
            self.label_list.append((myLabel, logo, idx))
            self.id_list.append(Queue())
            self.loc_list.append((-1, -1))
        self.now_squeue = Queue()

        self.money_label = QLabel(self)
        self.money_label.setFixedWidth(100)
        self.money_label.setFixedHeight(60)
        self.money_label.move(1200, 50)
        self.money_label.setText("0")
        self.money_label.setAlignment(Qt.AlignCenter)
        pe = QPalette()
        pe.setColor(QPalette.WindowText, Qt.green)
        self.money_label.setPalette(pe)
        self.money_label.setFont(QFont("Roman times", 50, QFont.Bold))

        self.setMouseTracking(True)

    def timerEvent(self, event):
        idx = random.randint(0, len(self.label_list)-1)
        id_ = self.label_list[idx][0](self, self.label_list[idx][1], self.label_list[idx][2]).startTimer(800) # ????????????????????????????????????????????????????????????logo
        self.id_list[idx].put(id_)

    def mouseMoveEvent(self, event):
        for idx in range(len(self.label_list)):
            self.loc_list[idx] = (event.x(), event.y())


class offerWinget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setMouseTracking(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = Main()
    myWin.startTimer(800)
    myWin.show()
    sys.exit(app.exec_())
