import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk
import tkinter.font as tkfont
import emoji

class ChatFrame(ctk.CTkFrame):
    def __init__(self,master, chat, curUser, friendPic, bgColor, msgbox, textColor, emoji_time, **kwargs):
        super().__init__(master, **kwargs)
        self.chat = chat
        self.curUser = curUser

        # font = tkfont.Font(family="Inter", size=30)
        # text_width = font.measure(self.chat['text'])
        # print('The width of the text is:', text_width)
        # height = 50
        # if text_width > 1500:
        #     height += (text_width // 1500) * 50

        for char in chat["name"]:
            if char == " ":
                print("Empty detected")

        if chat["name"] == self.curUser:
            emotion = chat["emotion"]

            # text label
            self.messages = ctk.CTkLabel(self, text=self.chat['text'],text_color=textColor, fg_color=msgbox, font=("Inter", 30), wraplength=1000, corner_radius=10)
            self.messages.grid(row=0, column=2, padx=(0, 20), ipadx=10, ipady=10, sticky="e")

            # time and emotion frame
            self.frame = ctk.CTkFrame(self, width=50, height=100, fg_color=bgColor)
            self.frame.grid(row=0, column=1, padx = (0,5), sticky="e")

            # time label
            self.time = ctk.CTkLabel(self.frame, text=chat["time"][11:],text_color=emoji_time, fg_color=bgColor, font=("Inter", 15))
            self.time.grid(row=1, column=0)

            # show emotion
            self.emotion = ctk.CTkLabel(self.frame, text=self.show_emotion(emotion),text_color=emoji_time, fg_color=bgColor, font=("Inter", 30))
            self.emotion.grid(row=0, column=0)

        else:
            emotion = chat["emotion"]

            # text label
            self.messages = ctk.CTkLabel(self, text=chat["text"],text_color=textColor, fg_color=msgbox, font=("Inter", 30), wraplength=1000, corner_radius=10)
            self.messages.grid(row=0, column=1, ipadx=10, ipady=10, sticky="w")

            # recipient's name label display left next to the received message
            profile_logo = ctk.CTkImage(Image.open(f"profilePic\\{friendPic}.png"), size=(60, 60))
            profile = ctk.CTkLabel(self, text="", image=profile_logo)
            profile.grid(row = 0, column = 0, padx=30, sticky='w')

            # time and emotion frame
            self.frame = ctk.CTkFrame(self, width=50, height=100, fg_color=bgColor)
            self.frame.grid(row=0, column=2, padx = (5,0), sticky="w")

            # time label
            self.time = ctk.CTkLabel(self.frame, text=chat["time"][11:],text_color=emoji_time, fg_color=bgColor, font=("Inter", 15))
            self.time.grid(row=1, column=0)
            
            # show emotion
            self.emotion = ctk.CTkLabel(self.frame, text=self.show_emotion(emotion),text_color=emoji_time, fg_color=bgColor, font=("Inter", 30))
            self.emotion.grid(row=0, column=0)
    
    def show_emotion(self, emotion):
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
