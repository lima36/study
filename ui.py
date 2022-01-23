"Golf CC Reservation"
# -*- coding: utf8 -*- 

import tkinter as tk
from tkinter import ttk, Frame, Label, StringVar, Entry, Button, IntVar
from tkcalendar import Calendar
# from tkinter import ttk
from sys import platform
from datetime import datetime, timedelta
from time import strftime

import jauro
import kucc

urls = ["https://jayurocc.com/Member/Login",
        "https://kugolf.co.kr/login/login.asp"]
tee_times = ["06:00", "07:00", "08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00"]


def cc_open():
    cc.Start()

def cc_login():
    cc.Login()

def cc_reserve():
    cc.Reserve()

def cc_close():
    cc.Close()

def display_time():
    string = strftime('%Y/%m/%d %H:%M:%S %p')
    time_lbl.config(text = string)
    time_lbl.after(1000, display_time)

def cc_change(event=None):
    global cc
    print(comboExample.current())
    if comboExample.current() == 0:
        cc = jauro.jauro()

    elif comboExample.current() == 1:
        cc = kucc.kucc()
    
    print(cc)

def cc_onclosing():
    root.destroy()

if __name__ == "__main__":
    def callback():
        print (bookday.get())
        
        return True

    def callback2(bookday):
        print("callback2")
        global target_time_str
        print("callback2", int(bookday.get()))
        td=datetime.now() + timedelta(days=int(float(bookday.get())))
        target_date_str.delete(0, tk.END)
        target_date_str.insert(0,str(td.year)+"-"+str(td.month)+"-"+str(td.day))

    cc = None
    root  = tk.Tk()
    root.geometry('390x400') 
    root.title('Golf Reserve')

    top_frame = Frame(root, bg='cyan', width = 450, height=40, pady=3)
    top_frame.grid(row=0, sticky="ew")

    center_frame = Frame(root, bg='blue', width=450, height=80, padx=3, pady=3)
    center_frame.grid(row=1, sticky="ew")

    btm_frame2 = Frame(root, bg='yellow', width=450, height=30, pady=3)
    btm_frame2.grid(row=2, sticky='ew')

    btm_frame = Frame(root, bg='violet', width = 450, height = 40, pady=3)
    btm_frame.grid(row=3, sticky='ew')

    btm_frame3 = Frame(root, bg='red', width = 450, height = 40, pady=3)
    btm_frame3.grid(row=4, sticky='ew')
    ############################################################################
    comboLabel = Label(top_frame, width=5, text="URL : ").grid(row=0, column=0, padx=10, pady=2,sticky='w')
    url_str = StringVar()
    comboExample = ttk.Combobox(top_frame, textvariable=url_str, width=30, values=urls)
    comboExample.current(0)
    cc_change()
    comboExample.bind("<<ComboboxSelected>>", cc_change)
    comboExample.grid(row=0, column=1, columnspan=1)

    openButton = Button(top_frame, text="Open", command=cc_open).grid(row=0, column=2, padx=2, pady=2, sticky='e')
    #############################################################################
    # #username label and text entry box
    usernameLabel = Label(center_frame, width=10, text="UserName : ").grid(row=0, column=0, padx=10, pady=2, sticky='w')
    username = StringVar(value='lima36')
    usernameEntry = Entry(center_frame, textvariable=username).grid(row=0, column=1, padx=2, pady=2,sticky='w')  

    # #password label and password entry box
    passwordLabel = Label(center_frame, width=10, text="Password : ").grid(row=1, column=0, padx=10, pady=2, sticky='w')  
    password = StringVar(value='peace@2020')
    passwordEntry = Entry(center_frame, textvariable=password, show='*').grid(row=1, column=1, padx=2, pady=2)  

    loginButton = Button(center_frame, text="Login", command=cc_login).grid(row=0, column=2, rowspan=2, padx=2, pady=2, sticky='e')
    ##############################################################################
    Label(btm_frame2, width=10, text="Today: ").grid(row=0, column=0, padx=10, pady=2, sticky='w')
    # Label(btm_frame2, text=str(today.year)+"-"+str(today.month)+"-"+str(today.day)).grid(row=0, column=1)
    Label(btm_frame2, width=10, text="Reserve:").grid(row=1, column=0, padx=10, pady=2, sticky='w')
    time_lbl = Label(btm_frame2, font = ('calibri', 10, 'bold'), background = 'purple', foreground = 'white')
    time_lbl.grid(row=0, column=1, columnspan=4)
    display_time()
    ##############################################################################
    bookday = IntVar(value=21)
    # bookdayEntry = Entry(btm_frame2,textvariable=bookday, width=3, validate="focusout", validatecommand=callback)
    bookdayEntry = Entry(btm_frame2,textvariable=bookday, width=3)
    bookday.trace("w", lambda name, index, mode, bookday=bookday: callback2(bookday))
    # bookdayEntry.bind("<Enter>", callback2)
    bookdayEntry.grid(row=1, column=1)
    Label(btm_frame2, text="days after").grid(row=1, column=2)

    target = datetime.now() + timedelta(days=21)
    target_date = StringVar(value=str(target.year)+"-"+str(target.month)+"-"+str(target.day))
    target_date_str = Entry(btm_frame2, width=10, textvariable=target_date)
    target_date_str.grid(row=1, column=3)

    target_time = StringVar(value="09:00")
    target_time_str =Entry(btm_frame2, width=10, textvariable=target_time)
    target_time_str.grid(row=1, column=4)

    ######################################################################################
    reserveButton = Button(btm_frame, text="Reserve", command=cc_reserve).grid(row=0, column=0, padx=2, pady=2, sticky='ew')
    refeshButton = Button(btm_frame, text="Refresh").grid(row=0, column=1, padx=2, pady=2,sticky='ew')
    closeButton = Button(btm_frame, text="Close", command=cc_close).grid(row=0, column=2, padx=2, pady=2,sticky='ew')
    
    ######################################################################################
    # Add Calendar
    cal = Calendar(btm_frame3, font="Arial 10", selectmode='day', firstweekday="sunday", year=target.year, month=target.month, day=target.day, date_pattern="Y-M-D")
    cal.grid(row=0, column=0, rowspan=3)

    Button(btm_frame3, text = "Go Today").grid(row=0, column=1)
    Button(btm_frame3, text = "Get Date").grid(row=1, column=1)
    
    ######################################################################################
    root.protocol("WM_DELETE_WINDOW", cc_onclosing)
    root.mainloop()
