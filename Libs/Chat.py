import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import time
from threading import Thread
from datetime import datetime

class Chat:
    def __init__(self, userRef, username):

        self.ref = db.reference('/')
        self.username = username
        self.currentFriend = ""
    
    def createChatroom(self, friend): # Create Chatroom when there is no chatroom
        ref = db.reference("/Chatrooms")
        nameLs = [self.username, friend.lower()]
        nameLs.sort()
        name = str(nameLs[0] + "-" + nameLs[1])
        ref.child(name).set({
            "message": {
                "start": {
                    "text": " ",
                    "time": " ",
                    "name": " " ,
                    "emotion": " "
                }
            }
            }
        )
        return nameLs[0] + nameLs[1]
    
    def send(self, message, friend): #send message to a friend
        nameLs = [self.username, friend.lower()]
        nameLs.sort()
        chat = db.reference("/Chatrooms/" + nameLs[0] + "-" + nameLs[1] +"/message")
        sentText = chat.push()

        # Current Date and Time
        now = datetime.now()
        date_time = now.strftime("%m/%d/%Y")

        sentText.set({
            "text": message,
            "time": date_time,
            "name": self.username,
            "emotion": " "
        })

        self.currentFriend = nameLs[1]
        return nameLs[0] + nameLs[1]
    
    def loadchat(self, friend): #load chat from the chatroom
        nameLs = [self.username, friend.lower()]
        nameLs.sort()
        chat = db.reference("/Chatrooms/" + nameLs[0] + "-" + nameLs[1] +"/message")
        message = chat.get()
        self.currentFriend = nameLs[1]
        return message
    
    def countMessage(self, friend): #count the total message in the chatroom
        nameLs = [self.username, friend.lower()]
        nameLs.sort()
        chat = db.reference("/Chatrooms/" + nameLs[0] + "-" + nameLs[1] +"/message")
        message = chat.get()
        keys = message.keys()
        return len(keys)
    
    def changeEmotion(self, emotion, friend):
        nameLs = [self.username, friend.lower()]
        nameLs.sort()
        chat = db.reference("/Chatrooms/" + nameLs[0] + "-" + nameLs[1] +"/message")
        lastText = chat.get().keys()
        chat.child(lastText[-1]).child("emotion").update({"emotion": emotion})
    
class CustomThread(Thread): #Threading to constantly track change in database
    def __init__(self, friend, chatroom):
        Thread.__init__(self)
        self.noOfMessage = 0
        self.friend = friend
        self.exit = False
        self.chatroom = chatroom

    def run(self):
        while True:
            if self.chatroom.countMessage(self.friend) != self.noOfMessage:
                self.chatroom.loadchat(self.friend)
                self.noOfMessage = self.chatroom.countMessage(self.friend)
            time.sleep(1)
    
    