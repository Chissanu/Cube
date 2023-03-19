import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from datetime import datetime

# Fetch the service account key JSON file contents
cred = credentials.Certificate("Cognitive\Cube\db_key.json")

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://cube-bc9c8-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

ref = db.reference('/')

def createAccount(username, password):
    # Current Date and Time
    now = datetime.now()
    date_time = now.strftime("%m/%d/%Y")
    
    # Set pointer to users table
    user_ref = ref.child('users')
    users = user_ref.get()

    #Check if account exists in DB
    try:
        for user in users.keys():
            if users[user]['username'] == username:
                return "User already existed!"
    except:
        pass
    
    # Create User in DB
    user_ref.push({
        'username' : username,
        'password' : password,
        'created'  : date_time
    })

def login(username, password):
    # Set pointer to users table
    user_ref = ref.child('users')
    users = user_ref.get()
    try:
        for user in users.keys():
            if users[user]['username'] == username and users[user]['password'] == password:
                return "Success"
        return "Account not found"
    except:
        return "No account found in DB"
    

"""
This function is for creating an account and it will verify if
the user is already exists in the DB or not
INPUT: username, password
OUTPUT: Error if exists

"""
userInput = int(input("1) Login \n2) Register \n>"))
name = input("Whats username? >")
password = input("Whats pass? >")

if userInput == 1:
    err = login(name,password)
else:
    err = createAccount(name,password)
if err:
    print(err)
