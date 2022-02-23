



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
    login_info = { "msId": id, "msPw": pw, "autoLogin" :'0'}
    url_login = 'https://www.seowongolf.co.kr/hills/member/actionLogin.do'
    res = session.post (url_login, login_info)
    print('-> login page ', res.content)

    url_reserve='https://www.seowongolf.co.kr/hills/reservation/reservation.do'
    res = session.get(url_reserve)
    # print(res.content)

    # url_treelist = 'https://www.seowongolf.co.kr/hills/reservation/getTeeList.do?&date=20220308&roundf=1&_=1644937256179'

if __name__ == '__main__':
    user_id = input('Input ID:')
    user_pw = input('Password: ')
    user_phone = input('Phone Number with "-":')

    target = datetime.datetime.today() + dateutil.relativedelta.relativedelta(days=21)
    targetDate1 = datetime.datetime.strftime(target, '%Y%m%d')
    print(targetDate1)
    target_date = targetDate1#'20220226'
    target_time = '0800:1255'
    # target_date = input('Target date (ex> yyyymmdd): ')
    # target_time = input('Target time (ex: 0655:0955): ')

    make_reserve(user_id, user_pw, target_date, target_time, user_phone)