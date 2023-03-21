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
        
    def checkNull(self,arr):
        for val in arr:
            if val == "":
                arr.pop(0)
        return arr

    """
    This function will add friend based from friend ID
    INPUT: CurrentUserID, FriendUserID
    OUTPUT: Error if exists
    """
    def addFriend(self, curr, username):
        # Change input to lowercase
        curr = curr.lower()
        username = username.lower()
        
        # Safe Guard to prevent add themselves
        if curr == username:
            return "You can't add yourself!"
        
        # Set pointer to users
        users_ref = self.ref.child('users')
        
        # Set Reference to current user
        currUserRef = self.ref.child('users').child(curr)

        # Query current user data
        currUser = currUserRef.get()
        
        # Query all users
        users = users_ref.get()

        # Check if user have 1 pending or multiple if single it will convert to array and put in array
        currUserPending = currUser['pending']
        currUserPending = self.checkNull(currUserPending)
        
        #Update database to show sending request on current user and incoming on receiver
        try:
            for user in users.keys():
                if user == username:
                    # Check if user alreadt add this friend
                    if username not in currUserPending:
                        currUserPending.append(username)
                    
                    # Update value to DB
                    currUserRef.update({
                        'pending' : currUserPending
                    })
                    
                    # Set reference to friend data
                    friendIncomingRef = self.ref.child('users').child(username)
                    
                    # Query incoming friend request of the friend
                    friendIncoming = friendIncomingRef.get()['incoming']
                    friendIncoming = self.checkNull(friendIncoming)
                    friendIncoming.append(curr)
                    friendIncomingRef.update({
                        'incoming' : friendIncoming
                    })
                    return "Success"
            return "No user with that ID"
        except Exception as e:
            print(e)
    
    def rejectFriendRequest(self):
        pass