from tkinter import ttk
from tkinter import *
import PIL.ImageTk
import PIL.Image
import sqlite3
import sys
import os
import re

sys.dont_write_bytecode = True

full_path=os.path.dirname(os.path.realpath(__file__))

btc_path=os.path.join(full_path+r'\resources\BTC.png')
eth_path=os.path.join(full_path+r'\resources\ETH.png')
xrp_path=os.path.join(full_path+r'\resources\XRP.png')
xmr_path=os.path.join(full_path+r'\resources\XMR.png')
doge_path=os.path.join(full_path+r'\resources\DOGE.png')
usd_path=os.path.join(full_path+r'\resources\USD.png')
eur_path=os.path.join(full_path+r'\resources\EUR.png')
ron_path=os.path.join(full_path+r'\resources\RON.png')
pop_path=os.path.join(full_path+r'\resources\pop.png')
arrow_path=os.path.join(full_path+r'\resources\arrow.png')


def load_image(path):
    pop_file=open(path,"rb")
    pop_i=PIL.Image.open(pop_file)
    pop_img=PIL.ImageTk.PhotoImage(pop_i)
    return pop_img

#============================================================================================
#                                      LOGIN  WINDOW
#============================================================================================

def Login_Window():
    global login
    login=Tk()
    # login.overrideredirect(True)
    login.focus_force()
    icon_path=os.path.join(full_path+r'\resources\money.ico')
    login.iconbitmap(icon_path)
    login.title("Bank System")
    width=500
    height=325
    screen_width=login.winfo_screenwidth()
    screen_height=login.winfo_screenheight()
    x=(screen_width/2)-(width/2)
    y=(screen_height/2)-(height/2)
    login.geometry("%dx%d+%d+%d" % (width,height,x,y))
    login.resizable(0,0)
    login.bind('<Escape>',quit)

    global USERNAME,PASSWORD
    USERNAME=StringVar()
    PASSWORD=StringVar()

    #frames
    Top=Frame(login,bd=2,relief=RIDGE,bg="#cccccc")
    Top.pack(side=TOP,fill=X)
    Form=Frame(login,height=200)
    Form.pack(side=TOP,pady=20)

    #labels
    lbl_title=Label(Top,text="Login",font=('arial',15),bg="#cccccc")
    lbl_title.pack(fill=X)
    lbl_username=Label(Form,text="Username:",font=('arial',14),bd=15)
    lbl_username.grid(row=0,sticky="e")
    lbl_password=Label(Form,text="Password:",font=('arial',14),bd=15)
    lbl_password.grid(row=1,sticky="e")
    global lbl_text
    lbl_text=Label(Form,font=('arial',10))
    lbl_text.grid(row=2,columnspan=2,pady=5)

    #entry widgets
    global username,password
    username=Entry(Form,textvariable=USERNAME,font=(14))
    username.grid(row=0,column=1)
    username.focus_force()
    password=Entry(Form,textvariable=PASSWORD,show="*",font=(14))
    password.grid(row=1,column=1)
    username.bind('<Return>',pass_focus)

    #buttons
    btn_login=Button(Form,text="Login",bg="#cccccc",font=('arial',15),width=25,command=Login)
    btn_login.grid(row=3,columnspan=2)
    btn_login.bind('<Return>',Login)
    btn_register=Button(Form,text="Register",bg="#cccccc",font=('arial',15),width=25,command=Register)
    btn_register.grid(row=4,columnspan=2,pady=10)
    btn_register.bind('<Return>',Register)

    login.mainloop()

def quit(event=None):
    login.destroy()

def pass_focus(event=None):
    password.focus_set()
    return("break")

def Register(event=None):
    global conn,cursor
    conn=sqlite3.connect("bank.db")
    cursor=conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS `member` (mem_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,username TEXT,password TEXT,btc_value REAL,eth_value REAL,xrp_value REAL,xmr_value REAL,doge_value REAL,usd_value REAL,eur_value REAL,ron_value REAL)")

    if USERNAME.get()=="" or PASSWORD.get()=="":
        lbl_text.config(text="Please complete the required field!",fg="red")
        USERNAME.set("")
        PASSWORD.set("")
    else:
        cursor.execute("SELECT * FROM `member` WHERE `username`=? AND `password`=?",(USERNAME.get(),PASSWORD.get()))
        if cursor.fetchone() is None:
            cursor.execute("INSERT INTO `member` (username,password,btc_value,eth_value,xrp_value,xmr_value,doge_value,usd_value,eur_value,ron_value) VALUES (?,?,0,0,0,0,0,0,0,0)",(USERNAME.get(),PASSWORD.get()))
            conn.commit()
            lbl_text.config(text="Registration complete!",fg="green")
            # USERNAME.set("")
            PASSWORD.set("")
            password.focus_force()
        else:
            lbl_text.config(text="This user already exists!",fg="red")
            USERNAME.set("")
            PASSWORD.set("")
            username.focus_force()
    cursor.close()
    conn.close()

def Login(event=None):
    global conn,cursor
    conn=sqlite3.connect("bank.db")
    cursor=conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS `member` (mem_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,username TEXT,password TEXT,btc_value REAL,eth_value REAL,xrp_value REAL,xmr_value REAL,doge_value REAL,usd_value REAL,eur_value REAL,ron_value REAL)")
    if USERNAME.get()=="" or PASSWORD.get()=="":
        lbl_text.config(text="Please complete the required field!",fg="red")
    else:
        cursor.execute("SELECT * FROM `member` WHERE `username`=? AND `password`=?",(USERNAME.get(),PASSWORD.get()))
        if cursor.fetchone() is not None:
            login.withdraw()
            Home_Window()
            PASSWORD.set("")
            lbl_text.config(text="")
        else:
            lbl_text.config(text="Invalid username or password",fg="red")
            USERNAME.set("")
            PASSWORD.set("")
            username.focus_force()
    cursor.close()
    conn.close()

#============================================================================================
#                                       HOME  WINDOW
#============================================================================================

def logout(event=None):
    home.destroy()
    login.deiconify()
    pass_focus()
    PASSWORD.set("")
    lbl_text.config(text="")

def home_quit(event=None):
    global wallet_popped,calc_popped
    global wallet,calc,home
    if wallet_popped==True:
        wallet.destroy()
    if calc_popped==True:
        calc.destroy()
    home.destroy()
    login.destroy()

def update_deposit():
    global conn,cursor,deposit,deposit_value
    conn1=sqlite3.connect("bank.db")
    cursor1=conn1.cursor()

    if deposit.get()=="BTC":
        cursor1.execute("UPDATE `member` SET `btc_value`=? WHERE `username`=?",(deposit_value.get(),USERNAME.get(),))
    elif deposit.get()=="ETH":
        cursor1.execute("UPDATE `member` SET `eth_value`=? WHERE `username`=?",(deposit_value.get(),USERNAME.get(),))
    elif deposit.get()=="XRP":
        cursor1.execute("UPDATE `member` SET `xrp_value`=? WHERE `username`=?",(deposit_value.get(),USERNAME.get(),))
    elif deposit.get()=="XMR":
        cursor1.execute("UPDATE `member` SET `xmr_value`=? WHERE `username`=?",(deposit_value.get(),USERNAME.get(),))
    elif deposit.get()=="DOGE":
        cursor1.execute("UPDATE `member` SET `doge_value`=? WHERE `username`=?",(deposit_value.get(),USERNAME.get(),))
    elif deposit.get()=="EUR":
        cursor1.execute("UPDATE `member` SET `eur_value`=? WHERE `username`=?",(deposit_value.get(),USERNAME.get(),))
    elif deposit.get()=="USD":
        cursor1.execute("UPDATE `member` SET `usd_value`=? WHERE `username`=?",(deposit_value.get(),USERNAME.get(),))
    elif deposit.get()=="RON":
        cursor1.execute("UPDATE `member` SET `ron_value`=? WHERE `username`=?",(deposit_value.get(),USERNAME.get(),))

# add actual deposit using get_balance() function

    conn1.commit()
    cursor1.close()
    conn1.close()

def home_update(event=None):
    global home_currency1_value,home_currency1,home_currency2,home_currency2_value,home_text_label
    if home_currency1.get!='???' and home_currency2.get()!='???':
        home_text_label.config(text="")
        home_update_conversion()
    else:
        home_currency2_value.set("")
        home_text_label.config(text="Please complete the required fields!",fg="red")

def home_update_conversion(*args):
    global home_currency1_value,home_currency2_value,home_currency1,home_currency2,home_text_label
    if home_currency1.get()==home_currency2.get():
        home_currency2_value.set("")
        home_text_label.config(text="You can't exchange between the same currency!",fg="red")
    elif home_currency2.get()=="???" or bool(re.search(r'\d', home_currency1_value.get())) or home_currency1.get()=="???":
        if home_currency1.get()!="USD":
            cur1=home_currency1.get()
            value1=float(home_currency1_value.get())
            if cur1=="BTC":
                value1*=from_btc_price
            elif cur1=="ETH":
                value1*=from_eth_price
            elif cur1=="XRP":
                value1*=from_xrp_price
            elif cur1=="XMR":
                value1*=from_xmr_price
            elif cur1=="DOGE":
                value1*=from_doge_price
            elif cur1=="EUR":
                value1*=from_eur_price
            elif cur1=="RON":
                value1*=from_ron_price

            cur2=home_currency2.get()
            value2=value1
            if cur2=="BTC":
                value2*=to_btc_price
            elif cur2=="ETH":
                value2*=to_eth_price
            elif cur2=="XRP":
                value2*=to_xrp_price
            elif cur2=="XMR":
                value2*=to_xmr_price
            elif cur2=="DOGE":
                value2*=to_doge_price
            elif cur2=="EUR":
                value2*=to_eur_price
            elif cur2=="RON":
                value2*=to_ron_price

        else:
            value1=float(home_currency1_value.get())
            cur2=home_currency2.get()
            value2=value1
            if cur2=="BTC":
                value2*=to_btc_price
            elif cur2=="ETH":
                value2*=to_eth_price
            elif cur2=="XRP":
                value2*=to_xrp_price
            elif cur2=="XMR":
                value2*=to_xmr_price
            elif cur2=="DOGE":
                value2*=to_doge_price
            elif cur2=="EUR":
                value2*=to_eur_price
            elif cur2=="RON":
                value2*=to_ron_price


        home_text_label.config(text="A 5% converion fee ({fee}) has been taken from the total!".format(fee=5*value2/100),fg="black")
        value2-=5*value2/100
        home_currency2_value.set(value2)
    else:
        home_currency2_value.set("")
        home_text_label.config(text="Please complete the required fields!",fg="red")


def Home_Window():
    global home
    home=Toplevel()
    home.protocol("WM_DELETE_WINDOW",home_quit)
    # home.overrideredirect(True)  ELIMINA BARA DE SUS
    home.focus_force()
    icon_path=os.path.join(full_path+r'\resources\money.ico')
    home.title("Dashboard")
    home.iconbitmap(icon_path)
    global home_width,home_height
    home_width=700
    home_height=500
    screen_width=home.winfo_screenwidth()
    screen_height=home.winfo_screenheight()
    x=(screen_width/2)-(home_width/2)
    y=(screen_height/2)-(home_height/2)
    home.geometry("%dx%d+%d+%d" % (home_width,home_height,x,y))
    home.bind("<Escape>",home_quit)
    home.resizable(0,0)

    # FRAMES
    Top=Frame(home,bd=2,relief=RIDGE,background="#cccccc")
    Top.pack(side=TOP,fill=X)
    sep=ttk.Separator(home,orient="horizontal")
    sep.pack(side=TOP,fill=X)
    Top2=Frame(home,bd=25)
    Top2.pack(side=TOP)
    Top3=Frame(home,bd=25)
    Top3.pack(side=TOP)
    Top4=Frame(home,bd=25)
    Top4.pack(side=TOP)
    home_label_frame=Frame(home,bd=2)
    home_label_frame.pack(side=TOP)

    # TOP WIDGETS
    lbl_title=Label(Top,text="Welcome %s!"%(USERNAME.get()),font=('arial',15),bg="#cccccc")
    lbl_title.pack(side=LEFT)
    logout_button=Button(Top,text="Logout",bg="#bdbdbd",font=('arial',15),command=logout)#.pack(side='right')
    logout_button.pack(side=RIGHT)
    logout_button.bind("<Return>",logout)

    # MAIN BUTTONS
    wallet_button=Button(Top2,text="Wallet",bg="#cccccc",width=10,font=('arial',20),command=open_wallet)
    wallet_button.pack(side=LEFT)
    wallet_button.bind("<Return>",open_wallet)

    wallet_pop_button_image=load_image(pop_path)
    wallet_pop_button=Button(Top2,image=wallet_pop_button_image,bg="#cccccc",width=50,height=50,command=pop_wallet)
    wallet_pop_button.image=wallet_pop_button_image
    wallet_pop_button.pack(side=LEFT,padx=(0,10))
    wallet_pop_button.bind("<Return>",pop_wallet)

    calc_button=Button(Top2,text="Calculator",bg="#cccccc",width=10,font=('arial',20),command=open_calc)
    calc_button.pack(side=LEFT)
    calc_button.bind("<Return>",open_calc)

    calc_pop_button_image=load_image(pop_path)
    calc_pop_button=Button(Top2,image=calc_pop_button_image,bg="#cccccc",width=50,height=50,command=pop_calc)
    calc_pop_button.image=calc_pop_button_image
    calc_pop_button.pack(side=LEFT)
    calc_pop_button.bind("<Return>",pop_calc)

    # deposit_label=Label(Top3,text="Deposit: ",font=('arial',15))
    # deposit_label.pack(side=LEFT)

    global deposit_value
    deposit_value=StringVar()
    deposit_entry=Entry(Top3,textvariable=deposit_value,font=('arial',20),width=15)
    deposit_entry.pack(side=LEFT)
    deposit_entry.bind("<Return>",update_deposit)

    global deposit
    deposit=StringVar()
    deposit_choices={'BTC','ETH','XRP','XMR','DOGE','USD','EUR','RON'}
    deposit.set('???')
    deposit_dropdown=OptionMenu(Top3,deposit,*deposit_choices)
    deposit_dropdown.config(font=('arial',15))
    deposit_dropdown.pack(side=LEFT)

    deposit_button=Button(Top3,text="Deposit",font=('arial',13),command=update_deposit)
    deposit_button.pack(side=LEFT)

    global home_currency1_value
    home_currency1_value=StringVar()
    home_currency1_entry=Entry(Top4,textvariable=home_currency1_value,font=('arial',19),width=10)
    home_currency1_entry.pack(side=LEFT)
    home_currency1_entry.bind("<Return>",calc_update)
    home_currency1_entry.focus_force()

    global home_currency1
    home_currency1=StringVar()
    home_currency1_choices={'BTC','ETH','XRP','XMR','DOGE','USD','EUR','RON'}
    home_currency1.set('???')
    home_currency1_dropdown=OptionMenu(Top4,home_currency1,*home_currency1_choices)
    home_currency1_dropdown.config(font=('arial',15))
    home_currency1_dropdown.pack(side=LEFT)
    home_currency1.trace('w',home_update_conversion)

    arrow_label_img=load_image(arrow_path)
    arrow_label=Label(Top4,image=arrow_label_img)
    arrow_label.image=arrow_label_img
    arrow_label.pack(side=LEFT)

    global home_currency2
    home_currency2=StringVar()
    home_currency2_choices={'BTC','ETH','XRP','XMR','DOGE','USD','EUR','RON'}
    home_currency2.set('???')
    home_currency2_dropdown=OptionMenu(Top4,home_currency2,*home_currency2_choices)
    home_currency2_dropdown.config(font=('arial',15))
    home_currency2_dropdown.pack(side=LEFT)
    home_currency2.trace('w',home_update_conversion)

    equals_button=Button(Top4,text="=",font=('arial',13),command=home_update_conversion)
    equals_button.pack(side=LEFT)

    global home_currency2_value
    home_currency2_value=StringVar()
    home_currency2_entry=Entry(Top4,textvariable=home_currency2_value,font=('arial',19),width=20)
    home_currency2_entry.pack(side=LEFT)

    global home_text_label
    home_text_label=Label(home_label_frame,text="",font=('arial',15))
    home_text_label.pack()

    # and crypto conversion (currency -> crypto and crypto -> crypto) + 5% conversion fee

#============================================================================================
#                                      WALLET  WINDOW
#============================================================================================


# GLOBALS
wallet_init=False
wallet_popped=False


# METHODS
def open_wallet(even=None):
    global wallet_popped,wallet_init
    if wallet_init==False or wallet_popped==False or wallet.state()!="normal":
        home.withdraw()
        wallet_init=True
        wallet_popped=False
        Wallet_Window(wallet_popped)

def pop_wallet(event=None):
    global wallet_popped,wallet_init
    if wallet_popped==False:
        if wallet_init==False:
            wallet_init=True
        wallet_popped=True
        Wallet_Window(wallet_popped)

def wallet_go_back(event=None):
    global wallet_popped
    wallet.destroy()
    if wallet_popped==True:
        wallet_popped=False
        home.focus_force()
    else:
        home.deiconify()

def get_balance():
    global conn,cursor
    conn=sqlite3.connect("bank.db")
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM `member` WHERE `username`=?",(USERNAME.get(),))
    return(cursor.fetchall())


# WINDOW
def Wallet_Window(wallet_popped):
    global wallet
    wallet=Toplevel()
    # wallet.overrideredirect(True) ELIMINA BARA DE SUS
    wallet.protocol("WM_DELETE_WINDOW", wallet_go_back)
    wallet.bind("<Escape>",wallet_go_back)
    wallet_width=300
    wallet_height=500
    screen_width=wallet.winfo_screenwidth()
    screen_height=wallet.winfo_screenheight()

    if wallet_popped==False:
        wallet.focus_force()
        x=(screen_width/2)-(wallet_width/2)
        y=(screen_height/2)-(wallet_height/2)
    else:
        home.focus_force()
        x=(screen_width/2)+370
        y=(screen_height/2)-(wallet_height/2)

    wallet.geometry("%dx%d+%d+%d" % (wallet_width,wallet_height,x,y))
    icon_path=os.path.join(full_path+r'\resources\wallet.ico')
    wallet.title("Wallet")
    wallet.iconbitmap(icon_path)
    wallet.resizable(0,0)

    top_wallet=Frame(wallet,bd=2,relief=RIDGE,background="#cccccc")
    top_wallet.pack(side=TOP,fill=X)
    sep=ttk.Separator(wallet,orient="horizontal")
    sep.pack(side=TOP,fill=X)
    form_grid=Frame(wallet,height=400)
    form_grid.pack(side=TOP,pady=10)

    back_button=Button(top_wallet,text="Back",font=('arial',15),width=5,bg="#bdbdbd",command=wallet_go_back)
    back_button.pack(side="right")
    back_button.bind("<Return>",wallet_go_back)
    lbl_title=Label(top_wallet,text="Your Wallet",font=('arial',20),bg="#cccccc")
    lbl_title.pack(side="right",padx=30)

    lbl_grid_img=Label(form_grid,text="Currency",font=('arial',20))
    lbl_grid_img.grid(row=0,column=0,columnspan=2,pady=5)
    lbl_grig_bal=Label(form_grid,text="  Balance",font=('arial',20))
    lbl_grig_bal.grid(row=0,column=2,columnspan=2,pady=5)

    btc_img=load_image(btc_path)
    lbl_img_btc=Label(form_grid,image=btc_img)
    lbl_img_btc.image=btc_img
    lbl_img_btc.grid(row=1,column=0,pady=5)

    eth_img=load_image(eth_path)
    lbl_img_eth=Label(form_grid,image=eth_img,pady=5)
    lbl_img_eth.image=eth_img
    lbl_img_eth.grid(row=2,column=0,pady=5)

    xrp_img=load_image(xrp_path)
    lbl_img_xrp=Label(form_grid,image=xrp_img,pady=5)
    lbl_img_xrp.image=xrp_img
    lbl_img_xrp.grid(row=3,column=0,pady=5)

    xmr_img=load_image(xmr_path)
    lbl_img_xmr=Label(form_grid,image=xmr_img,pady=5)
    lbl_img_xmr.image=xmr_img
    lbl_img_xmr.grid(row=4,column=0,pady=5)

    doge_img=load_image(doge_path)
    lbl_img_doge=Label(form_grid,image=doge_img,pady=5)
    lbl_img_doge.image=doge_img
    lbl_img_doge.grid(row=5,column=0,pady=5)

    usd_img=load_image(usd_path)
    lbl_img_usd=Label(form_grid,image=usd_img,pady=5)
    lbl_img_usd.image=usd_img
    lbl_img_usd.grid(row=6,column=0,pady=5)

    eur_img=load_image(eur_path)
    lbl_img_eur=Label(form_grid,image=eur_img,pady=5)
    lbl_img_eur.image=eur_img
    lbl_img_eur.grid(row=7,column=0,pady=5)

    ron_img=load_image(ron_path)
    lbl_img_ron=Label(form_grid,image=ron_img,pady=5)
    lbl_img_ron.image=ron_img
    lbl_img_ron.grid(row=8,column=0,pady=5)

    btc_lbl_text=Label(form_grid,text="BTC",font=('arial',15))
    eth_lbl_text=Label(form_grid,text="ETH",font=('arial',15))
    xrp_lbl_text=Label(form_grid,text="XRP",font=('arial',15))
    xmr_lbl_text=Label(form_grid,text="XMR",font=('arial',15))
    doge_lbl_text=Label(form_grid,text="DOGE",font=('arial',15))
    usd_lbl_text=Label(form_grid,text="USD",font=('arial',15))
    eur_lbl_text=Label(form_grid,text="EUR",font=('arial',15))
    ron_lbl_text=Label(form_grid,text="RON",font=('arial',15))
    btc_lbl_text.grid(row=1,column=1,pady=5)
    eth_lbl_text.grid(row=2,column=1,pady=5)
    xrp_lbl_text.grid(row=3,column=1,pady=5)
    xmr_lbl_text.grid(row=4,column=1,pady=5)
    doge_lbl_text.grid(row=5,column=1,pady=5)
    usd_lbl_text.grid(row=6,column=1,pady=5)
    eur_lbl_text.grid(row=7,column=1,pady=5)
    ron_lbl_text.grid(row=8,column=1,pady=5)

    values=get_balance()

    btc_lbl_bal=Label(form_grid,text=values[0][3],font=('arial',15))
    eth_lbl_bal=Label(form_grid,text=values[0][4],font=('arial',15))
    xrp_lbl_bal=Label(form_grid,text=values[0][5],font=('arial',15))
    xmr_lbl_bal=Label(form_grid,text=values[0][6],font=('arial',15))
    doge_lbl_bal=Label(form_grid,text=values[0][7],font=('arial',15))
    usd_lbl_val=Label(form_grid,text=values[0][8],font=('arial',15))
    eur_lbl_val=Label(form_grid,text=values[0][9],font=('arial',15))
    ron_lbl_val=Label(form_grid,text=values[0][10],font=('arial',15))
    btc_lbl_bal.grid(row=1,column=2,columnspan=2,pady=5)
    eth_lbl_bal.grid(row=2,column=2,columnspan=2,pady=5)
    xrp_lbl_bal.grid(row=3,column=2,columnspan=2,pady=5)
    xmr_lbl_bal.grid(row=4,column=2,columnspan=2,pady=5)
    doge_lbl_bal.grid(row=5,column=2,columnspan=2,pady=5)
    usd_lbl_val.grid(row=6,column=2,columnspan=2,pady=5)
    eur_lbl_val.grid(row=7,column=2,columnspan=2,pady=5)
    ron_lbl_val.grid(row=8,column=2,columnspan=2,pady=5)


#============================================================================================
#                                    CALCULATOR  WINDOW
#============================================================================================

# 1 CURRENCY = x USD
from_btc_price=18777.23
from_eth_price=567.52
from_xrp_price=0.519107
from_xmr_price=149.44
from_doge_price=0.003177
from_eur_price=1.21
from_ron_price=0.25

# 1 USD = x CURRENCY
to_btc_price=0.000052
to_eth_price=0.001739
to_xrp_price=1.97
to_xmr_price=0.00680120
to_doge_price=314.73683815
to_eur_price=0.825655
to_ron_price=4.02

calc_init=False
calc_popped=False

def open_calc(even=None):
    global calc_popped,calc_init
    if calc_init==False or calc_popped==False or calc.state()!="normal":
        home.withdraw()
        calc_init=True
        calc_popped=False
        Calculator_Window(calc_popped)

def pop_calc(event=None):
    global calc_popped,calc_init
    if calc_popped==False:
        if calc_init==False:
            calc_init=True
        calc_popped=True
        Calculator_Window(calc_popped)

def calc_go_back(even=None):
    global calc_popped,home,home_width,home_height
    calc.destroy()
    if calc_popped==True:
        calc_popped=False

        screen_width=home.winfo_screenwidth()
        screen_height=home.winfo_screenheight()
        x=(screen_width/2)-(home_width/2)
        y=(screen_height/2)-(home_height/2)
        home.geometry("%dx%d+%d+%d" % (home_width,home_height,x,y))

        home.focus_force()
    else:
        home.deiconify()

def Calculator_Window(calc_popped):
    global calc,home
    calc=Toplevel()
    calc.protocol("WM_DELETE_WINDOW", calc_go_back)
    calc.bind("<Escape>",calc_go_back)
    calc_width=700
    calc_height=200
    screen_width=calc.winfo_screenwidth()
    screen_height=calc.winfo_screenheight()

    if calc_popped==False:
        calc.focus_force()
        x=(screen_width/2)-(calc_width/2)
        y=(screen_height/2)-(calc_height/2)
        calc.geometry("%dx%d+%d+%d" % (calc_width,calc_height,x,y))
    else:
        global home_width,home_height
        home_x=(screen_width/2)-(home_width/2)
        home_y=(screen_height/2)
        diff=home_height/2+160
        home.geometry("%dx%d+%d+%d" % (home_width,home_height,home_x,home_y-diff))
        calc.focus_force()
        x=(screen_width/2)-(calc_width/2)
        y=(screen_height/2)+275
        calc.geometry("%dx%d+%d+%d" % (calc_width,calc_height,home_x,home_y+140))

    icon_path=os.path.join(full_path+r'\resources\calc.ico')
    calc.title("Conversion Calculator")
    calc.iconbitmap(icon_path)
    calc.resizable(0,0)

    top_calc=Frame(calc,bd=2,relief=RIDGE,background="#cccccc")
    top_calc.pack(side=TOP,fill=X)
    top2_calc=Frame(calc,bd=2)
    top2_calc.pack(side=TOP)
    label_frame=Frame(calc,bd=2)
    label_frame.pack(side=TOP)

    back_button=Button(top_calc,text="Back",font=('arial',15),width=5,bg="#bdbdbd",command=calc_go_back)
    back_button.pack(side="right")
    back_button.bind("<Return>",calc_go_back)

    global currency1_value
    currency1_value=StringVar()
    currency1_entry=Entry(top2_calc,textvariable=currency1_value,font=('arial',19),width=10)
    currency1_entry.pack(side=LEFT)
    currency1_entry.bind("<Return>",calc_update)
    currency1_entry.focus_force()

    global currency1
    currency1=StringVar()
    currency1_choices={'BTC','ETH','XRP','XMR','DOGE','USD','EUR','RON'}
    currency1.set('???')
    currency1_dropdown=OptionMenu(top2_calc,currency1,*currency1_choices)
    currency1_dropdown.config(font=('arial',15))
    currency1_dropdown.pack(side=LEFT)
    currency1.trace('w',calc_update_conversion)

    arrow_label_img=load_image(arrow_path)
    arrow_label=Label(top2_calc,image=arrow_label_img)
    arrow_label.image=arrow_label_img
    arrow_label.pack(side=LEFT)

    global currency2
    currency2=StringVar()
    currency2_choices={'BTC','ETH','XRP','XMR','DOGE','USD','EUR','RON'}
    currency2.set('???')
    currency2_dropdown=OptionMenu(top2_calc,currency2,*currency2_choices)
    currency2_dropdown.config(font=('arial',15))
    currency2_dropdown.pack(side=LEFT)
    currency2.trace('w',calc_update_conversion)

    equals_button=Button(top2_calc,text="=",font=('arial',13),command=calc_update)
    equals_button.pack(side=LEFT)

    global currency2_value
    currency2_value=StringVar()
    currency2_entry=Entry(top2_calc,textvariable=currency2_value,font=('arial',19),width=20)
    currency2_entry.pack(side=LEFT)

    global calc_text_label
    calc_text_label=Label(label_frame,text="",font=('arial',15))
    calc_text_label.pack()


def calc_update(event=None):
    global currency1_value,currency1,currency2,calc_text_label
    if currency1.get!='???' and currency2.get()!='???':
        calc_text_label.config(text="")
        calc_update_conversion()
    else:
        currency2_value.set("")
        calc_text_label.config(text="Please complete the required fields!",fg="red")

def calc_update_conversion(*args):
    global currency1_value,currency2_value,currency1,currency2
    if currency1.get()==currency2.get():
        currency2_value.set("")
        calc_text_label.config(text="You can't exchange between the same currency!",fg="red")
    elif currency2.get=="???" or bool(re.search(r'\d', currency1_value.get())) or currency1.get()=="???":
        if currency1.get()!="USD":
            cur1=currency1.get()
            value1=float(currency1_value.get())
            if cur1=="BTC":
                value1*=from_btc_price
            elif cur1=="ETH":
                value1*=from_eth_price
            elif cur1=="XRP":
                value1*=from_xrp_price
            elif cur1=="XMR":
                value1*=from_xmr_price
            elif cur1=="DOGE":
                value1*=from_doge_price
            elif cur1=="EUR":
                value1*=from_eur_price
            elif cur1=="RON":
                value1*=from_ron_price

            cur2=currency2.get()
            value2=value1
            if cur2=="BTC":
                value2*=to_btc_price
            elif cur2=="ETH":
                value2*=to_eth_price
            elif cur2=="XRP":
                value2*=to_xrp_price
            elif cur2=="XMR":
                value2*=to_xmr_price
            elif cur2=="DOGE":
                value2*=to_doge_price
            elif cur2=="EUR":
                value2*=to_eur_price
            elif cur2=="RON":
                value2*=to_ron_price

        else:
            value1=float(currency1_value.get())
            cur2=currency2.get()
            value2=value1
            if cur2=="BTC":
                value2*=to_btc_price
            elif cur2=="ETH":
                value2*=to_eth_price
            elif cur2=="XRP":
                value2*=to_xrp_price
            elif cur2=="XMR":
                value2*=to_xmr_price
            elif cur2=="DOGE":
                value2*=to_doge_price
            elif cur2=="EUR":
                value2*=to_eur_price
            elif cur2=="RON":
                value2*=to_ron_price


        calc_text_label.config(text="A 5% converion fee ({fee}) has been taken from the total!".format(fee=5*value2/100),fg="black")
        value2-=5*value2/100
        currency2_value.set(value2)
    else:
        currency2_value.set("")
        calc_text_label.config(text="Please complete the required fields!",fg="red")


Login_Window()
