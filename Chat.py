import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

class Chat:
    def __init__(self):
        cred = credentials.Certificate("db_key.json")

        # Initialize the app with a service account, granting admin privileges
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://cube-bc9c8-default-rtdb.asia-southeast1.firebasedatabase.app/'
        })

        self.ref = db.reference('/')
        
    def sendChat(self, user, target):
        # Format userinput to lowercase
        user = user.lower()
        target = target.user()
        
        currUserRef = self.ref.child('users').child(user)
        
    def retrieveChat(self):
        pass
        
    
    