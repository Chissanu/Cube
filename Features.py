import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

class Features:
    def __init__(self):
        # Fetch the service account key JSON file contents
        cred = credentials.Certificate("db_key.json")

        # Initialize the app with a service account, granting admin privileges
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://cube-bc9c8-default-rtdb.asia-southeast1.firebasedatabase.app/'
        })

        self.ref = db.reference('/')
    
    # Chedck if value contain empty string
    def containNulls(self, arr):
        for val in arr:
            if val == "":
                return True
    
    # Check if array is empty if yes it will add empty string to represent NULL
    def addNull(self,arr):
        if not arr:
            arr = [""]
            return arr
        else:
            return arr
    
    # Remove empty string and return empty array
    def removeNull(self,arr):
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
        currUserPending = self.removeNull(currUserPending)
        
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
                    friendIncoming = self.removeNull(friendIncoming)
                    friendIncoming.append(curr)
                    friendIncomingRef.update({
                        'incoming' : friendIncoming
                    })
                    return "Success"
            return "No user with that ID"
        except Exception as e:
            print(e)
    
    """
    This function will accept friend request by query user and target data
    and check if possible or not then update data in DB
    INPUT: CurrentUser, TargetUser
    OUTPUT: Error if exists
    """      
    def acceptFriendRequest(self, user, target):
        # Format user and target to lowercase
        user = user.lower()
        target = target.lower()
        
        # Query current user data
        currUserRef = self.ref.child('users').child(user)
        currUserIncoming = currUserRef.get()['incoming']
        currUserFriends = currUserRef.get()['friends']
        
        # Query target user data
        targetUserRef = self.ref.child('users').child(target)
        targetUserPending = targetUserRef.get()['pending']
        targetUserFriend = targetUserRef.get()['friends']
        
        # Check if list has empty string
        err = self.containNulls(currUserIncoming)
        if err:
            return "You have no friend request!"
        
        for val in currUserIncoming:
            if val == target:
                # Remove from incoming array
                currUserIncoming.remove(target)
                
                # Append to friend list
                currUserFriends = self.removeNull(currUserFriends)
                currUserFriends.append(target)
                
                # Check if list is empty
                currUserIncoming = self.addNull(currUserIncoming)
                
                # Update current user friend list 
                currUserRef.update({
                    'incoming' : currUserIncoming,
                    'friends'  : currUserFriends
                })
                
                # Remove empty string and append to target friend list
                targetUserFriend = self.removeNull(targetUserFriend)
                targetUserFriend.append(user)
                
                # Remove from pending and check if there is value in list left
                targetUserPending.remove(user)
                targetUserPending = self.addNull(targetUserPending)
                targetUserRef.update({
                    'friends' : targetUserFriend,
                    'pending' : targetUserPending
                })
                return "Accepted"
        
    """
    This function will reject friend request by quering current and target user
    to check possibility and it will remvoe incoming friend request and pending
    friend request
    INPUT: CurrentUser, TargetUser
    OUTPUT: Error if exists
    """
    def rejectFriendRequest(self, user, target):
        # Format user and target to lowercase
        user = user.lower()
        target = target.lower()
        
        # Query current user data
        currUserRef = self.ref.child('users').child(user)
        currUserIncoming = currUserRef.get()['incoming']
        
        # Query target data
        targetUserRef = self.ref.child('users').child(target)
        targetUserPending = targetUserRef.get()['pending']
        
        for val in currUserIncoming:
            if val == target:
                # Remove from incoming array for current user
                currUserIncoming.remove(target)
                currUserIncoming = self.addNull(currUserIncoming)
                
                # Remove from pending array for target
                targetUserPending.remove(user)
                targetUserPending = self.addNull(targetUserPending)
                
                currUserRef.update({
                    'incoming' : currUserIncoming
                })
                
                targetUserRef.update({
                    'pending' : targetUserPending
                })
                return "Success"
        