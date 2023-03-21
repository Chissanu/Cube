from Database import Database
from Features import Features

"""
This function is for creating an account and it will verify if
the user is already exists in the DB or not
INPUT: username, password
OUTPUT: Error if exists
"""
def testDatabase():
    db = Database()
    userInput = int(input("1) Login \n2) Register \n> "))
    name = input("What is your name? >")
    username = input("Whats username? >")
    password = input("Whats pass? >")

    if userInput == 1:
        err = db.login(username,password)
    else:
        err = db.createAccount(username,name,password)
    if err:
        print(err)
        

def testFeatures():
    func = Features()
    #userInput = int(input("1) Send friend request\n2) Remove friend request\n> "))
    curUser = "c2"
    name = input("Whats friend ID? >")
    err = func.addFriend(curUser,name)
    if err:
        print(err)
    
testFeatures()
#testDatabase()