from tkinter import *
from tkinter.ttk import *
import tkinter as tk
import customtkinter
import os
from PIL import Image, ImageTk
from Libs.Database import Database
from Libs.FriendList import FriendList

# from chat_tester import chat_test

CURRENT_PATH = os.getcwd()

# color palatte
BG_COLOR = "#B9D6F2"
GENERAL_TEXT = "#000000"
GRAY = "#989898"
WHITE = "#FFFFFF"
BUTTON = "#061A40"
FRIEND_LIST = "#0353A4"
LIGHT_BG = "#DCE9F6"


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
        self.tempframe = None

        self.curUser = 'c1'
        self.name = 'c1'
        self.bio = "Blablalbalblblla"
        self.profilePic = "profilePic\\1.png"

        # self.username = None

        # self.chat()
        self.addFriend()
        # self.myProfile()
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
        username_entry = customtkinter.CTkEntry(self.master, placeholder_text="Username", font=("Inter", 20), corner_radius=15, text_color=GENERAL_TEXT, fg_color=WHITE, width=500, height=60)
        username_entry.grid(column=1, row=3, sticky = N)

        username_label = customtkinter.CTkLabel(self.master, text="Password", font=("Inter", 20), text_color=GENERAL_TEXT)
        username_label.grid(column=1, row=4, pady=(20,0), padx=(250,0), sticky=SW)
        password_entry = customtkinter.CTkEntry(self.master, placeholder_text="Password", show="*", font=("Inter", 20), corner_radius=15, text_color=GENERAL_TEXT, fg_color=WHITE, width=500, height=60)
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

        profile_logo = customtkinter.CTkImage(Image.open(self.profilePic), size=(80, 80))

        # create friendlist frame	
        friendList_frame = customtkinter.CTkScrollableFrame(self.master, width=480, height=1080, corner_radius=0, fg_color=FRIEND_LIST)	
        friendList_frame.grid(row=0, column=1, sticky="nsew")
        
        tempFriends = {}
        for val in self.db.showFriendList('c1'):
            tempFriends[val] = val
        
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

        # Remove texts after hitting enter to send a message
        def clear_text(e):
            chat_entry.delete("1.0","end")

        # Display texts from chat_entry on text box
        def temp_text(e):
            inp = chat_entry.get(1.0, "end-1c")
            self.boxes_subframe.insert(END,inp)
            # messagebox.delete(0,"end")

        # create a message boxes container  /   display text on frame (to be in chat form later)
        self.boxes_subframe = customtkinter.CTkTextbox(self.chat_frame, width=1370, height=905, corner_radius=0, fg_color=BG_COLOR)
        self.boxes_subframe.grid(row=1, column=0, sticky='nsew')
        self.boxes_subframe.grid_propagate(0)

        # create chat box and emoji btn
        tool_subframe = customtkinter.CTkFrame(self.chat_frame, width=1370, height=100, corner_radius=0, fg_color=BG_COLOR)
        tool_subframe.grid(row=2, column=0)
        tool_subframe.grid_propagate(0)

        other_logo = customtkinter.CTkImage(Image.open("logostorage\Other_btn.png"), size=(40, 40))
        other_label = customtkinter.CTkButton(tool_subframe, image=other_logo, text="", width=0, height=0, fg_color=BG_COLOR, command=lambda:temp_text())
        other_label.grid(row = 0, column = 0, padx = 30, pady = 30)

        # chat_entry = customtkinter.CTkEntry(tool_subframe, placeholder_text="Type something", font=("Inter", 20), corner_radius=10, text_color=GENERAL_TEXT, fg_color=WHITE, width=1050, height=50)
        chat_entry = customtkinter.CTkTextbox(tool_subframe, font=("Inter", 20), border_width=2, corner_radius=10, text_color=GENERAL_TEXT, fg_color=WHITE, width=1050, height=50)
        # chat_entry = Text(tool_subframe, font=("Inter", 19), borderwidth=2, bd=0.5, fg=GENERAL_TEXT, width=69, height=1)
        chat_entry.grid(row=0, column=1)
        chat_entry.bind("<Return>", temp_text)
        chat_entry.bind("<Return>", clear_text)

        sticker_logo = customtkinter.CTkImage(Image.open("logostorage\Sticker_btn.png"), size=(40, 40))
        sticker_label = customtkinter.CTkButton(tool_subframe, image=sticker_logo, text="", width=0, height=0, fg_color=BG_COLOR, command=None)
        sticker_label.grid(row = 0, column = 2, padx = 30, pady = 30)

        emoji_logo = customtkinter.CTkImage(Image.open("logostorage\Emoji_btn.png"), size=(40, 40))
        emoji_label = customtkinter.CTkButton(tool_subframe, image=emoji_logo, text="", width=0, height=0, fg_color=BG_COLOR, command=None)
        emoji_label.grid(row = 0, column = 3, padx = (0,30), pady = 30)

    def work_chat(self):
        pass

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
        container_frame = customtkinter.CTkFrame(self.master, width=480, height=1030, corner_radius=0, fg_color=FRIEND_LIST)
        container_frame.grid(row=0, column=1)

        request_label = customtkinter.CTkLabel(container_frame, text="Request Friend", font=("Inter", 25), height=50, text_color=WHITE)
        request_label.grid(row=0, column=0)

        requestList_frame = customtkinter.CTkScrollableFrame(container_frame, width=480, height=1030, corner_radius=0, fg_color=WHITE)	
        requestList_frame.grid(row=1, column=0, sticky="nsew")
        
        profile_logo = customtkinter.CTkImage(Image.open(self.profilePic), size=(80, 80))

        # create serch bar subframe
        self.search_subframe = customtkinter.CTkFrame(addFriend_frame, width=1000, height=250, fg_color=BG_COLOR)	
        self.search_subframe.grid(row=0, column=0, pady = (0, 20))
        self.search_subframe.grid_propagate(0)
        Grid.columnconfigure(self.search_subframe,0,weight=0)
        Grid.columnconfigure(self.search_subframe,1,weight=1)

        # create "add friend" label
        addFriend_text = customtkinter.CTkLabel(self.search_subframe, text="ADD FRIEND", font=("Inter", 50), text_color=GENERAL_TEXT)
        addFriend_text.grid(row=0, column=0, columnspan = 2, sticky= N, pady = (50,20))

        # create entry box
        username_entry = customtkinter.CTkEntry(self.search_subframe, placeholder_text="Enter your friend's username", font=("Inter", 20), corner_radius=15, text_color=GENERAL_TEXT, fg_color=WHITE, width=500, height=60)
        username_entry.grid(row=1, column=0, padx=(230,0), sticky=N)

        # create profile subframe
        self.profile_subframe = customtkinter.CTkFrame(addFriend_frame, width=1000, height=700, corner_radius=50, fg_color=LIGHT_BG)	
        self.profile_subframe.grid(row=2, column=0, pady=30)
        self.profile_subframe.grid_propagate(0)
        Grid.columnconfigure(self.profile_subframe,0,weight=1)
        Grid.rowconfigure(self.profile_subframe,0,weight=1)

        # create tempframe in profile subframe
        if self.tempframe == None:
            self.tempframe = customtkinter.CTkFrame(self.profile_subframe, width=1000, height=600, fg_color=LIGHT_BG)
            self.tempframe.grid(row=0, column=0)
        else: 
            self.tempframe.destroy()
            self.tempframe = customtkinter.CTkFrame(self.profile_subframe, width=1000, height=600, fg_color=LIGHT_BG)
            self.tempframe.grid(row=0, column=0)

        tempFriends = []
        try:
            for val in self.db.getIncoming(self.curUser):
                tempFriends.append(val)
        except:
            pass
        
        if tempFriends == []:
            label = customtkinter.CTkLabel(requestList_frame, text="No friend request", text_color=GENERAL_TEXT, font=("Inter", 30))
            label.grid(column = 0, row = 0, padx = 130, pady = 20, sticky = N)
        else:
            try:
                for i, button_name in enumerate(tempFriends):
                    friend_subframe = customtkinter.CTkFrame(requestList_frame, width=480, height=100, corner_radius=0, fg_color=WHITE)
                    friend_subframe.grid(row=i, column=0, sticky="nsew")
                    friend_subframe.grid_propagate(0)
                    friendBtn = customtkinter.CTkButton(friend_subframe, 
                                                        image=profile_logo, 
                                                        text="  "+ tempFriends[i], 
                                                        font=("Inter", 40),   
                                                        anchor=W, 
                                                        width=300, height=100,
                                                        text_color=GENERAL_TEXT,
                                                        fg_color=WHITE, 
                                                        command=lambda profile=tempFriends[i]: self.showProfile(profile))	
                    friendBtn.grid(row=0, column=0, sticky="nsew")	
                    
                    accept_logo = customtkinter.CTkImage(Image.open("logostorage\\accept_btn.png"), size=(40, 40))
                    accept_btn = customtkinter.CTkButton(friend_subframe, image=accept_logo, text="", width=0, fg_color=WHITE, command=lambda name=button_name, frame=friend_subframe: self.acceptBtn(name, frame))
                    accept_btn.grid(row = 0, column = 1)

                    reject_logo =  customtkinter.CTkImage(Image.open("logostorage\\reject_btn.png"), size=(40, 40))
                    reject_btn = customtkinter.CTkButton(friend_subframe, image=reject_logo, text="", width=0, fg_color=WHITE, command= lambda name=button_name, frame=friend_subframe: self.rejectBtn(name, frame))
                    reject_btn.grid(row = 0, column = 2, padx=(30,0))
            except Exception as e:
                print(e)
                pass
        
        # create search btn
        search_logo = customtkinter.CTkImage(Image.open("logostorage\\search_btn.png"), size=(40, 40))
        search_btn = customtkinter.CTkButton(self.search_subframe, image=search_logo, text="", width=0, fg_color=BG_COLOR, command=lambda: self.showProfile(username_entry.get()))
        search_btn.grid(row = 1, column = 1, padx=5, sticky=W)

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
        profile_image = customtkinter.CTkImage(Image.open(self.profilePic), size=(400, 400))
        profile_label = customtkinter.CTkButton(profile_frame, text="", image=profile_image, width=10, height=10, fg_color=BG_COLOR, corner_radius=50, command=lambda: self.popup())
        profile_label.grid(row=0, column=0, padx=(0,20), sticky=E)

        # information box subframe
        self.info_subframe = customtkinter.CTkFrame(profile_frame, width=910, height=800, fg_color=BG_COLOR)
        self.info_subframe.grid(row=0, column=1, sticky=W)
        self.info_subframe.grid_propagate(0)
        Grid.columnconfigure(self.info_subframe,0,weight=0)
        Grid.columnconfigure(self.info_subframe,1,weight=0)
        Grid.columnconfigure(self.info_subframe,2,weight=1)
        Grid.rowconfigure(self.info_subframe,0,weight=0)
        Grid.rowconfigure(self.info_subframe,1,weight=0)
        Grid.rowconfigure(self.info_subframe,2,weight=1)

        # create infoBox
        infobox_img = customtkinter.CTkImage(Image.open("logostorage\profile_box.png"), size=(910, 800))
        infobox_bg = customtkinter.CTkLabel(self.info_subframe, text="",image=infobox_img, width=0)
        infobox_bg.grid(row=0, column=0, rowspan = 3, columnspan=3, sticky=W)

        # create information in infobox
        # name
        self.padName = (50,10)
        name_label = customtkinter.CTkLabel(self.info_subframe, text="Name:     ", font=("Inter", 35), width=0, text_color=GENERAL_TEXT, fg_color=WHITE)
        name_label.grid(row=0, column=0, pady=self.padName, padx=(150, 0), sticky='w')
        self.name_text = customtkinter.CTkTextbox(self.info_subframe, width=550, height=60, corner_radius=0, font=("Inter", 40), text_color=GENERAL_TEXT, fg_color=WHITE)
        self.name_text.grid(row=0, column=1, padx=(0, 0), pady=self.padName, sticky='w')
        self.name_text.insert("0.0", text=self.name)
        self.name_text.configure(state="disabled")

        edit_image = customtkinter.CTkImage(Image.open("logostorage\\editText.png"), size=(30, 30))
        editName_label = customtkinter.CTkButton(self.info_subframe, text="", image=edit_image, width=0, fg_color=WHITE, corner_radius=0, command=lambda: self.edit_name())
        editName_label.grid(row=0, column=2, pady=self.padName, padx=(10,20), sticky='e')
        
        # bio
        bio_label = customtkinter.CTkLabel(self.info_subframe, text="Bio:         ", font=("Inter",35), width=0, text_color=GENERAL_TEXT, fg_color=WHITE)
        bio_label.grid(row=1, column=0, padx=(150, 0), pady=5, sticky='n')
        self.bio_text = customtkinter.CTkTextbox(self.info_subframe, width=550, height=200, corner_radius=0, font=("Inter", 40), text_color=GENERAL_TEXT, fg_color=WHITE)
        self.bio_text.grid(row=1, column=1, padx=(0, 0), sticky='w')
        self.bio_text.insert("0.0", text=self.bio)
        self.bio_text.configure(state="disabled")
        
        editBio_label = customtkinter.CTkButton(self.info_subframe, text="", image=edit_image, width=0, fg_color=WHITE, corner_radius=0, command=lambda: self.edit_bio())
        editBio_label.grid(row=1, column=2, padx=(10,20), sticky='ne')

        # emotion
        emotion_subframe = customtkinter.CTkFrame(self.info_subframe, width=700, height=400, fg_color=LIGHT_BG)
        emotion_subframe.grid(row=2, column=0, columnspan=3, padx=50, sticky=E)
        emotion_subframe.grid_propagate(0)

    def edit_bio(self):
        self.bio_text.configure(state="normal")
        self.bio_text.insert("0.0", text='')
        self.bio_text.bind("<Return>", self.edited_bio)
    
    def edited_bio(self, event):
        self.bio = self.bio_text.get("0.0", "end")
        self.bio_text.configure(state="disabled")
        
    def edit_name(self):
        self.name_text.configure(state="normal")
        self.name_text.insert("0.0", text='')
        self.name_text.bind("<Return>", self.edited_name)
 
    def edited_name(self, event):
        self.name = self.name_text.get("0.0", "end")
        self.name_text.configure(state="disabled")

    def acceptBtn(self, name, frame):
        self.db.acceptFriendRequest(self.curUser, name)
        frame.destroy()

    def rejectBtn(self, name, frame):
        self.db.rejectFriendRequest(self.curUser,name)
        frame.destroy()

    def showProfile(self, name):
        # error label
        error_label = customtkinter.CTkLabel(self.search_subframe, text="This user does not exist", font=("Inter", 25), text_color='red')
        error_label.grid(row=2, column=0, columnspan=2, padx=350, pady=10, sticky=W)

        # create variable
        profile = self.db.findFriend(name)
        picture = self.profilePic
        name = str(profile['name'])
        bio = str(profile['bio'])
        
        # destroy and gen tempframe
        self.tempframe.destroy()
        self.tempframe = customtkinter.CTkFrame(self.profile_subframe, width=1000, height=600, fg_color=LIGHT_BG)
        self.tempframe.grid(row=0, column=0)
        self.tempframe.grid_propagate(0)
        Grid.columnconfigure(self.tempframe,0,weight=1)
        Grid.rowconfigure(self.tempframe,2,weight=1)

        # show profile info in tempframe
        profile_logo = customtkinter.CTkImage(Image.open(picture), size=(250, 250))
        profile = customtkinter.CTkLabel(self.tempframe, text="", image=profile_logo)
        profile.grid(row = 0, column = 0, pady = (20,0))
        name_text = customtkinter.CTkLabel(self.tempframe, text=name, font=("Inter", 30, "bold"), text_color=GENERAL_TEXT)
        name_text.grid(row = 1, column = 0, pady = (10,10))
        bio_text = customtkinter.CTkTextbox(self.tempframe, width=450, height=200, corner_radius=0, font=("Inter", 30), text_color=GENERAL_TEXT, fg_color=WHITE)
        bio_text.grid(row=2, column=0, padx=(20,0), sticky=N)
        bio_text.insert("0.0", text=bio)
        bio_text.configure(state="disabled")

        # create add button
        add_btn = customtkinter.CTkButton(self.tempframe, text="add", font=("Inter", 30), corner_radius=10, text_color=WHITE, fg_color=BUTTON, width=150, height=50, command=lambda: self.afterAdd(name))
        add_btn.grid(row=3, column=0, sticky=S, pady = (20,20), padx = 350)

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

    # Function to display output message
    def display_chat(self, message):
        print(message)
        # create name in topbar
        for i in self.topbar_subframe.winfo_children():
            i.destroy()	
        name = customtkinter.CTkLabel(self.topbar_subframe, text=message, font=("Inter", 40), text_color=GENERAL_TEXT, anchor=W)	
        name.grid(row=0, column=0, pady = 15, padx=15, sticky=W)	

    # popup frame
    def popup(self):
        self.popup_window = tk.Toplevel(root)
        self.popup_window.geometry("1200x800+360+140")
        self.popup_window.configure(bg=FRIEND_LIST)

        Grid.columnconfigure(self.popup_window,0,weight=1)
        Grid.rowconfigure(self.popup_window,0,weight=0)  
        Grid.rowconfigure(self.popup_window,1,weight=1)  
        Grid.rowconfigure(self.popup_window,2,weight=0) 

        label = customtkinter.CTkLabel(self.popup_window, text="Choose the profile that you like", text_color=WHITE, font=("Inter", 40))
        label.grid(column = 0, row = 0, pady = 20)

        # create scrollable frame
        image_frame = customtkinter.CTkScrollableFrame(self.popup_window, width=480, height=300, corner_radius=0, fg_color=LIGHT_BG)	
        image_frame.grid(row=1, column=0, sticky="nsew")
        Grid.columnconfigure(image_frame,0,weight=1)
        Grid.columnconfigure(image_frame,1,weight=1)
        Grid.columnconfigure(image_frame,2,weight=1)
        Grid.columnconfigure(image_frame,3,weight=1)
        Grid.columnconfigure(image_frame,4,weight=1)

        profileImageDict = {
            0:"bla", 1:"bla", 2:"bla", 3:"bla", 4:"bla", 5:"bla", 6:"bla", 7:"bla", 8:"bla"
        }
        # create buttons
        row = 0
        col = 0
        for i in range(len(profileImageDict)):
            image = f"profilePic\\{i}.png"
            choose_image = customtkinter.CTkImage(Image.open(image), size=(200, 200))
            choose_label = customtkinter.CTkButton(image_frame, text="", image=choose_image, width=0, fg_color=LIGHT_BG, corner_radius=20, command=lambda newProfile = image: self.changeProfile(newProfile))
            choose_label.grid(row=row, column=col, padx=0, pady=15)
            col += 1
            if col > 4:
                col = 0
                row += 1

        self.popup_window.wait_window()
    
    # create confirm button
    def changeProfile(self, newProfile):
        self.profilePic = newProfile
        button = customtkinter.CTkButton(self.popup_window, text="Confirm", font=("Inter", 25), text_color=BUTTON, fg_color=LIGHT_BG, command=lambda:self.afterChangeProfile())
        button.grid(column = 0, row = 2, pady=20)

    # change profile and refresh it
    def afterChangeProfile(self):
        self.popup_window.destroy()
        self.myProfile()
    
    # after press add button in addFriend page
    def afterAdd(self, name):
        self.db.addFriend(self.curUser, name)
        self.chat()

    # function to create sidepar 
    def sidebar(self, page):
        if page == "chat":
            chat_img = "logostorage\Chat_selected.png"
            chat_command = None
            chat_hover = False
            addFriend_img = "logostorage\AddFriend_btn.png"
            addFriend_command = self.addFriend
            addFriend_hover = True
            myProfile_img = self.profilePic
            myProfile_command = self.myProfile
            myProfile_hover = True
        elif page == "addFriend":
            chat_img = "logostorage\Chat_btn.png"
            chat_command = self.chat
            chat_hover = True
            addFriend_img = "logostorage\AddFriend_selected.png"
            addFriend_command = None
            addFriend_hover = False
            myProfile_img = self.profilePic
            myProfile_command = self.myProfile
            myProfile_hover = True
        elif page == "myProfile":
            chat_img = "logostorage\Chat_btn.png"
            chat_command = self.chat
            chat_hover = True
            addFriend_img = "logostorage\AddFriend_btn.png"
            addFriend_command = self.addFriend
            addFriend_hover = True
            myProfile_img = self.profilePic
            myProfile_command = None
            myProfile_hover = False

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

        myProfile_logo = customtkinter.CTkImage(Image.open(myProfile_img), size=(40, 40))
        myProfile_label = customtkinter.CTkButton(sidebar_frame, image=myProfile_logo, text="", width=0, hover=myProfile_hover, fg_color=BUTTON, command=myProfile_command)
        myProfile_label.grid(row = 2, column = 0, pady = (600, 25))

        logout_logo = customtkinter.CTkImage(Image.open("logostorage\LogOut_btn.png"), size=(40, 40))
        logout_label = customtkinter.CTkButton(sidebar_frame, image=logout_logo, text="", width=0, fg_color=BUTTON, command=self.main_menu)
        logout_label.grid(row = 3, column = 0, pady = (30, 25))

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

# custom button class
class MyButton(customtkinter.CTkButton):
    def __init__(self, master, image_path, **kwargs):
        # Open the image file and convert it to a PhotoImage object
        self.photo = customtkinter.CTkImage(Image.open(image_path), size=(70, 70))

        # Call the parent constructor to create the button
        customtkinter.CTkButton.__init__(self, master, image=self.photo, bd=0, highlightthickness=0, **kwargs)

        # Set the button size to match the image size
        self.config(width=self.photo.width(), height=self.photo.height())

        # Use the image as the button background
        self.configure(image=self.photo, compound="center")

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