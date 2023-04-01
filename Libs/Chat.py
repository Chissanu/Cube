import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import time
from threading import Thread

class Chat:
    def __init__(self, userRef):

        self.ref = db.reference('/')
        print(userRef.get())
        self.username = userRef
        self.currentFriend = ""
        
    def getPrev(self, reference):
        for key, value in reference.get().items():
            if val == value:
                return key
    
    def createChatroom(self, username, friend): # Create Chatroom when there is no chatroom
        ref = db.reference("/Chatrooms")
        
        print(username)
        nameLs = [username, friend.lower()]
        nameLs.sort()
        name = str(nameLs[0] + "-" + nameLs[1])
        ref.child(name).set({
            "message": {
                "start": {
                    "text": " ",
                    "time": " ",
                    "name": " " 
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
        sentText.set({
            "text": message,
            "time": time.time(),
            "name": self.username
        })
        self.currentFriend = nameLs[1]
        return nameLs[0] + nameLs[1]
    
    def loadchat(self, friend): #load chat from the chatroom
        nameLs = [self.username, friend.lower()]
        nameLs.sort()
        chat = db.reference("/Chatrooms/" + nameLs[0] + "-" + nameLs[1] +"/message")
        message = chat.get()
        keys = message.keys()
        for i in keys:
            current = message[i]
            if current["name"] != " ":
                print(current["name"] + ": " + current["text"])
        self.currentFriend = nameLs[1]
        return nameLs[0] + nameLs[1]
    
    def countMessage(self, friend): #count the total message in the chatroom
        nameLs = [self.username, friend.lower()]
        nameLs.sort()
        chat = db.reference("/Chatrooms/" + nameLs[0] + "-" + nameLs[1] +"/message")
        message = chat.get()
        keys = message.keys()
        return len(keys)
    
class CustomThread(Thread): #Threading to constantly track change in database
    def __init__(self, friend, chatroom):
        Thread.__init__(self)
        self.noOfMessage = 0
        self.friend = friend
        self.exit = False
        self.chatroom = chatroom

    def run(self):
        while True:
            if self.chatroom.messageNo(self.friend) != self.noOfMessage:
                self.chatroom.loadChat(self.friend)
                self.noOfMessage = self.chatroom.messageNo(self.friend)
            time.sleep(1)
    
    