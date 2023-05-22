from tkinter import *
from tkinter.ttk import *
import tkinter as tk
import customtkinter
import os
import socket
from PIL import Image, ImageTk
from Libs.Database import Database
from Libs.ChatFrame import ChatFrame
from Libs.Client import Client
from Libs.Jessie import Processing, Detection
import tkinter.font as tkfont
from datetime import datetime
from threading import Thread
import time
from tkinter import filedialog

# from chat_tester import chat_test

CURRENT_PATH = os.getcwd()

# color palatte
BG_COLOR = "#F1F6F9"
BG2_COLOR = "#9BA4B5"
LIGHT_BG = "#FFFFFF"
GENERAL_TEXT = "#000000"
INPUT_TEXT = "#989898"
INPUT_BOX = "#FFFFFF"
BUTTON = "#394867"
BUTTON_TEXT = "#FFFFFF"
FRIEND_LIST = "#6B7A97"
SIDE_BAR = "#212A3E"
REQUEST_LIST = "#9BA4B5"
PROFILE_INFO = "#FFFFFF"
ADD_SHOWINFO = "#6B7A97"
MSG_BOX = "#9BA4B5"
MSG_TEXT = "#000000"
EMOJIANDTIME = "#000000"
TOPBUTT_BAR = "#212A3E"
TOPBUTT_TEXT = "#FFFFFF"

"""
SOCKET DATA
"""
LISTENER_LIMIT = 5
active_clients = []

class app:
    def __init__(self, master):
        self.master = master
        window_width = 1080
        window_height = 1920
        self.host = '192.168.0.110'
        self.port = 1105
        master.bind('<Escape>',lambda e: quit(e))
        # get the screen dimension
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        
        self.db = Database()
        self.initiateThread = False
        self.thread = None
        self.curChatFriend = None 
        self.control_collect = 0

        # find the center point
        center_x = int(screen_width/2 - window_width / 2)
        center_y = int(screen_height/2 - window_height / 2)
        self.master.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        self.master.resizable(0, 0)
        self.master['bg'] = BG2_COLOR
        self.tempframe = None

        self.calibrate = 70

        self.setIP()

        self.main_menu()
        
    """
    ======================================
    Main Menu Functions
    ======================================
    """ 
    def main_menu(self):
        # Setting up grid and frame for button widgets/ texts
        Grid.columnconfigure(root,0,weight=1)
        Grid.columnconfigure(root,1,weight=1)
        Grid.columnconfigure(root,2,weight=1)

        for i in self.master.winfo_children():
            i.destroy()
            
        # Title 
        tk.Label(self.master, text="CUBE", font=("Inter", 64, "bold"), bg=BG2_COLOR).grid(column=1, row=0, sticky=tk.N, padx=1, pady=45)
        
        # Cube logo
        self.image = customtkinter.CTkImage(Image.open(os.path.join("logostorage", "vaadin_cube.png")), size=(220, 220))
        img_label = customtkinter.CTkLabel(self.master, text="", image=self.image)
        img_label.grid(column=1, row=1)

        # Menu texts/ three buttons: Login, Register, & Quit
        tk.Label(self.master, text="Welcome\nGlad to see you!\n\n\n\n", font=("Inter", 25), bg=BG2_COLOR).grid(column=1, row=2, pady=20, sticky=tk.N)

        log_btn = customtkinter.CTkButton(self.master, text="Login", font=("Inter", 35), corner_radius=20, text_color=BUTTON_TEXT, fg_color=BUTTON, width=350, height=75, command=self.login_menu)
        log_btn.grid(column=1, row=2, pady=(70,0))

        reg_btn = customtkinter.CTkButton(self.master, text="Register", font=("Inter", 35), corner_radius=20, text_color=BUTTON_TEXT, fg_color=BUTTON, width=350, height=75, command=self.register_menu)
        reg_btn.grid(column=1, row=3)

        exit_btn = customtkinter.CTkButton(self.master, text="Quit", font=("Inter", 35), corner_radius=20, text_color=GENERAL_TEXT, fg_color=BUTTON_TEXT, width=250, height=75, command=root.destroy)
        exit_btn.grid(column=1, row=4, pady=100)
        
        
    """
    ======================================
    Login Functions
    ======================================
    """
    def loginDB(self,username,password):
        data = self.db.login(username,password)
        if type(data) == Exception:
            # create error label
            error_label = customtkinter.CTkLabel(self.errLogin_frame, text=data, font=("Inter", 20), text_color="red")
            error_label.grid(column=0, row=0)
        else:
            self.curUser = data.get()['username']
            self.name = data.get()['name']
            self.bio = data.get()['bio'][0]
            self.profilePic = data.get()['profileImage']
            print(f"Logged In as {self.curUser}")
            self.myProfile()
        
    def login_menu(self):  
        Grid.rowconfigure(root,3,weight=0)
        Grid.rowconfigure(root,4,weight=0)

        for i in self.master.winfo_children():
            i.destroy()
        # Arrow on top corner left
        self.arrow_logo = customtkinter.CTkImage(Image.open(os.path.join("logostorage", "material-symbols_arrow-back.png")), size=(50, 50))
        arrow_label = customtkinter.CTkButton(self.master, image=self.arrow_logo, text="", width=0, fg_color=BG2_COLOR, command=self.main_menu)
        arrow_label.grid(row = 0, column = 0, padx=10, pady=10,sticky=tk.NW, columnspan=2)

        # Cube logo
        self.image = customtkinter.CTkImage(Image.open(os.path.join("logostorage", "vaadin_cube.png")), size=(180, 180))
        img_label = customtkinter.CTkLabel(self.master, text="", image=self.image)
        img_label.grid(column=1, row=0, pady=35)

        tk.Label(self.master, text="Login", font=("Inter", 40), bg= BG2_COLOR).grid(column=1, row=1, pady=5, sticky=tk.N)

        # Insert text widget/ To add in sending data to firebase admin things after actual login attempt
        username_label = customtkinter.CTkLabel(self.master, text="Username", font=("Inter", 20), text_color=GENERAL_TEXT)
        username_label.grid(column=1, row=2, pady=(20,0), padx=(250,0), sticky=SW)
        username_entry = customtkinter.CTkEntry(self.master, placeholder_text="Username", font=("Inter", 20), corner_radius=15, text_color=GENERAL_TEXT, fg_color=INPUT_BOX, width=500, height=60)
        username_entry.grid(column=1, row=3, sticky = N)

        username_label = customtkinter.CTkLabel(self.master, text="Password", font=("Inter", 20), text_color=GENERAL_TEXT)
        username_label.grid(column=1, row=4, pady=(20,0), padx=(250,0), sticky=SW)
        password_entry = customtkinter.CTkEntry(self.master, placeholder_text="Password", show="*", font=("Inter", 20), corner_radius=15, text_color=GENERAL_TEXT, fg_color=INPUT_BOX, width=500, height=60)
        password_entry.grid(column=1, row=5, sticky = N)
        
        # create error frame
        self.errLogin_frame = customtkinter.CTkFrame(self.master, width=500, height=100, corner_radius=0, fg_color=BG2_COLOR)
        self.errLogin_frame.grid(row=6, column=1)
        self.errLogin_frame.grid_propagate(0)

        # setting up error frame 
        Grid.columnconfigure(self.errLogin_frame,0,weight=1)
        Grid.rowconfigure(self.errLogin_frame,0,weight=1)

        # Login button
        log_btn = customtkinter.CTkButton(self.master, text="Login", font=("Inter", 25), corner_radius=20, text_color=BUTTON_TEXT, fg_color=BUTTON, width=500, height=60,
                                          command=lambda : self.loginDB(username_entry.get(),password_entry.get()))
        log_btn.grid(column=1, row=7, sticky = "s", pady=(100,100))

    """
    ======================================
    Register Functions
    ======================================
    """
    def registerDB(self,username,name,password,confirm):
        if password == confirm:
            print("Creating Account...")
            data = self.db.createAccount(username,name,password)
        else:
            data = Exception("Password do not match")
        if type(data) == Exception:
            # create error label
            print('error')  
            self.errorReg.configure(text=data)

        else:
            self.curUser = data.get()['username']
            self.name = data.get()['name']
            self.bio = data.get()['bio'][0]
            self.profilePic = data.get()['profileImage']
            self.myProfile()
        
    def register_menu(self): 
        Grid.rowconfigure(root,3,weight=0)
        Grid.rowconfigure(root,4,weight=0)

        for i in self.master.winfo_children():
            i.destroy()
        # Arrow on top corner left
        self.arrow_logo = customtkinter.CTkImage(Image.open(os.path.join("logostorage", "material-symbols_arrow-back.png")), size=(50, 50))
        arrow_label = customtkinter.CTkButton(self.master, image=self.arrow_logo, text="", width=0, fg_color=BG2_COLOR, command=self.main_menu)
        arrow_label.grid(row = 0, column = 0, padx=10, pady=10, sticky=tk.NW, columnspan=2)
    
        # Cube logo
        self.image = customtkinter.CTkImage(Image.open(os.path.join("logostorage", "vaadin_cube.png")), size=(180, 180))
        img_label = customtkinter.CTkLabel(self.master, text="", image=self.image)
        img_label.grid(column=1, row=0, pady=35)

        tk.Label(self.master, text="Register", font=("Inter", 40), bg=BG2_COLOR).grid(column=1, row=1, pady=5)

        # Insert text widget/ To add in sending data to firebase admin things after actual login attempt
        username_label = customtkinter.CTkLabel(self.master, text="Name", font=("Inter", 20), text_color=GENERAL_TEXT)
        username_label.grid(column=1, row=2, pady=(50,0), padx=(250,0), sticky=SW)
        name_entry = customtkinter.CTkEntry(self.master, placeholder_text="Name", font=("Inter", 20), corner_radius=15, text_color=GENERAL_TEXT, fg_color=INPUT_BOX, width=500, height=60)
        name_entry.grid(column=1, row=3)

        username_label = customtkinter.CTkLabel(self.master, text="Username", font=("Inter", 20), text_color=GENERAL_TEXT)
        username_label.grid(column=1, row=4, pady=(20,0), padx=(250,0), sticky=SW)
        username_entry = customtkinter.CTkEntry(self.master, placeholder_text="Username", font=("Inter", 20), corner_radius=15, text_color=GENERAL_TEXT, fg_color=INPUT_BOX, width=500, height=60)
        username_entry.grid(column=1, row=5)

        username_label = customtkinter.CTkLabel(self.master, text="Password", font=("Inter", 20), text_color=GENERAL_TEXT)
        username_label.grid(column=1, row=6, pady=(20,0), padx=(250,0), sticky=SW)
        password_entry = customtkinter.CTkEntry(self.master, placeholder_text="Password", show="*", font=("Inter", 20), corner_radius=15, text_color=GENERAL_TEXT, fg_color=INPUT_BOX, width=500, height=60)
        password_entry.grid(column=1, row=7)

        username_label = customtkinter.CTkLabel(self.master, text="Confirm password", font=("Inter", 20), text_color=GENERAL_TEXT)
        username_label.grid(column=1, row=8, pady=(20,0), padx=(250,0), sticky=SW)
        confirm_entry = customtkinter.CTkEntry(self.master, placeholder_text="Confirm password", show="*", font=("Inter", 20), corner_radius=15, text_color=GENERAL_TEXT, fg_color=INPUT_BOX, width=500, height=60)
        confirm_entry.grid(column=1, row=9)

        # create error frame
        errReg_frame = customtkinter.CTkFrame(self.master, width=500, height=100, corner_radius=0, fg_color=BG2_COLOR)
        errReg_frame.grid(row=10, column=1, rowspan=2)
        errReg_frame.grid_propagate(0)

        # setting up error frame 
        Grid.columnconfigure(errReg_frame,0,weight=1)
        Grid.rowconfigure(errReg_frame,0,weight=1)

        # declaire the error_label before configure it in the showProfile() function
        self.errorReg = customtkinter.CTkLabel(errReg_frame, text="", font=("Inter", 20), text_color="red")
        self.errorReg.grid(column=0, row=0)

        # Register button
        reg_btn = customtkinter.CTkButton(self.master, text="Register", font=("Inter", 25), corner_radius=20, text_color=BUTTON_TEXT, fg_color=BUTTON, width=500, height=60,
                                          command= lambda : self.registerDB(username_entry.get(),name_entry.get(),password_entry.get(),confirm_entry.get()))
        reg_btn.grid(column=1, row=12, sticky = "s", pady=50)
    
    """
    ======================================
    Main Chat FUNCTIONS
    ======================================
    """
    def mainChat(self):
        self.curChatFriend = None 
        # Setting up grid and frame for button widgets/ texts
        # comment these out for now, as they messed with the alignment of widgets for tkinter
        Grid.columnconfigure(root, index = 0, weight = 0)
        Grid.columnconfigure(root, index = 1, weight = 0)
        Grid.columnconfigure(root, index = 2, weight = 0)

        for i in self.master.winfo_children():
            i.destroy()

        # create sidebar
        self.sidebar("chat")

        # create friendlist frame	
        friendList_frame = customtkinter.CTkScrollableFrame(self.master, width=480, height=1080, corner_radius=0, fg_color=FRIEND_LIST)	
        friendList_frame.grid(row=0, column=1, sticky="nsew")
        
        tempFriends = []
        try:
            for val in self.db.showFriendList(self.curUser):
                friend = self.db.findFriend(val)
                tempFriends.append(friend)
        except Exception as e:
            print(e)
            pass
            
        if tempFriends == []:
            label = customtkinter.CTkLabel(friendList_frame, text="No friend", text_color=GENERAL_TEXT, font=("Inter", 30))
            label.grid(column = 0, row = 0, padx = 180, pady = 20, sticky = N)

        else:
            try:
                for i, button_name in enumerate(tempFriends):
                    profile_pic = customtkinter.CTkImage(Image.open(os.path.join("profilePic", f"{tempFriends[i]['profileImage']}.png")), size=(80, 80))
                    profile_name = tempFriends[i]['name']
                    if len(profile_name) > 13:
                        profile_name = profile_name[:13] + '...'
                    profile_user = tempFriends[i]['username']

                    friendBtn = customtkinter.CTkButton(friendList_frame, 
                                                image=profile_pic, 
                                                text="  "+ profile_name, 
                                                font=("Inter", 40), 
                                                anchor=W, 
                                                width=500, height=100, 
                                                fg_color=FRIEND_LIST, 
                                                command=lambda user=profile_user: self.display_chat(user))	
                    friendBtn.grid(row=i, column=0, sticky="nsew")
            except Exception as e:
                label = customtkinter.CTkLabel(friendList_frame, text="No friend", text_color=GENERAL_TEXT, font=("Inter", 30))
                label.grid(column = 0, row = 0, padx = 180, pady = 20, sticky = N)
                print(e)
                pass

        # create chat frame
        self.chat_frame = customtkinter.CTkFrame(self.master, width=1370, height=1080, corner_radius=0, fg_color=BG_COLOR)
        self.chat_frame.grid(row=0, column=2, sticky="nsew")

        # create topbar
        self.topbar_subframe = customtkinter.CTkFrame(self.chat_frame, width=1355, height=75, corner_radius=0, fg_color=TOPBUTT_BAR)
        self.topbar_subframe.grid(row=0, column=0, sticky='w')
        self.topbar_subframe.grid_propagate(0)

        self.boxes_subframe = customtkinter.CTkScrollableFrame(self.chat_frame, width=1370, height=905, corner_radius=0, fg_color=BG_COLOR, scrollbar_button_color="black")
        self.boxes_subframe.grid(row=1, column=0, sticky='nsew')
        Grid.columnconfigure(self.boxes_subframe,0,weight=1)

        # create chat box and emoji btn
        self.tool_subframe = customtkinter.CTkFrame(self.chat_frame, width=1385, height=100, corner_radius=0, fg_color=TOPBUTT_BAR)
        self.tool_subframe.grid(row=2, column=0)
        self.tool_subframe.grid_propagate(0)
            
    """
    ======================================
    Display Chat FUNCTIONS
    ======================================
    """
    def upload_image(self):
        # Open a file dialog to select an image file
        filepath = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        data = {
                "name" : self.curUser,
                "msg" : filepath
                }
        self.add_message(data, "image")
        self.db.send(filepath, self.curChatFriend, self.realTimeEmotion)
        
    def send_text(self,e):
        msg = str(self.chat_entry.get())

        # Current Date and Time
        if self.socketOn == True:
            self.send_message(msg)

        self.db.send(str(msg),self.curChatFriend,self.realTimeEmotion)
        self.chat_entry.delete(0, END)
        
    def topEmoji(self):
        self.yourEmojiLabel = customtkinter.CTkButton(self.topbar_subframe, text=self.convert_emotion("neutral"), font=("Inter", 50), width=70, height=70, text_color=TOPBUTT_TEXT, fg_color=TOPBUTT_BAR, border_spacing=1, command=lambda: self.controlAI())    
        self.yourEmojiLabel.grid(row=0, column=2, padx=(0,15), pady=(0,10))

    def controlAI(self):
        print("ehe")
    
    def display_chat(self, friend):
        other_logo = customtkinter.CTkImage(Image.open(os.path.join("logostorage", "Other_btn.png")), size=(40, 40))
        other_label = customtkinter.CTkButton(self.tool_subframe, image=other_logo, text="", width=0, height=0, fg_color=TOPBUTT_BAR, command=lambda:self.upload_image())
        other_label.grid(row = 0, column = 0, padx = 30, pady = 30)

        self.chat_entry = customtkinter.CTkEntry(self.tool_subframe, font=("Inter", 20), border_width=2, corner_radius=10, text_color=GENERAL_TEXT, fg_color=INPUT_BOX, width=1050, height=50)
        self.chat_entry.grid(row=0, column=1)

        self.chat_entry.bind("<Return>", lambda e: self.send_text(e))

        sticker_logo = customtkinter.CTkImage(Image.open(os.path.join("logostorage", "Sticker_btn.png")), size=(40, 40))
        sticker_label = customtkinter.CTkButton(self.tool_subframe, image=sticker_logo, text="", width=0, height=0, fg_color=TOPBUTT_BAR, command=None)
        sticker_label.grid(row = 0, column = 2, padx = 30, pady = 30)

        emoji_logo = customtkinter.CTkImage(Image.open(os.path.join("logostorage", "Emoji_btn.png")), size=(40, 40))
        emoji_label = customtkinter.CTkButton(self.tool_subframe, image=emoji_logo, text="", width=0, height=0, fg_color=TOPBUTT_BAR, command=None)
        emoji_label.grid(row = 0, column = 3, padx = (0,30), pady = 30)

        try:
            self.socketOn = True
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connect()
            print("connect using socket")
        except:
            self.socketOn = False
            
        # Detect Emotion Thread
        self.realTimeAI = Thread(target=self.turnOnAI, args=(1,)).start()
        # Detect Emotion Output Thread
        if self.control_collect == 0:
            self.realTimeEmotion = Thread(target=self.detectAI, args=(1,)).start()
            self.control_collect = 1
              
        self.curChatFriend = friend
        name = self.db.findFriend(self.curChatFriend)["name"]

        Grid.columnconfigure(self.topbar_subframe,0,weight=1)
        Grid.columnconfigure(self.topbar_subframe,1,weight=1)
        Grid.rowconfigure(self.topbar_subframe,0,weight=1)
        
        # create name in topbar
        for i in self.topbar_subframe.winfo_children():
            i.destroy()	
        name = customtkinter.CTkLabel(self.topbar_subframe, text=name, font=("Inter", 40), text_color=TOPBUTT_TEXT, anchor=W)	
        name.grid(row=0, column=0, pady = 15, padx=(15,0), sticky="w")

        # create emoji in topbar
        self.topEmoji()

        # Load Chat
        chat_history = self.db.loadchat(friend)
        
        # Clear frame
        for widget in self.boxes_subframe.winfo_children():
            widget.destroy()
        
        # chatFrameList = []
        self.index = 0

        try:
            for index, key in enumerate(chat_history):
                msgBox = ChatFrame(self.boxes_subframe,chat_history[key], self.curUser, self.db.getFriendPic(friend), fg_color = BG_COLOR, bgColor=BG_COLOR, msgbox=MSG_BOX, textColor=MSG_TEXT, emoji_time=EMOJIANDTIME, uploadImage=False)
                # chatFrameList.append(msgBox)
                if chat_history[key]["name"] == self.curUser:
                    msgBox.grid(row=index,column=0, ipady=10, sticky="e")
                    Grid.columnconfigure(msgBox,0,weight=0)
                    Grid.columnconfigure(msgBox,1,weight=0)
                    Grid.columnconfigure(msgBox,2,weight=1)
                elif chat_history[key]["name"] == friend:
                    msgBox.grid(row=index,column=0, ipady=10, sticky="w")
                    Grid.columnconfigure(msgBox,0,weight=0)
                    Grid.columnconfigure(msgBox,1,weight=1)
                    Grid.columnconfigure(msgBox,2,weight=0)
                    
                self.index += 1
        except Exception as e:
            print(e)
            print("no chat")
    """
    ======================================
    Add Friends Functions
    ======================================
    """ 
    def acceptBtn(self, name, frame):
        self.db.acceptFriendRequest(self.curUser, name)
        try:
            print("Loading chat")
            err = self.db.loadchat(name)
            if type(err) == Exception:
                self.db.createChatroom(name)
        except:
            print("Creating Chatroom from main.py")
            self.db.createChatroom(name)
        frame.destroy()

    def rejectBtn(self, name, frame):
        self.db.rejectFriendRequest(self.curUser,name)
        frame.destroy()
        
    def addFriend(self):
        for i in self.master.winfo_children():
            i.destroy()

        # create sidebar
        self.sidebar("addFriend")

        # create addFriend frame
        addFriend_frame = customtkinter.CTkFrame(self.master, width=1370, height=1080, fg_color=BG_COLOR)
        addFriend_frame.grid(row=0, column=2, sticky='nsew')
        addFriend_frame.grid_propagate(0)
        Grid.columnconfigure(addFriend_frame,0,weight=1)

        # create requestList frame	
        container_frame = customtkinter.CTkFrame(self.master, width=480, height=1030, corner_radius=0, fg_color=TOPBUTT_BAR)
        container_frame.grid(row=0, column=1)

        request_label = customtkinter.CTkLabel(container_frame, text="Request Friend", font=("Inter", 25), height=50, text_color=TOPBUTT_TEXT)
        request_label.grid(row=0, column=0)

        requestList_frame = customtkinter.CTkScrollableFrame(container_frame, width=480, height=1030, corner_radius=0, fg_color=REQUEST_LIST)	
        requestList_frame.grid(row=1, column=0, sticky="nsew")

        # create serch bar subframe
        self.search_subframe = customtkinter.CTkFrame(addFriend_frame, width=1000, height=250, fg_color=BG_COLOR)	
        self.search_subframe.grid(row=0, column=0, pady = (0, 20))
        self.search_subframe.grid_propagate(0)
        Grid.columnconfigure(self.search_subframe,0,weight=0)
        Grid.columnconfigure(self.search_subframe,1,weight=1)

        # declaire the error_label before configure it in the showProfile() function
        self.errorAddFriend = customtkinter.CTkLabel(self.search_subframe, text="", font=("Inter", 25), text_color=BG_COLOR)

        # create "add friend" label
        addFriend_text = customtkinter.CTkLabel(self.search_subframe, text="ADD FRIEND", font=("Inter", 50), text_color=GENERAL_TEXT)
        addFriend_text.grid(row=0, column=0, columnspan = 2, sticky= N, pady = (50,20))

        # create entry box
        username_entry = customtkinter.CTkEntry(self.search_subframe, placeholder_text="Enter your friend's username", font=("Inter", 20), corner_radius=15, text_color=GENERAL_TEXT, fg_color=INPUT_BOX, width=500, height=60)
        username_entry.grid(row=1, column=0, padx=(230,0), sticky=N)

        # create profile subframe
        self.profile_subframe = customtkinter.CTkFrame(addFriend_frame, width=1000, height=700, corner_radius=50, fg_color=ADD_SHOWINFO)	
        self.profile_subframe.grid(row=2, column=0, pady=30)
        self.profile_subframe.grid_propagate(0)
        Grid.columnconfigure(self.profile_subframe,0,weight=1)
        Grid.rowconfigure(self.profile_subframe,0,weight=1)

        # create tempframe in profile subframe
        if self.tempframe == None:
            self.tempframe = customtkinter.CTkFrame(self.profile_subframe, width=1000, height=600, fg_color=ADD_SHOWINFO)
            self.tempframe.grid(row=0, column=0)
        else: 
            self.tempframe.destroy()
            self.tempframe = customtkinter.CTkFrame(self.profile_subframe, width=1000, height=600, fg_color=ADD_SHOWINFO)
            self.tempframe.grid(row=0, column=0)

        tempFriends = []
        try:
            for val in self.db.getIncoming(self.curUser):
                profile = self.db.findFriend(val)
                tempFriends.append(profile)
        except:
            pass
        
        if tempFriends == []:
            label = customtkinter.CTkLabel(requestList_frame, text="No friend request", text_color=GENERAL_TEXT, font=("Inter", 30))
            label.grid(column = 0, row = 0, padx = 130, pady = 20, sticky = N)
        else:
            try:
                for i, button_name in enumerate(tempFriends):
                    friend_subframe = customtkinter.CTkFrame(requestList_frame, width=480, height=100, corner_radius=0, fg_color=REQUEST_LIST)
                    friend_subframe.grid(row=i, column=0, sticky="nsew")
                    friend_subframe.grid_propagate(0)
                    Grid.columnconfigure(friend_subframe,0,weight=1)
                    Grid.columnconfigure(friend_subframe,1,weight=1)
                    Grid.columnconfigure(friend_subframe,2,weight=1)

                    profile_pic = customtkinter.CTkImage(Image.open(os.path.join("profilePic", f"{tempFriends[i]['profileImage']}.png")), size=(80, 80))
                    profile_name = tempFriends[i]['name']
                    if len(profile_name) > 8:
                        profile_name = profile_name[:5] + '...'
                    profile_user = tempFriends[i]['username']
                    # print(tempFriends[i])

                    friendBtn = customtkinter.CTkButton(friend_subframe, 
                                                        image= profile_pic, 
                                                        text="  "+ profile_name, 
                                                        font=("Inter", 40),   
                                                        anchor='w', 
                                                        width=300, height=100,
                                                        text_color=GENERAL_TEXT,
                                                        fg_color=REQUEST_LIST, 
                                                        command=lambda profile=profile_user: self.showProfile(profile))	
                    friendBtn.grid(row=0, column=0, sticky="nsew")	
                    friendBtn.grid_propagate(0)
                    
                    accept_logo = customtkinter.CTkImage(Image.open(os.path.join("logostorage", "accept_btn.png")), size=(40, 40))
                    accept_btn = customtkinter.CTkButton(friend_subframe, image=accept_logo, text="", width=0, fg_color=REQUEST_LIST, command=lambda name=profile_user, frame=friend_subframe: self.acceptBtn(name, frame))
                    accept_btn.grid(row = 0, column = 1)

                    reject_logo =  customtkinter.CTkImage(Image.open(os.path.join("logostorage", "reject_btn.png")), size=(40, 40))
                    reject_btn = customtkinter.CTkButton(friend_subframe, image=reject_logo, text="", width=0, fg_color=REQUEST_LIST, command= lambda name=profile_user, frame=friend_subframe: self.rejectBtn(name, frame))
                    reject_btn.grid(row = 0, column = 2, padx=(30,0))
            except Exception as e:
                print(e)
                pass
        
        # create search btn
        search_logo = customtkinter.CTkImage(Image.open(os.path.join("logostorage", "search_btn.png")), size=(40, 40))
        search_btn = customtkinter.CTkButton(self.search_subframe, image=search_logo, text="", width=0, fg_color=BG_COLOR, command=lambda: self.showProfile(username_entry.get()))
        search_btn.grid(row = 1, column = 1, padx=5, sticky='w')
                   
    """
    ======================================
    Profile Functions
    ======================================
    """
    def edit_bio(self):
        self.bio_text.configure(state="normal")
        self.bio_text.insert("0.0", text='')
        self.bio_text.bind("<Return>", self.edited_bio)
    
    def edited_bio(self, event):
        self.bio = self.bio_text.get("0.0", "end")
        self.db.changeBio(self.curUser, self.bio)
        self.bio_text.configure(state="disabled")
        
    def edit_name(self):
        self.name_text.configure(state="normal")
        self.name_text.insert("0.0", text='')
        self.name_text.bind("<Return>", self.edited_name)
 
    def edited_name(self, event):
        self.name = self.name_text.get("0.0", "end")
        self.db.changeName(self.curUser, self.name)
        self.name_text.configure(state="disabled")
        
    def emotion_stat(self, emotion, total, quantity, i):
        # create emotion 
        self.emotion = customtkinter.CTkLabel(self.emotion_subframe, text=self.convert_emotion(emotion),text_color=GENERAL_TEXT, fg_color=PROFILE_INFO, font=("Inter", 50))
        self.emotion.grid(row=i, column=0, pady=(10,0), padx=(20,30))
        
        if total != 0:
            # create progress bar
            for j in range(round(10*quantity/total)):
                progress = customtkinter.CTkLabel(self.emotion_subframe, text="🟥",text_color=GENERAL_TEXT, fg_color=PROFILE_INFO, font=("Inter", 50))
                progress.grid(row=i, column=j+1, pady=(10,0))
    
    def convert_emotion(self, emotion):
        if emotion == "happy":
            return "😄"
        elif emotion == "sad":
            return "😟"
        elif emotion == "neutral":
            return "🙂"
        elif emotion == "angry":
            return "😡"
        elif emotion == "disgust":
            return "🤢"
        elif emotion == "surprise":
            return "😲"
    
    # popup frame
    def popup(self):
        self.popup_window = tk.Toplevel(root)
        self.popup_window.geometry("1200x800+360+140")
        self.popup_window.configure(bg=TOPBUTT_BAR)

        Grid.columnconfigure(self.popup_window,0,weight=1)
        Grid.rowconfigure(self.popup_window,0,weight=0)  
        Grid.rowconfigure(self.popup_window,1,weight=1)  
        Grid.rowconfigure(self.popup_window,2,weight=0) 

        label = customtkinter.CTkLabel(self.popup_window, text="Choose the profile that you like", text_color=TOPBUTT_TEXT, font=("Inter", 40))
        label.grid(column = 0, row = 0, pady = 20)

        # create scrollable frame
        image_frame = customtkinter.CTkScrollableFrame(self.popup_window, width=480, height=300, corner_radius=0, fg_color=LIGHT_BG)	
        image_frame.grid(row=1, column=0, sticky="nsew")
        Grid.columnconfigure(image_frame,0,weight=1)
        Grid.columnconfigure(image_frame,1,weight=1)
        Grid.columnconfigure(image_frame,2,weight=1)
        Grid.columnconfigure(image_frame,3,weight=1)
        Grid.columnconfigure(image_frame,4,weight=1)

        folder_path = 'profilePic'
        num_files = len([f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))])
        
        # create buttons
        row = 0
        col = 0
        for i in range(num_files):
            image = os.path.join("profilePic", f"{i}.png")
            choose_image = customtkinter.CTkImage(Image.open(image), size=(200, 200))
            choose_label = customtkinter.CTkButton(image_frame, text="", image=choose_image, width=0, fg_color=LIGHT_BG, corner_radius=20, command=lambda newProfile = i: self.changeProfile(newProfile))
            choose_label.grid(row=row, column=col, padx=0, pady=15)
            col += 1
            if col > 4:
                col = 0
                row += 1

        self.popup_window.wait_window()

    # change profile and refresh it
    def afterChangeProfile(self):
        self.popup_window.destroy()
        self.myProfile()
    
    # after press add button in addFriend page
    def afterAdd(self, name):
        self.db.addFriend(self.curUser, name)
        self.mainChat()
    
    # create confirm button
    def changeProfile(self, newProfile):
        self.db.changeProfilePic(self.curUser, newProfile)
        self.profilePic = newProfile
        button = customtkinter.CTkButton(self.popup_window, text="Confirm", font=("Inter", 25), text_color=GENERAL_TEXT, fg_color=TOPBUTT_TEXT, command=lambda:self.afterChangeProfile())
        button.grid(column = 0, row = 2, pady=20)
                
    def myProfile(self):
        Grid.columnconfigure(root,0,weight=0)
        Grid.columnconfigure(root,1,weight=1)

        for i in self.master.winfo_children():
            i.destroy()

        # create sidebar
        self.sidebar("myProfile")

        # create frame
        profile_frame = customtkinter.CTkFrame(self.master, width=1850, height=1080, fg_color=BG_COLOR)
        profile_frame.grid(row=0, column=1, sticky="nsew")
        profile_frame.grid_propagate(0)
        Grid.columnconfigure(profile_frame,0,weight=1)
        Grid.columnconfigure(profile_frame,1,weight=1)
        Grid.rowconfigure(profile_frame,0,weight=1)

        # profile logo
        profile_image = customtkinter.CTkImage(Image.open(os.path.join("profilePic", f"{self.profilePic}.png")), size=(400, 400))
        profile_label = customtkinter.CTkButton(profile_frame, text="", image=profile_image, width=10, height=10, fg_color=BG_COLOR, corner_radius=50, command=lambda: self.popup())
        profile_label.grid(row=0, column=0, padx=(0,20), sticky='e')

        # information box subframe
        self.info_subframe = customtkinter.CTkFrame(profile_frame, width=910, height=800, fg_color=BG_COLOR)
        self.info_subframe.grid(row=0, column=1, sticky='w')
        self.info_subframe.grid_propagate(0)
        Grid.columnconfigure(self.info_subframe,0,weight=0)
        Grid.columnconfigure(self.info_subframe,1,weight=0)
        Grid.columnconfigure(self.info_subframe,2,weight=1)
        Grid.rowconfigure(self.info_subframe,0,weight=0)
        Grid.rowconfigure(self.info_subframe,1,weight=0)
        Grid.rowconfigure(self.info_subframe,2,weight=1)

        # create infoBox
        infobox_img = customtkinter.CTkImage(Image.open(os.path.join("logostorage", "profile_box.png")), size=(910, 800))
        infobox_bg = customtkinter.CTkLabel(self.info_subframe, text="",image=infobox_img, width=0)
        infobox_bg.grid(row=0, column=0, rowspan = 3, columnspan=3, sticky=W)

        # create information in infobox
        # name
        self.padName = (50,10)
        name_label = customtkinter.CTkLabel(self.info_subframe, text="Name:     ", font=("Inter", 35), width=0, text_color=GENERAL_TEXT, fg_color=PROFILE_INFO)
        name_label.grid(row=0, column=0, pady=self.padName, padx=(150, 0), sticky='w')
        self.name_text = customtkinter.CTkTextbox(self.info_subframe, width=550, height=70, corner_radius=0, font=("Inter", 40), text_color=GENERAL_TEXT, fg_color=PROFILE_INFO, wrap="word")
        self.name_text.grid(row=0, column=1, padx=(0, 0), pady=self.padName, sticky='w')
        self.name_text.insert("0.0", text=self.name)
        self.name_text.configure(state="disabled")

        edit_image = customtkinter.CTkImage(Image.open(os.path.join("logostorage", "editText.png")), size=(30, 30))
        editName_label = customtkinter.CTkButton(self.info_subframe, text="", image=edit_image, width=0, fg_color=PROFILE_INFO, corner_radius=0, command=lambda: self.edit_name())
        editName_label.grid(row=0, column=2, pady=self.padName, padx=(10,20), sticky='e')
        
        # bio
        bio_label = customtkinter.CTkLabel(self.info_subframe, text="Bio:         ", font=("Inter",35), width=0, text_color=GENERAL_TEXT, fg_color=PROFILE_INFO)
        bio_label.grid(row=1, column=0, padx=(150, 0), pady=5, sticky='n')
        self.bio_text = customtkinter.CTkTextbox(self.info_subframe, width=550, height=200, corner_radius=0, font=("Inter", 40), text_color=GENERAL_TEXT, fg_color=PROFILE_INFO, wrap="word")
        self.bio_text.grid(row=1, column=1, padx=(0, 0), sticky='w')
        
        bioFormat = self.bio
        if self.bio == "":
            bioFormat = "None"
            
        self.bio_text.insert("0.0", text=bioFormat)
        self.bio_text.configure(state="disabled")
        
        editBio_label = customtkinter.CTkButton(self.info_subframe, text="", image=edit_image, width=0, fg_color=PROFILE_INFO, corner_radius=0, command=lambda: self.edit_bio())
        editBio_label.grid(row=1, column=2, padx=(10,20), sticky='ne')

        # emotion
        self.emotion_subframe = customtkinter.CTkFrame(self.info_subframe, width=700, height=420, fg_color=PROFILE_INFO)
        self.emotion_subframe.grid(row=2, column=0, columnspan=3, padx=50, sticky=E)
        self.emotion_subframe.grid_propagate(0)

        # show stat of each emotion
        curUserProfile = self.db.findFriend(self.curUser)
        emotionDict = curUserProfile['emotions']
        sum_of_values = 0

        for key, value in emotionDict.items():
            sum_of_values += value
        self.emotion_stat("happy", sum_of_values, emotionDict["happy"], 0)
        self.emotion_stat("sad", sum_of_values, emotionDict["sad"], 1)
        self.emotion_stat("neutral", sum_of_values, emotionDict["neutral"], 2)
        self.emotion_stat("angry", sum_of_values, emotionDict["angry"], 3)
        self.emotion_stat("disgust", sum_of_values, emotionDict["disgust"], 4)
        self.emotion_stat("surprise", sum_of_values, emotionDict["surprise"], 5)
    
    # function show profile in addfriend page
    def showProfile(self, name):
        # create variable
        try:
            profile = self.db.findFriend(name)
            self.errorAddFriend.grid(row=2, column=0, columnspan=2, padx=350, pady=10, sticky=W)

            if type(profile) == Exception:
                # error label
                self.errorAddFriend.configure(text="This user does not exist", text_color='red')
            else:
                self.errorAddFriend.configure(text="")
            
            picture = os.path.join("profilePic",f"{profile['profileImage']}.png")
            name = str(profile['name'])
            user = str(profile['username'])
            bio = str(profile['bio'][0])
            sortedEmotion = sorted(profile['emotions'].items(), key=lambda x: x[1], reverse=True)
            emojis = ""
            for val in sortedEmotion[:3]:
                if val[1] != 0:
                    emojis += self.convert_emotion(val[0]) + " "
                else:
                    emojis = "No emotion in database"
            
            # destroy and gen tempframe
            self.tempframe.destroy()
            self.tempframe = customtkinter.CTkFrame(self.profile_subframe, width=1000, height=600, fg_color=ADD_SHOWINFO)
            self.tempframe.grid(row=0, column=0)
            self.tempframe.grid_propagate(0)
            Grid.columnconfigure(self.tempframe,0,weight=1)
            Grid.rowconfigure(self.tempframe,2,weight=1)
            Grid.rowconfigure(self.tempframe,3,weight=2)

            # show profile info in tempframe
            profile_logo = customtkinter.CTkImage(Image.open(picture), size=(250, 250))
            profile = customtkinter.CTkLabel(self.tempframe, text="", image=profile_logo)
            profile.grid(row = 0, column = 0, pady = (20,0))

            # check len name
            if len(name) > 13:
                name = name[:13] + '...'
            name_text = customtkinter.CTkLabel(self.tempframe, text=name, font=("Inter", 30, "bold"), text_color=GENERAL_TEXT, fg_color=ADD_SHOWINFO)
            name_text.grid(row = 1, column = 0, pady = (10,10))
            
            bio_text = customtkinter.CTkTextbox(self.tempframe, width=450, height=150, corner_radius=0, font=("Inter", 30), text_color=GENERAL_TEXT, fg_color=ADD_SHOWINFO, wrap="word")
            bio_text.grid(row=2, column=0, padx=(20,0), sticky="n")
            
            bioText = bio
            if bioText == "":
                bioText = "None"
            
            bio_text.insert("0.0", text=bioText)
            bio_text.configure(state="disabled")

            emotion_text = customtkinter.CTkLabel(self.tempframe, text=("Most used Emotions: " + emojis), font=("Inter", 30, "bold"), text_color=GENERAL_TEXT)
            emotion_text.grid(row = 3, column = 0, sticky="n")

            # create add button
            add_btn = customtkinter.CTkButton(self.tempframe, text="add", font=("Inter", 30), corner_radius=10, text_color=BUTTON_TEXT, fg_color=BUTTON, width=150, height=50, command=lambda: self.afterAdd(user))
            add_btn.grid(row=4, column=0, sticky=S, padx = 350)
        except Exception as e:
            print(e)
            print("Profile not found")

    """
    ======================================
    Settings Functions
    ======================================
    """
    def setting(self):
        Grid.columnconfigure(root,0,weight=0)
        Grid.columnconfigure(root,1,weight=2)

        for i in self.master.winfo_children():
            i.destroy()

        # create sidebar
        self.sidebar("setting")

        # container frame
        container_frame = customtkinter.CTkFrame(self.master, width=1850, height=1080, corner_radius=0, fg_color=BG2_COLOR)
        container_frame.grid(row=0, column=1, sticky="nsew")
        container_frame.grid_propagate(0)

        Grid.columnconfigure(container_frame,0,weight=2)
        Grid.columnconfigure(container_frame,1,weight=2)
        Grid.rowconfigure(container_frame,0,weight=2)
        Grid.rowconfigure(container_frame,1,weight=2)

        # create button
        changeTheme_btn = customtkinter.CTkButton(container_frame, text="Change Theme", font=("Inter", 50), corner_radius=20, text_color=BUTTON_TEXT, fg_color=BUTTON, width=500, height=100, command=self.changeTheme)
        changeTheme_btn.grid(row = 0, column=0, sticky="s")

        calibrate_btn = customtkinter.CTkButton(container_frame, text="Calibrate", font=("Inter", 50), corner_radius=20, text_color=BUTTON_TEXT, fg_color=BUTTON, width=500, height=100, command=self.calibrateThread)
        calibrate_btn.grid(row=0, column=1, sticky="s")

        # create description text
        changeTheme_label = customtkinter.CTkLabel(container_frame, text="", font=("Inter", 35), text_color="gray")
        changeTheme_label.grid(row=1, column=0)

        calibrate_label = customtkinter.CTkLabel(container_frame, text="Calibrating the AI helps with your emotion accuracy.", font=("Inter", 35), text_color="gray")
        calibrate_label.grid(row=1, column=1, pady=(15,0), sticky="n")

    # Function to toggle switch the themes (light & dark)
    def changeTheme(self):
        self.popup_window = tk.Toplevel(root)
        self.popup_window.geometry("1200x800+360+140")
        self.popup_window.configure(bg=TOPBUTT_BAR)

        Grid.columnconfigure(self.popup_window,0,weight=1)
        Grid.rowconfigure(self.popup_window,0,weight=0)  
        Grid.rowconfigure(self.popup_window,1,weight=1)  
        Grid.rowconfigure(self.popup_window,2,weight=0) 

        label = customtkinter.CTkLabel(self.popup_window, text="Choose Color theme", text_color=TOPBUTT_TEXT, font=("Inter", 40))
        label.grid(column = 0, row = 0, pady = 20)

        # create scrollable frame
        theme_toggle_frame = customtkinter.CTkFrame(self.popup_window, width=1850, height=1080, fg_color=BG_COLOR)
        theme_toggle_frame.grid(row=1, column=0, sticky="nsew")
        theme_toggle_frame.grid_propagate(0)

        Grid.columnconfigure(theme_toggle_frame,0,weight=1)
        Grid.columnconfigure(theme_toggle_frame,1,weight=1)
        Grid.columnconfigure(theme_toggle_frame,2,weight=1)
        Grid.columnconfigure(theme_toggle_frame,3,weight=1)

        folder_path = 'colorThemePic'
        num_files = len([f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))])
        
        # create buttons
        row = 0
        col = 0
        for i in range(num_files):
            image = os.path.join(folder_path, f"{i}.png")
            choose_image = customtkinter.CTkImage(Image.open(image), size=(200, 200))
            choose_label = customtkinter.CTkButton(theme_toggle_frame, text="", image=choose_image, width=0, fg_color=LIGHT_BG, corner_radius=20, command=lambda colorTheme = i: self.changeThemeBtn(colorTheme))
            choose_label.grid(row=row, column=col, padx=0, pady=15)
            col += 1
            if col > 3:
                col = 0
                row += 1

        self.popup_window.wait_window()

    def changeThemeBtn(self, colorTheme):
        global BG_COLOR
        global BG2_COLOR
        global LIGHT_BG
        global GENERAL_TEXT
        global INPUT_TEXT
        global INPUT_BOX
        global BUTTON
        global BUTTON_TEXT
        global FRIEND_LIST
        global SIDE_BAR
        global REQUEST_LIST
        global PROFILE_INFO
        global ADD_SHOWINFO
        global MSG_BOX
        global MSG_TEXT
        global EMOJIANDTIME
        global TOPBUTT_BAR
        global TOPBUTT_TEXT

        if colorTheme == 0:
            print("theme 1")
            # color palatte
            BG_COLOR = "#F5E9CF"
            BG2_COLOR = "#7DB9B6"
            LIGHT_BG = "#FFFFFF"
            GENERAL_TEXT = "#000000"
            INPUT_TEXT = "#989898"
            INPUT_BOX = "#FFFFFF"
            BUTTON = "#4D455D"
            BUTTON_TEXT = "#FFFFFF"
            FRIEND_LIST = "#7DB9B6"
            SIDE_BAR = "#4D455D"
            REQUEST_LIST = "#6D6374"
            PROFILE_INFO = "#FFFFFF"
            ADD_SHOWINFO = "#6B7A97"
            MSG_BOX = "#6D5D6E"
            MSG_TEXT = "#FFFFFF"
            EMOJIANDTIME = "#000000"
            TOPBUTT_BAR = "#4D455D"
            TOPBUTT_TEXT = "#FFFFFF"

            self.setting()
    """
    ======================================
    Sockets Functions
    ======================================
    """
    def setIP(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        self.host = s.getsockname()[0]
        s.close()
        
    def add_message(self, data, inputType):
        if inputType == "text":
            now = datetime.now()
            date_time = now.strftime("%m/%d/%Y %H:%M")
            #print(date_time)
            chatObject = {
                "text": data['msg'],
                "time": date_time,
                "name": data['name'],
                "emotion": self.realTimeEmotion
            }
            # print(chatObject)
            if data['name'] != self.curUser:
                profilePic = self.db.getFriendPic(data['name'])
            else:
                profilePic = None

            msgBox = ChatFrame(self.boxes_subframe,chatObject, self.curUser, profilePic, width=1355, height=100, fg_color = BG_COLOR, bgColor=BG_COLOR, msgbox=MSG_BOX, textColor=MSG_TEXT, emoji_time=EMOJIANDTIME, uploadImage=False)

            if self.curUser == data['name']:
                msgBox.grid(row=self.index,column=0, ipady=10, sticky="e")
                Grid.columnconfigure(msgBox,0,weight=0)
                Grid.columnconfigure(msgBox,1,weight=0)
                Grid.columnconfigure(msgBox,2,weight=1)
            else:
                msgBox.grid(row=self.index,column=0, ipady=10, sticky="w")
                Grid.columnconfigure(msgBox,0,weight=0)
                Grid.columnconfigure(msgBox,1,weight=1)
                Grid.columnconfigure(msgBox,2,weight=0)
            self.index += 1
        elif inputType == "image":
            now = datetime.now()
            date_time = now.strftime("%m/%d/%Y %H:%M")
            #print(date_time)
            chatObject = {
                "text": data['msg'],
                "time": date_time,
                "name": data['name'],
                "emotion": self.realTimeEmotion
            }
            # print(chatObject)
            if data['name'] != self.curUser:
                profilePic = self.db.getFriendPic(data['name'])
            else:
                profilePic = None

            msgBox = ChatFrame(self.boxes_subframe,chatObject, self.curUser, profilePic, width=1355, height=100, fg_color = BG_COLOR, bgColor=BG_COLOR, msgbox=MSG_BOX, textColor=MSG_TEXT, emoji_time=EMOJIANDTIME, uploadImage=True)

            if self.curUser == data['name']:
                msgBox.grid(row=self.index,column=0, ipady=10, sticky="e")
                Grid.columnconfigure(msgBox,0,weight=0)
                Grid.columnconfigure(msgBox,1,weight=0)
                Grid.columnconfigure(msgBox,2,weight=1)
            else:
                msgBox.grid(row=self.index,column=0, ipady=10, sticky="w")
                Grid.columnconfigure(msgBox,0,weight=0)
                Grid.columnconfigure(msgBox,1,weight=1)
                Grid.columnconfigure(msgBox,2,weight=0)
            self.index += 1
        
    def connect(self):
        # try except block
        try:
            # Connect to the server
            self.client.connect((self.host, self.port))
            print("Successfully connected to server")
            print("[SERVER] Successfully connected to the server")
        except:
            print(f"Unable to connect to server", f"Unable to connect to server {self.host}:{self.port}")

        if self.curUser != '':
            self.client.sendall(self.curUser.encode())
        else:
            print("Invalid username", "Username cannot be empty")

        self.socketThread = Thread(target=self.listen_for_messages_from_server, args=(self.client, )).start()
        
    def send_message(self,message):
        if message != '':
            self.client.sendall(message.encode())
            # message_textbox.delete(0, len(message))
        else:
            print("Empty Message")
    
    def listen_for_messages_from_server(self,client):
        while 1:
            message = self.client.recv(2048).decode('utf-8')
            if message != '':
                username = message.split("~")[0]
                content = message.split('~')[1]

                data = {
                    "name" : username,
                    "msg" : content
                }
                self.add_message(data, "text")
                
            else:
                print("Error")

    """
    ======================================
    AI Functions
    ======================================
    """
    def turnOnAI(self,name):
        print("Detecting")
        self.ai = self.db.getAI()
        self.ai.realTimeDetection(0, "Libs\Jessie_1.pt", self.calibrate)
        print("AI Has been turned off")

    def detectAI(self, name):
        while True:
            self.realTimeEmotion = self.ai.real_time_emotion
            try:
                self.yourEmojiLabel.configure(text=self.convert_emotion(str(self.realTimeEmotion)))
            except:
                pass
            
            # print(self.realTimeEmotion)
            
    def calibrateThread(self):
        self.popup_window = tk.Toplevel(root)
        self.popup_window.geometry("1200x800+360+140")
        print("Creating Thread to Calibrate AI")

        Grid.columnconfigure(self.popup_window,0,weight=2)
        Grid.rowconfigure(self.popup_window,0,weight=2)  


        self.calibrate_label = customtkinter.CTkLabel(self.popup_window, text="Creating Thread to Calibrate AI\n0%", text_color=GENERAL_TEXT, font=("Inter", 50))
        self.calibrate_label.grid(column = 0, row = 0)

        self.aiT = Thread(target=self.calibrateAI, args=(1,)).start()
        self.popup_window.wait_window()
        
    def calibrateAI(self,name):
        print("Calibrating")
        self.ai = self.db.getAI()
        self.calibrate = self.ai.calibration(0, "Libs\Jessie_1.pt", self.calibrate_label)
        self.calibrate_label.configure(text="Ending Thread to Calibrate AI")
        print("Ending Thread to Calibrate AI")
        print(f"The calibration result is {self.calibrate}")

    """
    ======================================
    Sidebar Functions
    ======================================
    """
    # function to create sidepar 
    def sidebar(self, page):
        if page == "chat":
            chat_img = os.path.join("logostorage", "Chat_selected.png")
            chat_command = None
            chat_hover = False
            addFriend_img = os.path.join("logostorage", "AddFriend_btn.png")
            addFriend_command = self.addFriend
            addFriend_hover = True
            theme_Toggle = os.path.join("logostorage", "Settings_btn.png")
            theme_Toggle_command = self.setting
            theme_Toggle_hover = True
            myProfile_img = os.path.join("profilePic", f"{self.profilePic}.png")
            myProfile_command = self.myProfile
            myProfile_hover = True
        elif page == "addFriend":
            chat_img = os.path.join("logostorage", "Chat_btn.png")
            chat_command = self.mainChat
            chat_hover = True
            addFriend_img = os.path.join("logostorage", "AddFriend_selected.png")
            addFriend_command = None
            addFriend_hover = False
            theme_Toggle = os.path.join("logostorage", "Settings_btn.png")
            theme_Toggle_command = self.setting
            theme_Toggle_hover = True
            myProfile_img = os.path.join("profilePic", f"{self.profilePic}.png")
            myProfile_command = self.myProfile
            myProfile_hover = True
        elif page == "myProfile":
            chat_img = os.path.join("logostorage", "Chat_btn.png")
            chat_command = self.mainChat
            chat_hover = True
            addFriend_img = os.path.join("logostorage", "AddFriend_btn.png")
            addFriend_command = self.addFriend
            addFriend_hover = True
            theme_Toggle = os.path.join("logostorage", "Settings_btn.png")
            theme_Toggle_command = self.setting
            theme_Toggle_hover = True
            myProfile_img = os.path.join("profilePic", f"{self.profilePic}.png")
            myProfile_command = None
            myProfile_hover = False
        elif page == "setting":
            chat_img = os.path.join("logostorage", "Chat_btn.png")
            chat_command = self.mainChat
            chat_hover = True
            addFriend_img = os.path.join("logostorage", "AddFriend_btn.png")
            addFriend_command = self.addFriend
            addFriend_hover = True
            theme_Toggle = os.path.join("logostorage", "Settings_seleted.png")
            theme_Toggle_command = None
            theme_Toggle_hover = False
            myProfile_img = os.path.join("profilePic", f"{self.profilePic}.png")
            myProfile_command = self.myProfile
            myProfile_hover = True

        # create sidebar
        try:
            self.ai = self.db.getAI()
            self.ai.stop_detection()
        except:
            pass

        sidebar_frame = customtkinter.CTkFrame(self.master, width=70, height=1080, corner_radius=0, fg_color=SIDE_BAR)
        sidebar_frame.grid(row=0, column=0, sticky="nsew")
        sidebar_frame.grid_propagate(0)

        Grid.columnconfigure(sidebar_frame, index = 0, weight = 1)

        chat_logo = customtkinter.CTkImage(Image.open(chat_img), size=(40, 40))
        chat_label = customtkinter.CTkButton(sidebar_frame, image=chat_logo, text="", width=0, hover=chat_hover, fg_color=SIDE_BAR, command=chat_command)
        chat_label.grid(row = 0, column = 0, pady = (30, 25))

        addFriend_logo = customtkinter.CTkImage(Image.open(addFriend_img), size=(40, 40))
        addFriend_label = customtkinter.CTkButton(sidebar_frame, image=addFriend_logo, text="", width=0, hover=addFriend_hover, fg_color=SIDE_BAR, command=addFriend_command)
        addFriend_label.grid(row = 1, column = 0, pady = (30, 25))

        setting_logo = customtkinter.CTkImage(Image.open(theme_Toggle), size=(40, 40))
        setting_label = customtkinter.CTkButton(sidebar_frame, image=setting_logo, text="", width=0, hover=theme_Toggle_hover, fg_color=SIDE_BAR, command=theme_Toggle_command)
        setting_label.grid(row = 2, column = 0, pady = (30, 25))

        myProfile_logo = customtkinter.CTkImage(Image.open(myProfile_img), size=(40, 40))
        myProfile_label = customtkinter.CTkButton(sidebar_frame, image=myProfile_logo, text="", width=0, hover=myProfile_hover, fg_color=SIDE_BAR, command=myProfile_command)
        myProfile_label.grid(row = 3, column = 0, pady = (450, 25))

        logout_logo = customtkinter.CTkImage(Image.open(os.path.join("logostorage", "LogOut_btn.png")), size=(40, 40))
        logout_label = customtkinter.CTkButton(sidebar_frame, image=logout_logo, text="", width=0, fg_color=SIDE_BAR, command=self.main_menu)
        logout_label.grid(row = 4, column = 0, pady = (30, 25))

        shutdown_logo = customtkinter.CTkImage(Image.open(os.path.join("logostorage", "Shutdown_btn.png")), size=(40, 40))
        shutdown_label = customtkinter.CTkButton(sidebar_frame, image=shutdown_logo, text="", width=0, fg_color=SIDE_BAR, command=root.destroy)
        shutdown_label.grid(row = 5, column = 0, pady = (30, 25))

    def quit(self,e):
        self.destroy()

if __name__ == '__main__':
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
        
    finally:
        root = Tk()
        # root = customtkinter.CTk()           
        root.title("Cube")         
        root.attributes('-fullscreen', True)
        app(root)
        root.mainloop()

