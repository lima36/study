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

def make_reserve(user_id, user_pw, target_date, target_time):

    session = requests.session()

    # 1. Main Page
    url_main = 'https://kugolf.co.kr/index.asp'
    res = session.get(url_main)
    print('Main page -->', res)

    # 2. Login with ID and Password
    url_login='https://kugolf.co.kr/login/login_ok.asp'
    login_info = { "mem_id": user_id, "usr_pwd": user_pw}
    res = session.post(url_login, login_info)
    print('Login page -->', res)

    # 3. Collect date info from calendar
    url_cal = 'https://kugolf.co.kr/GolfRes/mainpage/main_calendar_ajax_view.asp'
    res=session.post(url_cal)
    print('Retrive calendar info -->', res)
    soup = bs(res.text, 'html.parser')
    list_date = soup.find_all('a', href=re.compile(r'javascript:main_timefrom_change'))

    dateinfo = []
    for t in list_date:
        rlt = re.search(r'(.*)\((.*)\)(.*)', t.attrs['href'])
        dateinfo.append([item.replace("'", "") for item in rlt.group(2).split(',') ])

    # 3-1 check the target date from the date info
    time2_info = {}
    for info in dateinfo:
        if info[0] == target_date:
            time2_info = {
                'pointdate' :       info[0],
                'openyn':           info[1],
                'dategbn' :         info[2],
                'courseid' :        info[3],
                'time' :            info[4],
                'atype' :           info[5],
                'main_link_code':   info[6]
            }
            print('time2_info-->\n',time2_info)
            
    if time2_info == {}:
        print('\nTarget date is not available : '+ target_date)
        return
    else:
        print('\n Target date is available : ' + target_date)

    # 4. Time list from the selected date
    url_time = 'https://kugolf.co.kr/GolfRes/onepage/real_timelist_ajax_list.asp'
    time3_info = {
        'golfrestype':  time2_info['main_link_code'],
        'courseid':     time2_info['courseid'],
        'usrmemcd':     11,
        'pointdate':    time2_info['pointdate'],
        'openyn':       time2_info['openyn'],
        'dategbn':      time2_info['dategbn'],
        'choice_time':  time2_info['time'],
        'cssncourseum': '' ,
        'inputtype':    'I',
    }
    print('\ntime3_info for time table request -->\n', time3_info)

    res=session.post(url_time, time3_info)
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
    time4_info = {}
    for info in time_table:
        if int(info[2]) >= int(target_time[:4]) and int(info[2]) < int(target_time[5:]):
            time4_info = {
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

    if time4_info == {}:
        print("No available time : " + target_date + ", " +target_time[:4] + " ~ " + target_time[5:])
        for info in time_table:
            print(info)#, end=' ')
        return
    else:
        print('\nDesired time : ' + target_date + ", " + target_time[:4] + " ~ " + target_time[5:])
        print(time4_info)

    today = datetime.date.today().strftime("%Y%m%d")
    target=datetime.datetime.strptime(target_date, '%Y%m%d')
    prev=target + dateutil.relativedelta.relativedelta(months=-1)
    next=target + dateutil.relativedelta.relativedelta(months=1)
    prevDate = prev.strftime('%Y%m') 
    nowDate = target.strftime('%Y%m')
    nextDate = next.strftime('%Y%m'), 

    # 6. Collect member info
    url_from = 'https://kugolf.co.kr/GolfRes/onepage/real_timeinfo_ajax_from.asp'
    dummy3 = {
        'cmrtype': 'N',
        'golfrestype': 'real',
        'courseid': 0,
        'usrmemcd': 11,
        'pointdate': target,
        'openyn': time3_info['openyn'],
        'dategbn': time3_info['dategbn'],
        'choice_time': 00,
        'inputtype': time3_info['inputtype']
    }

    res = session.post(url_from, dummy3)
    print("Collect member infomation --> ",res)
    soup3 = bs(res.text, 'html.parser')
    memberno = soup3.find('input', {'name':'memberno'})['value']

    print(time4_info['pointid'])
    if time4_info['pointid'] == '1':
        pointname = '바른'
    elif time4_info['pointid'] == '2':
        pointname = '미쁨'
    elif time4_info['pointid'] == '3':
        pointname = '혼솔'
    else:
        print("Error")
        exit()

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
    'openyn': time3_info['openyn'],
    'dategbn': time3_info['dategbn'],
    'pointid': time4_info['pointid'],
    'pointtime': time4_info['pointtime'],
    'modaltype':'' ,
    'inputtype': 'I',
    'flagtype': 'I',
    'punish_cd': 'UNABLE',
    'self_r_yn': 'N',
    'res_gubun': 'N',
    'virtual_tf': ''
    }

    res=session.post(url_info, dummy4)
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
    dummy2 = {
    'cmd': 'ins',
    'cmval': 0,
    'cmkind': '',
    'cmrtype': 'N',
    'calltype': 'AJAX',
    'gonexturl': '/GolfRes/onepage/my_golfreslist.asp',
    'backurl': '',
    'pointdate': time3_info['pointdate'],
    'openyn': time3_info['openyn'],
    'dategbn': time3_info['dategbn'],
    'pointid': time4_info['pointid'],
    'pointname': pointname,
    'pointtime': time4_info['pointtime'],
    'flagtype': time4_info['flagtype'],
    'punish_cd': time4_info['punish_cd'],
    'self_r_yn': 'N',
    'res_gubun': time4_info['res_gubun'],
    'virtual_tf': time4_info['virtual_tf'],
    'coupon_info': '',
    'oldpointtime': '',
    'oldpointid': '',
    'usrmemcd': time3_info['usrmemcd'],
    'memberno': memberno,
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
    res=session.post(url_resok, dummy2)
    print('Final Reservation --> ', res)

    print('\n\n====Final Result====')
    for i, tar in enumerate(re.split('[,:]', res.text)):
        if not tar:
            continue
        if i == 3:
            tar=tar.replace('%u', '\\u').encode().decode('unicode_escape')
            tar=tar.replace("%20", ' ')
        print(tar)
    print('========================')

if __name__ == '__main__':
    user_id = ''
    user_pw = ''

    # target_date='20220225'
    # target_time='0900:1300'

    target = datetime.datetime.today() + dateutil.relativedelta.relativedelta(days=21)
    targetDate1 = datetime.datetime.strftime(target, '%Y%m%d')
    print(targetDate1)
    target_date = targetDate1 #'20220226'
    target_time = '0800:1400'
    # target_date = input('Target date (ex> yyyymmdd): ')
    # target_time = input('Target time (ex: 0655:0955): ')
    test = 1
    if test == 1:
        make_reserve(user_id, user_pw, target_date, target_time)
    else:
        sched = BackgroundScheduler()
        # sched = BlockingScheduler()
        # sched.add_job(job,'interval', seconds=3, id='test',args=['hello?'])
        sched.add_job(make_reserve,'cron', args=[user_id, user_pw, target_date, target_time],week='1-53', day_of_week='0-6', hour='10', minute='00', second='01')
        sched.start()

        while True:
            print("Running main process............... : ", datetime.datetime.today())
            time.sleep(60)
