from selenium import webdriver 
from selenium.webdriver.common.keys import Keys 
import time
from selenium.webdriver.support.ui import Select

class SRT_page(): 
    def __init__(self): 
        print("__init__") 
        super().__init__() 
    
    def login(self): 
        print("login") 
        self.driver = webdriver.Chrome('/home/lima/Work_Python/chromedriver_linux64/chromedriver') 
        self.driver.get("https://etk.srail.kr/cmc/01/selectLoginForm.do?pageId=TK0701000000") 
        self.driver.find_element_by_id("srchDvNm01").send_keys("1891503494") 
        self.driver.find_element_by_id("hmpgPwdCphd01").send_keys("peace@2020") 
        self.driver.find_element_by_id("hmpgPwdCphd01").send_keys(Keys.RETURN) 
        time.sleep(0.5) 
        self.driver.get("https://etk.srail.kr/hpg/hra/01/selectScheduleList.do?pageId=TK0101010000")

    def plan(self, dep, arr, dat, hou): 
        time.sleep(1) 
        #//*[@id="search-form"]/fieldset/div[1]/div/div/div[1]/label
        #//*[@id="dptRsStnCdNm"]
        #//*[@id="arvRsStnCdNm"]
        self.driver.find_element_by_xpath('//*[@id="dptRsStnCdNm"]').clear() # 출발지 칸을 비우고 
        self.driver.find_element_by_xpath('//*[@id="dptRsStnCdNm"]').send_keys(dep) # 입력했던 도시명 입력 
        self.driver.find_element_by_xpath('//*[@id="arvRsStnCdNm"]').clear() # 도착지 칸을 비우고 
        self.driver.find_element_by_xpath('//*[@id="arvRsStnCdNm"]').send_keys(arr) # 입력했던 도시명 입력 # 시간 입력하기 
        #/html/body/div/div[4]/div/div[2]/form/fieldset/div[1]/div/div/div[3]/div[2]/select
#        self.driver.execute_script(f'arguments[0].innerText = {dat};', self.driver.find_element_by_xpath("/html/body/div/div[4]/div/div[2]/form/fieldset/div[1]/div/div/div[3]/div[1]/select"))
        dd = Select(self.driver.find_element_by_id('dptDt'))
        print(dd.options)
        dd.select_by_visible_text(dat)
        hh = Select(self.driver.find_element_by_id('dptTm'))
        hh.select_by_visible_text(hou)
        # select = self.driver.find_element_by_xpath("/html/body/div/div[4]/div/div[2]/form/fieldset/div[1]/div/div/div[3]/div[2]/select")
        # select.select_by_visible_text(hou)
        # self.driver.execute_script(f'arguments[0].innerText = {hou};', select)
        #/html/body/div/div[4]/div/div[2]/form/fieldset/div[1]/div/div/div[3]/div[1]/select
        #/html/body/div/div[4]/div/div[2]/form/fieldset/div[1]/div/div/div[3]/div[2]/select
        #self.driver.execute_script(f'arguments[0].innerText = {hou};', 
        #self.driver.find_element_by_xpath( "/html/body/div[1]/div[4]/div/div[2]/form/fieldset/div[1]/div/div/div[3]/div[2]/a/span[2]")) # 날짜 입력하기
        #self.driver.find_element_by_xpath( "/html/body/div[1]/div[4]/div/div[2]/form/fieldset/div[1]/div/div/div[3]/div[1]/a/span[2]").click() 
        # self.driver.find_element_by_xpath( "/html/body/div/div[4]/div/div[2]/form/fieldset/div[1]/div/div/div[3]/div[1]/select").click()
        # self.driver.find_elements_by_link_text(dat)[0].click() # 검색 버튼을 누르고 2초간 기다리기 

        #/html/body/div/div[4]/div/div[2]/form/fieldset/div[2]/input
        #/html/body/div/div[4]/div/div[2]/form/fieldset/div[1]/div/div/div[3]/span
        self.driver.find_element_by_xpath('/html/body/div[1]/div[4]/div/div[2]/form/fieldset/div[2]/input').click() 
        time.sleep(2) 
        self.seats = [] 
        for count in range(1, 11): 
            seat_list = [] 
            try: 
                seat_tr = self.driver.find_element_by_xpath( f"/html/body/div[1]/div[4]/div/div[3]/div[1]/form/fieldset/div[6]/table/tbody/tr[{count}]/td[2]").text 
                seat_dep = self.driver.find_element_by_xpath( f"/html/body/div[1]/div[4]/div/div[3]/div[1]/form/fieldset/div[6]/table/tbody/tr[{count}]/td[4]").text 
                seat_arr = self.driver.find_element_by_xpath( f"/html/body/div[1]/div[4]/div/div[3]/div[1]/form/fieldset/div[6]/table/tbody/tr[{count}]/td[5]").text 
                seat_ava = self.driver.find_element_by_xpath( f"/html/body/div[1]/div[4]/div/div[3]/div[1]/form/fieldset/div[6]/table/tbody/tr[{count}]/td[7]/a").text 
            except: 
                seat_tr = "없음" 
                seat_dep = "없음" 
                seat_arr = "없음" 
                seat_ava = "없음" 
            finally: 
                seat_list.append(seat_tr) 
                seat_list.append(seat_dep) 
                seat_list.append(seat_arr) 

            seat_list.append(seat_ava) 
            self.seats.append(seat_list) 
        return self.seats

        
    def try_reservation(self, checked): 
        while True: 
            try: 
                for index in checked: 
                    index = index + 1 
                    if self.driver.find_element_by_xpath( f"/html/body/div[1]/div[4]/div/div[3]/div[1]/form/fieldset/div[6]/table/tbody/tr[{index}]/td[7]/a").text == "예약하기": 
                        element = self.driver.find_element_by_xpath( f"/html/body/div[1]/div[4]/div/div[3]/div[1]/form/fieldset/div[6]/table/tbody/tr[{index}]/td[7]/a") 
                        self.driver.execute_script("arguments[0].click();", element) 
                        return "done" 
                    else: 
                        pass 
                    self.driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME) 
                    element = self.driver.find_element_by_xpath( '/html/body/div[1]/div[4]/div/div[2]/form/fieldset/div[2]/input') 
                    self.driver.execute_script("arguments[0].click();", element) 
                    time.sleep(1) 
            except: 
                time.sleep(8) 
                continue
#출처: https://conansjh20.tistory.com/68 [취미는 파이썬]