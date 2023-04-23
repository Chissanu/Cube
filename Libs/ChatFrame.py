import customtkinter as ctk
import tkinter as tk

class ChatFrame(tk.Frame):
    def __init__(self,parent,chat):
        super().__init__(parent)
        self.chat = chat
        
        # print(chat)
        self.msg_box = tk.Frame(self,width=1370,height=200,background="cyan")
        self.messages = ctk.CTkLabel(self, text=self.chat['text'],text_color="#000000", bg_color="#e9f2b9", font=("Inter", 15))
        self.messages.grid(row=0, column=1, padx=32, pady=0, sticky="ne")