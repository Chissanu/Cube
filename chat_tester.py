from Libs import Database as dbb

class chat_test:
    def __init__(self):
        self.username = "MiaKhalifa"
        self.name = "Mia"
        self.password = "1234"
        self.friendUsername = "JordiElnino"
        self.friendName = "Jordi"
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
        return self.database.Chatroom(self.userRef)
        
    def createChatroom(self):
        try:
            self.database.loadchat(self.friendUsername)
        except:
            self.database.createChatroom(self.friendUsername)
            
    def enterChatRoom(self):
        thread = self.database.CustomThread(self.friendUsername, self.chat)
        thread.start()
        while True:
            message = input("Enter message: ")
            self.chat.send(message, self.friendUsername)
            
test = chat_test()
#test.register()
test.login()
test.chatroom()
test.createChatroom()
test.enterChatRoom()
        
        