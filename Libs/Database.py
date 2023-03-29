import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from datetime import datetime
from Libs.Features import Features as features
from Libs.Chat import Chat as chat

class Database:
    def __init__(self):
        # Fetch the service account key JSON file contents
        cred = credentials.Certificate("db_key.json")

        # Initialize the app with a service account, granting admin privileges
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://cube-bc9c8-default-rtdb.asia-southeast1.firebasedatabase.app/'
        })
        self.ref = db.reference('/')

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
        print(username)
        password = str(password)
        # Set pointer to users table
        user_ref = self.ref.child('users')
        users = user_ref.get()
        try:
            for user in users.keys():
                if user == username and users[user]['password'] == password:
                    return db.reference("/users/" + username)
            return "Wrong password or Account not found!"
        except:
            return "No account found in DB!"
        
    def enterDir(self, currentDir, targetDir):
        try:
            a = currentDir.reference(targetDir)
        except:
            a = None
        return a
    
    def listDir(self, currentDir):
        ls = currentDir.get.keys()
        return ls
    
class Features:
    def __init__(self):
        self.ref = db.reference("/")
        self.features = features.Features(db.reference("/"))
        
    def addFriend(self, curr, username):
        return self.features.addFriend(self, curr, username)
    
    def acceptFriendRequest(self, user, target):
        return self.features.acceptFriendRequest(self, user, target)
    
    def rejectFriendRequest(self, user, target):
        return self.features.rejectFriendRequest(self, user, target)
    
class Chat:
    def __init__(self, username):
        self.ref = db.reference("/")
        self.chat = chat.Chat(username, self.ref)
        self.thread = None
        
    def createChatroom(self, friend):
        return self.chat.createChatroom(self, friend)
    
    def send(self, message, friend):
        return self.chat.send(message, friend)
    
    def loadchat(self, friend):
        return self.chat.loadchat(friend)
    
    def countMessage(self, friend):
        return self.chat.countMessage(friend)
    
    def customThread(self, friend, chatroom):
        self.thread = chat.CustomThread(friend, chatroom)
