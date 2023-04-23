import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk
import tkinter.font as tkfont

class ChatFrame(ctk.CTkFrame):
    def __init__(self,master, chat, curUser, friendPic, **kwargs):
        super().__init__(master, **kwargs)
        self.chat = chat
        self.curUser = curUser

        # font = tkfont.Font(family="Inter", size=30)
        # text_width = font.measure(self.chat['text'])
        # print('The width of the text is:', text_width)
        # height = 50
        # if text_width > 1500:
        #     height += (text_width // 1500) * 50

        if chat["name"] == self.curUser:
            print("here")
            # text label
            self.messages = ctk.CTkLabel(self, text=self.chat['text'],text_color="#000000", fg_color="#DCE9F6", font=("Inter", 30), wraplength=1000, corner_radius=10)
            self.messages.grid(row=0, column=2, padx=(0, 20), ipadx=10, ipady=10, sticky="e")

            # time label
            self.messages = ctk.CTkLabel(self, text=chat["time"][-5:-1],text_color="#000000", fg_color="#e9f2b9", font=("Inter", 15))
            self.messages.grid(row=0, column=1, padx=(10,0), sticky="e")
        else:
            # time label display
            self.messages = ctk.CTkLabel(self, text=chat["time"][-5:-1],text_color="#000000", fg_color="#e9f2b9", font=("Inter", 15))
            self.messages.grid(row=0, column=2, padx=(0,10), sticky="w")
            
            # text label display below time
            self.messages = ctk.CTkLabel(self, text=chat["text"],text_color="#000000", fg_color="#DCE9F6", font=("Inter", 30), wraplength=1000, corner_radius=10)
            self.messages.grid(row=0, column=1, ipadx=10, ipady=10, sticky="w")
            
            # recipient's name label display left next to the received message
            profile_logo = ctk.CTkImage(Image.open(f"profilePic\\{friendPic}.png"), size=(60, 60))
            profile = ctk.CTkLabel(self, text="", image=profile_logo)
            profile.grid(row = 0, column = 0, padx=30, sticky='w')
            
            # self.messages = customtkinter.CTkLabel(self.boxes_subframe, text=chat_history[key]["name"],text_color="#000000", bg_color="#e9f2b9", font=("Inter", 18))
            # self.messages.grid(row=row_num, column=1, padx=1, pady=25, sticky="ww")

    def getHeight(self):
        return self.messages
        # newHeight = self.messages.winfo_height()
        # x, y, width, height = self.grid_bbox(self.messages)
        # print(height)
        # self.configure(height=newHeight)
