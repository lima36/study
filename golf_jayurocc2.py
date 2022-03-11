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

import os
from os.path import exists
import json
import base64
import ssl

idpass = './id.json'
#------------------------------------------------------------------
# Golf Class
#------------------------------------------------------------------

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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
        ssl._create_default_https_context = ssl._create_unverified_context
        page1 = self.sess.get(url_main, verify=False)
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

        # htmlfile(soup2)

        htbargs                                 = 'LIST|'+ self.today + '|' + self.target_date + '|Y|2|'
        self.view_info['ctl00$Content$htbArgs'] = htbargs
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

        empty = soup.find('tr', attrs={'id' :'ctl00_Content_rptResvListEmpty'})
        if empty:
            return None

        table=soup.find('table', class_='table_reserv02')
        table_html = str(table) # 'table'변수는 bs4.element.tag 형태이기 때문에 table를 문자열 형태로 바꿔준다  
        df_list = pd.read_html(table_html)
        df = df_list[0]
        out = df.iloc[0,:].to_dict()
        print(out)
        return out

    def cancel_reservation(self):
        print('cancel reservation')
        url = 'https://www.jayurocc.com/Reservation/ReservationList'
        page=self.sess.get(url)
        soup = bs(page.content, 'html.parser')

        


        # Get the reserved information
        result = {}
        table = soup.find('table', class_='table_reserv02')
        for header, value in zip(*(tr.find_all(['td','th']) for tr in table.find_all('tr'))):
            result[header.text] = value.text

        canceldata=soup.find('a', id='ctl00_Content_rptResvList_ctl00_reserveCanlink')['href']
        cancelvalue = re.search(r'javascript:ReservationCancel\((.*)\)', canceldata).group(1).replace("'", '').split(',')
        canceltitle = ['strReserveDate', 'strReserveTime', 'strCourseCode', 'strSeq', 'intDayGubun', 'strReserveGubun', 'strHole', 'strCancelName', 'intBuljum']
        canceldict = {canceltitle[i]: cancelvalue[i] for i in range(len(canceltitle))}
        print(str(canceldict))

        param = {'__EVENTTARGET' :  'ctl00$Content$btnCancel',
                '__VIEWSTATE' :     soup.find('input', id='__VIEWSTATE')['value'],
                '__VIEWSTATEGENERATOR': soup.find('input', id='__VIEWSTATEGENERATOR')['value'],
                '__EVENTVALIDATION' : soup.find('input', id='__EVENTVALIDATION')['value'],
                'PageConnectAuthCode':soup.find('input', id='PageConnectAuthCode')['value'],
                'strReserveDate' :  canceldict['strReserveDate'],
                'strReserveTime' :  canceldict['strReserveTime'],
                'strCourseCode' :   canceldict['strCourseCode'],
                'strSeq':           canceldict['strSeq'],
                'intDayGubun':      canceldict['intDayGubun'],
                'strReserveGubun':  canceldict['strReserveGubun'],
                'strHole':          canceldict['strHole'],
                'strCancelName':    canceldict['strCancelName'],
                'intBuljum' :       canceldict['intBuljum']
        }

        page2=self.sess.post(url, param)
        print("Cancel Completed:",page2)
        soup2 = bs(page2.content, 'html.parser')
        for script in soup2.find_all("script"):
            # <script language="javascript">alert('2022-02-13 10:00:00 부터 예약이 가능합니다.');
            # (?<=...) Matches if the current position in the string is preceded by a match for ...
            # (?=...)  Matches if ... matches next, but doesn’t consume any of the string. 
            alert = re.search(r"(?<=alert\(\').+(?=\'\);)", str(script))
            if alert:
                print("alert", alert.group())
                # print(alert)
                return alert.group()


    def close(self):
        print("Session will be closed")
        self.sess.close()


def htmlfile(html):
    with open('log.html', 'w') as f:
        f.write(str(html))


sched = BackgroundScheduler(timezone="Asia/Seoul")

def job2(user_id, user_pw, target_date, target_time):
    global sched
    today       = datetime.datetime.now(timezone("Asia/Seoul")).date()
    # target      = today + dateutil.relativedelta.relativedelta(days=21)
    # targetDate1 = datetime.datetime.strftime(target, '%Y%m%d')
    # target_date = target
    # target_time = '0800:1400'
    # print(target_date, target_time)

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
    print('Remove alredy executed')
    sched.remove_job("102")
    cc.close()


def golfjob():
    if exists(idpass):
        with open(idpass, 'r') as infile:
            data=json.load(infile)
            user_id = data['id']
            user_pw = base64.b64decode(data['password']).decode('utf-8')
    else:
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
            cc.make_reservation()
        else:
            print("Reserve Page Error")
    sched.remove_job("102")
    cc.close()


def golfjob2(user_id, user_pw, fdate, ftime, day):
    print('golfjob2', fdate, ftime, day)
    today       = datetime.datetime.now(timezone("Asia/Seoul")).date()

    if day==21:
        target      = today + dateutil.relativedelta.relativedelta(days=21)
        target_date = target
    else:
        target_date = fdate

    target_time = ftime

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


def printlog(target_date, target_time):
    now = datetime.datetime.now()
    print(str(now) + str(target_date + "," + target_time))
    # print("Running main process............... : " + str(datetime.datetime.now(timezone('Asia/Seoul'))))


stop_flag = 0
jobid = 0
def addGoldJob(user_id, user_pw, schedule, target_date, target_time, day=21):
    global jobid
    print('autoReserve in Jayuro', schedule.hour(), schedule.minute(), schedule.second(), target_date, target_time, day)
    while sched.get_job(jobid):
        print(jobid, sched.get_job(jobid).id)
        jobid += 1
    
    sched.add_job(golfjob2,'cron', args=[user_id, user_pw, target_date, target_time, day], week='1-53', day_of_week='0-6', \
                                        hour=schedule.hour(), minute=schedule.minute(), second=schedule.second(), id=str(jobid))
        
    if sched.state == 1: #apscheduler.schedulers.base.STATE_RUNNING
        print('Scheduler is running')
    elif sched.state == 2:
        print('Scheduler is paused')
    elif sched.state == 0:
        print('Scheduler is stopped')
        sched.start()


def autoReserve(user_id, user_pw, schedule, target_date, target_time, day=21):
    global sched
    global stop_flag
    print('autoReserve in Jayuro', schedule.hour(), schedule.minute(), schedule.second(), target_date, target_time, day)
 
    if stop_flag == 0 or stop_flag ==2:
        # sched = BackgroundScheduler(timezone="Asia/Seoul")
        #sched = BlockingScheduler()
        # sched.add_job(job,'interval', seconds=3, id='test')
        # qt_sched.add_job(job2,'cron', args=[user_id, user_pw, target_date, target_time], week='1-53', day_of_week='0-6', hour='10', minute='00', second='01', id="100")
        sched.add_job(golfjob2,'cron', args=[user_id, user_pw, target_date, target_time, day], week='1-53', day_of_week='0-6', \
                                        hour=schedule.hour(), minute=schedule.minute(), second=schedule.second(), id="102")
        sched.add_job(printlog,'interval', seconds=60, args=[target_date, target_time], id="101")
        if stop_flag == 0:
            sched.start()
        stop_flag = 1

        for jj in sched.get_jobs():
            print(jj)

        print('scheduler is started')


def autoStop():
    global sched
    global stop_flag
    
    print('autoStop in Jayuro')
    if stop_flag == 0 or stop_flag ==1:
        for jj in sched.get_jobs():
            print(jj)

        sched.remove_all_jobs()
        print(sched.get_jobs())
        stop_flag = 2
        return


def autoInfo():
    print('Auto information in Jayuro')
    print(sched.get_jobs())
    for jj in sched.get_jobs():
        print(jj)


###################################################################
# Main Loop
###################################################################
if __name__ == '__main__':
    sched = BackgroundScheduler(timezone="Asia/Seoul")
    #sched = BlockingScheduler()
    # sched.add_job(job,'interval', seconds=3, id='test',args=['hello?'])
    # sched.add_job(job,'cron', args=[user_id, user_pw, target_date, target_time],week='1-53', day_of_week='0-6', hour='10', minute='00', second='01')
    # sched.add_job(job,'cron', week='1-53', day_of_week='0-6', hour='10', minute='00', second='01')
    sched.add_job(printlog,'interval', seconds=3, id='test',args=['hello?'])
    # sched.add_job(autoStop, 'interval', seconds=3, id = 'rebate')
    sched.start()

    while True:
        print("Running main process............... : ", datetime.datetime.now(timezone('Asia/Seoul')).date())
        for jj in sched.get_jobs():
            print(jj)
        time.sleep(1)

