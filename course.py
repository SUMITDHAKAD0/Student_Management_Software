from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sqlite3


class CourseClass:
    def __init__(self, root):
        
        self.root = root
        self.root.title('Student Result Management System')
        self.root.geometry('1280x480+80+170')
        self.root.config(bg='white')
        self.root.focus_force()
        
        # ======= title =========
        title=Label(self.root, text='Manage Course Details  ', font=('goudy old style', 20, 'bold'), bg='#033054', fg='white').place(x=10, y=15, width=1180, height=35)
        
        # ========= variables ==========
        self.var_course = StringVar()
        self.var_duration = StringVar()
        self.var_charges = StringVar()
        
        
        # ======== widgets ===========
        lbl_course= Label(self.root, text='Course Name', font=('goudy old style',15, 'bold'), bg='white').place(x=10, y=60)
        lbl_duration= Label(self.root, text='Duration', font=('goudy old style',15, 'bold'), bg='white').place(x=10, y=100)
        lbl_charges= Label(self.root, text='Charges', font=('goudy old style',15, 'bold'), bg='white').place(x=10, y=140)
        lbl_descripton= Label(self.root, text='Description', font=('goudy old style',15, 'bold'), bg='white').place(x=10, y=180)
        
        # ========= Entry fields =========
        self.txt_course= Entry(self.root, textvariable=self.var_course, font=('goudy old style',15, 'bold'), bg='lightyellow')
        self.txt_course.place(x=150, y=60, width=200)
        txt_duration= Entry(self.root, textvariable=self.var_duration, font=('goudy old style',15, 'bold'), bg='lightyellow').place(x=150, y=100, width=200)
        txt_charges= Entry(self.root, textvariable=self.var_charges, font=('goudy old style',15, 'bold'), bg='lightyellow').place(x=150, y=140, width=200)
        self.txt_descripton= Text(self.root, font=('goudy old style',15, 'bold'), bg='lightyellow')
        self.txt_descripton.place(x=150, y=180, width=500 , height=130 )
        
        # ======== Buttons ========
        self.btn_add = Button(self.root, text='Save', command=self.add, font=('goudy old style',15, 'bold'), bg='#2196f3', fg='white', cursor='hand2')
        self.btn_add.place(x=150, y=400, width=110, height=40)
        self.btn_update = Button(self.root, command=self.update, text='Update', font=('goudy old style',15, 'bold'), bg='#4caf50', fg='white', cursor='hand2')
        self.btn_update.place(x=270, y=400, width=110, height=40)
        self.btn_delete = Button(self.root, command=self.delete, text='Delete', font=('goudy old style',15, 'bold'), bg='#f44336', fg='white', cursor='hand2')
        self.btn_delete.place(x=390, y=400, width=110, height=40)
        self.btn_clear = Button(self.root, command=self.clear, text='Clear', font=('goudy old style',15, 'bold'), bg='#607d8b', fg='white', cursor='hand2')
        self.btn_clear.place(x=510, y=400, width=110, height=40)
        
        # ======== Serch Panel =========
        self.var_search = StringVar()
        lbl_search_courseName= Label(self.root, text='Course Name', font=('goudy old style',15, 'bold'), bg='white').place(x=720, y=60)
        txt_search_courseName= Entry(self.root, textvariable=self.var_search, font=('goudy old style',15, 'bold'), bg='lightyellow').place(x=870, y=60, width=180)
        btn_search = Button(self.root, command=self.search, text='Search', font=('goudy old style',15, 'bold'), bg='#2196f3', fg='white', cursor='hand2').place(x=1070, y=60, width=120, height=28)
        
        # ========= Content ========
        self.c_frame = Frame(self.root, bd=2, relief=RIDGE)
        self.c_frame.place(x=720, y=100, width=470, height=340)
        
        scrolly = Scrollbar(self.c_frame, orient=VERTICAL)
        scrollx = Scrollbar(self.c_frame, orient=HORIZONTAL)
        
        self.courseTable = ttk.Treeview(self.c_frame, columns=('cid', 'name', 'duration', 'charges', 'description'), xscrollcommand=scrollx.set, yscrollcommand=scrolly.set)
        
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT , fill=Y)
        scrollx.config(command=self.courseTable.xview)
        scrolly.config(command=self.courseTable.yview)
        
        self.courseTable.heading('cid', text='Course ID')
        self.courseTable.heading('name', text='Name')
        self.courseTable.heading('duration', text='Duration')
        self.courseTable.heading('charges', text='Charges')
        self.courseTable.heading('description', text='Description')
        self.courseTable['show'] = 'headings'
        self.courseTable.column('cid', width = 100)
        self.courseTable.column('name', width = 100)
        self.courseTable.column('duration', width = 100)
        self.courseTable.column('charges', width = 100)
        self.courseTable.column('description', width = 150)
        
        self.courseTable.pack(fill=BOTH, expand=1)
        
        self.courseTable.bind('<ButtonRelease-1>', self.get_data )
        self.show()
        
        
    # ========== database table access ==========
    def get_data(self, ev):
        self.txt_course.config(state = 'readonly')
        r = self.courseTable.focus()
        content = self.courseTable.item(r)
        row = content['values']
        #print(row)
        self.var_course.set(row[1])
        self.var_duration.set(row[2])
        self.var_charges.set(row[3])
        self.txt_descripton.delete('1.0', END)
        self.txt_descripton.insert(END, row[4])
        
    
    # ======== Clear Button =======
    def clear(self):
        self.show()
        self.var_course.set('')
        self.var_duration.set('')
        self.var_charges.set('')
        self.var_search.set('')
        self.txt_descripton.delete('1.0', END)
        self.txt_course.config(state = NORMAL)
        
    # ======== Save button =======
    def add(self):
        con = sqlite3.connect(database = 'rms.db')
        cur = con.cursor()
        try:
            if (self.var_course.get() == ""):
                messagebox.showerror('Error', 'Course name should be required', parent=self.root)
            else:
                cur.execute('SELECT * FROM course WHERE name =?', (self.var_course.get(),))
                row = cur.fetchone()    
                if (row != None):
                    messagebox.showerror('Error', 'Course name already Present', parent=self.root)
                else:
                    cur.execute('INSERT INTO course (name, duration, charges, description) VALUES(?, ?, ?, ?)', (
                        self.var_course.get(),
                        self.var_duration.get(),
                        self.var_charges.get(),
                        self.txt_descripton.get('1.0', END) 
                    ))
                    con.commit()
                    messagebox.showinfo('Success', 'Course Added Successfully', parent=self.root)
                    self.show()
                    
        except Exception as ex:
            messagebox.showerror('Error', f'Error due to {str(ex)}')
    
    # ========= Update Button =========
    def update(self):
        con = sqlite3.connect(database = 'rms.db')
        cur = con.cursor()
        try:
            if (self.var_course.get() == ""):
                messagebox.showerror('Error', 'Course name should be required', parent=self.root)
            else:
                cur.execute('SELECT * FROM course WHERE name =?', (self.var_course.get(),))
                row = cur.fetchone()    
                if (row == None):
                    messagebox.showerror('Error', 'Select Course From List', parent=self.root)
                else:
                    cur.execute('UPDATE course set duration=?, charges=?, description=? where name=?', (
                        self.var_duration.get(),
                        self.var_charges.get(),
                        self.txt_descripton.get('1.0', END),
                        self.var_course.get()
                    ))
                    con.commit()
                    messagebox.showinfo('Success', 'Course Update Successfully', parent=self.root)
                    self.show()
                    
        except Exception as ex:
            messagebox.showerror('Error', f'Error due to {str(ex)}')
    
    
    # ========= Delete Button =========
    def delete(self):
        con = sqlite3.connect(database = 'rms.db')
        cur = con.cursor()
        try:
            if (self.var_course.get() == ""):
                messagebox.showerror('Error', 'Course name should be required', parent=self.root)
            else:
                cur.execute('SELECT * FROM course WHERE name =?', (self.var_course.get(),))
                row = cur.fetchone()    
                if (row == None):
                    messagebox.showerror('Error', 'Please Select Course From the List First ', parent=self.root)
                else:
                    op = messagebox.askyesno('Confirm', 'Do You Really Want to dalete?', parent=self.root)
                    if (op == True):
                        cur.execute('DELETE FROM course WHERE name=?', (self.var_course.get(),))
                        con.commit()
                        messagebox.showinfo('Delete', 'Course Daleted SuccessFully', parent=self.root)
                        self.clear()
                    
        except Exception as ex:
            messagebox.showerror('Error', f'Error due to {str(ex)}')
    
        
    
    # ======== show data on table ==========
    def show(self):
        con = sqlite3.connect(database = 'rms.db')
        cur = con.cursor()
        try:
            cur.execute('SELECT * FROM course ')
            rows = cur.fetchall()
            self.courseTable.delete(*self.courseTable.get_children() )
            for row in rows:
                self.courseTable.insert('', END, values = row)
                        
        except Exception as ex:
            messagebox.showerror('Error', f'Error due to {str(ex)}')
    
        
    # ======== Search ==========
    def search(self):
        con = sqlite3.connect(database = 'rms.db')
        cur = con.cursor()
        try:
            cur.execute(f"SELECT * FROM course WHERE name LIKE '%{self.var_search.get()}%' ")
            rows = cur.fetchall()
            self.courseTable.delete(*self.courseTable.get_children() )
            for row in rows:
                self.courseTable.insert('', END, values = row)
                        
        except Exception as ex:
            messagebox.showerror('Error', f'Error due to {str(ex)}')
        
        
        
        
if __name__ == '__main__':
    root = Tk()
    obj = CourseClass(root)
    root.mainloop()