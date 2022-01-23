import utils
from ChromeBrowser import ChromeBrowser

import time

class kucc(ChromeBrowser):
    # for singleton
    def __new__(cls):
        if not hasattr(cls,'instance'):
            print('create')
            cls.instance = super(kucc, cls).__new__(cls)
        else:
            print('recycle')
        return cls.instance

    def __init__(self):
        super().__init__()
        
    def Start(self):
        self.open_page("https://kugolf.co.kr/login/login.asp")
          
    def Login(self):
        self.waitUntilOpen('log_id')
        self.input_id("log_id","lima36")
        self.input_id("login_pw","peace@2020")
        self.click_login2("bt_login")
        self.ClosePopup()
        
    def ClosePopup(self):
        self.close_popup_alert()
    
    def Reserve(self):
        print("Reserve")
        self.GoToReservation(utils.get_today(), utils.get_target(21))
        
    def GoToReservation(self, today, target):
        print("GoToReservation")
        prevDate = str(today.year) + str(today.month-1)
        nowDate = str(today.year) + str(today.month)
        nextDate = str(target.year) + str(target.month)
        pointDate = str(target.year) + str(target.month) + str(target.day)
        print(nowDate, nextDate)
        url3 = "https://kugolf.co.kr/GolfRes/onepage/real_reservation.asp?usrmemcd=&pointdate="+ pointDate + "#pointdate=" + pointDate + \
                "&courseid=0&openyn=1&dategbn=2&choice_time=00&settype=T&prevDate=" +prevDate + "&nowDate="+ nowDate + "&nextDate=" + nextDate
        self.open_page2(url3)

        time.sleep(0.3)

        # cmd = "javascript:quick_timefrom_change('" + str(target.year) + str(target.month).zfill(2) + str(target.day).zfill(2) + "'," + "'1'" +",'"+ str(target.weekday()+2) + "'," + "''" + "," + "'05'" + "," + "'Y'" + "," + "'real'" + ");"
        # cmd2 = "javascript:timefrom_change('20211214','1','2','','00','T');"
        cmd3 = "javascript:quick_layout_info_html('')"
        self.run_script(cmd3)

    def Close(self):
        self.close_chrome()
# cc = None
# def open():
#     global cc
#     if not cc:
#         cc = kucc()

if __name__ == "__main__":
    a = kucc()
    print(a)
    b = kucc()
    print(b)