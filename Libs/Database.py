import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from datetime import datetime
from Libs.Features import Features
from Libs.Chat import Chat, CustomThread

class Database:
    def __init__(self):
        # Fetch the service account key JSON file contents
        cred = credentials.Certificate("db_key.json")

        # Initialize the app with a service account, granting admin privileges
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://cube-bc9c8-default-rtdb.asia-southeast1.firebasedatabase.app/'
        })
        self.ref = db.reference('/')
        
        self.features = Features(self.ref)
        
        self.chat = None
        self.username = None
        #self.thread = None

    def createAccount(self, username, name, password):
        username = username.lower()
        # Check if username is empty
        if username == "":
            return "Name must not be empty!"
        # Current Date and Time
        now = datetime.now()
        date_time = now.strftime("%m/%d/%Y")
        
        # Set pointer to users table
        users_ref = db.reference('users')
        
        # Create new table with new username
        new_user_ref = users_ref.child(username)
        
        # Query users
        users = users_ref.get()        
        #Check if account exists in DB
        try:
            for user in users.keys():
                if users[user]['username'] == username:
                    return "User already existed!"
        except:
            pass
        
        # Create User in DB
        new_user_ref.set({
            'name' : name,
            'password' : password,
            'pending'  : [""],
            'incoming' : [""],
            'friends'  : [""],
            'created'  : date_time
        })

    def login(self, username, password):
        username = username.lower()
        password = str(password)
        # Set pointer to users table
        user_ref = self.ref.child('users')
        users = user_ref.get()
        try:
            for user in users.keys():
                if user == username and users[user]['password'] == password:
                    self.username = username
                    return db.reference("/users/" + username)
            return Exception("Wrong password or Account not found!")
        except:
            return Exception("No account found in DB!")
        
    def enterDir(self, currentDir, targetDir):
        try:
            a = currentDir.reference(targetDir)
        except:
            a = None
        return a
    
    def listDir(self, currentDir):
        ls = currentDir.get.keys()
        return ls
    
    """"
    Function to call Features.py fuctions
    """
    def addFriend(self, curr, user):
        return self.features.addFriend(curr,user)
    
    def acceptFriendRequest(self, user, target):
        return self.features.acceptFriendRequest(user,target)
    
    def rejectFriendRequest(self, user, target):
        return self.features.rejectFriendRequest(user, target)
    
    def showFriendList(self,user):
        return self.features.showFriendList(user)
    
    def Chatroom(self, ref):
        self.chat = Chat(ref)
    
    def createChatroom(self, friend):
        return self.chat.createChatroom(self.username, friend)
    
    def send(self, message, friend):
        return self.chat.send(message, friend)
    
    def loadchat(self, friend):
        return self.chat.loadchat(friend)
    
    def countMessage(self, friend):
        return self.chat.countMessage(friend)
    
    def customThread(self, friend, chatroom):
        self.thread = CustomThread(friend, chatroom)
# class Chat:
#     def __init__(self, username):
#         self.ref = db.reference("/")
#         self.chat = chat.Chat(username, self.ref)
#         self.thread = None
        
#     def createChatroom(self, friend):
#         return self.chat.createChatroom(self, friend)
    
#     def send(self, message, friend):
#         return self.chat.send(message, friend)
    
#     def loadchat(self, friend):
#         return self.chat.loadchat(friend)
    
#     def countMessage(self, friend):
#         return self.chat.countMessage(friend)
    
#     def customThread(self, friend, chatroom):
#         self.thread = chat.CustomThread(friend, chatroom)
