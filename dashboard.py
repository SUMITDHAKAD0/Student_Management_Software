from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw
from datetime import *
import time
import sqlite3
from math import *
import os
from course import CourseClass
from student import StudentClass
from result import ResultClass
from report import ReportClass


class RMS:
    def __init__(self, root):
        
        self.root = root
        self.root.title('Student Result Management System')
        self.root.geometry('1350x700+0+0')
        self.root.config(bg='white')
        
        # ======== icons =========
        
        self.logo_dash = ImageTk.PhotoImage(file='images/logo_p.png')
        
        
        # ======= title =========
        title=Label(self.root, image=self.logo_dash, text='Student Result Management System', padx=10, compound=LEFT, font=('goudy old style', 20, 'bold'), bg='#033054', fg='white').place(x=0, y=0, relwidth=1, height=50)
        
        # ========= Menu Fram========
        
        m_frame= LabelFrame(self.root, text='Menus', font=('times new roman',15, 'bold'), bg='white')
        m_frame.place(x=10, y=70, width=1400, height=80)
        
        btn_course = Button(m_frame, command=self.add_course,  text='Course', font=('goudy old style',15, 'bold'), bg='#0b5377', fg='white', cursor='hand2').place(x=20, y=5, width=200, height=40)
        btn_student = Button(m_frame, command=self.add_student, text='Student', font=('goudy old style',15, 'bold'), bg='#0b5377', fg='white', cursor='hand2').place(x=240, y=5, width=200, height=40)
        btn_result = Button(m_frame, command=self.add_result, text='Result', font=('goudy old style',15, 'bold'), bg='#0b5377', fg='white', cursor='hand2').place(x=460, y=5, width=200, height=40)
        btn_view = Button(m_frame, command=self.add_report, text='View Student Result', font=('goudy old style',15, 'bold'), bg='#0b5377', fg='white', cursor='hand2').place(x=680, y=5, width=200, height=40)
        btn_logout = Button(m_frame, command=self.logout, text='Logout', font=('goudy old style',15, 'bold'), bg='#0b5377', fg='white', cursor='hand2').place(x=900, y=5, width=200, height=40)
        btn_exit = Button(m_frame, command=self.exit_, text='Exit', font=('goudy old style',15, 'bold'), bg='#0b5377', fg='white', cursor='hand2').place(x=1120, y=5, width=200, height=40)
        
        
        # ========= Content Window ============
        self.bg_img = Image.open('images/bg.png')
        self.bg_img = self.bg_img.resize((920, 350),Image.ANTIALIAS)
        self.bg_img = ImageTk.PhotoImage(self.bg_img)
        self.lbl_bg = Label(self.root, image=self.bg_img).place(x=400, y=180, width=920, height=350)
        
        
        # ============ Update details =========
        self.lbl_course = Label(self.root, text='Total Course\n[ 0 ]', font=('goudy old style', 20), bd=10, relief=RIDGE, bg='#e43b06', fg='white')
        self.lbl_course.place(x=400, y=550, width=300, height=100)
        
        self.lbl_student = Label(self.root, text='Total Student\n[ 0 ]', font=('goudy old style', 20), bd=10, relief=RIDGE, bg='#0676ad', fg='white')
        self.lbl_student.place(x=710, y=550, width=300, height=100)
        
        self.lbl_result = Label(self.root, text='Total Result\n[ 0 ]', font=('goudy old style', 20), bd=10, relief=RIDGE, bg='#038074', fg='white')
        self.lbl_result.place(x=1020, y=550, width=300, height=100)
        
        # ======= Footer =========
        footer=Label(self.root, text='SRMS-Student Result Management System\nContact Us for any Technical Issue 96xxxxxx42', font=('goudy old style', 12), bg='#262626', fg='white').pack(side=BOTTOM, fill=X)
        self.update_details()

        # ========== Clock =========
        
        self.lbl = Label(self.root, text='\nAnalog Clock', compound=BOTTOM, font=('Book Antique', 25, 'bold'), bg='#081923', fg='white', bd=0)
        self.lbl.place(x=10, y=180, height=450, width=350)
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
    
    def update_details(self):
        con = sqlite3.connect(database = 'rms.db')
        cur = con.cursor()
        try:
            cur.execute('SELECT * FROM course ')
            cr = cur.fetchall()
            self.lbl_course.config(text=f'Total Courses\n [{str(len(cr))}]')

            cur.execute('SELECT * FROM student ')
            cr = cur.fetchall()
            self.lbl_student.config(text=f'Total Students\n [{str(len(cr))}]')

            cur.execute('SELECT * FROM result ')
            cr = cur.fetchall()
            self.lbl_result.config(text=f'Total Results\n [{str(len(cr))}]')

            self.lbl_course.after(200, self.update_details)          
        except Exception as ex:
            messagebox.showerror('Error', f'Error due to {str(ex)}')
        
        
    def add_course(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = CourseClass(self.new_win)
        
    def add_student(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = StudentClass(self.new_win)

    def add_result(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = ResultClass(self.new_win)
        
    def add_report(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = ReportClass(self.new_win)

    def logout(self):
        op = messagebox.askyesno('Confirm', 'Do You Really want to LogOut?', parent=self.root)
        if (op == True):
            self.root.destroy()
            os.system('python Login_Window.py')

    def exit_(self):
        op = messagebox.askyesno('Confirm', 'Do You Really want to EXIT?', parent=self.root)
        if (op == True):
            self.root.destroy()
            

if __name__ == '__main__':
    root = Tk()
    obj = RMS(root)
    root.mainloop()