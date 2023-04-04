from Libs.Database import Database

def getChat():
    db = Database()
    db.login("MiaKhalifa", "1234")
    db.Chatroom("jordielnino")
    message = db.loadchat("jordielnino")
    return message

print(getChat())