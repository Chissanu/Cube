from Libs.Database import Database

def getChat():
    db = Database()
    db.login("MiaKhalifa", "1234")
    db.Chatroom("jordielnino")
    return db.loadchat("jordielnino")

print(getChat())