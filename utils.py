# -*- coding: utf8 -*- 
import datetime
from datetime import date


def get_today():
    return date.today()

def get_target(days):
    target = datetime.datetime.now() + datetime.timedelta(days=days)
    return target
