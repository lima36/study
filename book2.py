import requests
import requests_html
from bs4 import BeautifulSoup as bs
import re
import time
sess = requests.session()

querys = ['키출판사', '초등수학']
max_page = 10

    
def yes24(query):
    url = 'http://www.yes24.com/Product/Search?domain=ALL&query='
    req=sess.get(url + query)
    soup=bs(req.content, 'html.parser')
    end_btn = soup.find('a', class_='bgYUI end')
    total = int(end_btn.attrs['title'])
    total = max_page if total > max_page else total

    for num in range(1, total+1): # 1 ~ total page
        req=sess.get(url + query + '&page=' + str(num))
        soup=bs(req.content, 'html.parser')
        searchlist=soup.find('ul', attrs={'id':'yesSchList'})
        items=searchlist.find_all('div', class_='itemUnit')
        for item in items:
            name    = item.find('a', class_='gd_name')
            title   = name.text.strip()
            link    = name.attrs['href']
            saleNum = item.find('span', class_='saleNum').text.strip()
            sale    = re.search(r'([0-9,]+)',saleNum)[1]
            
            info_date = item.find('span', class_='authPub info_date').text.strip()
            info_pub = item.find('span', class_='authPub info_pub').text.strip()
            # price = item.find('em', class_='yes_b').text.strip()
            price2 = item.select('div.info_row.info_price > strong > em')[0].text.strip()
            try:
                score = item.select('div.info_row.info_rating > span.rating_grade > em')[0].text.strip()
            except:
                score = " "
            print(title, link, sale, info_date, info_pub, price2, score)
            
def get_request(html_session, url, render = False):
    res = html_session.get(url)
    try:
        res.raise_for_status()
    except ValueError as e:
        raise('Dead link')

    if render:
        res.html.render(sleep = 0, timeout = 5)
        
    soup = bs(res.html.html, 'html.parser')
    
    return soup         
            
def kybo(query):
    url = 'https://search.kyobobook.co.kr/web/search?vPstrKeyWord='# + query #&currentPage=3'
    print(url+query)
    url2 = url + query
    html_session = requests_html.HTMLSession()
    soup_html = get_request(html_session, url+query, True)
    total = int(soup_html.find('span', attrs={'id':'totalpage'}).text.strip())

    print(total)
    
    total = max_page if total > max_page else max_page
    for num in range (1, total + 1):
        req = sess.get(url + query + '&page=' + str(num))
        soup=bs(req.content, 'html.parser')
        searchlist=soup.find('tbody', attrs={'id':'search_list'})
        items = searchlist.find_all('tr')
        for item in items:
            name = item.select('td.detail > div.title > a > strong')[0].text.strip()
            print(name)
    

for query in querys:
    kybo(query)
