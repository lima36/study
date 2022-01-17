"Engergy Crawling"
from types import NoneType
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from selenium import webdriver
import openpyxl

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import date
import re

#--------------------------------------------------------------
# Email 보내기
def send_email():   
    # 세션 생성
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login('limitsigma36@gmail.com', 'ebgqlgebhmiaqrvo')

    # 제목, 본문 작성
    msg = MIMEMultipart()
    msg['Subject'] = '한국에너지공단 공지사항 : ' + date.today().strftime("%Y/%m/%d")
    msg.attach(MIMEText(result, 'plain'))

    ## 파일첨부 (파일 미첨부시 생략가능)
    # attachment = open('파일명', 'rb')
    # part = MIMEBase('application', 'octet-stream')
    # part.set_payload((attachment).read())
    # encoders.encode_base64(part)
    # part.add_header('Content-Disposition', "attachment; filename= " + filename)
    # msg.attach(part)

    # 메일 전송
    s.sendmail("limitsigma36@gmail.com", "lima36@empal.com", msg.as_string())

    # 세션 종료
    s.quit()
    
#-----------------------------------------------------------------
url = "https://greenhome.kemco.or.kr/ext/inf/noti/selectNoticeList.do?pageIndex=1&boardType=N&sn=0"
import urllib.request as req
res = req.urlopen(url)
soup = BeautifulSoup(res,'html.parser')
result = ""
titles = soup.select('#content > table > tbody > tr')
for title in titles:
    trs = title.find_all('td')
    # print(trs[3].text.strip())
    
    
    addr=title.find('a', href=True, text=True)
    addr_text = addr['href']
    print(re.findall('\d+', addr_text)[1])
    
    #https://greenhome.kemco.or.kr/ext/inf/noti/selectNoticeDetail.do?searchCnd=0&searchWrd=&sn=502&boardType=N&pageIndex=1
    infourl = "https://greenhome.kemco.or.kr/ext/inf/noti/selectNoticeDetail.do?searchCnd=0&searchWrd=&sn=" + re.findall('\d+', addr_text)[1] + "&boardType=N&pageIndex=1"
    
    result += trs[3].text.strip() + ":" + trs[1].text.strip() + " : " + infourl + "\n" 
print(result)
send_email()
