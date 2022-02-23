# -*- coding: utf8 -*- 
# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# https://www.online-toolz.com/langs/ko/tool-ko-text-unicode-entities-convertor.html

###############################################################
# KU CC
# https://kugolf.co.kr
###############################################################

from importlib.resources import open_binary
import os
import sys
import time
import datetime
from turtle import onclick

import requests
from bs4 import BeautifulSoup as bs
import dateutil.relativedelta
import re
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.background import BlockingScheduler


class KU:
    def __init__(self,today, target_date, target_time, parent=None):
        self.sess = requests.session()
        self.today = today
        self.target_date = target_date
        self.target_time = target_time
        self.dateinfo   = []
        self.time2_info = {}
        self.time3_info = {}
        self.time4_info = {}
        self.memberno   = ''


    def login(self, user_id, user_pw):
        url_login='https://kugolf.co.kr/login/login_ok.asp'
        login_info = { "mem_id": user_id, "usr_pwd": user_pw}
        res = self.sess.post(url_login, login_info)
        print('Login page -->', res)


    def collect_info(self):
        url_cal = 'https://kugolf.co.kr/GolfRes/mainpage/main_calendar_ajax_view.asp'
        date_info = {'golfrestype': 'real',
                    'schDate': self.target_date,
                    'usrmemcd': 11,
                    'toDay': self.target_date,
                    'calnum': 1}
        res=self.sess.post(url_cal, date_info)

        print('Retrive calendar info -->', res)
        soup = bs(res.text, 'html.parser')
        list_date = soup.find_all('a', href=re.compile(r'javascript:main_timefrom_change'))

        for t in list_date:
            rlt = re.search(r'(.*)\((.*)\)(.*)', t.attrs['href'])
            self.dateinfo.append([item.replace("'", "") for item in rlt.group(2).split(',') ])

        for info in self.dateinfo:
            print(info)

    
    def check_target(self):
        for info in self.dateinfo:
            if info[0] == self.target_date:
                self.time2_info = {
                    'pointdate' :       info[0],
                    'openyn':           info[1],
                    'dategbn' :         info[2],
                    'courseid' :        info[3],
                    'time' :            info[4],
                    'atype' :           info[5],
                    'main_link_code':   info[6]
                }
                print('time2_info-->\n', self.time2_info)
                
        if self.time2_info == {}:
            print('\nTarget date is not available : '+ self.target_date)
            return False
        else:
            print('\n Target date is available : ' + self.target_date)
            return self.check_time()


    def check_time(self):
        url_time = 'https://kugolf.co.kr/GolfRes/onepage/real_timelist_ajax_list.asp'
        self.time3_info = {
            'golfrestype':  self.time2_info['main_link_code'],
            'courseid':     self.time2_info['courseid'],
            'usrmemcd':     11,
            'pointdate':    self.time2_info['pointdate'],
            'openyn':       self.time2_info['openyn'],
            'dategbn':      self.time2_info['dategbn'],
            'choice_time':  self.time2_info['time'],
            'cssncourseum': '' ,
            'inputtype':    'I',
        }
        print('\ntime3_info for time table request -->\n', self.time3_info)

        res=self.sess.post(url_time, self.time3_info)
        print('--> Result :',res)

        soup = bs(res.text, 'html.parser')
        list_time = [a.get('onclick') for a in soup.find_all('button') if "신청" in a]
        print('\n Number of available time : ', len(list_time))
        if len(list_time) == 0:
            print("\n Error --> No Tee-Off")
            return

        time_table = []
        for t in list_time:
            rlt = re.search(r'(.*)\((.*)\)(.*)', t)
            time_table.append([item.strip().replace("'", "") for item in rlt.group(2).split(',') ])

        # 5. Check the desired time
        for info in time_table:
            if int(info[2]) >= int(target_time[:4]) and int(info[2]) < int(target_time[5:]):
                self.time4_info = {
                'atype':            info[0], 
                'pointid':          info[1], 
                'pointtime':        info[2], 
                'flagtype':         info[3], 
                'punish_cd':        info[4], 
                'alert_info':       info[5], 
                'self_t_yn':        info[6], 
                'res_gubun':        info[7], 
                'virtual_tf':       info[8], 
                'impend_time_yn':   info[9],
                'strGoldenTime':    info[10]
                }
                break

        if self.time4_info == {}:
            print("No available time : " + self.target_date + ", " + self.target_time[:4] + " ~ " + self.target_time[5:])
            for info in time_table:
                print(info)#, end=' ')
            return False
        else:
            print('\nDesired time : ' + self.target_date + ", " + self.target_time[:4] + " ~ " + self.target_time[5:])
            print(self.time4_info)
            return True


    def member_number(self):
        url_from = 'https://kugolf.co.kr/GolfRes/onepage/real_timeinfo_ajax_from.asp'
        dummy3 = {
            'cmrtype': 'N',
            'golfrestype': 'real',
            'courseid': 0,
            'usrmemcd': 11,
            'pointdate': target,
            'openyn': self.time3_info['openyn'],
            'dategbn': self.time3_info['dategbn'],
            'choice_time': 00,
            'inputtype': self.time3_info['inputtype']
        }

        res = self.sess.post(url_from, dummy3)
        print("Collect member infomation --> ", res)
        soup3 = bs(res.text, 'html.parser')
        self.memberno = soup3.find('input', {'name':'memberno'})['value']
        print("Member Number : ", self.member_number)


    def reserve(self):
        url_info = 'https://kugolf.co.kr/GolfRes/onepage/real_resapply_ajax_from.asp'
        dummy4={
        'cmd': 'ins',
        'cmval': '0',
        'cmkind':'' ,
        'cmrtype': 'N',
        'backurl': '',
        'golfrestype': 'real',
        'usrmemcd': 11,
        'today': today,
        'pointdate': target_date,
        'openyn': self.time3_info['openyn'],
        'dategbn': self.time3_info['dategbn'],
        'pointid': self.time4_info['pointid'],
        'pointtime': self.time4_info['pointtime'],
        'modaltype':'' ,
        'inputtype': 'I',
        'flagtype': 'I',
        'punish_cd': 'UNABLE',
        'self_r_yn': 'N',
        'res_gubun': 'N',
        'virtual_tf': ''
        }

        res = self.sess.post(url_info, dummy4)
        print('\nAdditional personel information request --> ',res)
        soup = bs(res.text, 'html.parser')
        golfuser_name = soup.find('input', {'name':'golfuser_name'})['value']
        unicode_name = [hex(ord(x)) for x in golfuser_name]
        golfuser_name_x=""
        for one_ch in unicode_name:
            one_ = one_ch.replace('0x', '%u')
            golfuser_name_x += one_

        hand_tel1='010'
        hand_tel2=soup.find('input', {'name':'hand_tel2'})['value']
        hand_tel3=soup.find('input', {'name':'hand_tel3'})['value']

        url_resok = 'https://kugolf.co.kr/GolfRes/onepage/real_resok.asp'
        if self.time4_info['pointid'] == '1':
            pointname = '바른'
        elif self.time4_info['pointid'] == '2':
            pointname = '미쁨'
        elif self.time4_info['pointid'] == '3':
            pointname = '혼솔'
        else:
            print("Error")
            exit()

        dummy2 = {
        'cmd': 'ins',
        'cmval': 0,
        'cmkind': '',
        'cmrtype': 'N',
        'calltype': 'AJAX',
        'gonexturl': '/GolfRes/onepage/my_golfreslist.asp',
        'backurl': '',
        'pointdate': self.time3_info['pointdate'],
        'openyn': self.time3_info['openyn'],
        'dategbn': self.time3_info['dategbn'],
        'pointid': self.time4_info['pointid'],
        'pointname': pointname,
        'pointtime': self.time4_info['pointtime'],
        'flagtype': self.time4_info['flagtype'],
        'punish_cd': self.time4_info['punish_cd'],
        'self_r_yn': 'N',
        'res_gubun': self.time4_info['res_gubun'],
        'virtual_tf': self.time4_info['virtual_tf'],
        'coupon_info': '',
        'oldpointtime': '',
        'oldpointid': '',
        'usrmemcd': self.time3_info['usrmemcd'],
        'memberno': self.memberno,
        'bookgseq': '',
        'oldhane_tel': '',
        'column_cpon_code': '',
        'golfuser_name': golfuser_name_x,
        'hand_tel1': '010',
        'hand_tel2': hand_tel2,
        'hand_tel3': hand_tel3
        }
        # print('\nFinal Reservation Request\n', dummy2)
        [print(key,':',value) for key, value in dummy2.items()]
        res=self.sess.post(url_resok, dummy2)
        print('Final Reservation --> ', res)

        print('\n\n====[Final Result]====')
        for i, tar in enumerate(re.split('[,:]', res.text)):
            if not tar:
                continue
            if i == 3:
                tar=tar.replace('%u', '\\u').encode().decode('unicode_escape')
                tar=tar.replace("%20", ' ')
            print(tar)
        print('========================')


    def check_reserve(self):
        url_check = 'https://kugolf.co.kr/GolfRes/onepage/my_golfreslist.asp'
        res=self.sess.get(url_check)
        print(res.text)

    
    def close(self):
        self.sess.close()
        self.sess = None


def job(user_id, user_pw, target_date, target_time):
    cc = KU(today, target_date, target_time)
    cc.login(user_id, user_pw)
    cc.collect_info()
    if cc.check_target():
        cc.reserve()
    cc.close()


if __name__ == '__main__':
    user_id = input('Input Id :')
    user_pw = input('password :')

    today = datetime.datetime.today()
    target = today + dateutil.relativedelta.relativedelta(days=21)
    targetDate1 = datetime.datetime.strftime(target, '%Y%m%d')
    print(targetDate1)
    target_date = targetDate1 #'20220226'
    target_time = '0800:1400'

    test = 2
    if test == 1:
        job(user_id, user_pw, target_date, target_time)

    elif test == 2:
        cc = KU(today, target_date, target_time)
        cc.login(user_id, user_pw)
        cc.check_reserve()
        cc.close()

    else:
        sched = BackgroundScheduler()
        # sched = BlockingScheduler()
        # sched.add_job(job,'interval', seconds=3, id='test',args=['hello?'])
        sched.add_job(job, 'cron', args=[user_id, user_pw, target_date, target_time],week='1-53', day_of_week='0-6', hour='10', minute='00', second='01')
        sched.start()

        while True:
            print("Running main process............... : ", datetime.datetime.today())
            time.sleep(60)
