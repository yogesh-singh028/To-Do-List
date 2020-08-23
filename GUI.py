# add button : Icons made by <a href="https://www.flaticon.com/authors/pixel-perfect" title="Pixel perfect">Pixel perfect</a> from <a href="https://www.flaticon.com/" title="Flaticon"> www.flaticon.com</a>
# delte buttton : Icons made by <a href="https://www.flaticon.com/authors/pixel-perfect" title="Pixel perfect">Pixel perfect</a> from <a href="https://www.flaticon.com/" title="Flaticon"> www.flaticon.com</a>

# GUI ...
# Import library ....
from tkinter import *
from tkinter import messagebox
import sqlite3
import threading


class ToDoList():
    def __init__(self,root):
        self.root = root
        self.root.protocol("WM_DELETE_WINDOW", self.callbackforroot)
        self.top_list_val = 0

        # frames ...

        frame_1 = Frame(self.root,bg='white',bd=4,relief=RIDGE) # #3333cc
        frame_1.place(x=10,y=20,height=330,width=290)
        # buttons ...
        delete_img = PhotoImage(file='remove.png')
        self.add_img = PhotoImage(file='add (1).png')
        self.delete_btn = Button(self.root,image=delete_img,command=self.call_delete_task,bg='#3333cc',relief=FLAT,activebackground='#3333cc')
        self.delete_btn.image=delete_img
        self.delete_btn.place(x=20,y=370)

        self.add_btn = Button(self.root, image=self.add_img, command=self.add_task_window, bg='#3333cc', relief=FLAT,
                                 activebackground='#3333cc')
        self.add_btn.image = self.add_img
        self.add_btn.place(x=220, y=370)

        # list box .....
        scrollbar = Scrollbar(frame_1)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.task_list = Listbox(frame_1,selectmode = SINGLE,height=20,font=('arial',12,'bold'),yscrollcommand = scrollbar.set)
        self.task_list.pack(fill=BOTH)
        scrollbar.config(command=self.task_list.yview)

        self.task_list.bind('<Double-1>',self.show_task)
        self.read_data()

        # functions ...

    def add_task_window(self):
        self.top_list_val +=1
        if self.top_list_val > 1 :
            pass
        else:
            self.root.update_idletasks()
            x, y = self.root.winfo_x(), self.root.winfo_y()
            x += 100;y += 200
            self.top = Toplevel(self.root)
            self.top.geometry('300x180+{}+{}'.format(x,y))
            self.top.title(" Add Task ")
            self.top.resizable(0,0)
            self.top.configure(bg='#3333cc')
            self.top.protocol("WM_DELETE_WINDOW", self.callbackForTop)
            # widgets .....
            Label(self.top,text='Enter Task :',font=('arial',13,'bold' ),fg='#3333cc',bg='white').place(x=10,y=20)

            self.task_title = Text(self.top,width=18,font=('times',13))
            self.task_title.place(x=120,y=20,height=110)
            self.task_title.focus_set()
            #self.task_title.bind('<Return>',self.add_task)
            add_btn = Button(self.top, image=self.add_img, command=self.call_add_task, bg='#3333cc', relief=FLAT,
                                  activebackground='#3333cc')
            add_btn.image = self.add_img
            add_btn.place(x=20, y=60)
            self.top.mainloop()


    def delete_task(self):
        id = self.task_list.get(ACTIVE)
        conn = sqlite3.connect('ToDoList.db')
        try:
            delete_query = "DELETE from TaskData1 where Task = '{}'".format(id)
            conn.execute(delete_query)
        except Exception as e:
            self.toast("Error :{}".format(e))
        else:
            self.task_list.delete(ACTIVE)

        conn.commit()
        conn.close()


    def add_task(self, *args):
        # self.clear entries ...

        if self.task_title.get(0.0,END) == '':
            pass
        else:
            conn = sqlite3.connect('ToDoList.db')
            try:
                data = str(self.task_title.get(0.0, END))
                insert_query = 'INSERT INTO TaskData1 (Task) VALUES("{}")'.format(data)
                conn.execute(insert_query)

            except Exception as e:
                self.toast("Error :{}".format(e))
            else:
                #self.toast("Task is Added")
                self.task_list.insert(END,data)
                self.task_title.delete(1.0,END)

            conn.commit()
            conn.close()


    def show_task(self, *args):
        val = self.task_list.get(ACTIVE)
        if val == '':
            pass
        else:
            messagebox.showinfo('Task is',val)


    def callbackForTop(self):
        self.top.destroy()
        self.top_list_val = 0


    def callbackforroot(self):
        if messagebox.askokcancel("Quit", "Do you really wish to quit?"):
            self.root.destroy()

    def read_data(self):
        self.database_creation()

        conn = sqlite3.connect('ToDoList.db')
        try:
            data = conn.execute("SELECT * from TaskData1")
            data = data.fetchall()
            self.task_list.delete(0,END)
            #print(data)
            for d in data:
                #print(d[0])
                self.task_list.insert(END,d[0])
        except Exception as e:
            self.toast("Error :{}".format(e))
        conn.commit()
        conn.close()


    def toast(self,msg = 'hello and welcome'):
        self.root.update_idletasks()
        x,y = self.root.winfo_x(),self.root.winfo_y()
        self.tw = Toplevel(self.root)
        x +=100 ; y+=360
        self.tw.wm_geometry("+%d+%d" % (x, y))
        self.tw.wm_overrideredirect(True)
        self.tw.configure(bg='gray')
        # adding widget..
        lbl = Label(self.tw,text=msg,justify='left',background="#ffffff", relief='solid', borderwidth=1,
                       wraplength = 180)
        lbl.pack(ipadx=10)
        lbl.after(1000,self.tw.destroy)
        self.tw.mainloop()

    # -------------- threading functions for better performance ..

    def call_add_task(self):
        x = threading.Thread(target=self.add_task)
        x.start()
        self.toast("Task is Added")


    def call_delete_task(self):
        x = threading.Thread(target=self.delete_task)
        x.start()
        self.toast("Task is Removed")

    def database_creation(self):
        conn = sqlite3.connect('ToDoList.db')
        try:
            # print("Opened database")
            conn.execute('CREATE TABLE  if not exists TaskData1 (Task TEXT)')
            # print("A database table has been created now")
        except Exception as e:
            pass
        conn.close()


if __name__ == '__main__':
    root = Tk()
    root.geometry('310x450+300+100')
    root.configure(bg='#3333cc')# #9999ff #3333cc
    root.resizable(0,0)
    root.title('To Do List')
    ToDoList(root)
    root.mainloop()