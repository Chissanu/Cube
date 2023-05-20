import socket
import threading

HOST = '192.168.1.113'
PORT = 1105
LISTENER_LIMIT = 5
active_clients = []

class Client:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.msgQueue = []

    def add_message(self, message):
        self.msgQueue.append(message)
        print(f"Message added : {message}")
        print(self.msgQueue)
        
    def setUsername(self, name):
        self.username = name
    
    def connect(self):
        # try except block
        try:
            # Connect to the server
            self.client.connect((HOST, PORT))
            print("Successfully connected to server")
            print("[SERVER] Successfully connected to the server")
        except:
            print(f"Unable to connect to server", f"Unable to connect to server {HOST} {PORT}")

        if self.username != '':
            self.client.sendall(self.username.encode())
        else:
            print("Invalid username", "Username cannot be empty")

        threading.Thread(target=self.listen_for_messages_from_server, args=(self.client, )).start()

        # username_textbox.config(state=tk.DISABLED)
        # username_button.config(state=tk.DISABLED)

    def send_message(self,message):
        #message = message_textbox.get()
        if message != '':
            self.client.sendall(message.encode())
            # message_textbox.delete(0, len(message))
        else:
            print("Empty Message")
    
    def listen_for_messages_from_server(self,client):
        while 1:

            message = self.client.recv(2048).decode('utf-8')
            if message != '':
                username = message.split("~")[0]
                content = message.split('~')[1]

                self.add_message(f"[{username}] {content}")
                
            else:
                print("Error")
