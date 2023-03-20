from tkinter import *
from tkinter import ttk

class app:
    def __init__(self, master):
        self.master = master
        self.master.geometry("400x400")
        self.login()
    
    def login(self):
        for i in self.master.winfo_children():
            i.destroy()
        self.frame1 = Frame(self.master, width=300, height=300)
        self.frame1.pack()
        self.reg_txt = ttk.Label(self.frame1, text='login')
        self.reg_txt.pack()
        
        # this will create a label widget
        self.l1 = ttk.Label(self.frame1, text = "First:")
        self.l2 = ttk.Label(self.frame1, text = "Second:")

        self.l1.pack()
        self.l1_label = Entry(self.frame1, bd=5)
        self.l1_label.pack()

        self.l2.pack()
        self.l2_label = Entry(self.frame1, bd=5, show='*')
        self.l2_label.pack()

        ttk.Label(self.frame1, text="").pack()
        self.register_btn = ttk.Button(self.frame1, text="Go to Register", command=self.register)
        self.register_btn.pack()

    
    def register(self):
        for i in self.master.winfo_children():
            i.destroy()
        self.frame2 = Frame(self.master, width=300, height=300)
        self.frame2.pack()
        self.reg_txt2 = ttk.Label(self.frame2, text='register')
        self.reg_txt2.pack()
        ttk.Label(self.frame2, text="").pack()
        self.login_btn = ttk.Button(self.frame2, text="Go to Login", command=self.login)
        self.login_btn.pack()

root = Tk()
app(root)
root.mainloop()