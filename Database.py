import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from datetime import datetime

class Database:
    def __init__(self):
        # Fetch the service account key JSON file contents
        cred = credentials.Certificate("db_key.json")

        # Initialize the app with a service account, granting admin privileges
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://cube-bc9c8-default-rtdb.asia-southeast1.firebasedatabase.app/'
        })
        self.ref = db.reference('/')

    def createAccount(self, username, password):
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
            'username' : username,
            'password' : password,
            'friends'  : [],
            'created'  : date_time
        })

    def login(self, username, password):
        # Set pointer to users table
        user_ref = self.ref.child('users')
        users = user_ref.get()
        try:
            for user in users.keys():
                if users[user]['username'] == username and users[user]['password'] == password:
                    return "Success"
            return "Wrong password or Account not found!"
        except:
            return "No account found in DB!"