import utils
from ChromeBrowser import ChromeBrowser


class jauro(ChromeBrowser):
    # def __init__(self):
    #     super().__init__()
        
    def Start(self):
        self.open_page("https://jayurocc.com/Member/Login")
          
    def Login(self):
        self.waitUntilOpen('ctl00_Content_UserID')
        self.input_id("ctl00_Content_UserID","lima36")
        self.input_passwd("ctl00_Content_UserPassword","peace@2020")
        self.click_login("LoginButton")
        
    def ClosePopup(self):
        self.waitOpen(0.3)
        self.close_popup_id('HidePopupLayerButton63')
        self.close_popup_id('HidePopupLayerButton66')
    
    def Reserve(self):
        self.open_page("https://jayurocc.com/Reservation/Reservation")
        self.close_popup_class("pointBtn")
        self.GoToReservation(utils.get_today(), utils.get_target(21))
        
    def GoToReservation(self, today, target):
        print("reservation")
        cmd = "javascript:Update('LIST|" + str(today.year)+"-"+str(today.month).zfill(2) +"-" + str(today.day).zfill(2)+"|" \
                                         + str(target.year).zfill(2)+"-"+ str(target.month).zfill(2) + "-"+ str(target.day).zfill(2) + "|N|2||');"
        self.run_script(cmd)
