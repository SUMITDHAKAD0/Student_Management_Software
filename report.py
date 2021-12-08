from tkinter import *
from tkinter import ttk, messagebox
#from PIL import Image, ImageTk
import sqlite3

class ReportClass:
    def __init__(self, root):
        
        self.root = root
        self.root.title('Student Result Management System')
        self.root.geometry('1280x480+80+170')
        self.root.config(bg='white')
        self.root.focus_force()
        
        # ======= title =========
        title=Label(self.root, text='View Student Results ', font=('goudy old style', 20, 'bold'), bg='orange', fg='white').place(x=10, y=15, width=1180, height=35)
        
        # ======== Variable =========
        self.var_search = StringVar()
        self.var_id = ''

        # ======== Search ===========
        lbl_search= Label(self.root, text='Search By Roll No.', font=('goudy old style',20, 'bold'), bg='white').place(x=280, y=100)
        txt_search= Entry(self.root, textvariable=self.var_search, font=('goudy old style',20), bg='lightyellow').place(x=520, y=100, width=150)
        btn_search = Button(self.root, command=self.search, text='Search', font=('goudy old style',15, 'bold'), bg='#03a9f4', fg='white', cursor='hand2').place(x=680, y=100, width=100, height=35)
        btn_clear = Button(self.root, command=self.clear,text='Clear', font=('goudy old style',15, 'bold'), bg='grey', fg='white', cursor='hand2').place(x=800, y=100, width=100, height=35)
        
        # ======== Result Labels ===========
        lbl_roll= Label(self.root, text='Roll No.', font=('goudy old style',15, 'bold'), bg='white',bd=2, relief=GROOVE).place(x=150, y=230, width=150, height=50)
        lbl_name = Label(self.root, text='Name', font=('goudy old style',15, 'bold'), bg='white',bd=2, relief=GROOVE).place(x=300, y=230, width=150, height=50)
        lbl_course= Label(self.root, text='Course', font=('goudy old style',15, 'bold'), bg='white',bd=2, relief=GROOVE).place(x=450, y=230, width=150, height=50)
        lbl_marks= Label(self.root, text='Marks Obtained', font=('goudy old style',15, 'bold'), bg='white',bd=2, relief=GROOVE).place(x=600, y=230, width=150, height=50)
        lbl_full_marks= Label(self.root, text='Total Marks', font=('goudy old style',15, 'bold'), bg='white',bd=2, relief=GROOVE).place(x=750, y=230, width=150, height=50)
        lbl_per= Label(self.root, text='Percentage', font=('goudy old style',15, 'bold'), bg='white',bd=2, relief=GROOVE).place(x=900, y=230, width=150, height=50)
        
        # ======== Entry Fields ===========
        self.roll= Label(self.root,  font=('goudy old style',15, 'bold'), bg='white',bd=2, relief=GROOVE)
        self.roll.place(x=150, y=280, width=150, height=50)
        self.name = Label(self.root,  font=('goudy old style',15, 'bold'), bg='white',bd=2, relief=GROOVE)
        self.name.place(x=300, y=280, width=150, height=50)
        self.course= Label(self.root,  font=('goudy old style',15, 'bold'), bg='white',bd=2, relief=GROOVE)
        self.course.place(x=450, y=280, width=150, height=50)
        self.marks= Label(self.root,  font=('goudy old style',15, 'bold'), bg='white',bd=2, relief=GROOVE)
        self.marks.place(x=600, y=280, width=150, height=50)
        self.full= Label(self.root,  font=('goudy old style',15, 'bold'), bg='white',bd=2, relief=GROOVE)
        self.full.place(x=750, y=280, width=150, height=50)
        self.per= Label(self.root,  font=('goudy old style',15, 'bold'), bg='white',bd=2, relief=GROOVE)
        self.per.place(x=900, y=280, width=150, height=50)

        # ======== Delete Button ========
        btn_delete = Button(self.root, command=self.delete, text='Delete', font=('goudy old style',15, 'bold'), bg='red', fg='white', cursor='hand2').place(x=520, y=350, width=150, height=35)
        
        # ======== Search ==========
    def search(self):
        con = sqlite3.connect(database = 'rms.db')
        cur = con.cursor()
        try:
            if (self.var_search.get() == ''):
                messagebox.showerror('Error', "Roll No. Should Required", parent=self.root)
            else:
                # print(self.var_search)
                cur.execute("select * from result where roll=?", (self.var_search.get(),))
                row = cur.fetchone()
                if row != None:
                    self.var_id = row[0]
                    self.roll.config(text=row[1])
                    self.name.config(text=row[2])
                    self.course.config(text=row[3])
                    self.marks.config(text=row[4])
                    self.full.config(text=row[5])
                    self.per.config(text=row[6])     
                else:
                    messagebox.showerror('Error', 'No Record Found', parent=self.root)    
        except Exception as ex:
            messagebox.showerror('Error', f'Error due to {str(ex)}')
    
    # ========= Delete Button =========
    def delete(self):
        con = sqlite3.connect(database = 'rms.db')
        cur = con.cursor()
        try:
            if (self.var_id == ""):
                messagebox.showerror('Error', 'Search Student Result First', parent=self.root)
            else:
                cur.execute('SELECT * FROM result WHERE rid =?', (self.var_id,))
                row = cur.fetchone()    
                if (row == None):
                    messagebox.showerror('Error', 'Invalid Student Result', parent=self.root)
                else:
                    op = messagebox.askyesno('Confirm', 'Do You Really Want to dalete?', parent=self.root)
                    if (op == True):
                        cur.execute('DELETE FROM result WHERE rid=?', (self.var_id,))
                        con.commit()
                        messagebox.showinfo('Delete', 'Result Daleted SuccessFully', parent=self.root)
                        self.clear()            
        except Exception as ex:
            messagebox.showerror('Error', f'Error due to {str(ex)}')
    

    # ======== Clear Button =======
    def clear(self):
        self.var_search.set('')
        self.var_id = ''
        self.roll.config(text='')
        self.name.config(text='')
        self.course.config(text='')
        self.marks.config(text='')
        self.full.config(text='')
        self.per.config(text='') 

               

if __name__ == '__main__':
    root = Tk()
    obj = ReportClass(root)
    root.mainloop()