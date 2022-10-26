from tkinter import *
import subprocess
import sqlite3
import sys
import os

root=Tk()
root.title("Python Simple Login App")
width=500
height=320
screen_width=root.winfo_screenwidth()
screen_height=root.winfo_screenheight()
x=(screen_width/2)-(width/2)
y=(screen_height/2)-(height/2)
root.geometry("%dx%d+%d+%d" % (width,height,x,y))
root.resizable(0,0)
exec=r"C:\Users\lynyx\AppData\Local\Programs\Python\Python38-32\pythonw.exe"
full_path=os.path.dirname(os.path.realpath(__file__))

#=========================METHODS=================================
def Register(event=None):
    global conn,cursor
    conn=sqlite3.connect("game_db.db")
    cursor=conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS `member` (mem_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,username TEXT,password TEXT)")
    if USERNAME.get()=="" or PASSWORD.get()=="":
        lbl_text.config(text="Please complete the required field!",fg="red")
        USERNAME.set("")
        PASSWORD.set("")
    else:
        cursor.execute("SELECT * FROM `member` WHERE `username`=? AND `password`=?",(USERNAME.get(),PASSWORD.get()))
        if cursor.fetchone() is None:
            cursor.execute("INSERT INTO `member` (username,password) VALUES (?,?)",(USERNAME.get(),PASSWORD.get()))
            conn.commit()
            lbl_text.config(text="Registration complete!",fg="green")
            USERNAME.set("")
            PASSWORD.set("")
        else:
            lbl_text.config(text="This user already exists!",fg="red")
            USERNAME.set("")
            PASSWORD.set("")
    cursor.close()
    conn.close()

def Login(event=None):
    global conn,cursor
    conn=sqlite3.connect("game_db.db")
    cursor=conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS `member` (mem_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,username TEXT,password TEXT)")
    if USERNAME.get()=="" or PASSWORD.get()=="":
        lbl_text.config(text="Please complete the required field!",fg="red")
    else:
        cursor.execute("SELECT * FROM `member` WHERE `username`=? AND `password`=?",(USERNAME.get(),PASSWORD.get()))
        if cursor.fetchone() is not None:
            HomeWindow()
            USERNAME.set("")
            PASSWORD.set("")
            lbl_text.config(text="")
        else:
            lbl_text.config(text="Invalid username or password",fg="red")
            USERNAME.set("")
            PASSWORD.set("")
    cursor.close()
    conn.close()

def start_dino():
    dino_path=os.path.join(full_path+"\dino.pyw")
    Home.withdraw()
    p=subprocess.run([exec, dino_path])
    if p is not None:
        Home.deiconify()

def start_snake():
    snake_path=os.path.join(full_path+"\snake.pyw")
    Home.withdraw()
    p=subprocess.run([exec, snake_path])
    if p is not None:
        Home.deiconify()

def start_hockey():
    hockey_path=os.path.join(full_path+"\hockey.pyw")
    Home.withdraw()
    p=subprocess.run([exec, hockey_path])
    if p is not None:
        Home.deiconify()

def HomeWindow():
    global Home
    root.withdraw()
    Home=Toplevel()
    Home.title("Welcome")
    width=600
    height=500
    screen_width=root.winfo_screenwidth()
    screen_height=root.winfo_screenheight()
    x=(screen_width/2)-(width/2)
    y=(screen_height/2)-(height/2)
    Home.resizable(0,0)
    Home.geometry("%dx%d+%d+%d" % (width,height,x,y))
    lbl_home=Label(Home,text="Successfull Login!",font=("%s 30 underline".format("Arial"))).pack()
    dino_btn_play=Button(Home,text="Play Dino Game",font=('comic sans ms',20),command=start_dino).pack(pady=25)
    snake_btn_play=Button(Home,text="Play Snake Game",font=('comic sans ms',20),command=start_snake).pack(pady=25)
    hockey_btn_play=Button(Home,text="Play Air Hockey",font=('comic sans ms',20),command=start_hockey).pack(pady=25)
    btn_back=Button(Home,text="Logout",font=('comic sans ms',20),command=Back).pack(pady=25)

def Back():
    Home.destroy()
    root.deiconify()

#variables
USERNAME=StringVar()
PASSWORD=StringVar()

#frames
Top=Frame(root,bd=2,relief=RIDGE)
Top.pack(side=TOP,fill=X)
Form=Frame(root,height=200)
Form.pack(side=TOP,pady=20)

#labels
lbl_title=Label(Top,text="Login App",font=('arial',15))
lbl_title.pack(fill=X)
lbl_username=Label(Form,text="Username:",font=('arial',14),bd=15)
lbl_username.grid(row=0,sticky="e")
lbl_password=Label(Form,text="Password:",font=('arial',14),bd=15)
lbl_password.grid(row=1,sticky="e")
lbl_text=Label(Form,font=('arial',10))
lbl_text.grid(row=2,columnspan=2,pady=5)

#entry widgets
username=Entry(Form,textvariable=USERNAME,font=(14))
username.grid(row=0,column=1)
password=Entry(Form,textvariable=PASSWORD,show="*",font=(14))
password.grid(row=1,column=1)

#buttons
btn_login=Button(Form,text="Login",font=('arial',15),width=25,command=Login)
btn_login.grid(row=3,columnspan=2)
btn_login.bind('<Return>',Login)
btn_register=Button(Form,text="Register",font=('arial',15),width=25,command=Register)
btn_register.grid(row=4,columnspan=2,pady=10)
btn_register.bind('<Return>',Register)

root.mainloop()
