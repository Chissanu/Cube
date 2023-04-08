from Libs import Database as dbb

class chat_test:
    def __init__(self):
        self.username = "c1"
        self.name = "Mia"
        self.password = "1"
        self.friendUsername = "Ruj3146"
        self.friendName = "ruj3146"
        self.friendPassword = "1234"
        self.chat = None
        self.ref = "/"
        self.database = dbb.Database()
        #self.chat = dbb.Chat()
        self.userRef = None
        
    def register(self):
        self.database.createAccount(self.username, self.name, self.password)
        self.database.createAccount(self.friendUsername, self.friendName, self.friendPassword)
        
    def login(self):
        self.ref = self.database.login(self.username, self.password)
        print(self.ref)
        self.userRef = self.ref
        
    def chatroom(self):
        self.chat = self.database.Chatroom(self.userRef)
        return self.chat
        
    def createChatroom(self):
        try:
            self.database.loadchat(self.friendUsername)
        except:
            self.database.createChatroom(self.friendUsername)
            
    def enterChatRoom(self):
        thread = self.database.customThread(self.friendUsername, self.chat)
        while True:
            message = input("Enter message: ")
            self.chat.send(message, self.friendUsername)
            
test = chat_test()
#test.register()
test.login()
test.chatroom()
test.createChatroom()
test.enterChatRoom()
        
        