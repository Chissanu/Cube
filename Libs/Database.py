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
                    return Exception("User already existed")
        except:
            pass
        
        # Create User in DB
        new_user_ref.set({
            'name' : name,
            'username' : username,
            'password' : password,
            'pending'  : [""],
            'incoming' : [""],
            'friends'  : [""],
            'bio'      : [""],
            'emotions' : [""],
            'profileImage' : 0,
            'created'  : date_time
        })
        return new_user_ref

    def login(self, username, password):
        username = username.lower()
        password = str(password)
        # Set pointer to users table
        userRef = self.ref.child('users')
        users = userRef.get()
        try:
            for user in users.keys():
                if user == username and users[user]['password'] == password:
                    self.username = user
                    return db.reference("/users/" + username)
            return Exception("Wrong password or Account not found!")
        except:
            return Exception("No account found in DB!")
        
    def changeProfilePic(self,user,target):
        userRef = self.ref.child('users').child(user)
        userRef.update({
            'profileImage' : target
        })
        return
    
    def changeBio(self, user, message):
        userRef = self.ref.child('users').child(user)
        userRef.update({
            'bio' : message
        })
        return
    
    def changeName(self, user, name):
        userRef = self.ref.child('users').child(user)
        userRef.update({
            'name' : name
        })
        return
        
    def deleteUser(self,user):
        userRef = self.ref.child('users').child(user)
        userRef.delete()
        return
        
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
    def addFriend(self, curr, user): # Function to add friend
        return self.features.addFriend(curr,user)
    
    def acceptFriendRequest(self, user, target): # Function to accept friend request
        return self.features.acceptFriendRequest(user,target)
    
    def rejectFriendRequest(self, user, target): # Function to reject friend request
        return self.features.rejectFriendRequest(user, target)
    
    def showFriendList(self,user): #list friendlist
        return self.features.showFriendList(user)
    
    def findFriend(self,user):
        return self.features.findFriend(user)
    
    def getIncoming(self, user):
        return self.features.showIncoming(user)
    
    """
    Function to call Chat.py functions
    """
    
    def Chatroom(self, ref): #initialize chatroom so that you can use other functions
        self.chat = Chat(ref, self.username)
        return self.chat
    
    def createChatroom(self, friend): #create chatroom
        return self.chat.createChatroom(self.username, friend)
    
    def send(self, message, friend): # send message
        return self.chat.send(message, friend)
    
    def loadchat(self, friend): # load chat
        return self.chat.loadchat(friend)
    
    def countMessage(self, friend): # count number of message in the database
        return self.chat.countMessage(friend)
    
    def customThread(self, friend, chatroom): #create thread to look constantly read the number of messages
        self.thread = CustomThread(friend, chatroom)
        self.thread.start()
        
    
