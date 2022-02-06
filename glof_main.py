from PyQt5 import QtWidgets 
from PyQt5 import uic 
from PyQt5.QtCore import * 
from PyQt5.QtWidgets import (QWidget, QComboBox,
                             QLabel, QApplication)
from PyQt5.QtCore import QTime, Qt, QTimer

from selenium.webdriver.common.keys import Keys
import sys
import golf_jayurocc2
import datetime
import dateutil.relativedelta
from PyQt5.QtWidgets import QMessageBox

class Form(QtWidgets.QDialog): 
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent) 
        uic.loadUi("/home/lima/Work_Python/Golf/golf.ui", self)

        self.golfcourse.addItem('자유로 CC')
        self.golfcourse.addItem('KU Golf')
        self.golfcourse.currentIndexChanged.connect(self.onActivated)

        self.login.clicked.connect(self.onLoginClicked)
        self.start.clicked.connect(self.onStart)
        self.target_time1 = ""
        self.target_time2 = ""
        self.target_time3 = ""
        
        self.dateTimeEdit_1.setDateTime(datetime.datetime.today())
        self.dateTimeEdit_2.setDateTime(datetime.datetime.today())
        self.dateTimeEdit_3.setDateTime(datetime.datetime.today())

        self.err = 1
        self.status.setText("Preparing")
        self.logging("Preparing....")
        self.display()

        self.checkThreadTimer = QTimer()
        self.checkThreadTimer.setInterval(1000) #.5 seconds
        self.checkThreadTimer.timeout.connect(self.display)
        self.checkThreadTimer.start()

        self.show()

    def onActivated(self, text):
        print('onActivated')
        print(self.golfcourse.currentText())

    def onLoginClicked(self):
        self.logging("onLoginClicked....")

        print('onLoginClicked')
        print(self.id.text(), self.password.text())

        today = datetime.datetime.today().date()
        target = datetime.datetime.today().date() + dateutil.relativedelta.relativedelta(days=21)
        targetDate1 = datetime.datetime.strftime(target, '%Y%m%d')
        target_date = target#'20220226'
        target_time = '0800:1400'

        if self.golfcourse.currentText() == "자유로 CC":
            self.cc = golf_jayurocc2.Golf(str(today), str(target_date), str(target_time))
            self.err  = self.cc.login(self.id.text(), self.password.text())
            if (self.err == 1):
                self.status.setText("Login Failed")
                msg = QMessageBox()
                msg.setWindowTitle("Error")
                msg.setText("Login Error : " + self.id.text())
                msg.setIcon(QMessageBox.Critical)
                msg.exec_()
                print(self.err)
            else:
                self.status.setText("Login Success")

    def onStart(self):
        print("Start ...")
        # if self.err == 200:
        print(self.golfcourse.currentText())
        today = datetime.datetime.today()
        if self.checkBox_1.isChecked():
            self.target_time1 = self.dateTimeEdit_1.dateTime()
            print(self.target_time1)
            if self.target_time1 < today:
                print('time error')
        if self.checkBox_2.isChecked():
            self.target_time2 = self.dateTimeEdit_2.dateTime()
            print(self.target_time2)
            if self.target_time2 < today:
                print('time error')
        if self.checkBox_3.isChecked():
            self.target_time3 = self.dateTimeEdit_3.dateTime()
            print(self.target_time3)
            if self.target_time3 < today:
                print('time error')

        if self.cc.goto_reservepage() > 0:
            self.status.setText("Reserveing")
            self.logging("Reserve On-Going....")
        else:
            self.status.setText("Reserve Failed")
            self.logging("Reserve Failed....")

        self.cc.change_reservedate()
        self.status.setText("Date checking")
        self.logging("Target Date checking....")

        self.cc.make_reservation()
        self.status.setText("Reservation")
        self.logging("Reservation Completed....")

    def logging(self, text):
        dt_now = datetime.datetime.now()
        d_today = datetime.date.today()

        now = str(dt_now.strftime('%H:%M:%S'))
        self.log.appendPlainText("[" + now + "] " + text)

    def display(self):
        time_ = QTime.currentTime()
        now_ = QDate.currentDate()
        # print(time_.toString('h.m.s'))
        self.showtime.setText(now_.toString('yyyy-MM-dd') +",  " +time_.toString('hh:mm:ss'))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = Form()
    sys.exit(app.exec())