import customtkinter
import threading as td
from Dimension_dev import Detection
# install here - https://pypi.org/project/emoji/
# Guidelines - https://github.com/ikatyang/emoji-cheat-sheet/blob/master/README.md#smileys--emotion
from emoji import emojize

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("minimal example app")
        self.minsize(400, 300)

        self.emoji = emojize(":smile:", language = 'alias')
        self.label = customtkinter.CTkLabel(text = self.emoji)

        self.button = customtkinter.CTkButton(master=self, command=self.button_callback)
        self.button.pack(padx=20, pady=20)

    def button_callback(self):
        print("button pressed")


    def pack_label(self):
        self.label.pack(padx=20, pady=20)

    def update_label(self):
        detect = Detection()
        detect.timedDetection("http://192.168.1.101:4747/mjpegfeed", "C:\\Users\\Firesoft\\Documents\\Computing\\Testing_Grounds\\trained_models\\model_201.pt", 5)
        result = detect.getMostOccuringEmotion()
        if result == "happy":
            emoji = emojize(":smile:", language = 'alias')
            self.label.config(text = emoji)
        else:
            emoji = emojize(":neutral_face:", language = 'alias')
            self.label.config(text = emoji)

    def run(self):
        thread_1 = td.Thread(target = self.pack_label)
        thread_2 = td.Thread(target = self.update_label)

        thread_1.start()
        thread_2.start()

app = App()
app.run()

app.mainloop()