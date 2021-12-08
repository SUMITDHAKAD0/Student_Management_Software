from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
#import pymysql
import sqlite3
import os

class Register:
    def __init__(self, root):
        self.root = root
        self.root.title('Registration Window')
        self.root.geometry('1350x700+0+0')
        self.root.config(bg='white')
        
        
        # ======== Background Image ========
        self.bg = ImageTk.PhotoImage(file = 'images/b2.jpg')
        bg = Label(self.root, image=self.bg).place(x=250, y=0, relwidth=1, relheight=1)
        
        # ======== Left Image ========
        self.left = ImageTk.PhotoImage(file = 'images/side.png')
        bg = Label(self.root, image=self.left).place(x=80, y=100, width=400, height=500)
        
        # ======== Register Frame ========
        frame1 = Frame(self.root, bg='white')
        frame1.place(x=480, y=100, width=700, height=500)
        
        title=Label(frame1, text='REGISTER HERE', font=('times new roman', 20, 'bold'), bg='white', fg='green').place(x=50, y=30)
        
        # ========= Widgets =========
        f_name = Label(frame1, text='First Name', font=('times new roman', 15, 'bold'), bg='white', fg='grey').place(x=50, y=100)
        self.txt_fname = Entry(frame1, font=('times new roman', 15), bg='lightgrey')
        self.txt_fname.place(x=50, y=130, width=250)
        
        l_name = Label(frame1, text='Last Name', font=('times new roman', 15, 'bold'), bg='white', fg='grey').place(x=370, y=100)
        self.txt_lname = Entry(frame1, font=('times new roman', 15), bg='lightgrey')
        self.txt_lname.place(x=370, y=130, width=250)
        
        contact = Label(frame1, text='Contact No.', font=('times new roman', 15, 'bold'), bg='white', fg='grey').place(x=50, y=170)
        self.txt_contact = Entry(frame1, font=('times new roman', 15), bg='lightgrey')
        self.txt_contact.place(x=50, y=200, width=250)
        
        email = Label(frame1, text='E-Mail', font=('times new roman', 15, 'bold'), bg='white', fg='grey').place(x=370, y=170)
        self.txt_email = Entry(frame1, font=('times new roman', 15), bg='lightgrey')
        self.txt_email.place(x=370, y=200, width=250)
        
        question = Label(frame1, text='Security Question', font=('times new roman', 15, 'bold'), bg='white', fg='grey').place(x=50, y=240)
        self.cmb_quest = ttk.Combobox(frame1, font=('times new roman', 13), state='readonly', justify=CENTER)
        self.cmb_quest['values'] = ('Select', 'Your Pet Name', 'your Birth Place', 'Your Best Friend Name')
        self.cmb_quest.place(x=50, y=270, width=250)
        self.cmb_quest.current(0)
        
        answer = Label(frame1, text='Answer', font=('times new roman', 15, 'bold'), bg='white', fg='grey').place(x=370, y=240)
        self.txt_answer = Entry(frame1, font=('times new roman', 15), bg='lightgrey')
        self.txt_answer.place(x=370, y=270, width=250)
        
        password = Label(frame1, text='Password', font=('times new roman', 15, 'bold'), bg='white', fg='grey').place(x=50, y=310)
        self.txt_password = Entry(frame1, font=('times new roman', 15), bg='lightgrey')
        self.txt_password.place(x=50, y=340, width=250)
        
        cpassword = Label(frame1, text='Confirm Password', font=('times new roman', 15, 'bold'), bg='white', fg='grey').place(x=370, y=310)
        self.txt_cpassword = Entry(frame1, font=('times new roman', 15), bg='lightgrey')
        self.txt_cpassword.place(x=370, y=340, width=250)
        
        # ====== Check Box ========
        self.var_check = IntVar()
        chk = Checkbutton(frame1, variable=self.var_check, text='I Agree The Terms & Condition', onvalue=1, offvalue=0, font=('times new roman', 12), bg='white').place(x=50, y=380)
        
        # ======== Button =========
        self.btn_img = ImageTk.PhotoImage(file = 'images/register.png')
        btn_register = Button(frame1, command=self.register_data, image=self.btn_img, bd=0, cursor='hand2').place(x=50, y=420)
        
        btn_login = Button(self.root, command=self.signin_window, text='Sign In', font=('times new roman', 20) , bd=0, cursor='hand2').place(x=195, y=460, width=180)
    
    # ========= Login_Page ========
    def signin_window(self):
        self.root.destroy()
        os.system('python Login_Window.py')
        
# ================ DataBase work ==============

    def clear(self):
        self.txt_fname.delete(0, END),
        self.txt_lname.delete(0, END),
        self.txt_contact.delete(0, END),
        self.txt_email.delete(0, END),
        self.cmb_quest.current(0),
        self.txt_answer.delete(0, END),
        self.txt_password.delete(0, END),
        self.txt_cpassword.delete(0, END)
        

    def register_data(self):
        if (self.txt_fname.get()=='' or self.txt_contact.get()=='' or self.txt_email.get()=='' or self.cmb_quest.get() == 'Select' or self.txt_answer.get()=='' or self.txt_password.get()=='' or self.txt_cpassword.get()==''):
            messagebox.showerror('Error', 'All Fields are Required', parent=self.root)
        
        elif (self.txt_password.get() != self.txt_cpassword.get()):
            messagebox.showerror('Error', 'Password And confirm Password are Different', parent=self.root)  
        elif(self.var_check.get() == 0):
            messagebox.showerror('Error', 'Agree our Terms & Condition', parent=self.root)  
        else:
            try:
                con = sqlite3.connect(database = 'rms.db')
                cur = con.cursor()
                cur.execute('select * from emp where email=?', (self.txt_email.get(),))
                row = cur.fetchone()
                print(row)
                if (row != None):
                    messagebox.showerror('Error', 'User Already Exist Try Another Email', parent=self.root)  
                else:
                    cur.execute('INSERT INTO emp (fname, lname, contact, email, question, answer, password) values(?,?,?,?,?,?,?)',
                                   (
                                       self.txt_fname.get(),
                                       self.txt_lname.get(),
                                       self.txt_contact.get(),
                                       self.txt_email.get(),
                                       self.cmb_quest.get(),
                                       self.txt_answer.get(),
                                       self.txt_password.get()   
                                   )
                               )
                    con.commit()
                    con.close()
                    messagebox.showinfo('Success', 'Register Successfull', parent=self.root)
                    self.clear()
                    self.signin_window()
            except Exception as ex:
                messagebox.showerror('Error', f'Error Due to : {str(ex)}', parent=self.root)
            
#             messagebox.showinfo('Success', 'Register Successfull', parent=self.root)
#              print(self.txt_fname.get(),
#              self.txt_lname.get(),
#              self.txt_contact.get(),
#              self.txt_email.get(),
#              self.cmb_quest.get(),
#              self.txt_answer.get(),
#              self.txt_password.get(),
#              self.txt_cpassword.get())
        
root = Tk()
obj = Register(root)
root.mainloop()