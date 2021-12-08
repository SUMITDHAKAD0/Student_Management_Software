from tkinter import * 
from tkinter import messagebox, ttk
from PIL import Image, ImageTk, ImageDraw
from datetime import *
import time
from math import *
#import pymysql
import sqlite3
import os

class Login_Window:
    def __init__(self, root):
        self.root = root
        self.root.title('Log In System')
        self.root.geometry('1350x700+0+0')
        self.root.config(bg='#021e2f')
        
        # ======= Title =======
        #title=Label(self.root, text='Python Analog Clock', font=('times new roman', 50, 'bold'), fg='white', bg='#04444a').place(x=0, y=50, relwidth=1)
        
        # ======== Bckground Colors ========
        
        left_lbl = Label(self.root, bg='#0BA3D2', bd=0)
        left_lbl.place(x=0, y=0, relheight=1, width=600)
        
        right_lbl = Label(self.root, bg='#031F3C', bd=0)
        right_lbl.place(x=600, y=0, relheight=1, relwidth=1)
        
        # ========== Frame =========
        
        login_frame = Frame(self.root, bg='white')
        login_frame.place(x=250, y=100, width=800, height=500)
    
        title=Label(login_frame, text='LOGIN HERE', font=('times new roman', 30, 'bold'), bg='white', fg='#08A3D2').place(x=250, y=50)
        
        email = Label(login_frame, text='EMAIl ADDRESS', font=('times new roman', 18, 'bold'), bg='white', fg='grey').place(x=250, y=150)
        self.txt_email = Entry(login_frame, font=('times new roman', 15), bg='lightgrey')
        self.txt_email.place(x=250, y=180, width=350, height = 35)
        
        password = Label(login_frame, text='PASSWORD', font=('times new roman', 18, 'bold'), bg='white', fg='grey').place(x=250, y=250)
        self.txt_password = Entry(login_frame, font=('times new roman', 15), bg='lightgrey')
        self.txt_password.place(x=250, y=280, width=350, height = 35)
        
        btn_register = Button(login_frame, command=self.register_window, text='Create New Account', font=('times new roman', 14), bg='white', fg='#B00857', bd=0, cursor='hand2').place(x=250, y=320)
        
        btn_forget = Button(login_frame, command=self.forget_password_window,  text='Forget Password', font=('times new roman', 14), bg='white', fg='red', bd=0, cursor='hand2').place(x=450, y=320)
        
        btn_login = Button(login_frame, command=self.login, text='Log In', font=('times new roman', 20, 'bold'), fg='white', bg='#B00857', cursor='hand2').place(x=250, y=380, width=150, height=40)
         
        # ========== Clock =========
        
        self.lbl = Label(self.root, text='\nAnalog Clock', compound=BOTTOM, font=('Book Antique', 25, 'bold'), bg='#081923', fg='white', bd=0)
        self.lbl.place(x=90, y=120, height=450, width=350)
        self.working()
        
    def clock_image(self, hr, min_, sec_, ):
        # RGB, (height, width), (color scale of 255(white))
        clock = Image.new('RGB', (400, 400), (8, 25, 35))
        draw = ImageDraw.Draw(clock)

        # ==== For clock Image ======
        bg = Image.open('images/c.png')
        bg = bg.resize((300, 300), Image.ANTIALIAS)
        clock.paste(bg, (50, 50))
        
        # ==== Hour line image ===
        origin = 200, 200
        # === origin x1, y1, x2, y2
        draw.line((origin, 200+50*sin(radians(hr)), 200-50*cos(radians(hr))), fill='#DF005E', width=4)
        # ==== Minute line image ===
        draw.line((origin, 200+80*sin(radians(min_)), 200-80*cos(radians(min_))), fill='white', width=3)
        # ==== Second line image ===
        draw.line((origin, 200+100*sin(radians(sec_)), 200-100*cos(radians(sec_))), fill='yellow', width=2)
        draw.ellipse((195, 195, 210, 210), fill='#1AD5D5')
        clock.save('images/clock_new.png')
        
    def working(self):
        h = datetime.now().time().hour
        m = datetime.now().time().minute
        s = datetime.now().time().second
        
        hr = (h/12)*360
        min_ = (m/60)*360
        sec_ = (s/60)*360
        self.clock_image(hr, min_, sec_)
        self.img = ImageTk.PhotoImage(file='images/clock_new.png')
        self.lbl.config(image=self.img)
        self.lbl.after(200, self.working)
        
        
    # =========== database base work ==============
    def login(self):
        if (self.txt_email.get() == '' or self.txt_password.get() == ''):
            messagebox.showerror('Error', 'Username and Password must Required', parent=self.root)
        else:
            try:
                con = sqlite3.connect(database = 'rms.db')
                cur = con.cursor()
                cur.execute('SELECT * FROM emp WHERE email=? and password=?', (self.txt_email.get(), self.txt_password.get()))
                row = cur.fetchone()
                if (row == None):
                    messagebox.showerror('Error', 'Invalid Username or Password', parent=self.root)
                else:
                    messagebox.showinfo('Success', f'Welcome {self.txt_email.get()}', parent=self.root)
                    self.root.destroy()
                    os.system('python dashboard.py')
                con.close()
                
            except Exception as ex:
                print(ex)
                messagebox.showerror('Error', f'Error Due to : {str(ex)}', parent=self.root)
    
    # ========= Registration_Page ========
    def register_window(self):
        self.root.destroy()
        import Registration_Page
    
    # ======= clear all of forget window data =======
    def reset(self):
        self.cmb_quest.current(0)
        self.txt_answer.delete(0, END)
        self.txt_new_password.delete(0, END)
        self.txt_password.delete(0, END)
        self.txt_email.delete(0, END)

    def forget_password(self):
        if (self.cmb_quest.get()=='Select' or self.txt_answer.get()=='' or self.txt_new_password.get()==''):
            messagebox.showerror('Error', 'All Fields are Required', parent=self.root2)
        else:
            try:
                con = sqlite3.connect(database = 'rms.db')
                cur = con.cursor()
                cur.execute('SELECT * FROM emp WHERE email=? and question=? and answer=? ', (self.txt_email.get(), self.cmb_quest.get(), self.txt_answer.get()))
                row = cur.fetchone()
                if (row == None):
                    messagebox.showerror('Error', 'Please Select Correct Security Question / Enter Correct Answer', parent=self.root2)
                else:
                    cur.execute('UPDATE  emp SET password=? WHERE email=? ', (self.txt_new_password.get(), self.txt_email.get()))
                    con.commit()
                    con.close()
                    messagebox.showinfo('Success', 'Password Updated Successfully', parent=self.root2)
                    self.reset()
                    self.root2.destroy()

            
            except Exception as ex:
                messagebox.showerror('Error', f'Error Due to : {str(ex)}', parent=self.root)
    





    # ========= forget password ========
    def forget_password_window(self):

        if (self.txt_email.get() == ''):
            messagebox.showerror('Error', 'Please Enter Your Email Address', parent=self.root)
        else:
            try:
                con = sqlite3.connect(database = 'rms.db')
                cur = con.cursor()
                cur.execute('SELECT * FROM emp WHERE email=?', (self.txt_email.get(),))
                row = cur.fetchone()
                if (row == None):
                    messagebox.showerror('Error', 'Please Enter Your Valied Email Address', parent=self.root)
                else:
                    con.close()
                    self.root2 = Toplevel()
                    self.root2.title('Forget Password')
                    self.root2.geometry('350x400+495+200')
                    self.root2.config(bg='white')
                    self.root2.focus_force()
                    self.root2.grab_set()

                    title=Label(self.root2, text='Forget Password', font=('times new roman', 20, 'bold'), fg='red', bg='white').place(x=0, y=10, relwidth=1)
                    
                    question = Label(self.root2, text='Security Question', font=('times new roman', 15, 'bold'), bg='white', fg='grey').place(x=50, y=80)
                    self.cmb_quest = ttk.Combobox(self.root2, font=('times new roman', 13), state='readonly', justify=CENTER)
                    self.cmb_quest['values'] = ('Select', 'Your Pet Name', 'your Birth Place', 'Your Best Friend Name')
                    self.cmb_quest.place(x=50, y=110, width=250)
                    self.cmb_quest.current(0)
                    
                    answer = Label(self.root2, text='Answer', font=('times new roman', 15, 'bold'), bg='white', fg='grey').place(x=50, y=160)
                    self.txt_answer = Entry(self.root2, font=('times new roman', 15), bg='lightgrey')
                    self.txt_answer.place(x=50, y=190, width=250)
                    
                    new_password = Label(self.root2, text='New Password', font=('times new roman', 15, 'bold'), bg='white', fg='grey').place(x=50, y=240)
                    self.txt_new_password = Entry(self.root2, font=('times new roman', 15), bg='lightgrey')
                    self.txt_new_password.place(x=50, y=270, width=250)
                    
                    btn_change_pass = Button(self.root2, command=self.forget_password, text='Change Password', font=('times new roman', 15, 'bold'), fg='white', bg='green', cursor='hand2').place(x=100, y=330, width=150, height=40)
                   
                
            except Exception as ex:
                print(ex)
                messagebox.showerror('Error', f'Error Due to : {str(ex)}', parent=self.root)
    
                
            
        
            
    
        
root = Tk()
obj = Login_Window(root)
root.mainloop()