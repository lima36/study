# -*- coding: utf8 -*- 
# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# https://www.online-toolz.com/langs/ko/tool-ko-text-unicode-entities-convertor.html

###############################################################
# Jauro CC
# This site is made of __doPostback
# We should visit each page to reach the final reservation
# https://www.jayurocc.com
###############################################################

from importlib.resources import open_binary
from logging import INFO
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

def make_reserve(user_id, user_pw, today, target_date, target_time):
    print(today, target_date, target_time)

    sess = requests.session()

    # 1.Main Login Page
    url_main = 'https://www.jayurocc.com/Member/Login'
    login_info = {'ctl00$Content$UserID':user_id, 
    'ctl00$Content$UserPassword':user_pw,
    'ctl00$Content$ReturnURL':'/Moonos',
    'ctl00$Content$SaveIDCheck': '',
    'ctl00_Content_SaveIDCheck': '' }

    # 2.Retrive the __doPostback information
    page1 = sess.get(url_main)
    soup1 = bs(page1.content, 'html.parser')

    # 3.Login the page
    login_info['__EVENTTARGET'] = 'ctl00$Content$SendLoginButton'   
    login_info['__EVENTARGUMENT'] = ''
    login_info['__VIEWSTATE'] = soup1.find('input', id='__VIEWSTATE')['value']
    login_info['__VIEWSTATEGENERATOR'] = soup1.find('input', id='__VIEWSTATEGENERATOR')['value']
    login_info['__EVENTVALIDATION'] = soup1.find('input', id='__EVENTVALIDATION')['value']

    resp = sess.post(url_main, data=login_info)
    print('Login Mage --> ',resp)

    # 4.Check the target date timetable
    #https://www.jayurocc.com/Reservation/Reservation?date=20220226#
    url2 = 'https://www.jayurocc.com/Reservation/Reservation'
    page2=sess.get(url2)
    print('Reservation page --> ', page2)
    soup2 = bs(page2.content, 'html.parser')
    view_info ={}
    htbargs = 'LIST|'+ today + '|' + target_date + '|Y|2|'
    view_info['ctl00$Content$htbArgs'] = htbargs#'LIST|2022-02-06|2022-02-25|Y|2||',
    view_info['__EVENTTARGET'] = 'ctl00$Content$btnUp'
    view_info['__VIEWSTATE'] = soup2.find('input', id='__VIEWSTATE')['value']
    view_info['__VIEWSTATEGENERATOR'] = soup2.find('input', id='__VIEWSTATEGENERATOR')['value']
    view_info['__EVENTVALIDATION'] = soup2.find('input', id='__EVENTVALIDATION')['value']

    page3=sess.post(url2, view_info)
    soup3 = bs(page3.content, 'html.parser')
    info_list = soup3.find_all('a', href=re.compile(r'javascript:Reserve'))

    # 5.Make list of available button
    time_table = []
    for info in info_list:
        rlt = re.search(r'(.*)\((.*)\)(.*)', str(info))
        time_table.append(rlt.group(2).replace("'","").split(','))

    # 6.Compare the target time
    target_info ={}
    for t in time_table:
        if int(t[1]) > int(target_time[:4]) and int(t[1]) < int(target_time[5:]):
            target_info['strReserveDate'] = t[0]
            target_info['strReserveTime'] = t[1]
            target_info['strCourseCode'] = t[2]
            target_info['strDayGubun'] = t[3]
            target_info['strSeq'] = t[4]
            target_info['strHole'] = t[5]
            target_info['DaegiYN1'] = t[6]
            target_info['CadYN'] = t[7]
            target_info['strBu'] = t[8]
            target_info['strGreenFee'] = t[9]
            target_info['strGreenFee1'] = t[10]
            break

    # 7.With the target date/time, proceed the reservation
    page4=sess.post(url2, view_info)
    soup4 = bs(page4.content, 'html.parser')
    url_reservecheck = 'https://www.jayurocc.com/Reservation/ReservationCheck'
    reserve_info = {
        #'strReserveType': 1,
        #'strClubCode': 'M',
        'strReserveDate': target_info['strReserveDate'] ,
        'strReserveTime': target_info['strReserveTime'],
        'strCourseCode': target_info['strCourseCode'],
        'strDayGubun': target_info['strDayGubun'],
        'strSeq': target_info['strSeq'],
        'strHole': target_info['strHole'],
        'DaegiYN1': target_info['DaegiYN1'],
        'CadYN': target_info['CadYN'],
        'strBu': target_info['strBu'],
        'strGreenFee': target_info['strGreenFee'],
        'strGreenFee1': target_info['strGreenFee1'],
        'ctl00$Content$htbArgs': 'LIST|2022-02-06|2022-02-25|Y|1||',
        "PageConnectAuthCode" : soup4.find('input', id='PageConnectAuthCode')['value'],
        "__EVENTTARGET":'',
        "__EVENTARGUMENT":'',
        "__EVENTVALIDATION" : soup4.find('input', id='__EVENTVALIDATION')['value'],
        '__VIEWSTATEGENERATOR' : soup4.find('input', id='__VIEWSTATEGENERATOR')['value'],
        "__VIEWSTATE": soup4.find('input', id='__VIEWSTATE')['value'],
    }
    page5 = sess.post(url_reservecheck, reserve_info)
    print('Reserve check -->', page5)
    soup5 = bs(page5.content, 'html.parser')

    # 8. Finally, make the reservation
    final_info = {
        'ctl00$Content$ReserveDate': target_info['strReserveDate'],
        'ctl00$Content$ReserveTime': target_info['strReserveTime'],
        'ctl00$Content$CourseCode': target_info['strCourseCode'],
        'ctl00$Content$DayGubun': target_info['strDayGubun'],
        'ctl00$Content$ReserveType': 1,
        'ctl00$Content$Seq': target_info['strSeq'],
        'ctl00$Content$Hole': target_info['strHole'],
        'ctl00$Content$Bu': target_info['strBu'],
        'ctl00$Content$DaegiYN1': target_info['DaegiYN1'],
        'ctl00$Content$ChangeDayGubun': '<%=strChangeDayGubun %>',
        'ctl00$Content$ClubCode': 'M',
        'ctl00$Content$SendPageConnectAuthCode' : soup5.find('input', id='PageConnectAuthCode')['value'],
        "PageConnectAuthCode" : soup5.find('input', id='PageConnectAuthCode')['value'],
        "__EVENTTARGET":'ctl00$Content$lbtOK',
        "__EVENTARGUMENT":'',
        "__EVENTVALIDATION" : soup5.find('input', id='__EVENTVALIDATION')['value'],
        '__VIEWSTATEGENERATOR' : soup5.find('input', id='__VIEWSTATEGENERATOR')['value'],
        "__VIEWSTATE": soup5.find('input', id='__VIEWSTATE')['value'],
    }

    page6 = sess.post(url_reservecheck, final_info)
    soup6 = bs(page6.content, 'html.parser')

    print('-----------------------------------------')
    print('Reservation : ', target_date, target_time)
    print(soup6)
    print('-----------------------------------------')


if __name__ == '__main__':
    user_id = 'lima36'
    user_pw = 'peace@2020'

    # target_date='20220225'
    # target_time='0900:1300'
    today = datetime.datetime.today().date()
    target = datetime.datetime.today().date() + dateutil.relativedelta.relativedelta(days=21)
    targetDate1 = datetime.datetime.strftime(target, '%Y%m%d')
    print(targetDate1)
    target_date = target#'20220226'
    target_time = '0800:1400'

    make_reserve(user_id, user_pw, str(today), str(target_date), target_time)