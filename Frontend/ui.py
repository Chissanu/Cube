from tkinter import *
from tkinter.ttk import *
import tkinter as tk
import customtkinter
import os
from PIL import Image, ImageTk

CURRENT_PATH = os.getcwd()

class app:
    def __init__(self, master):
        self.master = master
        window_width = 1080
        window_height = 1920
        # get the screen dimension
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        # find the center point
        center_x = int(screen_width/2 - window_width / 2)
        center_y = int(screen_height/2 - window_height / 2)
        self.master.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        self.master.resizable(0, 0)
        self.master['bg'] = '#B9D6F2'
        self.main_menu()


    def login(self):  
        #   Setting up grid and frame for button widgets/ texts
        #   comment these out for now, as they messed with the alignment of widgets for tkinter
        # Grid.columnconfigure(root, index = 0, weight = 1)
        # Grid.rowconfigure(root, 0, weight = 1)

        for i in self.master.winfo_children():
            i.destroy()

        self.arrow_logo = customtkinter.CTkImage(Image.open("C:/Users/mrput/Documents/VSProject/Cuby/logostorage/material-symbols_arrow-back.png"), size=(50, 50))
        arrow_label = customtkinter.CTkButton(self.master, image=self.arrow_logo, text="", fg_color='#D9D9D9', command=self.main_menu)
        arrow_label.grid(row = 0, column = 0, sticky=tk.NW)


    def register(self):  
        #   Setting up grid and frame for button widgets/ texts
        #   comment these out for now, as they messed with the alignment of widgets for tkinter
        # Grid.columnconfigure(root, index = 0, weight = 1)
        # Grid.rowconfigure(root, 0, weight = 1)

        for i in self.master.winfo_children():
            i.destroy()

        self.arrow_logo = customtkinter.CTkImage(Image.open("Frontend\\logostorage\\material-symbols_arrow-back.png"), size=(50, 50))
        arrow_label = customtkinter.CTkButton(self.master, image=self.arrow_logo, text="", fg_color='#D9D9D9', command=self.main_menu)
        arrow_label.grid(row = 0, column = 0, sticky=tk.NW)
    
    
    def main_menu(self):
        #   Setting up grid and frame for button widgets/ texts
        Grid.columnconfigure(root,1,weight=1)
        Grid.rowconfigure(root,3,weight=1)
        Grid.rowconfigure(root,4,weight=1)

        for i in self.master.winfo_children():
            i.destroy()
        #   Title 
        tk.Label(self.master, text="Cube", font=("Inter", 64), bg='#B9D6F2').grid(column=1, row=0, sticky=tk.N, padx=1, pady=45)
        
        #   Cube logo
        self.imge = customtkinter.CTkImage(Image.open("Frontend\\logostorage\\vaadin_cube.png"), size=(220, 220))
        img_label = customtkinter.CTkLabel(self.master, text="", image=self.imge)
        img_label.grid(column=1, row=1)

        #   Menu texts/ three buttons: Login, Register, & Quit
        tk.Label(self.master, text="Welcome\nglad to see you!\n\n\n\n", font=("Inter", 25), bg='#B9D6F2').grid(column=1, row=2, padx=1, pady=10, rowspan=2, sticky=tk.N)

        bt1 = customtkinter.CTkButton(self.master, text="Login", font=("Inter", 35), corner_radius=20, text_color="#FFFFFF", fg_color='#051739', width=350, height=75, command=self.login)
        bt1.grid(column=1, row=2, rowspan=2, sticky=tk.S, pady=30)

        bt2 = customtkinter.CTkButton(self.master, text="Register", font=("Inter", 35), corner_radius=20, text_color="#FFFFFF", fg_color='#051739', width=350, height=75, command=self.register)
        bt2.grid(column=1, row=3, pady=100)

        bt3 = customtkinter.CTkButton(self.master, text="Quit", font=("Inter", 35), corner_radius=20, text_color="#000000", fg_color='#FFFFFF', width=250, height=75, command=root.destroy)
        bt3.grid(column=1, row=4)

if __name__ == '__main__':
    try:
        from ctypes import windll

        windll.shcore.SetProcessDpiAwareness(1)
    finally:
        root = Tk()
        root.attributes('-fullscreen', True)
        app(root)
        root.mainloop()
