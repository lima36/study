from PyQt5 import QtWidgets 
from PyQt5 import uic 
from PyQt5.QtCore import * 
from srt_book import SRT_page 
import sys 
import time 
import playsound 
import datetime
from selenium.webdriver.common.keys import Keys

class Form(QtWidgets.QDialog): 
    def __init__(self, parent=None): 
        QtWidgets.QDialog.__init__(self, parent) 
        self.ui = uic.loadUi("/home/lima/Work_Python/Golf/gui/gui.ui")
        self.dep = self.ui.depCity #출발지 
        self.arr = self.ui.arrCity #도착지 
        self.dat = self.ui.depDate #출발일 
        self.hou = self.ui.depHour #출발시간
        self.table = self.ui.resTable #검색결과표 
        self.check_list = [self.ui.checkBox_01, #체크박스 10개 
        self.ui.checkBox_02, 
        self.ui.checkBox_03, 
        self.ui.checkBox_04, 
        self.ui.checkBox_05, 
        self.ui.checkBox_06, 
        self.ui.checkBox_07, 
        self.ui.checkBox_08, 
        self.ui.checkBox_09, 
        self.ui.checkBox_10 ] 
        self.srt = SRT_page() 
        self.srt.login() 
        time.sleep(3) 
        c = str(datetime.datetime.today().date()).replace('-', '/') 
        self.dat.setDate(QDate.fromString(c, "yyyy/MM/dd")) 
        self.ui.searchSeat.clicked.connect(self.find_seats) 
        self.ui.tryReservation.clicked.connect(self.try_seat) 
        self.ui.show()
    
    def find_seats(self): 
        self.selected_dep = self.dep.currentText() # 입력한 출발지 불러오기 
        self.selected_arr = self.arr.currentText() # 입력한 도착지 불러오기 
        d = datetime.datetime(int(self.dat.date().toString("yyyy/MM/dd").split("/")[0]), 
        int(self.dat.date().toString("yyyy/M/dd").split("/")[1]), 
        int(self.dat.date().toString("yyyy/M/dd").split("/")[2])).weekday() 
        week_days = ["(월)","(화)","(수)","(목)","(금)","(토)","(일)"] 
        self.selected_dat = self.dat.date().toString("yyyy/MM/dd")+week_days[d] 
        self.selected_hou = self.hou.currentText() 
        res = self.srt.plan(self.selected_dep, self.selected_arr, self.selected_dat, self.selected_hou) 
        for num1 in range(10): 
            for num2 in range(4): 
                self.table.setItem(num1, num2, QtWidgets.QTableWidgetItem(res[num1][num2]))


    def try_seat(self): 
        print("예약하기") 
        self.checked_group = [] 
        for index, element in enumerate(self.check_list): 
            if element.isChecked() == True: 
                self.checked_group.append(index) 
            else: 
                pass 
        print(self.checked_group) 
        done = self.srt.try_reservation(self.checked_group) 
        playsound.playsound('/home/lima/Downloads/Various Artists - Top Hits of 2002/01. Nelly - Dilemma.mp3', True)


    
#출처: https://conansjh20.tistory.com/69 [취미는 파이썬]
if __name__ == '__main__': 
    app = QtWidgets.QApplication(sys.argv) 
    w = Form() 
    sys.exit(app.exec())