import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

class Features:
    def __init__(self, db):
        self.ref = db
    
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
            return Exception("You can't add yourself!")
        
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
        
        currUserIncoming = currUser['incoming']
        currUserIncoming = self.removeNull(currUserIncoming)
        
        currUserFriend = currUser['friends']
        currUserFriend = self.removeNull(currUserFriend)
        
                            
        # Set reference to friend data
        friendIncomingRef = self.ref.child('users').child(username)
        
        # Query friends of friend
        friendFriends = friendIncomingRef.get()['friends']
        
        friendFriends = self.removeNull(friendFriends)
        
        # Query incoming friend request of the friend
        friendIncoming = friendIncomingRef.get()['incoming']
        
        # Query pending friend request of the friend
        friendPending = friendIncomingRef.get()['pending']
        
        #Update database to show sending request on current user and incoming on receiver
        try:
            for user in users.keys():
                if user == username:
                    # Check if user already add this friend
                    if username not in currUserPending:
                        currUserPending.append(username)
                    
                    if username in currUserIncoming:
                        currUserFriend.append(username)
                        currUserIncoming.remove(username)
                        friendFriends.append(curr)
                        friendPending.remove(curr)
                        currUserPending.remove(username)
                    else:
                        friendIncoming = self.removeNull(friendIncoming)
                        friendIncoming.append(curr) 
                    
                    # It will add empty string to array if the list is empty
                    currUserFriend = self.addNull(currUserFriend)
                    currUserIncoming = self.addNull(currUserIncoming)
                    currUserPending = self.addNull(currUserPending)
                    # Update value to DB
                    currUserRef.update({
                        'pending' : currUserPending,
                        'friends' : currUserFriend,
                        'incoming': currUserIncoming,
                    })
                    
                    friendIncoming = self.addNull(friendIncoming)
                    friendPending = self.addNull(friendPending)
                    friendFriends = self.addNull(friendFriends)
                                
                    friendIncomingRef.update({
                        'friends'  : friendFriends,
                        'incoming' : friendIncoming,
                        'pending'  : friendPending
                    })
                    return "Success"
            return Exception("No user with that ID")
        except Exception as e:
            print(e)
    
    def findFriend(self, user):
        # Convert to lowercase
        user = user.lower()
        
        # Query users
        userList = self.ref.child('users').get()
        
        # Check if user exist in users db
        if user in userList:
            data = userList[user]
            friendData = {
                'name' : data['name'],
                'username' : data['username'],
                'profileImage' : data['profileImage'],
                'bio' : data['bio'],
                'emotions' : data['emotions']  
            }
            return friendData
        else:
            return Exception("Not found")
        
    def getTargetProfilePic(self,target):
        # Convert to lowercase
        target = target.lower()
        
        # Set pointer
        targetRef = self.ref.child('users').child(target)
        
        return targetRef.get()['profileImage']
     
    def showIncoming(self,user):
        # Convert to lowercase
        user = user.lower()
        
        # Query current user data
        userRef = self.ref.child('users').child(user)
        
        userIncomingReq = userRef.get()['incoming']
        
        # Check if user has any incoming requests
        if userIncomingReq[0] == "":
            return None
        else:
            return userIncomingReq
    
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
            return Exception("You have no friend request!")
        
        for val in currUserIncoming:
            if val == target:
                # Remove from incoming array
                currUserIncoming.remove(target)
                
                # Append to friend list
                currUserFriends = self.removeNull(currUserFriends)
                tempDict = {}
                count = 0
                for index, value in enumerate(currUserFriends):
                    count += 1
                    tempDict[index] = value
                
                tempDict[count] = val

                print(tempDict)
                # Check if list is empty
                currUserIncoming = self.addNull(currUserIncoming)
                
                # Update current user friend list 
                currUserRef.update({
                    'incoming' : currUserIncoming,
                    'friends'  : tempDict
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
    
    def showFriendList(self, user):
        # Format user to lowercase
        user = user.lower()
        
        # Query current user data
        currUserRef = self.ref.child('users').child(user)
        return currUserRef.get()['friends']
        