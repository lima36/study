# -*- coding: utf8 -*- 
# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# https://www.online-toolz.com/langs/ko/tool-ko-text-unicode-entities-convertor.html

###############################################################
# La vie bell CC
# https://lavieestbellegolfnresort.com
###############################################################

import sys
import time
import datetime

import requests
from bs4 import BeautifulSoup as bs
import dateutil.relativedelta
import re
from pytz import timezone

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
    url_login = "https://lavieestbellegolfnresort.com/oldcourse/login/login.asp"
    res = session.get(url_login)
    print('-> login page ', res)

    # Login OK
    url_login_ok = "https://lavieestbellegolfnresort.com/oldcourse/login/login_ok.asp"
    res = session.post(url_login_ok, login_info)
    print('-> login ok ', res)

    # Main Page
    url_main = "https://lavieestbellegolfnresort.com/oldcourse/index.asp"
    res = session.get(url_main)
    print('-> live.asp ', res)

    # calendar setting
    target=datetime.datetime.strptime(target_date, '%Y%m%d')
    prev=target + dateutil.relativedelta.relativedelta(months=-1)
    next=target + dateutil.relativedelta.relativedelta(months=1)
    calendar_info1 = {"prevDate": prev.strftime('%Y%m'), 
                      "nowDate":  target.strftime('%Y%m'), 
                      "nextDate": next.strftime('%Y%m'), 
                      "pointdate":target.strftime('%Y%m')}
    url1 = "https://lavieestbellegolfnresort.com/oldcourse/GolfRes/onepage/real_calendar_ajax_view.asp"
    res = session.post(url1, calendar_info1)

    # date selection
    soup = bs(res.text, 'html.parser')
    list_date = soup.find_all('a', href=re.compile(r'javascript:timefrom_change'))
    available = []
    for t in list_date:
        rlt = re.search(r'(.*)\((.*)\)(.*)', t.attrs['href'])
        available.append([item.replace("'", "") for item in rlt.group(2).split(',') ])

    if len(available) <1:
        print("No available List 0", )
        sys.exit()

    time2_info = {}
    time3_info = {}
    for i, info in enumerate(available):
        if info[0] == target_date:
            print("target date is available")
            print(info)
            time2_info = {'pointdate': info[0],
                   'openyn': info[1],
                   'dategbn': info[2],
                   'courseid': info[3],
                   'time': info[4]}
            break

    if time2_info == {}:
        print("No Available Date1 ")
        sys.exit()

    url3 = "https://lavieestbellegolfnresort.com/oldcourse/GolfRes/onepage/real_timelist_ajax_list.asp"
    res = session.post(url3, time2_info)
    print(res)

    # date selection
    soup1 = bs(res.text, 'html.parser')
    time_list = soup1.find_all('a')
    time_list2 = soup1.find_all('a', href=re.compile(r'javascript:subcmd'))
    time_table = []
    for aa in time_list2:
        rlt = re.search(r'\((.*)\)$', aa.attrs['href'])
        time_table.append([text.strip().replace("'", "") for text in rlt.group(1).split(',')])

    for k, bb in enumerate(time_table):
        if int(bb[2]) >= int(target_time[0:4]) and int(bb[2]) < int(target_time[5:9]):
            print(bb)
            time3_info = {
                   "atype": bb[0],
                   "pointid": bb[1],
                   "pointtime": bb[2],
                   "pointname": bb[3],
                   "bookgdatekor": bb[4],
                   "bookghole": bb[5],
                   "flagtype": bb[6],
                   "punish_cd": bb[7],
                   "greenfee_base": bb[8],
                   "greenfee_dis": bb[9],
                   "part_cd": bb[10],
                   "alert_info": bb[11],
                   "self_t_yn": bb[12],
                   "res_gubun": bb[13] 
                   }
            break
        else:
            print("No Available time")
            sys.exit()

    if time3_info == {}:
        print("No Available Date 2")
        sys.exit()

    url4 = "https://lavieestbellegolfnresort.com/oldcourse/GolfRes/onepage/real_resOk.asp"
    dummy = {
        'cmd':"ins",
        'cmval':"0",
        'cmkind':"",
        'calltype':'AJAX',
        'gonexturl': './my_golfreslist.asp',
        'backurl' :"",
        'pointdate': time2_info['pointdate'],
        'openyn':time2_info['openyn'],
        'dategbn':time2_info['dategbn'],
        'pointid':time3_info['pointid'],
        'pointname':time3_info['pointname'],
        'pointtime' :time3_info['pointtime'],
        'golfuser_name':'',
        'hand_tel1':tele[0],
        'hand_tel2':tele[1],
        'hand_tel3':tele[2],
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
        'res_gubun':time3_info['res_gubun']
    }

    res = session.post(url4, dummy)
    print('reservation :', res.text)

    # result = eval(res.text)
    # message = result['gomsg'].replace('%u', '\\u').encode().decode('unicode_escape')
    # print(message)

def golfjob2(user_id, user_pw, fdate, ftime, day):
    print('golfjob2', fdate, ftime, day)
    today       = datetime.datetime.now(timezone("Asia/Seoul")).date()

    if day==21:
        target      = today + dateutil.relativedelta.relativedelta(days=21)
        target_date = target
    else:
        target_date = fdate

    target_time = ftime
    user_phone = "010-7795-5647"

    make_reserve(user_id, user_pw, target_date, target_time, user_phone)


# Main Loop
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    user_id = '아이디'
    user_pw = '비밀번호'
    user_phone = "전화번호" #010-7795-5647

    target_date = '20220208'
    target_time = '0655:1255'
    # target_date = input('Target date (ex> yyyymmdd): ')
    # target_time = input('Target time (ex: 0655:0955): ')

    make_reserve(user_id, user_pw, target_date, target_time, user_phone)