from tkinter import *
from tkinter.ttk import *
import tkinter as tk
import customtkinter
import os
from PIL import Image, ImageTk
from Libs.Database import Database
from Libs.FriendList import FriendList

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

        # self.username = None

        # self.chat()
        self.addFriend()
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
        username_label = customtkinter.CTkLabel(self.master, text="Username", font=("Inter", 20), text_color=GENERAL_TEXT)
        username_label.grid(column=1, row=2, pady=(20,0), padx=(250,0), sticky=SW)
        username_entry = customtkinter.CTkEntry(self.master, placeholder_text="Put your Username", font=("Inter", 20), corner_radius=15, text_color=GENERAL_TEXT, fg_color=WHITE, width=500, height=60)
        username_entry.grid(column=1, row=3, sticky = N)

        username_label = customtkinter.CTkLabel(self.master, text="Password", font=("Inter", 20), text_color=GENERAL_TEXT)
        username_label.grid(column=1, row=4, pady=(20,0), padx=(250,0), sticky=SW)
        password_entry = customtkinter.CTkEntry(self.master, placeholder_text="Put the Password", show="*", font=("Inter", 20), corner_radius=15, text_color=GENERAL_TEXT, fg_color=WHITE, width=500, height=60)
        password_entry.grid(column=1, row=5, sticky = N)
        
        # create error frame
        self.errLogin_frame = customtkinter.CTkFrame(self.master, width=500, height=100, corner_radius=0, fg_color=BG_COLOR)
        self.errLogin_frame.grid(row=6, column=1)
        self.errLogin_frame.grid_propagate(0)

        # setting up error frame 
        Grid.columnconfigure(self.errLogin_frame,0,weight=1)
        Grid.rowconfigure(self.errLogin_frame,0,weight=1)

        # Login button
        log_btn = customtkinter.CTkButton(self.master, text="Login", font=("Inter", 25), corner_radius=20, text_color=WHITE, fg_color=BUTTON, width=500, height=60,
                                          command=lambda : self.loginDB(username_entry.get(),password_entry.get()))
        log_btn.grid(column=1, row=7, sticky = "s", pady=(100,100))

    def register(self):  
        """
        Setting up grid and frame for button widgets/ texts
        comment these out for now, as they messed with the alignment of widgets for tkinter
        Grid.columnconfigure(root, index = 0, weight = 1)
        Grid.rowconfigure(root, 0, weight = 1)
        """

        Grid.rowconfigure(root,3,weight=0)
        Grid.rowconfigure(root,4,weight=0)

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
        username_label = customtkinter.CTkLabel(self.master, text="Name", font=("Inter", 20), text_color=GENERAL_TEXT)
        username_label.grid(column=1, row=2, pady=(50,0), padx=(250,0), sticky=SW)
        name_entry = customtkinter.CTkEntry(self.master, placeholder_text="Name", font=("Inter", 20), corner_radius=15, text_color=GENERAL_TEXT, fg_color=WHITE, width=500, height=60)
        name_entry.grid(column=1, row=3)

        username_label = customtkinter.CTkLabel(self.master, text="Username", font=("Inter", 20), text_color=GENERAL_TEXT)
        username_label.grid(column=1, row=4, pady=(20,0), padx=(250,0), sticky=SW)
        username_entry = customtkinter.CTkEntry(self.master, placeholder_text="Username", font=("Inter", 20), corner_radius=15, text_color=GENERAL_TEXT, fg_color=WHITE, width=500, height=60)
        username_entry.grid(column=1, row=5)

        username_label = customtkinter.CTkLabel(self.master, text="Password", font=("Inter", 20), text_color=GENERAL_TEXT)
        username_label.grid(column=1, row=6, pady=(20,0), padx=(250,0), sticky=SW)
        password_entry = customtkinter.CTkEntry(self.master, placeholder_text="Password", show="*", font=("Inter", 20), corner_radius=15, text_color=GENERAL_TEXT, fg_color=WHITE, width=500, height=60)
        password_entry.grid(column=1, row=7)

        username_label = customtkinter.CTkLabel(self.master, text="Confirm password", font=("Inter", 20), text_color=GENERAL_TEXT)
        username_label.grid(column=1, row=8, pady=(20,0), padx=(250,0), sticky=SW)
        confirm_entry = customtkinter.CTkEntry(self.master, placeholder_text="Confirm password", show="*", font=("Inter", 20), corner_radius=15, text_color=GENERAL_TEXT, fg_color=WHITE, width=500, height=60)
        confirm_entry.grid(column=1, row=9)

        # create error
        self.errReg_frame = customtkinter.CTkFrame(self.master, width=500, height=100, corner_radius=0, fg_color=BG_COLOR)
        self.errReg_frame.grid(row=10, column=1, rowspan=2)
        self.errReg_frame.grid_propagate(0)

        # setting up error frame 
        Grid.columnconfigure(self.errReg_frame,0,weight=1)
        Grid.rowconfigure(self.errReg_frame,0,weight=1)

        # Register button
        reg_btn = customtkinter.CTkButton(self.master, text="Register", font=("Inter", 25), corner_radius=20, text_color=WHITE, fg_color=BUTTON, width=500, height=60,
                                          command= lambda : self.registerDB(username_entry.get(),name_entry.get(),password_entry.get(),confirm_entry.get()))
        reg_btn.grid(column=1, row=12, sticky = "s", pady=50)

        # create error label
        # error_label = customtkinter.CTkLabel(self.master, text="Wrong Password or Account not found", font=("Inter", 20), text_color="red")
        # error_label.grid(column=1, row=10, pady=(20,0))

    def chat(self):  
        # Setting up grid and frame for button widgets/ texts
        # comment these out for now, as they messed with the alignment of widgets for tkinter
        Grid.columnconfigure(root, index = 0, weight = 0)
        Grid.columnconfigure(root, index = 1, weight = 0)
        Grid.columnconfigure(root, index = 2, weight = 0)

        for i in self.master.winfo_children():
            i.destroy()

        # create sidebar
        self.sidebar("chat")

        profile_logo = customtkinter.CTkImage(Image.open("logostorage\profile_pic.png"), size=(80, 80))

        # create friendlist frame	
        friendList_frame = customtkinter.CTkScrollableFrame(self.master, width=480, height=1080, corner_radius=0, fg_color=FRIEND_LIST)	
        friendList_frame.grid(row=0, column=1, sticky="nsew")
        
        tempFriends = {}
        for val in self.db.showFriendList('c1'):
            tempFriends[val] = 'Nothing here'
        
        for i, button_name in enumerate(tempFriends):	
            friendBtn = customtkinter.CTkButton(friendList_frame, 
                                                image=profile_logo, 
                                                text="  "+ button_name, 
                                                font=("Inter", 40), 
                                                anchor=W, 
                                                width=500, height=100, 
                                                fg_color=FRIEND_LIST, 
                                                command=lambda message=tempFriends[button_name]: self.display_chat(message))	
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

    def addFriend(self):
        Grid.columnconfigure(root,2,weight=1)

        for i in self.master.winfo_children():
            i.destroy()

        # create sidebar
        self.sidebar("addFriend")

        # create requestList frame	
        container_frame = customtkinter.CTkFrame(self.master, width=480, height=1080, corner_radius=0, fg_color=FRIEND_LIST)
        container_frame.grid(row=0, column=1, sticky="nsew")

        request_label = customtkinter.CTkLabel(container_frame, text="Request Friend", font=("Inter", 25), height=50, text_color=WHITE)
        request_label.grid(row=0, column=0)

        requestList_frame = customtkinter.CTkScrollableFrame(container_frame, width=480, height=1030, corner_radius=0, fg_color=WHITE)	
        requestList_frame.grid(row=1, column=0, sticky="nsew")
        
        profile_logo = customtkinter.CTkImage(Image.open("logostorage\profile_pic.png"), size=(80, 80))

        curUser = 'c1'
        tempFriends = {}
        for val in self.db.getIncoming(curUser):
            tempFriends[val] = 'Nothing here'

        try:
            for i, button_name in enumerate(tempFriends):
                friend_subframe = customtkinter.CTkFrame(requestList_frame, width=480, height=100, corner_radius=0, fg_color=WHITE)
                friend_subframe.grid(row=i, column=0, sticky="nsew")
                friend_subframe.grid_propagate(0)
                friendBtn = customtkinter.CTkButton(friend_subframe, 
                                                    image=profile_logo, 
                                                    text="  "+ button_name, 
                                                    font=("Inter", 40),   
                                                    anchor=W, 
                                                    width=300, height=100,
                                                    text_color=GENERAL_TEXT,
                                                    fg_color=WHITE, 
                                                    command=lambda message=tempFriends[button_name]: NONE)	
                friendBtn.grid(row=0, column=0, sticky="nsew")	
                
                accept_logo = customtkinter.CTkImage(Image.open("logostorage\\accept_btn.png"), size=(40, 40))
                accept_btn = customtkinter.CTkButton(friend_subframe, image=accept_logo, text="", width=0, fg_color=WHITE, command=lambda name=button_name, frame=friend_subframe, i=i: self.acceptBtn(curUser, name, frame, i))
                accept_btn.grid(row = 0, column = 1)

                reject_logo =  customtkinter.CTkImage(Image.open("logostorage\\reject_btn.png"), size=(40, 40))
                reject_btn = customtkinter.CTkButton(friend_subframe, image=reject_logo, text="", width=0, fg_color=WHITE, command= lambda: NONE)
                reject_btn.grid(row = 0, column = 2, padx=(30,0))
        except:
            print("Friends not found")
            pass

        # create addFriend frame
        addFriend_frame = customtkinter.CTkFrame(self.master, corner_radius=50, fg_color=WHITE)
        addFriend_frame.grid(row=0, column=2, padx=150)

        # create "add friend" label
        addFriend_text = customtkinter.CTkLabel(addFriend_frame, text="ADD FRIEND", font=("Inter", 50), text_color=GENERAL_TEXT)
        addFriend_text.grid(row=0, column=0, sticky = N, pady = (50,20), padx = 350)

        # create entry box
        username_entry = customtkinter.CTkEntry(addFriend_frame, placeholder_text="Enter your friend's username", font=("Inter", 20), corner_radius=15, text_color=GENERAL_TEXT, fg_color=WHITE, width=500, height=60)
        username_entry.grid(row=1, column=0, pady=20)

        # create profile
        profile_subframe = customtkinter.CTkFrame(addFriend_frame, width=300, height=300, corner_radius=0, fg_color=WHITE)	
        profile_subframe.grid(row=2, column=0)
        profile_logo = customtkinter.CTkImage(Image.open("logostorage\profile_pic.png"), size=(250, 250))
        profile = customtkinter.CTkLabel(profile_subframe, text="", image=profile_logo)
        profile.grid(row = 0, column = 0, pady = (20,0))
        name = customtkinter.CTkLabel(profile_subframe, text="Takeshiii", font=("Inter", 30, "bold"), text_color=GENERAL_TEXT)
        name.grid(row = 1, column = 0, pady = (10,10))

        # add button
        add_btn = customtkinter.CTkButton(addFriend_frame, text="add", font=("Inter", 40), corner_radius=20, text_color=WHITE, fg_color=BUTTON, width=250, height=60, command=self.chat)
        add_btn.grid(column=0, row=4, pady = (20,50), padx = 350)

    def acceptBtn(self, curUser, name, frame, i):
        print(name)
        print(i)
        self.db.acceptFriendRequest(curUser, name)
        frame.destroy()  

    def main_menu(self):
        # Setting up grid and frame for button widgets/ texts
        Grid.columnconfigure(root,0,weight=1)
        Grid.columnconfigure(root,1,weight=1)
        Grid.columnconfigure(root,2,weight=1)

        for i in self.master.winfo_children():
            i.destroy()
        # Title 
        tk.Label(self.master, text="CUBE", font=("Inter", 64, "bold"), bg=BG_COLOR).grid(column=1, row=0, sticky=tk.N, padx=1, pady=45)
        
        # Cube logo
        self.image = customtkinter.CTkImage(Image.open("logostorage\\vaadin_cube.png"), size=(220, 220))
        img_label = customtkinter.CTkLabel(self.master, text="", image=self.image)
        img_label.grid(column=1, row=1)

        # Menu texts/ three buttons: Login, Register, & Quit
        tk.Label(self.master, text="Welcome\nGlad to see you!\n\n\n\n", font=("Inter", 25), bg=BG_COLOR).grid(column=1, row=2, pady=20, sticky=tk.N)

        btn1 = customtkinter.CTkButton(self.master, text="Login", font=("Inter", 35), corner_radius=20, text_color=WHITE, fg_color=BUTTON, width=350, height=75, command=self.login)
        btn1.grid(column=1, row=2, pady=(70,0))

        btn2 = customtkinter.CTkButton(self.master, text="Register", font=("Inter", 35), corner_radius=20, text_color=WHITE, fg_color=BUTTON, width=350, height=75, command=self.register)
        btn2.grid(column=1, row=3)

        btn3 = customtkinter.CTkButton(self.master, text="Quit", font=("Inter", 35), corner_radius=20, text_color=GENERAL_TEXT, fg_color=WHITE, width=250, height=75, command=root.destroy)
        btn3.grid(column=1, row=4, pady=100)

        # btn4 = customtkinter.CTkButton(self.master, text="popup", font=("Inter", 35), corner_radius=20, text_color=GENERAL_TEXT, fg_color=WHITE, width=250, height=75, command=lambda : self.popup("popup"))
        # btn4.grid(column=1, row=5)

    # Function to display output message
    def display_chat(self, message):
        print(message)
        # create name in topbar
        for i in self.topbar_subframe.winfo_children():
            i.destroy()	
        name = customtkinter.CTkLabel(self.topbar_subframe, text=message, font=("Inter", 40), text_color=GENERAL_TEXT, anchor=W)	
        name.grid(row=0, column=0, pady = 15, padx=15, sticky=W)	

    # popup frame
    def popup(self, msg):
        popup_window = tk.Toplevel(root)
        popup_window.geometry("400x300+750+350")
        popup_window.configure(bg="#DCE9F6")

        Grid.columnconfigure(popup_window,0,weight=1)
        Grid.rowconfigure(popup_window,0,weight=1)  

        label = customtkinter.CTkLabel(popup_window, text=msg, text_color=GENERAL_TEXT, font=("Inter", 40))
        label.grid(column = 0, row = 0)
        button = customtkinter.CTkButton(popup_window, text="Close", font=("Inter", 25), command=popup_window.destroy)
        button.grid(column = 0, row = 1, pady=20)
        popup_window.wait_window()

    # function to create sidepar 
    def sidebar(self, page):
        if page == "chat":
            chat_img = "logostorage\Chat_selected.png"
            chat_command = None
            chat_hover = False
            addFriend_img = "logostorage\AddFriend_btn.png"
            addFriend_command = self.addFriend
            addFriend_hover = True
        elif page == "addFriend":
            chat_img = "logostorage\Chat_btn.png"
            chat_command = self.chat
            chat_hover = True
            addFriend_img = "logostorage\AddFriend_selected.png"
            addFriend_command = None
            addFriend_hover = False

        # create sidebar
        sidebar_frame = customtkinter.CTkFrame(self.master, width=70, height=1080, corner_radius=0, fg_color=BUTTON)
        sidebar_frame.grid(row=0, column=0, sticky="nsew")
        sidebar_frame.grid_propagate(0)

        Grid.columnconfigure(sidebar_frame, index = 0, weight = 1)

        chat_logo = customtkinter.CTkImage(Image.open(chat_img), size=(40, 40))
        chat_label = customtkinter.CTkButton(sidebar_frame, image=chat_logo, text="", width=0, hover=chat_hover, fg_color=BUTTON, command=chat_command)
        chat_label.grid(row = 0, column = 0, pady = (30, 25))

        addFriend_logo = customtkinter.CTkImage(Image.open(addFriend_img), size=(40, 40))
        addFriend_label = customtkinter.CTkButton(sidebar_frame, image=addFriend_logo, text="", width=0, hover=addFriend_hover, fg_color=BUTTON, command=addFriend_command)
        addFriend_label.grid(row = 1, column = 0, pady = (30, 25))

        # notification_logo = customtkinter.CTkImage(Image.open("logostorage\\Notifications_btn.png"), size=(40, 40))
        # notification_label = customtkinter.CTkButton(sidebar_frame, image=notification_logo, text="", width=0, fg_color=BUTTON, command=NONE)
        # notification_label.grid(row = 2, column = 0, pady = (30, 25))

        logout_logo = customtkinter.CTkImage(Image.open("logostorage\LogOut_btn.png"), size=(40, 40))
        logout_label = customtkinter.CTkButton(sidebar_frame, image=logout_logo, text="", width=0, fg_color=BUTTON, command=self.main_menu)
        logout_label.grid(row = 3, column = 0, pady = (700, 25))

        shutdown_logo = customtkinter.CTkImage(Image.open("logostorage\Shutdown_btn.png"), size=(40, 40))
        shutdown_label = customtkinter.CTkButton(sidebar_frame, image=shutdown_logo, text="", width=0, fg_color=BUTTON, command=root.destroy)
        shutdown_label.grid(row = 4, column = 0, pady = (30, 25))
    
    
    """
    Backend Code
    """
    def loginDB(self,username,password):
        print("Logging in...")
        err = self.db.login(username,password)
        if type(err) == Exception:
            # create error label
            error_label = customtkinter.CTkLabel(self.errLogin_frame, text=err, font=("Inter", 20), text_color="red")
            error_label.grid(column=0, row=0)
        else:
            self.chat()

    
    def registerDB(self,username,name,password,confirm):
        if password == confirm:
            print("Creating Account...")
            err = self.db.createAccount(username,name,password)
        else:
            err = Exception("Password do not match")
        if type(err) == Exception:
            # create error label
            error_label = customtkinter.CTkLabel(self.errReg_frame, text=err, font=("Inter", 20), text_color="red")
            error_label.grid(column=0, row=0)
        else:
            self.chat()
        
        
    def quit(self,e):
        self.destroy()


if __name__ == '__main__':
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
        
    finally:
        root = Tk()
        # root = customtkinter.CTk()                    
        root.attributes('-fullscreen', True)
        app(root)
        root.mainloop()