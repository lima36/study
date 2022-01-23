# -*- coding: utf8 -*- 
from abc import ABCMeta, abstractmethod
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.alert import Alert

import time
# import os
import platform
# import datetime
# from datetime import date
import utils

class ChromeBrowser(metaclass=ABCMeta):
    "Class CCOpen using Chromebrowser"
    # 클래스 변수 : 클래스 끼리 공유를 해야할 변수

    # 초기자(initializer)
    def __init__(self):
        # 인스턴스 변수
        if platform.system() == "Linux" or platform.system() == "Linux2":
            self.exec_chrome = "/home/lima/Work_Python/Code_Test/driver/chromedriver"
        elif platform.system() == "Windows":
            self.exec_chrome = "../chromedriver_win32/chromedriver.exe"
        else:
            self.exec_chrome = "../chromedriver_win32/chromedriver.exe"
            
        self.options = webdriver.ChromeOptions()
        # self.options.add_argument("--start-maximized")
        self.options.add_argument("--disable-gpu")
        self.options.add_experimental_option("detach", True)
        self.options.add_experimental_option("excludeSwitches", ["enable-logging"])
        
    def open_page(self, url):
        self.driver = webdriver.Chrome(self.exec_chrome, options=self.options)
        self.driver.get(url)
    
    def open_page2(self, url):
        self.driver.get(url)
    
    def input_id(self, id, text):
        self.driver.find_element_by_id(id).send_keys(text)
    
    def input_passwd(self, id, text):
        self.driver.find_element_by_id(id).send_keys(text)
        
    def click_login(self, id):
        self.driver.find_element_by_id(id).click()
        
    def click_login2(self, cls):
        dd = self.driver.find_element_by_class_name(cls)
        dd.click()
        # da = Alert(self.driver)
        # da.accept()
    
    def close_popup_alert(self):
        try:
            Alert(self.driver).accept()
        except:
            pass
        
    def close_popup_id(self, id):
        try:
            popup=self.driver.find_element_by_id(id).click()
            popup.click()
        except:
            pass
        
    def close_popup_class(self, name):
        try:
            self.driver.find_element_by_class_name(name).click()
        except:
            pass
        
    def moveBottom(self):
        time.sleep(1)
        self.driver.execute_script("window.scrollTo(0, 1000)")   
        
    def close_chrome(self):
        print('close chrome browser')
        self.driver.close()
    
    def refresh_chrome(self):
        self.driver.refresh()
        
    def waitOpen(self, gap):
        time.sleep(gap)
        
    def waitUntilOpen(self, id):
        delay = 3 # seconds
        try:
            myElem = WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.ID, id)))
            print("Page is ready!")
        except TimeoutException:
            print("Loading took too much time!")
    
    # def openPage(self, url):
    #     self.driver.get(url)
        
    def run_script(self, cmd):
        print("run_script")
        self.driver.execute_script(cmd)
