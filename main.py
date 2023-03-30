from tkinter import *
from tkinter.ttk import *
import tkinter as tk
import customtkinter
import os
from PIL import Image, ImageTk
from Libs.Database import Database

CURRENT_PATH = os.getcwd()

# color palatte
BG_COLOR = "#B9D6F2"
GENERAL_TEXT = "#000000"
GRAY = "#989898"
WHITE = "#FFFFFF"
BUTTON = "#061A40"
FRIEND_LIST = "#0353A4"

class app:
    def __init__(self, master):
        self.master = master
        window_width = 1080
        window_height = 1920
        master.bind('<Escape>',lambda e: quit(e))
        # get the screen dimension
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        
        self.db = Database()

        # find the center point
        center_x = int(screen_width/2 - window_width / 2)
        center_y = int(screen_height/2 - window_height / 2)
        self.master.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        self.master.resizable(0, 0)
        self.master['bg'] = BG_COLOR
        self.chat()
        # self.main_menu()

    def login(self):  
        """
        Setting up grid and frame for button widgets/ texts
        comment these out for now, as they messed with the alignment of widgets for tkinter
        Grid.columnconfigure(root, index = 0, weight = 1)
        Grid.rowconfigure(root, 0, weight = 1)
        """
        for i in self.master.winfo_children():
            i.destroy()
        # Arrow on top corner left
        self.arrow_logo = customtkinter.CTkImage(Image.open("logostorage\\material-symbols_arrow-back.png"), size=(50, 50))
        arrow_label = customtkinter.CTkButton(self.master, image=self.arrow_logo, text="", width=0, fg_color=BG_COLOR, command=self.main_menu)
        arrow_label.grid(row = 0, column = 0, padx=10, pady=10,sticky=tk.NW, columnspan=2)

        # Cube logo
        self.image = customtkinter.CTkImage(Image.open("logostorage\\vaadin_cube.png"), size=(180, 180))
        img_label = customtkinter.CTkLabel(self.master, text="", image=self.image)
        img_label.grid(column=1, row=0, pady=35)

        tk.Label(self.master, text="Login", font=("Inter", 40), bg= BG_COLOR).grid(column=1, row=1, pady=5, sticky=tk.N)

        # Insert text widget/ To add in sending data to firebase admin things after actual login attempt
        username_entry = customtkinter.CTkEntry(self.master, placeholder_text="Username", font=("Inter", 20), corner_radius=15, text_color=GENERAL_TEXT, fg_color=WHITE, width=500, height=60)
        username_entry.grid(column=1, row=2, sticky = N, pady=(50, 40))

        entry_2 = customtkinter.CTkEntry(self.master, placeholder_text="Password", show="*", font=("Inter", 20), corner_radius=15, text_color=GENERAL_TEXT, fg_color=WHITE, width=500, height=60)
        entry_2.grid(column=1, row=3, sticky = N)

        # Login button
        log_btn = customtkinter.CTkButton(self.master, text="Login", font=("Inter", 25), corner_radius=20, text_color=WHITE, fg_color=BUTTON, width=500, height=60, command=self.chat)
        log_btn.grid(column=1, row=4, sticky = "s", pady=(100,100))


    def register(self):  
        """
        Setting up grid and frame for button widgets/ texts
        comment these out for now, as they messed with the alignment of widgets for tkinter
        Grid.columnconfigure(root, index = 0, weight = 1)
        Grid.rowconfigure(root, 0, weight = 1)
        """

        for i in self.master.winfo_children():
            i.destroy()
        # Arrow on top corner left
        self.arrow_logo = customtkinter.CTkImage(Image.open("logostorage\\material-symbols_arrow-back.png"), size=(50, 50))
        arrow_label = customtkinter.CTkButton(self.master, image=self.arrow_logo, text="", width=0, fg_color=BG_COLOR, command=self.main_menu)
        arrow_label.grid(row = 0, column = 0, padx=10, pady=10, sticky=tk.NW, columnspan=2)
    
        # Cube logo
        self.image = customtkinter.CTkImage(Image.open("logostorage\\vaadin_cube.png"), size=(180, 180))
        img_label = customtkinter.CTkLabel(self.master, text="", image=self.image)
        img_label.grid(column=1, row=0, pady=35)

        tk.Label(self.master, text="Register", font=("Inter", 40), bg=BG_COLOR).grid(column=1, row=1, pady=5)

        # Insert text widget/ To add in sending data to firebase admin things after actual login attempt
        name_entry = customtkinter.CTkEntry(self.master, placeholder_text="Name", font=("Inter", 20), corner_radius=15, text_color=GENERAL_TEXT, fg_color=WHITE, width=500, height=60)
        name_entry.grid(column=1, row=2, pady=(50,20))

        username_entry = customtkinter.CTkEntry(self.master, placeholder_text="Username", font=("Inter", 20), corner_radius=15, text_color=GENERAL_TEXT, fg_color=WHITE, width=500, height=60)
        username_entry.grid(column=1, row=3)

        password_entry = customtkinter.CTkEntry(self.master, placeholder_text="Password", show="*", font=("Inter", 20), corner_radius=15, text_color=GENERAL_TEXT, fg_color=WHITE, width=500, height=60)
        password_entry.grid(column=1, row=4)

        confirm_entry = customtkinter.CTkEntry(self.master, placeholder_text="Confirm password", show="*", font=("Inter", 20), corner_radius=15, text_color=GENERAL_TEXT, fg_color=WHITE, width=500, height=60)
        confirm_entry.grid(column=1, row=5, pady=(15,0))
        
        #self.db.createAccount(username_entry,name_entry,password_entry)

        # Register button
        reg_btn = customtkinter.CTkButton(self.master, text="Register", font=("Inter", 25), corner_radius=20, text_color=WHITE, fg_color=BUTTON, width=500, height=60,
                                          command= lambda : self.registerDB(username_entry.get(),name_entry.get(),password_entry.get(),confirm_entry.get()))
        reg_btn.grid(column=1, row=6, sticky = "s", pady=(200,100))

    def chat(self):  
        # Setting up grid and frame for button widgets/ texts
        # comment these out for now, as they messed with the alignment of widgets for tkinter
        Grid.columnconfigure(root, index = 0, weight = 0)
        Grid.columnconfigure(root, index = 1, weight = 0)
        Grid.columnconfigure(root, index = 2, weight = 0)
        Grid.rowconfigure(root, 0, weight = 0)

        for i in self.master.winfo_children():
            i.destroy()

        # create sidebar
        sidebar_frame = customtkinter.CTkFrame(self.master, width=100, height=1080, corner_radius=0, fg_color=BUTTON)
        sidebar_frame.grid(row=0, column=0, sticky="nsew")

        chat_logo = customtkinter.CTkImage(Image.open("logostorage\Chat_selected.png"), size=(50, 50))
        chat_label = customtkinter.CTkLabel(sidebar_frame, image=chat_logo, text="")
        chat_label.grid(row = 0, column = 0, padx = 25, pady = (30, 25))

        addFriend_logo = customtkinter.CTkImage(Image.open("logostorage\AddFriend_btn.png"), size=(50, 50))
        addFriend_label = customtkinter.CTkButton(sidebar_frame, image=addFriend_logo, text="", width=50, fg_color=BUTTON, command=self.addFriend)
        addFriend_label.grid(row = 1, column = 0, padx = 25, pady = (30, 25))

        logout_logo = customtkinter.CTkImage(Image.open("logostorage\LogOut_btn.png"), size=(50, 50))
        logout_label = customtkinter.CTkButton(sidebar_frame, image=logout_logo, text="", width=50, fg_color=BUTTON, command=self.main_menu)
        logout_label.grid(row = 2, column = 0, padx = 25, pady = (665, 25))

        shutdown_logo = customtkinter.CTkImage(Image.open("logostorage\ShutDown_btn.png"), size=(50, 50))
        shutdown_label = customtkinter.CTkButton(sidebar_frame, image=shutdown_logo, text="", width=50, fg_color=BUTTON, command=root.destroy)
        shutdown_label.grid(row = 3, column = 0, padx = 25, pady = (30, 25))

        # create friendlist frame	
        friendList_frame = customtkinter.CTkScrollableFrame(self.master, width=450, height=1080, corner_radius=0, fg_color=FRIEND_LIST)	
        friendList_frame.grid(row=0, column=1, sticky="nsew")	
        friendListBtn = {
        "P'Oak": "P'Oak profile",
        "Putt": "Putt profile",
        "Most": "Most profile",
        "Ruj": "Ruj profile"
        }
        for i, button_name in enumerate(friendListBtn):	
            friendBtn = customtkinter.CTkButton(friendList_frame, 
                                                image=shutdown_logo, 
                                                text="  "+ button_name, 
                                                font=("Inter", 40), 
                                                anchor=W, 
                                                width=500, height=100, 
                                                fg_color=FRIEND_LIST, 
                                                command=lambda message=friendListBtn[button_name]: self.display_chat(message))	
            friendBtn.grid(row=i, column=0, sticky="nsew")	

        # create chat frame
        self.chat_frame = customtkinter.CTkFrame(self.master, width=1370, height=1080, corner_radius=0, fg_color=BG_COLOR)
        self.chat_frame.grid(row=0, column=2, sticky="nsew")

        # create topbar
        self.topbar_subframe = customtkinter.CTkFrame(self.chat_frame, width=1370, height=75, corner_radius=0, fg_color=WHITE)
        self.topbar_subframe.grid(row=0, column=0)
        self.topbar_subframe.grid_propagate(0)

        # create a message boxes container
        self.boxes_subframe = customtkinter.CTkFrame(self.chat_frame, width=1370, height=905, corner_radius=0, fg_color=BG_COLOR)
        self.boxes_subframe.grid(row=1, column=0)
        self.boxes_subframe.grid_propagate(0)

        # create chat box and emoji btn
        tool_subframe = customtkinter.CTkFrame(self.chat_frame, width=1370, height=100, corner_radius=0, fg_color=BG_COLOR)
        tool_subframe.grid(row=2, column=0)
        tool_subframe.grid_propagate(0)

        other_logo = customtkinter.CTkImage(Image.open("logostorage\Other_btn.png"), size=(40, 40))
        other_label = customtkinter.CTkButton(tool_subframe, image=other_logo, text="", width=0, height=0, fg_color=BG_COLOR, command=None)
        other_label.grid(row = 0, column = 0, padx = 30, pady = 30)

        chat_entry = customtkinter.CTkEntry(tool_subframe, placeholder_text="Type something", font=("Inter", 20), corner_radius=10, text_color=GENERAL_TEXT, fg_color=WHITE, width=1050, height=50)
        chat_entry.grid(row=0, column=1)

        sticker_logo = customtkinter.CTkImage(Image.open("logostorage\Sticker_btn.png"), size=(40, 40))
        sticker_label = customtkinter.CTkButton(tool_subframe, image=sticker_logo, text="", width=0, height=0, fg_color=BG_COLOR, command=None)
        sticker_label.grid(row = 0, column = 2, padx = 30, pady = 30)

        emoji_logo = customtkinter.CTkImage(Image.open("logostorage\Emoji_btn.png"), size=(40, 40))
        emoji_label = customtkinter.CTkButton(tool_subframe, image=emoji_logo, text="", width=0, height=0, fg_color=BG_COLOR, command=None)
        emoji_label.grid(row = 0, column = 3, padx = (0,30), pady = 30)

    # Function to display output message
    def display_chat(self, message):
        print(message)
        # create name in topbar
        for i in self.topbar_subframe.winfo_children():
            i.destroy()	
        name = customtkinter.CTkLabel(self.topbar_subframe, text=message, font=("Inter", 40), text_color=GENERAL_TEXT, anchor=W)	
        name.grid(row=0, column=0, pady = 15, padx=15, sticky=W)	

    def addFriend(self):

        Grid.columnconfigure(root,1,weight=1)

        for i in self.master.winfo_children():
            i.destroy()

        # create sidebar
        sidebar_frame = customtkinter.CTkFrame(self.master, width=100, height=1080, corner_radius=0, fg_color=BUTTON)
        sidebar_frame.grid(row=0, column=0, sticky="nsew")

        chat_logo = customtkinter.CTkImage(Image.open("logostorage\Chat_btn.png"), size=(50, 50))
        chat_label = customtkinter.CTkButton(sidebar_frame, image=chat_logo, text="", width=50, fg_color=BUTTON, command=self.chat)
        chat_label.grid(row = 0, column = 0, padx = 25, pady = (25, 25))

        addFriend_logo = customtkinter.CTkImage(Image.open("logostorage\AddFriend_selected.png"), size=(50, 50))
        addFriend_label = customtkinter.CTkLabel(sidebar_frame, image=addFriend_logo, text="")
        addFriend_label.grid(row = 1, column = 0, padx = 25, pady = (30, 25))

        logout_logo = customtkinter.CTkImage(Image.open("logostorage\LogOut_btn.png"), size=(50, 50))
        logout_label = customtkinter.CTkButton(sidebar_frame, image=logout_logo, text="", width=50, fg_color=BUTTON, command=self.main_menu)
        logout_label.grid(row = 2, column = 0, padx = 25, pady = (670, 25))

        shutDown_logo = customtkinter.CTkImage(Image.open("logostorage\ShutDown_btn.png"), size=(50, 50))
        shutDown_label = customtkinter.CTkButton(sidebar_frame, image=shutDown_logo, text="", width=50, fg_color=BUTTON, command=root.destroy)
        shutDown_label.grid(row = 3, column = 0, padx = 25, pady = (30, 30))

        # create addFriend frame
        addFriend_frame = customtkinter.CTkFrame(self.master, corner_radius=50, fg_color=WHITE)
        addFriend_frame.grid(row=0, column=1)

        # create "add friend" label
        addFriend_text = customtkinter.CTkLabel(addFriend_frame, text="ADD FRIEND", font=("Inter", 50), text_color=GENERAL_TEXT)
        addFriend_text.grid(row=0, column=0, sticky = N, pady = (50,20), padx = 350)

        # create entry box
        username_entry = customtkinter.CTkEntry(addFriend_frame, placeholder_text="Enter your friend's username", font=("Inter", 20), corner_radius=15, text_color=GENERAL_TEXT, fg_color=WHITE, width=500, height=60)
        username_entry.grid(column=0, row=1, pady=20)

        # create profile
        profile_logo = customtkinter.CTkImage(Image.open("logostorage\profile_pic.png"), size=(250, 250))
        profile = customtkinter.CTkLabel(addFriend_frame, text="", image=profile_logo)
        profile.grid(row = 2, column = 0, pady = (20,0))
        name = customtkinter.CTkLabel(addFriend_frame, text="Takeshiii", font=("Inter", 30, "bold"), text_color=GENERAL_TEXT)
        name.grid(row = 3, column = 0, pady = (10,10))

        # add button
        add_btn = customtkinter.CTkButton(addFriend_frame, text="add", font=("Inter", 40), corner_radius=20, text_color=WHITE, fg_color=BUTTON, width=250, height=60, command=self.chat)
        add_btn.grid(column=0, row=4, pady = (20,50), padx = 350)

    def main_menu(self):
        # Setting up grid and frame for button widgets/ texts
        Grid.columnconfigure(root,0,weight=1)
        Grid.columnconfigure(root,1,weight=1)
        Grid.columnconfigure(root,2,weight=1)
        Grid.rowconfigure(root,3,weight=1)
        Grid.rowconfigure(root,4,weight=1)

        for i in self.master.winfo_children():
            i.destroy()
        # Title 
        tk.Label(self.master, text="CUBE", font=("Inter", 64, "bold"), bg=BG_COLOR).grid(column=1, row=0, sticky=tk.N, padx=1, pady=45)
        
        # Cube logo
        self.image = customtkinter.CTkImage(Image.open("logostorage\\vaadin_cube.png"), size=(220, 220))
        img_label = customtkinter.CTkLabel(self.master, text="", image=self.image)
        img_label.grid(column=1, row=1)

        # Menu texts/ three buttons: Login, Register, & Quit
        tk.Label(self.master, text="Welcome\nGlad to see you!\n\n\n\n", font=("Inter", 25), bg=BG_COLOR).grid(column=1, row=2, padx=1, pady=10, rowspan=2, sticky=tk.N)

        btn1 = customtkinter.CTkButton(self.master, text="Login", font=("Inter", 35), corner_radius=20, text_color=WHITE, fg_color=BUTTON, width=350, height=75, command=self.login)
        btn1.grid(column=1, row=3, pady=100)

        btn2 = customtkinter.CTkButton(self.master, text="Register", font=("Inter", 35), corner_radius=20, text_color=WHITE, fg_color=BUTTON, width=350, height=75, command=self.register)
        btn2.grid(column=1, row=2, rowspan=2, sticky=tk.S, pady=30)

        btn3 = customtkinter.CTkButton(self.master, text="Quit", font=("Inter", 35), corner_radius=20, text_color=GENERAL_TEXT, fg_color=WHITE, width=250, height=75, command=root.destroy)
        btn3.grid(column=1, row=4)
    
    
    """
    Backend Code
    """
    def registerDB(self,username,name,password,confirm):
        if password == confirm:
            self.db.createAccount(username,name,password)
        
        
    def quit(self,e):
        self.destroy()


if __name__ == '__main__':
    try:
        from ctypes import windll

        windll.shcore.SetProcessDpiAwareness(1)
    finally:
        root = Tk()
        # root = customtkinter.CTk()                    # TO DO: may change the app from using Tk to customtkinterCTk as app frame instead
        root.attributes('-fullscreen', True)
        app(root)
        root.mainloop()