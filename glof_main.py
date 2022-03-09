from PyQt5 import QtWidgets 
from PyQt5 import uic 
from PyQt5.QtCore import * 
from PyQt5.QtWidgets import (QWidget, QComboBox,
                             QLabel, QApplication)
from PyQt5.QtCore import QTime, Qt, QTimer
from PyQt5.QtWidgets import QApplication, QDialog, QDialogButtonBox, QVBoxLayout

from selenium.webdriver.common.keys import Keys
import sys

import golf_jayurocc2
import golf_laviebell
import golf_kugolf
import golf_ariji

import datetime
import dateutil.relativedelta
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtGui

import os
from os.path import exists
import json

from PyQt5.QtGui import *

import time
import bcrypt
import base64
idpass = './id.json'

from apscheduler.schedulers.background import BackgroundScheduler

class Form(QtWidgets.QDialog): 
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent) 
        uic.loadUi("/home/lima/Work_Python/Golf/golf.ui", self)
        self.cc = None
        self.golfcourse.addItem('자유로 CC')
        self.golfcourse.addItem('KU Golf')
        self.golfcourse.addItem('LavieBell')
        self.golfcourse.addItem('Ariji CC')
        self.golfcourse.currentIndexChanged.connect(self.onActivated)

        self.login.clicked.connect(self.onLoginClicked)
        self.make_reserve.clicked.connect(self.onReserve)
        self.target_time1 = ""
        self.target_time2 = ""
        self.target_time3 = ""

        # self.get_timetable.clicked.connect(self.GetTimeTable)
        self.listWidget.itemDoubleClicked.connect(self.onTimetable)
        self.calendarWidget.clicked.connect(self.GetTimeTable)
        

        today = datetime.datetime.today()
        selected_date = QDate(today.year,today.month, today.day+21)
        self.calendarWidget.setSelectedDate(selected_date)
        self.err = 1
        self.progress = -1

        self.checkBox_auto.clicked.connect(self.onAutoEnabled)
        self.auto_start.clicked.connect(self.onAutoReserve)
        self.auto_stop.clicked.connect(self.onAutoStop)
        self.auto_info.clicked.connect(self.onAutoInfo)
        self.radio_fixed.clicked.connect(self.onRadioDay)
        self.radio_plusday.clicked.connect(self.onRadioDay)
        

        self.onAutoEnabled()

        self.status.setText("Preparing")
        self.logging("Preparing....")
        self.display()

        self.checkThreadTimer = QTimer()
        self.checkThreadTimer.setInterval(1000) #.5 seconds
        self.checkThreadTimer.timeout.connect(self.display)
        self.checkThreadTimer.start()
        self.logout.clicked.connect(self.onLogout)
        self.timetable_available = False
        

        if self.saveIDPASS:
            if exists(idpass):
                with open(idpass, 'r') as infile:
                    data=json.load(infile)
                    self.id.setText(data['id'])
                    passwd = base64.b64decode(data['password']).decode('utf-8')
                    self.password.setText(passwd)

        self.listWidget.insertItem(0, "Ready...")
        self.get_reserved_info.clicked.connect(self.onGetReservation)
        self.get_reserved_info_cancel.clicked.connect(self.cancelReserve)

        self.auto = AutoReserve()
        self.show()


    def onAutoEnabled(self):
        flag = self.checkBox_auto.isChecked()
 
        # setting date to the date edit
        today = datetime.datetime.today().date() + datetime.timedelta(days=22)
        self.target_date.setDate(QDate(today.year, today.month, today.day))
        if flag:
            self.scheduler_time.setDisabled(False)
            self.target_date.setDisabled(False)
            self.target_time_start.setDisabled(False)
            self.target_time_end.setDisabled(False)

            self.auto_start.setDisabled(False)
            self.auto_stop.setDisabled(False)
            self.auto_info.setDisabled(False)
            
            
            self.radio_fixed.setDisabled(False)
            self.radio_plusday.setDisabled(False)
            self.radio_fixed.setChecked(True)
            self.onRadioDay()
        else:
            self.scheduler_time.setDisabled(True)
            self.target_date.setDisabled(True)
            self.target_time_start.setDisabled(True)
            self.target_time_end.setDisabled(True)

            self.auto_start.setDisabled(True)
            self.auto_stop.setDisabled(True)
            self.auto_info.setDisabled(True)
            self.radio_fixed.setDisabled(True)
            self.radio_plusday.setDisabled(True)
            self.plusday.setDisabled(True)
            


    def onRadioDay(self):
        if self.radio_fixed.isChecked() : 
            self.target_date.setDisabled(False)
            self.plusday.setDisabled(True)
        if self.radio_plusday.isChecked():
            self.target_date.setDisabled(True)
            self.plusday.setDisabled(False)

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
            self.cc = golf_jayurocc2.Jayuro(str(today), str(target_date), str(target_time))
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
                if self.saveIDPASS:
                    if exists(idpass):
                        os.remove(idpass)

                    with open(idpass, 'w') as outfile:
                        # passwd = bcrypt.hashpw(self.password.text().encode('utf-8'), bcrypt.gensalt())
                        # print(passwd)
                        
                        passwd=base64.b64encode(self.password.text().encode('utf-8'))
                        print(passwd)
                        a = passwd.decode('ascii')
                        print(a)
                        data = {'id':self.id.text(), 'password':a}
                        json.dump(data, outfile)

                self.logging("Login Successfully")
                self.status.setText("Login Success")

                self.progress = 0
                self.GetTimeTable()

    def onLogout(self):
        if self.cc == None:
            self.logging("Login is needed")
            return
        print('logging out ....')
        self.cc.logout()
        self.logging("Logout... Teminated")
        self.cc = None


    def GetTimeTable(self):
        print("Get Golf Time Table")
        self.listWidget.clear()
        today = datetime.datetime.today()
        target = self.calendarWidget.selectedDate()
        if self.progress == -1:
            print("Login is not done")
            self.listWidget.insertItem(0, "Please login first")
            return

        t=target.toPyDate()
        print(t)
        
        if today.date() > target.toPyDate() :
            print('Today : ', today.day)
            print('Target Date : ', target.day())
            print("Target date is too late")
            self.listWidget.insertItem(0, "Unavailable")
            return

        print(target)
        target_date = '%4d-%02d-%02d' % (target.year(), target.month(), target.day())
        self.cc.set_date(target_date)

        if self.cc.goto_reservepage() > 0:
            self.status.setText("Reserving")
            self.logging("Reserve On-Going....")
        else:
            self.status.setText("Reserve Failed")
            self.logging("Reserve Failed....")
        
        table=self.cc.get_timetable()

        # model = QStandardItemModel()
        # self.listWidget.insertItem
        if len(table) <= 0:
            self.timetable_available = False
            self.listWidget.insertItem(0, "No available time")
        for i, data in enumerate(table):
            self.timetable_available = True
            self.listWidget.insertItem(i, str(','.join(data)))
        #     model.appendRow(QStandardItem(str(f)))
        # self.timetable.setModel(model)

        # for i in table:
        #     # self.timetable.addItem(str(i))
        #     self.timetable.appendRow(str(i))
        #     # istView.setModel(model) # listView에 만들어진 모델을 설정합니다.

    def onTimetable(self):
        print("onTimetable")
        if self.timetable_available == False:
            return

        sel = self.listWidget.currentItem().text().split(',')
        print(sel)

        self.cc.set_date(sel[0])
        self.cc.set_time(sel[1]+':'+sel[1])
        result = self.cc.change_reservedate()
        self.logging(result)
        if result == 0:
            self.panaltycheck(sel[0])
            # msg = self.cc.make_reservation()
            # print(msg)
            # self.logging(msg)
            # self.status.setText("Reservation")
            # self.logging("Reservation Completed....")

            print(sel)


    def onReserve(self):
        print("Make reservation ...")
        if self.cc is None:
            self.logging('Please login first')
            return 

        sel = self.listWidget.currentItem().text().split(',')
        self.cc.set_date(sel[0])
        self.cc.set_time(sel[1]+':'+sel[1])
        result = self.cc.change_reservedate()
        self.logging(sel)
        self.logging(result)

        if result == 0:
            msg = self.cc.make_reservation()
            self.logging(msg)
            self.status.setText("Reservation")
        print(sel)
        return

    def onAutoReserve(self):
        schedule = self.scheduler_time.time()
        print(schedule.hour(), schedule.minute(), schedule.second())
        if self.radio_fixed.isChecked():
            target_date_d = self.target_date.date()
            target_date = "%04d-%02d-%02d" % (target_date_d.year(), target_date_d.month(), target_date_d.day())
            plus_d = 0
        elif self.radio_plusday.isChecked():
            today = datetime.date.today()
            plus_d = int(self.plusday.text())
            today = today + datetime.timedelta(plus_d)
            target_date = today
        
        target_time_s = self.target_time_start.time()
        target_time_e = self.target_time_end.time()
        target_time = "%02d%02d:%02d%02d" %(target_time_s.hour(),target_time_s.minute(), target_time_e.hour(),target_time_e.minute())

        print(target_date, target_time)

        if self.golfcourse.currentText() == "자유로 CC":
        # golf_jayurocc2.autoReserve(self.id.text(), self.password.text(), schedule, target_date, target_time, plus_d)        
            self.auto.addGolfJob("Jayuro", golf_jayurocc2.golfjob2, self.id.text(), self.password.text(), schedule, target_date, target_time, plus_d)
        elif self.golfcourse.currentText() == "KU Golf":
            self.auto.addGolfJob("KU Golf", golf_kugolf.golfjob2, self.id.text(), self.password.text(), schedule, target_date, target_time, plus_d)
        elif self.golfcourse.currentText() == "LavieBell":
            self.auto.addGolfJob("LavieBell", golf_laviebell.golfjob2, self.id.text(), self.password.text(), schedule, target_date, target_time, plus_d)
        elif self.golfcourse.currentText() == "Ariji CC":
            self.auto.addGolfJob("Ariji CC", golf_ariji.golfjob2, self.id.text(), self.password.text(), schedule, target_date, target_time, plus_d)

    def onAutoStop(self):
        print('onAutoStop')
        self.auto.autoStop()

    def onAutoInfo(self):
        self.auto.autoInfo()

    def onAutoGetInfo(self):
        target_date_d = self.target_date.date()
        target_time_s = self.target_time_start.time()
        target_time_e = self.target_time_end.time()
        target_date = "%04d-%02d-%02d" %(target_date_d.year(), target_date_d.month(), target_date_d.day())
        target_time = "%02d%02d:%02d%02d" %(target_time_s.hour(),target_time_s.minute(), target_time_e.hour(),target_time_e.minute())
        print(target_date, target_time)

        self.cc.set_date(target_date)
        self.cc.set_time(target_time)
        result = self.cc.change_reservedate()
        self.logging(result)
        if result == 0:
            msg = self.cc.make_reservation()
            print(msg)
            self.logging(msg)
            self.status.setText("Time Table Information")
            self.logging("Retrieve time table....")


    def logging(self, text):
        dt_now = datetime.datetime.now()
        d_today = datetime.date.today()

        now = str(dt_now.strftime('%H:%M:%S'))
        self.log.appendPlainText("[" + now + "] " + str(text))
        self.log.moveCursor(QtGui.QTextCursor.End)

    def display(self):
        time_ = QTime.currentTime()
        now_ = QDate.currentDate()
        # print(time_.toString('h.m.s'))
        self.showtime.setText(now_.toString('yyyy-MM-dd') +",  " +time_.toString('hh:mm:ss'))

    def onGetReservation(self):
        if self.cc is None:
            self.logging('Please login first')
            return 

        data=self.cc.get_reservationinfo()
        self.listWidget.clear()
        print(data)

        i = 0
        for key in data:
            print(key,data[key])
            self.listWidget.insertItem(i,str(key) + ":" + str(data[key]))
            i = i+1

    def cancelReserve(self):
        if self.cc is None:
            self.logging('Please login first')
            return 
        data=self.cc.get_reservationinfo()
        msg = ""
        if data is None:
            self.logging('No Reserved Information')
            msg = "No Reservation !!"
        else:
            for key in data:
                msg += str(key) + ":" + str(data[key]) + "\n"

        dlg = CustomDialog(msg)
        
        if dlg.exec() == QDialog.Accepted:
            print('Accepted')
            self.golf.cancel_reservation()
        else:
            print('Rejected')


    def panaltycheck(self, targetdate):
        print("penelty check:", type(targetdate))
        if type(targetdate) is str:
            if '-' in(targetdate):
                targetdate = datetime.datetime.strptime(targetdate, '%Y-%m-%d')
            else:
                targetdate = datetime.datetime.strptime(targetdate, '%Y%m%d')
        
        # datetime.datetime.strftime(targetdate, '%Y%m%d')
        today = datetime.datetime.today()
        print('today:', today)
        print('target : ',targetdate)
        day_diff = (targetdate - today).days
        print(day_diff)
        if day_diff <= 7:
            dlg = CustomDialog("Too short : within 7 days\n Would make a reservation?")
            if dlg.exec() == QDialog.Accepted:
                print('Maing reservation')
            else:
                print('Cancelled')
                return True

        msg = self.cc.make_reservation()
        print(msg)
        self.logging(msg)
        self.status.setText("Reservation")
        self.logging("Reservation Completed....")


class CustomDialog(QDialog):
    def __init__(self, msg):
        super().__init__()

        self.setWindowTitle("Cancel Reservation")
        QBtn = QDialogButtonBox.Cancel | QDialogButtonBox.Ok

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        message = QLabel(str(msg))
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)


class AutoReserve():
    def __init__(self):
        self.scheduler  = BackgroundScheduler(timezone="Asia/Seoul")
        self.jobid      = 1
        self.jobdb      = {}

    def addGolfJob(self, ccName, BackFunc, user_id, user_pw, schedule, target_date, target_time, day=21):
        print('autoReserve in Jayuro', schedule.hour(), schedule.minute(), schedule.second(), target_date, target_time, day)
        print(self.jobid)
        while self.scheduler.get_job(self.jobid):
            print(self.jobid, self.scheduler.get_job(self.jobid))
        
        self.jobid += 1
        
        result = self.scheduler.add_job(BackFunc,'cron', args=[user_id, user_pw, target_date, target_time, day], week='1-53', day_of_week='0-6', \
                                            hour=schedule.hour(), minute=schedule.minute(), second=schedule.second(), id=str(self.jobid))
        print("result:", result)
        self.jobdb[self.jobid]= ccName

        if self.scheduler.state == 1: #apscheduler.schedulers.base.STATE_RUNNING
            print('Scheduler is running')
        elif self.scheduler.state == 2:
            print('Scheduler is paused')
        elif self.scheduler.state == 0:
            print('Scheduler is stopped')
            self.scheduler.start()

        return self.jobid

    def autoStop(self):   
        print('autoStop')
        for jj in self.scheduler.get_jobs():
            print(jj)

        self.scheduler.remove_all_jobs()
        print(self.scheduler.get_jobs())

    def autoInfo(self):
        print('Auto information')
        print(self.scheduler.get_jobs())
        for jj in self.scheduler.get_jobs():
            print(jj)

        for key in self.jobdb:
            print(key, self.jobdb[key])

    def printlog(self, target_date, target_time):
        now = datetime.datetime.now()
        print(str(now) + str(target_date + "," + target_time))
        # print("Running main process............... : " + str(datetime.datetime.now(timezone('Asia/Seoul'))))

    def getJobInfo(self):
        return self.jobdb

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = Form()
    sys.exit(app.exec())