# -*- coding: utf8 -*- 
# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# https://www.online-toolz.com/langs/ko/tool-ko-text-unicode-entities-convertor.html

###############################################################
# Jauro CC
# This site is made of __doPostback
# ASP.NET site --> webform control
# ct100 is auto created variable in the server
# We should visit each page to reach the final reservation
# https://www.jayurocc.com
###############################################################


import requests
from bs4 import BeautifulSoup as bs
import datetime
import dateutil.relativedelta

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.background import BlockingScheduler
from apscheduler.schedulers.qt import QtScheduler

import re
import time
from pytz import timezone
from PyQt5.QtCore import pyqtSignal
import pandas as pd
#------------------------------------------------------------------
# Golf Class
#------------------------------------------------------------------
class Jayuro:

    def __init__(self, today, target_date, target_time, parent=None): 
        self.sess = requests.session()
        self.today = today
        self.target_date = target_date
        self.target_time = target_time

    def set_date(self, target):
        self.target_date = target

    def set_time(self, time):
        self.target_time = time

    def login(self, user_id, user_pw):
        url_main = 'https://www.jayurocc.com/Member/Login'

        # 2.Retrive the __doPostback information
        page1 = self.sess.get(url_main)
        soup1 = bs(page1.content, 'html.parser')

        # 3.Login the page
        login_info = \
        {   'ctl00$Content$UserID':         user_id, 
            'ctl00$Content$UserPassword':   user_pw,
            'ctl00$Content$ReturnURL':  '   /Moonos',
            'ctl00$Content$SaveIDCheck':    '',
            'ctl00_Content_SaveIDCheck':    '',
            '__EVENTTARGET' :               'ctl00$Content$SendLoginButton'  , 
            '__EVENTARGUMENT' :             '',
            '__VIEWSTATE' :                 soup1.find('input', id='__VIEWSTATE')['value'],
            '__VIEWSTATEGENERATOR' :        soup1.find('input', id='__VIEWSTATEGENERATOR')['value'],
            '__EVENTVALIDATION' :           soup1.find('input', id='__EVENTVALIDATION')['value']
        }

        resp = self.sess.post(url_main, data=login_info)
        print('Login Mage --> ',resp)
        print(resp.url)

        if resp.url == url_main:
            print('Login Failed')
            return 1

        print('Successfully Logined')
        return resp.status_code

    def logout(self):
        url = 'https://www.jayurocc.com/Member/Logout'
        self.sess.get(url)
        self.sess.close()
        self.sess = None


    def goto_reservepage(self):
        # 4.Check the target date timetable
        #https://www.jayurocc.com/Reservation/Reservation?date=20220226#
        url2 = 'https://www.jayurocc.com/Reservation/Reservation'
        page2= self.sess.get(url2)
        print('Reservation page --> ', page2)
        soup2 = bs(page2.content, 'html.parser')
        self.view_info ={}

        print(self.target_date )

        htbargs                                 = 'LIST|'+ self.today + '|' + self.target_date + '|Y|2|'
        print(htbargs)
        self.view_info['ctl00$Content$htbArgs'] = htbargs#'LIST|2022-02-06|2022-03-07|Y|2||',
        self.view_info['__EVENTTARGET']         = 'ctl00$Content$btnUp'
        self.view_info['__VIEWSTATE']           = soup2.find('input', id='__VIEWSTATE')['value']
        self.view_info['__VIEWSTATEGENERATOR']  = soup2.find('input', id='__VIEWSTATEGENERATOR')['value']
        self.view_info['__EVENTVALIDATION']     = soup2.find('input', id='__EVENTVALIDATION')['value']

        page3 = self.sess.post(url2, self.view_info)
        soup3 = bs(page3.content, 'html.parser')
        self.info_list = soup3.find_all('a', href=re.compile(r'javascript:Reserve'))
        
        print("# of Reserve Available Time : ", len(self.info_list))

        return len(self.info_list) 


    def get_timetable(self):
        url2 = 'https://www.jayurocc.com/Reservation/Reservation'
        # 5.Make list of available button
        time_table = []
        for info in self.info_list:
            rlt = re.search(r'(.*)\((.*)\)(.*)', str(info))
            time_table.append(rlt.group(2).replace("'","").split(','))
        
        return time_table


    def change_reservedate(self):
        url2 = 'https://www.jayurocc.com/Reservation/Reservation'
        # 5.Make list of available button
        time_table = []
        for info in self.info_list:
            rlt = re.search(r'(.*)\((.*)\)(.*)', str(info))
            time_table.append(rlt.group(2).replace("'","").split(','))

        # 6.Compare the target time
        self.target_info ={}
        for t in time_table:
            if int(t[1]) >= int(self.target_time[:4]) and int(t[1]) <= int(self.target_time[5:]):
                self.target_info['strReserveDate']  = t[0]
                self.target_info['strReserveTime']  = t[1]
                self.target_info['strCourseCode']   = t[2]
                self.target_info['strDayGubun']     = t[3]
                self.target_info['strSeq']          = t[4]
                self.target_info['strHole']         = t[5]
                self.target_info['DaegiYN1']        = t[6]
                self.target_info['CadYN']           = t[7]
                self.target_info['strBu']           = t[8]
                self.target_info['strGreenFee']     = t[9]
                self.target_info['strGreenFee1']    = t[10]
                break

        # 7.With the target date/time, proceed the reservation
        page4=self.sess.post(url2, self.view_info)
        soup4 = bs(page4.content, 'html.parser')
        url_reservecheck = 'https://www.jayurocc.com/Reservation/ReservationCheck'
        reserve_info = {
            #'strReserveType': 1,
            #'strClubCode': 'M',
            'strReserveDate':           self.target_info['strReserveDate'] ,
            'strReserveTime':           self.target_info['strReserveTime'],
            'strCourseCode':            self.target_info['strCourseCode'],
            'strDayGubun':              self.target_info['strDayGubun'],
            'strSeq':                   self.target_info['strSeq'],
            'strHole':                  self.target_info['strHole'],
            'DaegiYN1':                 self.target_info['DaegiYN1'],
            'CadYN':                    self.target_info['CadYN'],
            'strBu':                    self.target_info['strBu'],
            'strGreenFee':              self.target_info['strGreenFee'],
            'strGreenFee1':             self.target_info['strGreenFee1'],
            'ctl00$Content$htbArgs':    'LIST|2022-02-06|2022-02-25|Y|1||',
            "PageConnectAuthCode" :     soup4.find('input', id='PageConnectAuthCode')['value'],
            "__EVENTTARGET":            '',
            "__EVENTARGUMENT":          '',
            "__EVENTVALIDATION" :       soup4.find('input', id='__EVENTVALIDATION')['value'],
            '__VIEWSTATEGENERATOR' :    soup4.find('input', id='__VIEWSTATEGENERATOR')['value'],
            "__VIEWSTATE":              soup4.find('input', id='__VIEWSTATE')['value'],
        }
        page5 = self.sess.post(url_reservecheck, reserve_info)
        print('Reserve check -->', page5)
        soup5 = bs(page5.content, 'html.parser')

        for script in soup5.find_all("script"):
            # <script language="javascript">alert('2022-02-13 10:00:00 부터 예약이 가능합니다.');
            # (?<=...) Matches if the current position in the string is preceded by a match for ...
            # (?=...)  Matches if ... matches next, but doesn’t consume any of the string. 
            alert = re.search(r"(?<=alert\(\').+(?=\'\);)", str(script))

            if alert:
                print("alert", alert.group())
                # print(alert)
                return alert.group()

        try:
            self.target_info['PageConnectAuthCode'] = soup5.find('input', id='PageConnectAuthCode')['value']
            self.target_info['__EVENTVALIDATION'] = soup5.find('input', id='__EVENTVALIDATION')['value']
            self.target_info['__VIEWSTATEGENERATOR'] = soup5.find('input', id='__VIEWSTATEGENERATOR')['value']
            self.target_info['__VIEWSTATE'] = soup5.find('input', id='__VIEWSTATE')['value']
        except:
            print("Retrive Parameter Error")
            print(self.target_info)
            f = open("page.txt", "w")
            f.write(str(soup5))
            f.close()
            return 2
        return 0


    def make_reservation(self):
        url_reservecheck = 'https://www.jayurocc.com/Reservation/ReservationCheck'
        # 8. Finally, make the reservation
        final_info = {
            'ctl00$Content$ReserveDate':                self.target_info['strReserveDate'],
            'ctl00$Content$ReserveTime':                self.target_info['strReserveTime'],
            'ctl00$Content$CourseCode':                 self.target_info['strCourseCode'],
            'ctl00$Content$DayGubun':                   self.target_info['strDayGubun'],
            'ctl00$Content$ReserveType':                1,
            'ctl00$Content$Seq':                        self.target_info['strSeq'],
            'ctl00$Content$Hole':                       self.target_info['strHole'],
            'ctl00$Content$Bu':                         self.target_info['strBu'],
            'ctl00$Content$DaegiYN1':                   self.target_info['DaegiYN1'],
            'ctl00$Content$ChangeDayGubun':             '<%=strChangeDayGubun %>',
            'ctl00$Content$ClubCode':                   'M',
            'ctl00$Content$SendPageConnectAuthCode':    self.target_info['PageConnectAuthCode'],
            "PageConnectAuthCode" :                     self.target_info['PageConnectAuthCode'],
            "__EVENTTARGET":                            'ctl00$Content$lbtOK',
            "__EVENTARGUMENT":                          '',
            "__EVENTVALIDATION" :                       self.target_info['__EVENTVALIDATION'],
            '__VIEWSTATEGENERATOR' :                    self.target_info['__VIEWSTATEGENERATOR'],
            "__VIEWSTATE":                              self.target_info['__VIEWSTATE'],
        }

        page6 = self.sess.post(url_reservecheck, final_info)
        soup6 = bs(page6.content, 'html.parser')

        for script in soup6.find_all("script"):
            # <script language="javascript">alert('2022-02-13 10:00:00 부터 예약이 가능합니다.');
            # (?<=...) Matches if the current position in the string is preceded by a match for ...
            # (?=...)  Matches if ... matches next, but doesn’t consume any of the string. 
            alert = re.search(r"(?<=alert\(\').+(?=\'\);)", str(script))

            if alert:
                print(alert.group())
                # print(alert)
                return alert.group()

        print('-----------------------------------------')
        print('Reservation : ', self.target_date, self.target_time)
        print(soup6)
        print('-----------------------------------------')



    def get_reservationinfo(self):
        url='https://www.jayurocc.com/Reservation/ReservationList'
        page=self.sess.get(url)
        soup = bs(page.content, 'html.parser')

        table=soup.find('table', class_='table_reserv02')
        table_html = str(table) # 'table'변수는 bs4.element.tag 형태이기 때문에 table를 문자열 형태로 바꿔준다  
        df_list = pd.read_html(table_html)
        df = df_list[0]
        out = df.iloc[0,:].to_dict()
        print(out)
        print(type(out))
        return out

    def close(self):
        print("Session will be closed")
        self.sess.close()



def job2(user_id, user_pw, target_date, target_time):
    today       = datetime.datetime.now(timezone("Asia/Seoul")).date()
    # target      = today + dateutil.relativedelta.relativedelta(days=21)
    # targetDate1 = datetime.datetime.strftime(target, '%Y%m%d')
    # target_date = target
    # target_time = '0800:1400'
    print(target_date, target_time)

    cc  = Jayuro(str(today), str(target_date), str(target_time))
    chk = cc.login(user_id, user_pw)
    if chk == 200:
        print(chk)
        cc.goto_reservepage()
        if cc.change_reservedate() == 0:
            print("Target date is available")
            cc.make_reservation()
        else:
            print("Reserve Page Error")

    cc.close()


def job():
    user_id = input('Input ID:')
    user_pw = input('Password:')

    today       = datetime.datetime.now(timezone("Asia/Seoul")).date()
    target      = today + dateutil.relativedelta.relativedelta(days=21)
    targetDate1 = datetime.datetime.strftime(target, '%Y%m%d')
    target_date = target#'20220226'
    target_time = '0800:1400'

    cc  = Jayuro(str(today), str(target_date), str(target_time))
    chk = cc.login(user_id, user_pw)
    if chk == 200:
        print(chk)
        cc.goto_reservepage()
        if cc.change_reservedate() == 0:
            print("Target date is available")
            # cc.make_reservation()
        else:
            print("Reserve Page Error")

    cc.close()

stop_flag = 0
sched = BackgroundScheduler(timezone="Asia/Seoul")
qt_sched = QtScheduler(timezone="Asia/Seoul")

def autoReserve(user_id, user_pw, target_date, target_time):
    global stop_flag
    global qt_sched
    print(stop_flag)
    
    if not qt_sched.running:
        print('scheduler is not running')
        # sched = BackgroundScheduler(timezone="Asia/Seoul")
        #sched = BlockingScheduler()
        # sched.add_job(job,'interval', seconds=3, id='test',args=['hello?'])
        qt_sched.add_job(job2,'cron', args=[user_id, user_pw, target_date, target_time], week='1-53', day_of_week='0-6', hour='15', minute='28', second='01', id="100")
        #sched.add_job(job,'cron', week='1-53', day_of_week='0-6', hour='10', minute='00', second='01')
        qt_sched.add_job(printlog,'interval', seconds=3, args=[target_date, target_time], id="101")
        qt_sched.start()
        print('scheduler is started')
        # while True:
        #     if stop_flag == 1:
        #         sched.remove_job(job2)
        #         stop_flag = 0
        #         exit()
        #     print("Running main process............... : ", datetime.datetime.now(timezone('Asia/Seoul')).date())
        #     time.sleep(1)


def autoStop():
    global qt_sched
    print('autoStop in Jayuro')
    if qt_sched.running:
        print('scheduler is running')
        qt_sched.remove_job("100")
        qt_sched.remove_job("101")
        qt_sched.remove_all_jobs()
        qt_sched.shutdown()
        global stop_flag
        stop_flag = 1
        print('scheduler is stopped')


# send_log = None
def printlog(target_date, target_time):
    # global send_log
    # send_log = pyqtSignal(str)
# 
    print(str(target_date + "," + target_time))
    # print("Running main process............... : " + str(datetime.datetime.now(timezone('Asia/Seoul'))))
# 
    # send_log.emit(str(target_date + "," + target_time))


###################################################################
# Main Loop
###################################################################
if __name__ == '__main__':
    sched = BackgroundScheduler(timezone="Asia/Seoul")
    #sched = BlockingScheduler()
    # sched.add_job(job,'interval', seconds=3, id='test',args=['hello?'])
    # sched.add_job(job,'cron', args=[user_id, user_pw, target_date, target_time],week='1-53', day_of_week='0-6', hour='10', minute='00', second='01')
    sched.add_job(job,'cron', week='1-53', day_of_week='0-6', hour='10', minute='00', second='01')
    sched.add_job(printlog,'interval', seconds=3, id='test',args=['hello?'])
    sched.start()

    while True:
        print("Running main process............... : ", datetime.datetime.now(timezone('Asia/Seoul')).date())
        time.sleep(1)

