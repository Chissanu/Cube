import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk
import tkinter.font as tkfont
import emoji
import requests
from io import BytesIO
import os


class ChatFrame(ctk.CTkFrame):
    def __init__(self,master, chat, curUser, friendPic, bgColor, msgbox, textColor, emoji_time, uploadImage, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.chat = chat
        msg = self.chat['text']
        self.curUser = curUser
        self.msgbox = msgbox
        self.textColor = textColor
        self.threshold = 500

        if chat["name"] == self.curUser:
            emotion = chat["emotion"]
            
            if emotion == "":
                print("---no emotion---")
                emotion = "neutral"

            if msg[0:8] in "https://":
                response = requests.get(msg)
                image_data = response.content
                image = Image.open(BytesIO(image_data))
                # Resize the image
                width, height = image.size
                if width > self.threshold or height > self.threshold:
                    # Calculate the aspect ratio
                    ratio = min(self.threshold / width, self.threshold / height)

                    # Calculate the new dimensions
                    new_width = int(width * ratio)
                    new_height = int(height * ratio)
                    image.thumbnail((new_width, new_height))
                
                tk_image =  ImageTk.PhotoImage(image)
                label = ctk.CTkLabel(self, image=tk_image, text="")
                label.grid(row=0, column=2, padx=(0, 20), sticky="e")  # Display the image in the grid
            elif uploadImage:
                uploadImage = Image.open(self.chat["text"])

                # Resize the image
                width, height = uploadImage.size
                if width > self.threshold or height > self.threshold:
                    # Calculate the aspect ratio
                    ratio = min(self.threshold / width, self.threshold / height)

                    # Calculate the new dimensions
                    width = int(width * ratio)
                    height = int(height * ratio)

                tk_image = ctk.CTkImage(uploadImage, size=(width, height))
                showImage = ctk.CTkLabel(self, image=tk_image, text="")
                showImage.grid(row=0, column=2, padx=(0, 20), sticky="e")
            else:
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
            self.emotion = ctk.CTkLabel(self.frame, text=self.convert_emotion(emotion),text_color=emoji_time, fg_color=bgColor, font=("Inter", 30))
            self.emotion.grid(row=0, column=0)

        else:
            emotion = chat["emotion"]

            if msg[0:8]=="https://":
                response = requests.get(msg)
                image_data = response.content
                image = Image.open(BytesIO(image_data))
                
                width, height = image.size
                # Resize the image
                if width > self.threshold or height > self.threshold:
                    # Calculate the aspect ratio
                    ratio = min(self.threshold / width, self.threshold / height)

                    # Calculate the new dimensions
                    new_width = int(width * ratio)
                    new_height = int(height * ratio)
                    image.thumbnail((new_width, new_height))
                
                tk_image =  ImageTk.PhotoImage(image)
                label = ctk.CTkLabel(self, image=tk_image, text="")
                label.grid(row=0, column=1)  # Display the image in the grid
            else:
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
            self.emotion = ctk.CTkLabel(self.frame, text=self.convert_emotion(emotion),text_color=emoji_time, fg_color=bgColor, font=("Inter", 30))
            self.emotion.grid(row=0, column=0)
    
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

