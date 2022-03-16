# -*- coding: utf8 -*- 
# step1. 관련 패키지 및 모듈 불러오기
from selenium import webdriver
import time
import pandas as pd
from selenium.webdriver.common.by import By
import re
from bs4  import BeautifulSoup as bs
import openpyxl
from openpyxl import load_workbook

wb = openpyxl.Workbook()
ws = wb.active


# step2. 네이버 뉴스 댓글정보 수집 함수
def get_naver_news_comments(url, wait_time=5, delay_time=0.1):
    # 크롬 드라이버로 해당 url에 접속
    driver = webdriver.Chrome("/home/lima/Work_Python/chromedriver_linux64/chromedriver")
    
    # (크롬)드라이버가 요소를 찾는데에 최대 wait_time 초까지 기다림 (함수 사용 시 설정 가능하며 기본값은 5초)
    driver.implicitly_wait(wait_time)
    
    # 인자로 입력받은 url 주소를 가져와서 접속
    driver.get(url)

    element = driver.find_element_by_id("cafe_main")
    driver.switch_to.frame(element)
    # 더보기가 안뜰 때 까지 계속 클릭 (모든 댓글의 html을 얻기 위함)
    # while True:
    #     # 예외처리 구문 - 더보기 광클하다가 없어서 에러 뜨면 while문을 나감(break)
    #     try:
    #         driver.find_element_by_css_selector('ul.comment_list')
    #         # more.click()
    #         time.sleep(delay_time)
            
    #     except:
    #         break
    
    # f = open('comment.txt', 'w', encoding='UTF-8')
    comments=driver.find_element_by_css_selector('a.button_comment')
    comments.click()

    data = []
    nextbtns = driver.find_elements_by_css_selector('div.CommentBox > div.ArticlePaginate > button')
    ind=1
    for i, next in enumerate(nextbtns):
        nextbtns[i].click()
        # 본격적인 크롤링 타임
        
        # commentitems = driver.find_elements_by_css_selector("li[class='CommentItem CommentItem--reply'")
        commentreplyonlys = driver.find_elements_by_css_selector("li.CommentItem--reply")
        commentsall = driver.find_elements_by_css_selector("li.CommentItem")
        
        # for cc in commentreplyonlys:
        #     for dd in commentsall:
        #         if cc == dd:
        #             print("same", cc, dd)
        #             break
        #         else:
                    
        #             print("different", cc, dd)
        #             continue


        commentlist = driver.find_element_by_css_selector("ul[class='comment_list'")
        html = commentlist.get_attribute('innerHTML')
        soup = bs(html, 'html.parser')
        j=5
        for li in soup.select('li'):
            rep = []
            if "CommentItem--reply" in li.attrs['class']:
                rep.append(li.text.strip())
                print(li.text.strip())
                data.append(li.text.strip())
                ws.cell(ind, j).value = str(li.text.strip())
                j += 1
            elif "CommentItem" in li.attrs['class']:
                j = 5
                try:
                    id = li.attrs['id'].strip()
                except:
                    print('error')
                    continue
                nickname=li.find('div', class_='comment_nick_info')
                print(nickname.text.strip())
                textbox = li.find('div', class_='comment_text_box')
                ask = textbox.text.strip()
                print(id, ask)
                ws.cell(ind, 1).value = str(i)
                ws.cell(ind, 2).value = str(id)
                ws.cell(ind, 3).value = str(nickname.text.strip())
                ws.cell(ind, 4).value = str(textbox.text.strip())

                ind += 1
                

        # for a in soup.find('li[class="CommentItem"]'):
        #     if soup.find('li[class="CommentItem CommentItem--reply"]'):
        #         print(a)


        # for comment in commentsall:
        #     html = comment.get_attribute('innerHTML')
        #     print(html)
        #     # try:
        #     print("====================")
        #     commentid = comment.find_element_by_tag_name('li')
        #     # commentid.find_element_by_tag_name('img').get_attribute('src')
        #     print("commentid", commentid)
        #     nick=comment.find_element_by_class_name('comment_nick_info')
        #     print(nick.text)

        #     comm = comment.find_element_by_class_name('text_comment')
        #     print(comm.text)
            

        #     comment.get_attribute()
        #     re.search(r'CommentItem', )
        #     rlts = comment.find_element_by_css_selector('li.CommentItem.CommentItem--reply')
        #     for rl in rlts:
        #         pass#print(rl.text)
        #     print(i)
            
                # if rlt:
                #     print('reply...')
                    
                    
            # items=comment.find_element_by_xpath("//li[contains(@class, 'CommentItem') and not(@class, 'CommentItem--reply')]")
            # replys=comment.find_elements_by_class_name('CommentItem--reply')
            # id = comment.find_element_by_class_name('comment_nickname')
            # print(replys.text)
            # print(id.text)
            # print(comment)
        # except:
            #     print('error', i)
            #     pass
            
            
        time.sleep(5)
        print(next.text)
        wb.save('./kiki.xlsx')
    wb.close()

    # 1)작성자
    # # selenium으로 작성자 포함된 태그 모두 수집
    # nicknames = driver.find_elements_by_css_selector('span.u_cbox_nick')
    # # 리스트에 텍스트만 담기 (리스트 컴프리핸션 문법)
    # list_nicknames = [nick.text for nick in nicknames]

    # # 2)댓글 시간
    # # selenium으로 댓글 시간 포함된 태그 모두 수집
    # datetimes = driver.find_elements_by_css_selector('span.u_cbox_date')
    # # 리스트에 텍스트만 담기 (리스트 컴프리핸션 문법)
    # list_datetimes = [datetime.text for datetime in datetimes]

    # # 3)댓글 내용
    # # selenium으로 댓글내용 포함된 태그 모두 수집
    # contents = driver.find_elements_by_css_selector('span.u_cbox_contents')
    # # 리스트에 텍스트만 담기 (리스트 컴프리핸션 문법)
    # list_contents = [content.text for content in contents]


    # # 4)작성자, 댓글 시간, 내용을 셋트로 취합
    # list_sum = list(zip(list_nicknames,list_datetimes,list_contents))

    # 드라이버 종료
    # driver.quit()
    
    # 함수를 종료하며 list_sum을 결과물로 제출
    # return list_sum

# step3. 실제 함수 실행 및 엑셀로 저장
if __name__ == '__main__': # 설명하자면 매우 길어져서 그냥 이렇게 사용하는 것을 권장
    

    # 원하는 기사 url 입력
    # url = '댓글 크롤링 원하는 기사의 url (주의! 댓글보기를 클릭한 상태의 url이어야 함'
    url = 'https://cafe.naver.com/dochithink?iframe_url_utf8=%2FArticleRead.nhn%253Fclubid%3D12843510%2526articleid%3D1832183%2526referrerAllArticles%3Dtrue'
    # 함수 실행
    comments = get_naver_news_comments(url)
    
    # 엑셀의 첫줄에 들어갈 컬럼명
    # col = ['작성자','시간','내용']
    
    # # pandas 데이터 프레임 형태로 가공
    # df = pd.DataFrame(comments, columns=col)
    
    # # 데이터 프레임을 엑셀로 저장 (파일명은 'news.xlsx', 시트명은 '뉴스 기사 제목')
    # df.to_excel('news.xlsx', sheet_name='뉴스 기사 제목')
    
    # from selenium import webdriver
    # from selenium.webdriver.support.ui import WebDriverWait
    # from selenium.webdriver.support import expected_conditions as EC
    # from selenium.webdriver.common.by import By
    # from selenium.common.exceptions import TimeoutException

    # driver = webdriver.Chrome('D:/7.Software/chromedriver_win32/chromedriver')

    # driver.get(url)
    # delay = 10 # seconds
    # try:
    #     myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a.button_comment')))# #app > div > div > div.ArticleContentBox > div.article_header > div.ArticleTool > a.button_comment
    #     print ("Page is ready!")
    # except TimeoutException:
    #     print ("Loading took too much time!")