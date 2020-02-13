import sys
from PyQt5 import QtWidgets, QtCore,QtGui
from PyQt5.QtWidgets import QToolTip, QMainWindow, QSlider, QSpinBox, QPushButton, QProgressBar
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, pyqtSignal
import psutil
from win10toast import ToastNotifier
import time
#import batt_det


class Window(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.top = 500
        self.bottom = 200
        self.width = 500
        self.height = 820
        self.notif = ToastNotifier()
        self.l = 20
        self.h = 95
        self.b = psutil.sensors_battery()
        self.percent = self.b.percent
        self.plugged = self.b.power_plugged
        self.InitWindow()
        self.threadclass = ThreadClass()
        self.threadclass.start()
        self.threadclass.update_progressbar_signal.connect(self.update_progressbar)

    def InitWindow(self):

        self.headingg = QtWidgets.QLabel('<B> POWER ALERT</B>', self)
        self.headingg.setGeometry(300, 0, 300, 50)  # settingGeometry(x-axis, y-axis, width of widget, height of widget)
        self.headingg.setFont(QFont('SansSerif', 15))
        QToolTip.setFont(QFont('SansSerif', 10))

        self.l_bat = QtWidgets.QLabel('<B> Set Low Power % </B>', self)
        self.l_bat.setFont(QFont('SansSerif', 9))
        self.l_bat.setGeometry(3, 80, 220, 50)
        self.l_bat.setToolTip('Set the battery % for which you want to get <B> low battery notification. </B>')

        self.h_bat = QtWidgets.QLabel('<B> Set High Power % </B>', self)
        self.h_bat.setFont(QFont('SansSerif', 9))
        self.h_bat.setGeometry(3, 120, 240, 50)
        self.h_bat.setToolTip('Set the battery % for which you want to get <B> high battery notification.</B>')

        self.l_set = QSlider(Qt.Horizontal, self)
        self.l_set.setGeometry(170, 100, 150, 20)
        self.l_set.setMinimum(1)
        self.l_set.setMaximum(100)
        self.l_set.setValue(20)
        self.l_set.setTickPosition(QSlider.TicksAbove)

        self.l_spin = QSpinBox(self)
        self.l_spin.setGeometry(335, 100, 50, 20)
        self.l_spin.setValue(20)
        self.l_set.valueChanged.connect(self.l_spin.setValue)
        self.l_spin.valueChanged.connect(self.l_set.setValue)

        self.h_set = QSlider(Qt.Horizontal, self)
        self.h_set.setGeometry(170, 140, 150, 20)
        self.h_set.setMinimum(10)
        self.h_set.setMaximum(100)
        self.h_set.setValue(95)
        self.h_set.setTickPosition(QSlider.TicksAbove)

        self.h_spin = QSpinBox(self)
        self.h_spin.setGeometry(335, 140, 50, 20)
        self.h_spin.setValue(95)
        self.h_set.valueChanged.connect(self.h_spin.setValue)
        self.h_spin.valueChanged.connect(self.h_set.setValue)

        self.tl_txt = QtWidgets.QLabel('<B> Time Left: </B>', self)
        self.tl_txt.setFont(QFont('SansSerif', 9))
        self.tl_txt.setGeometry(3, 160, 240, 50)

        self.ni_txt = QtWidgets.QLabel('<B> ALERT Interval: </B>', self)
        self.ni_txt.setFont(QFont('SansSerif', 9))
        self.ni_txt.setGeometry(3, 200, 240, 50)
        self.n_interval = QtWidgets.QLineEdit("10", self)
        # self.n_interval.setText("10")
        self.n_interval.setGeometry(180, 210, 40, 30)

        self.sec = QtWidgets.QLabel('(seconds)', self)
        self.sec.setFont(QFont('SansSerif', 9))
        self.sec.setGeometry(230, 210, 80, 30)

        self.runn = QPushButton("RUN", self)
        self.runn.setFont(QFont('SansSerif', 9, weight=QFont.Bold))
        self.runn.setGeometry(100, 260, 80, 50)
        self.runn.clicked.connect(self.notification)

        self.bat_display = QProgressBar(self)
        self.bat_display.setGeometry(230, 370, 400, 80)
        self.bat_display.setFont(QFont('SansSerif', 20, weight=QFont.Bold))

        self.created_by = QtWidgets.QLabel('<B> Created by- Manvir Singh Channa</B>', self)
        self.created_by.setGeometry(620, 440, 300, 50)
        self.to_contact = QtWidgets.QLabel('<B> Contact for feedback- manvirchanna247@gmail.com</B>', self)
        self.to_contact.setGeometry(500, 460, 570, 50)

        self.setWindowTitle('Power Alert')
        self.setWindowIcon(QIcon('Icon.png'))
        self.setGeometry(self.top, self.bottom, self.height, self.width)
        self.show()

    def notification(self):
        QtGui.QGuiApplication.processEvents()
        while True:
            self.b = psutil.sensors_battery()
            self.percent = self.b.percent
            self.plugged = self.b.power_plugged
            QtGui.QGuiApplication.processEvents()
            if not self.plugged and self.percent <= self.l_set.value():
                self.notif.show_toast("Battery is at {}%. ".format(self.percent), "Plug in the Charger!")
            QtGui.QGuiApplication.processEvents()
            if self.plugged and self.percent >= self.h_set.value():
                self.notif.show_toast("Battery is at {}%. ".format(self.percent), "Unplug the Charger!")

            time.sleep(int(self.n_interval.text()))

    def closeEvent(self, event):
        sys.exit()

    def update_progressbar(self, val):
        self.bat_display.setValue(val)

class ThreadClass(QtCore.QThread):
    update_progressbar_signal = pyqtSignal(float)

    def __init__(self, parent=None):
        super(ThreadClass, self).__init__(parent)

    def run(self):
        while True:
            val = batt_det.bat_details() #Getting current battery value
            
            time.sleep(1)
            self.update_progressbar_signal.emit(val)


app = QtWidgets.QApplication(sys.argv)
a_window = Window()
sys.exit(app.exec_())