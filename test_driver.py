from Libs.Database import Database


def genUser():
    db = Database()
    for i in range(5):
        username = 'c' + str(i + 1)
        name = username
        password = str(i + 1)
        db.createAccount(username,name,password)
        
def testDatabase():
    db = Database()
    userInput = int(input("1) Login \n2) Register \n3) Delete \n> "))

    if userInput == 1:
        username = input("Whats username? >")
        password = input("Whats pass? >")
        err = db.login(username,password)
    elif userInput == 3:
        name = input("Name >")
        err = db.deleteUser(name)
    else:
        name = input("What is your name? >")
        username = input("Whats username? >")
        password = input("Whats pass? >")
        err = db.createAccount(username,name,password)
    if err:
        print(err)

def testFeatures():
    db = Database()
    #userInput = int(input("1) Send friend request\n2) Remove friend request\n> "))
    curUser = "c1"
    name = input("Whats friend ID? >")
    err = db.addFriend(curUser,name)
    #err = db.acceptFriendRequest(curUser, name)
    #err = db.rejectFriendRequest(curUser,name)
    #err = db.findFriend(name)
    # err = db.getIncoming(name)
    if err:
        print(err)

def addMultiple():
    db = Database()
    curr = "c1"
    users = ['c2','c3','c4','c5']
    for i in range(4):
        db.addFriend(users[i],curr)
        
def deleteMultiple():
    db = Database()
    users = ['c1','c2','c3','c4','c5']
    for i in range(5):
        db.deleteUser(users[i])
        
#deleteMultiple()       
#genUser()
#addMultiple()
#testDatabase()
#testFeatures()