import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from datetime import datetime

class Features:
    def __init__(self):
        # Fetch the service account key JSON file contents
        cred = credentials.Certificate("db_key.json")

        # Initialize the app with a service account, granting admin privileges
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://cube-bc9c8-default-rtdb.asia-southeast1.firebasedatabase.app/'
        })

        self.ref = db.reference('/')

    def addFriend(self, curr, username):
        # Set pointer to users table
        user_ref = self.ref.child('users').child('-NQtPPeETgTXKu49GUjr').get()
        print(user_ref)
        # users = user_ref.get()
        
        # currUser = user_ref.order_by_child('username')
        # print(user_ref.order_by_child('users').equal_to("Oak").get())
        # try:
        #     for user in users.keys():
        #         if users[user]['username'] == username:
        #             return "Success"
        #     return "Account not found"
        # except:
        #     return "No account found in DB"