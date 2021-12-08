from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sqlite3


class ResultClass:
    def __init__(self, root):
        
        self.root = root
        self.root.title('Student Result Management System')
        self.root.geometry('1280x480+80+170')
        self.root.config(bg='white')
        self.root.focus_force()

        # ======= title =========
        title=Label(self.root, text='Add Student Result', font=('goudy old style', 20, 'bold'), bg='orange', fg='#262626').place(x=10, y=15, width=1180, height=50)
        
        # ======== Variables ========
        self.var_roll = StringVar()
        self.var_name = StringVar()
        self.var_course = StringVar()
        self.var_marks = StringVar()
        self.var_full_marks = StringVar()
        self.roll_list = []
        self.fetch_roll()


        # ======== widgets ===========
        lbl_select= Label(self.root, text='Select Student', font=('goudy old style',20, 'bold'), bg='white').place(x=50, y=100)
        lbl_name = Label(self.root, text='Name', font=('goudy old style',20, 'bold'), bg='white').place(x=50, y=160)
        lbl_course= Label(self.root, text='Course', font=('goudy old style',20, 'bold'), bg='white').place(x=50, y=220)
        lbl_marks= Label(self.root, text='Marks Obtained', font=('goudy old style',20, 'bold'), bg='white').place(x=50, y=280)
        lbl_full_marks= Label(self.root, text='Full Marks', font=('goudy old style',20, 'bold'), bg='white').place(x=50, y=340)
        
        # ======== Entry Fields =======
        self.txt_student= ttk.Combobox(self.root, textvariable=self.var_roll, values=self.roll_list, font=('goudy old style',15, 'bold'), state='readonly', justify=CENTER)
        self.txt_student.place(x=280, y=100, width=200)
        self.txt_student.set('Select')
        txt_name= Entry(self.root, textvariable=self.var_name, state = 'readonly', font=('goudy old style',20, 'bold'), bg='lightyellow').place(x=280, y=160, width=320)
        txt_course= Entry(self.root, textvariable=self.var_course, state = 'readonly', font=('goudy old style',20, 'bold'), bg='lightyellow').place(x=280, y=220, width=320)
        txt_marks= Entry(self.root, textvariable=self.var_marks, font=('goudy old style',20, 'bold'), bg='lightyellow').place(x=280, y=280, width=320)
        txt_full_marks= Entry(self.root, textvariable=self.var_full_marks, font=('goudy old style',20, 'bold'), bg='lightyellow').place(x=280, y=340, width=320)
        
        # ========= Image ============
        self.bg_img = Image.open('images/result.jpg')
        self.bg_img = self.bg_img.resize((500, 300),Image.ANTIALIAS)
        self.bg_img = ImageTk.PhotoImage(self.bg_img)
        self.lbl_bg = Label(self.root, image=self.bg_img).place(x=650, y=100)
        

        # ======= Search Button ========
        btn_search = Button(self.root, command=self.search, text='Search', font=('goudy old style',15, 'bold'), bg='#2196f3', fg='white', cursor='hand2').place(x=500, y=100, width=100, height=28)
        
        # ======= Buttons ==========
        btn_add = Button(self.root, command=self.add, text='Submit', font=('times new roman',15 ), bg='lightgreen', activebackground='lightgreen', cursor='hand2').place(x=300, y=420, width=120, height=35)
        btn_clear = Button(self.root, command=self.clear, text='Clear', font=('times new roman',15 ), bg='lightgrey', activebackground='lightgrey', cursor='hand2').place(x=430, y=420, width=120, height=35)
    
    # ======= fetch course name from course table ===========
    def fetch_roll(self):
        con = sqlite3.connect(database = 'rms.db')
        cur = con.cursor()
        try:
            cur.execute('SELECT roll FROM student')
            rows = cur.fetchall()
            if (len(rows) > 0):
                for row in rows:
                    self.roll_list.append(row[0])
        except Exception as ex:
            messagebox.showerror('Error', f'Error due to {str(ex)}')
    
    # ======== Search ==========
    def search(self):
        con = sqlite3.connect(database = 'rms.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT name, course FROM student WHERE roll=?", (self.var_roll.get(),))
            row = cur.fetchone()
            if (row != None):
                self.var_name.set(row[0])
                self.var_course.set(row[1])
            else:
                messagebox.showerror('Error', 'No Record Found', parent=self.root)    
        except Exception as ex:
            messagebox.showerror('Error', f'Error due to {str(ex)}')
    
    # ======== Add Data ========
    def add(self):
        con = sqlite3.connect(database = 'rms.db')
        cur = con.cursor()
        try:
            if (self.var_name.get() == ""):
                messagebox.showerror('Error', 'Please First Search Student Roll Number', parent=self.root)
            else:
                cur.execute('SELECT * FROM result WHERE roll=? and course=?', (self.var_roll.get(), self.var_course.get(),))
                row = cur.fetchone()    
                if (row != None):
                    messagebox.showerror('Error', 'Result already Present', parent=self.root)
                else:
                    per = (int(self.var_marks.get())*100)/int(self.var_full_marks.get())
                    cur.execute('INSERT INTO result (roll, name, course, marks_ob, full_marks, per) VALUES(?, ?, ?, ?, ?, ?)', (
                        self.var_roll.get(),
                        self.var_name.get(),
                        self.var_course.get(),
                        self.var_marks.get(),
                        self.var_full_marks.get(), 
                        str(per)
                    ))
                    con.commit()
                    messagebox.showinfo('Success', 'Result Added Successfully', parent=self.root)       
        except Exception as ex:
            messagebox.showerror('Error', f'Error due to {str(ex)}')
    
    # ======== Clear Button =======
    def clear(self):
        self.var_roll.set('Select')
        self.var_name.set('')
        self.var_course.set('')
        self.var_marks.set('')
        self.var_full_marks.set('')
    


if __name__ == '__main__':
    root = Tk()
    obj = ResultClass(root)
    root.mainloop()
