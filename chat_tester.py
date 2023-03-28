from Database import Database as dbb
from Features import Features as ft
import firebase_admin
from firebase_admin import db
from firebase_admin import credentials
import Chat

class chat_test:
    def __init__(self):
        self.username = "Tonkhaow"
        self.name = "Ton"
        self.password = "1234"
        self.friendUsername = "Nigger"
        self.friendName = "Nigg"
        self.friendPassword = "1234"
        # Fetch the service account key JSON file contents
        cred = credentials.Certificate("db_key.json")
        # Initialize the app with a service account, granting admin privileges
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://cube-bc9c8-default-rtdb.asia-southeast1.firebasedatabase.app/'
        })
        self.ref = db.reference('/')
        self.chat = None
        self.database = dbb()
        
    def register(self):
        self.database.createAccount(self.username, self.name, self.password)
        self.database.createAccount(self.friendUsername, self.friendName, self.friendPassword)
        
    def login(self):
        self.database.login(self.username, self.password)
        self.ref = self.database.reference('/users/'+ self.username)
        
    def createChatroom(self):
        self.chat = Chat.Chat(self.username)
        try:
            self.chat.loadchat(self.friendUsername)
        except:
            self.chat.createChatroom(self.friendUsername)
            
    def enterChatRoom(self):
        thread = Chat.CustomThread(self.friendUsername, self.chat)
        thread.start()
        while True:
            message = input("Enter message: ")
            self.chat.send(message, self.friendUsername)
            
test = chat_test()
test.register()
test.login()
test.createChatroom()
test.enterChatRoom()
        
        