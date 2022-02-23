# -*- coding: utf8 -*- 
# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# https://www.online-toolz.com/langs/ko/tool-ko-text-unicode-entities-convertor.html

###############################################################
# Ariji CC
# https://www.ariji.co.kr
###############################################################

import os
import sys
import time
import datetime

import requests
from bs4 import BeautifulSoup as bs
import dateutil.relativedelta
import re

from apscheduler import schedulers



def make_reserve(id, pw, target_date, target_time, telephone):
    if telephone == "":
        print("Phone Number should be input")
        sys.exit()
    else:
        tele = telephone.split('-')
    # Beginning session
    session = requests.session()

    # Login page
    login_info = { "mem_id": id, "usr_pwd": pw}
    url_login = "https://www.ariji.co.kr/login/login_ok.asp"
    res = session.get(url_login)
    print('-> login page ', res)

    # Login OK
    url_login_ok = "https://www.ariji.co.kr/login/login_ok.asp"
    res = session.post(url_login_ok, login_info)
    print('-> login ok ', res)

    # Main Page
    url_main = "https://www.ariji.co.kr/index.asp"
    res = session.get(url_main)
    print('-> live.asp ', res)

    # calendar setting
    url1 = "https://www.ariji.co.kr/membership/booking/time_calendar_form.asp"
    res = session.get(url1)
    print(res.status_code)
    # date selection
    soup = bs(res.text, 'html.parser')
    # calendar setting
    currentDate = datetime.datetime.strftime(datetime.datetime.today(), '%Y%m%d')
    print(currentDate)
    # fromDate = 
    target=datetime.datetime.strptime(target_date, '%Y%m%d')
    prev=target + dateutil.relativedelta.relativedelta(months=-1)
    next=target + dateutil.relativedelta.relativedelta(months=1)
    calendar_info1 = {"prevDate": prev.strftime('%Y%m'), 
                      "nowDate":  target.strftime('%Y%m'), 
                      "nextDate": next.strftime('%Y%m'), 
                      "pointdate":target.strftime('%Y%m')}

    url3 = 'https://www.ariji.co.kr/membership/booking/time_calendar_left.asp?fromDate=20220204&toDate=20220227&calKind=202202&currentDate=20220204'
    res = session.get(url3)
    print(res)

    soup = bs(res.text, 'html.parser')
    list_date = soup.find_all('a', href=re.compile(r'JavaScript:goSend'))
    available = []
    for t in list_date:
        rlt = re.search(r'(.*)\((.*)\)(.*)', t.attrs['href'])
        available.append([item.replace("'", "") for item in rlt.group(2).split(',') ])

    for aa in available:
        print(aa)
   
    if len(available) <1:
        print("No available List 0", )
        sys.exit()

    time2_info = {}
    time3_info = {}
    for i, info in enumerate(available):
        if info[1] == target_date:
            print("target date is available")
            print(info)
            time2_info = {'form': info[0],
                   'pointdate': target_date,
                   'dategbn': info[2],
                   'openyn': info[3],
                   'currentDate' :currentDate}
            break

    if time2_info == {}:
        print("No Available Date1 ")
        sys.exit()

    url5 = 'https://www.ariji.co.kr/membership/booking/time_list.asp'
    res = session.post(url5, time2_info)
    print(res)
    soup = bs(res.text, 'html.parser')
    time_list2 = soup.find_all('a', href=re.compile(r'JavaScript:goSend'))
    time_table = []
    for aa in time_list2:
        rlt = re.search(r'\((.*)\)', aa.attrs['href'])
        time_table.append([text.strip().replace("'", "") for text in rlt.group(1).split(',')])

    for k, bb in enumerate(time_table):
        if int(bb[2]) >= int(target_time[0:4]) and int(bb[2]) < int(target_time[5:9]):
            print(bb)
            time3_info = {
                   'form': bb[0],
                   'stpoint': bb[1],
                   'pointtime': bb[2],
                   'cors_name': bb[3],
                   'bookg_chk': bb[4],
                   'self_t_yn': bb[5],
                   'bookg_time_cost': bb[6]
                   }
            break
        else:
            print("No Available time")
            sys.exit()

    if time3_info == {}:
        print("No Available Date 2")
        sys.exit()

    url4 ='https://www.ariji.co.kr/membership/booking/time_res_ok.asp'
    dummy = {
        'menunm':'membership',
        'subnm':'calendar',
        'pointtime': time3_info['pointtime'],
        'stpoint' :time3_info['stpoint'],
        'stpoint_nm': '',
        'pointdate':time2_info['pointdate'],
        'dategbn':time2_info['dategbn'],
        'openyn':time2_info['openyn'],
        'currentdate':time2_info['currentDate'],
        'bookg_chk' :'',
        'bookg_time_cost':time3_info['bookg_time_cost'],
        'self_r_yn':'N',
        'tel1':tele[0],
        'tel2':tele[1],
        'tel3':tele[2]
    }

    res = session.post(url4, dummy)
    print('reservation :', res)

    # result = eval(res.text)
    # message = result['gomsg'].replace('%u', '\\u').encode().decode('unicode_escape')
    # print(message)
    for i, tar in enumerate(re.split('[,:]', res.text)):
        if not tar:
            continue
        if i == 3:
            tar=tar.replace('%u', '\\u').encode().decode('unicode_escape').reaplce('%20', ' ')
        print(tar)

# Main Loop
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    user_id = ''
    user_pw = ''
    user_phone = ""

    target = datetime.datetime.today() + dateutil.relativedelta.relativedelta(days=21)
    targetDate1 = datetime.datetime.strftime(target, '%Y%m%d')
    print(targetDate1)
    target_date = targetDate1#'20220226'
    target_time = '0800:1255'
    # target_date = input('Target date (ex> yyyymmdd): ')
    # target_time = input('Target time (ex: 0655:0955): ')

    make_reserve(user_id, user_pw, target_date, target_time, user_phone)
