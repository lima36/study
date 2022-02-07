# -*- coding: utf8 -*- 
# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import sys
import time
import datetime
from jinja2 import Undefined

import requests
from bs4 import BeautifulSoup as bs

import os
import re
import json
# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    user_id = ''
    user_pw = ''
    target_date = '20220209'
    target_time = '0655:1255'
    #target_date = input('Target date (ex> yyyymmdd): ')
    # target_time = input('Target time (ex: 0655:0955): ')
    date_selection = None
    time_selection = None

    login_time = datetime.time(8, 57, 00)
    open_time = datetime.time(9, 00, 00)


    # Beginning session
    session = requests.session()

    # Login page
    login_info = { "mem_id": user_id, "usr_pwd": user_pw}
    # login_info = { "log_id": user_id, "login_pw": user_pw}

    url_login = "https://lavieestbellegolfnresort.com/oldcourse/login/login.asp"

    res = session.get(url_login)
    res.raise_for_status()
    print('-> login page ', res)

    # Login OK
    url_login_ok = "https://lavieestbellegolfnresort.com/oldcourse/login/login_ok.asp"

    res = session.post(url_login_ok, login_info)
    print('-> login ok ', res)
    res=res.close()

    res = session.post('https://lavieestbellegolfnresort.com/oldcourse/GolfRes/onepage/real_reservation.asp')
    print('real_reservation.asp', res)

    res = session.post('https://lavieestbellegolfnresort.com/oldcourse/')
    print('oldcourse -->' , res)
    # Main Page
    url_main = "https://lavieestbellegolfnresort.com/oldcourse/index.asp"
    res = session.get(url_main)
    print('-> main page ', res)

    # Go to Reservation Page
    url_live = "https://lavieestbellegolfnresort.com/oldcourse/pagesite/reservation/live.asp"
    res = session.get(url_main)
    print('-> live.asp ', res)
    url_check = "https://lavieestbellegolfnresort.com/oldcourse/GolfRes/onepage/real_membercheck.asp"
    res = session.get(url_main)
    print('-> check.asp ', res)

    #pointdate, openyn, dategbn, courseid, time, atype, bookgtype
    bookinfo = {'pointdate':20220209,\
    'openyn':1,\
    'dategbn': 4,\
    'couseid': '',\
    'time':'00',\
    'atype':'T',\
    'bookgtype':''}

    url_time = 'https://lavieestbellegolfnresort.com/oldcourse/GolfRes/onepage/real_timelist_ajax_list.asp'
    res = session.post(url_time, bookinfo)
    print('===============================')
    soup1 = bs(res.text, 'html.parser')
    timetable = soup1.find_all('a', href=re.compile(r'javascript:subcmd'))
    print("Time Table")
    available = []
    for t in timetable:
        rlt = re.search(r'(.*subcmd)\((.*)\)(.*)', t.attrs['href'])
        available.append([item for item in rlt.group(2).split(',') ])

    for av in available:
        print(av)
    # calendar setting
    this_year = int(target_date[0:4])
    this_month = int(target_date[4:6])
    prev_year = this_year
    prev_month = this_month - 1
    if prev_month == 0:
        prev_month = 12
        prev_year = prev_year -1
    next_year = this_year
    next_month = this_month + 1
    if next_month == 13:
        next_month = 1
        next_year = next_year + 1
    prevDate = '%s%s' %(prev_year, prev_month)
    nextDate = '%s%s' %(next_year, next_month)
    nowDate = target_date[0:6]

    today = datetime.date.today()
    pointdate = '%s%s' %(today.year, today.month)

    #print("prevDate: ", prevDate, "nowDate: ", nowDate, "nextDate: ", nextDate, "pointdate : ", pointdate)

    calendar_info = {"prevDate": prevDate, "nowDate": nowDate, "nextDate": nextDate, "pointdate": pointdate}
    url1 = "https://lavieestbellegolfnresort.com/oldcourse/GolfRes/onepage/real_calendar_ajax_view.asp"
    res = session.post(url1, calendar_info)

    # date selection
    soup = bs(res.text, 'html.parser')

    list_date = soup.find_all('a')

    date_selection = None
    for a in list_date:
        href = a.attrs['href']
        #print(href)
        if target_date == href[28:36]:
            if href[55:56] == 'T':
                date_selection = href[27:57]
                break
            elif href[55:56] == 'C':
                print('closed day')
                break
            elif href[55:56] == 'E':
                print('empty')
                break
            elif href[55:56] == 'N':
                print('mot open')
                break
    if date_selection != None:
        print('date selection ok!')
        pointdate = date_selection[1:9]
        openyn = date_selection[12:13]
        dategbn = date_selection[16:17]
        courseid = date_selection[20:20]
        time_ = date_selection[23:25]
        atype = date_selection[28:29]
    else:
        print('date selection fail!')
        sys.exit()

    # print( "pointdate: ", pointdate,
    #        "openyn: ", openyn,
    #        "dategbn: ", dategbn,
    #        "courseid: ", courseid,
    #        "time: ", time,
    #        "atype: ", atype)

    # loading time list
    time_info = { 'pointdate': pointdate,
                  'openyn': openyn,
                  'dategbn': dategbn,
                  'courseid': courseid,
                  'time': time_,
                  'atype': atype }
    url2 = "https://lavieestbellegolfnresort.com/oldcourse/GolfRes/onepage/real_timeinfo_ajax_from.asp"
    res = session.post(url2, time_info)
    print(res)

    time2_info = { 'pointdate': pointdate,
                   'openyn': openyn,
                   'dategbn': dategbn,
                   'courseid': courseid,
                   'time': time_ }
    url3 = "https://lavieestbellegolfnresort.com/oldcourse/GolfRes/onepage/real_timelist_ajax_list.asp"
    print(url3)
    print(time2_info)
    res = session.post(url3, time2_info)
    print(res)

    print(url3)

    # date selection
    soup1 = bs(res.text, 'html.parser')

    time_list = soup1.find_all('a')

    num_time_list = len(time_list)
    if num_time_list == 0 :
        print('no time slot')
        sys.exit()

    print('\nAvailable time : %d' % (num_time_list-3))

    for a in time_list:
        href = a.attrs['href']
        if time_list.index(a) > 2:
            print("-> ", href[17:])

    for a in time_list:
        href = a.attrs['href']
        time_slot = href[27:31]
        # print(href)
        if target_time[0:4] <= time_slot and target_time[5:9] >= time_slot:
            time_selection = href[17:]
            print('\nSelected time : [ %s ]' % (time_slot))
            # print(time_selection)
            break
    print(time_selection)
    print("-------------------")
    time_selection = time_selection.replace("'", "")
    #print(time_selection)
    time_selection = time_selection[1:-1]
    #print(time_selection)

    atype, pointid, pointtime, pointname, bookgdatekor, \
    bookghole, flagtype, punish_cd, greenfee_base, \
    greenfee_dis, part_cd, alert_info, self_t_yn, res_gubun = [text.strip() for text in time_selection.split(',')]

    print(atype, pointid, pointtime, pointname, bookgdatekor)
    print(bookghole, flagtype, punish_cd, greenfee_base)
    print(greenfee_dis, part_cd, alert_info, self_t_yn, res_gubun)
    print("----------------")
    # 여기부터가 문제 부분
    # javascript:subcmd('R','1','1007','OUT', '2022년 2월 10일 (목요일)', '18홀', 'I', 'UNABLE', '150000', '130000', '', '', 'N', 'N')
    #function subcmd(atype, pointid, pointtime, pointname, bookgdatekor, bookghole, flagtype, punish_cd, greenfee_base, greenfee_dis, part_cd, alert_info, self_t_yn, res_gubun){
	

    time3_info = { "'atype": atype,
                   "pointid": pointid,
                   "pointtime": pointtime,
                   "pointname": pointname,
                   "bookgdatekor": bookgdatekor,
                   "bookghole": bookghole,
                   "flagtype": flagtype,
                   "punish_cd": punish_cd,
                   "greenfee_base": greenfee_base,
                   "greenfee_dis": greenfee_dis,
                   "part_cd": part_cd,
                   "alert_info": alert_info,
                   "self_t_yn": self_t_yn,
                   "res_gubun": res_gubun }
    


    url4 = "https://lavieestbellegolfnresort.com/oldcourse/GolfRes/onepage/real_resOk.asp"
    # url5 = "https://lavieestbellegolfnresort.com/oldcourse/GolfRes/onepage/my_golfreslist.asp"
    dummy = {
        'cmd':"ins",
        'cmval':"0",
        'cmkind':"",
        'calltype':'AJAX',
        'gonexturl': './my_golfreslist.asp',
        'backurl' :"",
        'pointdate': "20220209",
        'openyn':"1",
        'dategbn':"3",
        'pointid':"1",
        'pointname':"OUT",
        'pointtime' :"1007",
        'golfuser_name':'',
        'hand_tel1':'010',
        'hand_tel2':'7795',
        'hand_tel3' : '5647',
        'join_bookg_cnt': '',
        'pointhole': "18홀",
        'pointpartcd':'',
        'ref_check':'',
        'ref_name':'',
        'ref_tel1':'010',
        'ref_tel2':'',
        'ref_tel3':'',
        'coupon_info':'',
        'self_r_yn':'N',
        'self_c_yn':'',
        'res_gubun':'N'
    }
    print(dummy)
    #'%uB2E4%uB978%20%uACF3%uC5D0%uC11C%20%uD68C%uC6D0%u…DF8%uC778%uD558%uC5EC%20%uC8FC%uC2ED%uC2DC%uC694.'
    #"%uC608%uC57D%uC774%20%uC644%uB8CC%20%uB418%uC5C8%uC2B5%uB2C8%uB2E4.%20%uC608%uC57D%uD558%uC2E0%20%uC0AC%uD56D%uC744%20%uD655%uC778%uD558%uC5EC%20%uC8FC%uC2ED%uC2DC%uC694."
    #"%uC608%uC57D%uC774%20%uC644%uB8CC%20%uB418%uC5C8%uC2B5%uB2C8%uB2E4.%20%uC608%uC57D%uD558%uC2E0%20%uC0AC%uD56D%uC744%20%uD655%uC778%uD558%uC5EC%20%uC8FC%uC2ED%uC2DC%uC694."
    # data=json.dumps(time3_info)
    # res = session.post(url4, data)
    # time.sleep(3)
    res = session.post(url4, dummy)
    time.sleep(3)
    print('reservation :', res.text)
    #{"result" : "OK", "gomsg" : "%uC608%uC57D%uC774%20%uC644%uB8CC%20%uB418%uC5C8%uC2B5%uB2C8%uB2E4.%20%uC608%uC57D%uD558%uC2E0%20%uC0AC%uD56D%uC744%20%uD655%uC778%uD558%uC5EC%20%uC8FC%uC2ED%uC2DC%uC694.", "gonexturl" : "./my_golfreslist.asp"}
    # dd = res.text
    # msgs = (dd.split(',')[1]).split(':')[1].split('%')
    # for msg in msgs:
    #     print()
    # print(msgs)

    # print(url4, res.text)
    #
    # soup2 = bs(res.text, 'html.parser')

    # print(soup2)

    #https: // lavieestbellegolfnresort.com / oldcourse / GolfRes / onepage / real_resOk.asp
    #https: // lavieestbellegolfnresort.com / oldcourse / GolfRes / onepage / my_golfreslist.asp
