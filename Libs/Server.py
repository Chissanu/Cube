import socket
import threading

HOST = '127.0.0.1'
PORT = 1105
LISTENER_LIMIT = 5
active_clients = []

class Server:
    def __init__(self):
        self.main()
        
        # Main function
    def main(self):

        # Creating the socket class object
        # AF_INET: we are going to use IPv4 addresses
        # SOCK_STREAM: we are using TCP packets for communication
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Creating a try catch block
        try:
            # Provide the server with an address in the form of
            # host IP and port
            server.bind((HOST, PORT))
            print(f"Running the server on {HOST} {PORT}")
        except:
            print(f"Unable to bind to host {HOST} and port {PORT}")

        # Set server limit
        server.listen(LISTENER_LIMIT)

        # This while loop will keep listening to client connections
        while 1:

            client, address = server.accept()
            print(f"Successfully connected to client {address[0]} {address[1]}")

            threading.Thread(target=self.client_handler, args=(client, )).start()
    
    # Function to listen for upcoming messages from a client
    def listen_for_messages(self,client, username):

        while 1:

            message = client.recv(2048).decode('utf-8')
            if message != '':
                
                final_msg = username + '~' + message
                self.send_messages_to_all(final_msg)

            else:
                print(f"The message send from client {username} is empty")


    # Function to send message to a single client
    def send_message_to_client(self, client, message):

        client.sendall(message.encode())

    # Function to send any new message to all the clients that
    # are currently connected to this server
    def send_messages_to_all(self,message):
        
        for user in active_clients:

            self.send_message_to_client(user[1], message)

    # Function to handle client
    def client_handler(self, client):
        
        # Server will listen for client message that will
        # Contain the username
        while 1:

            username = client.recv(2048).decode('utf-8')
            if username != '':
                active_clients.append((username, client))
                prompt_message = "SERVER~" + f"{username} added to the chat"
                self.send_messages_to_all(prompt_message)
                break
            else:
                print("Client username is empty")

        threading.Thread(target=self.listen_for_messages, args=(client, username, )).start()
        
class Client:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def add_message(self, message):
        # message_box.config(state=tk.NORMAL)
        # message_box.insert(tk.END, message + '\n')
        # message_box.config(state=tk.DISABLED)
        pass
    
    def connect(self):

        # try except block
        try:
            # Connect to the server
            self.client.connect((HOST, PORT))
            print("Successfully connected to server")
            print("[SERVER] Successfully connected to the server")
        except:
            print(f"Unable to connect to server", f"Unable to connect to server {HOST} {PORT}")

        username = input("username: ")
        if username != '':
            self.client.sendall(username.encode())
        else:
            print("Invalid username", "Username cannot be empty")

        threading.Thread(target=self.listen_for_messages_from_server, args=(self.client, )).start()

        # username_textbox.config(state=tk.DISABLED)
        # username_button.config(state=tk.DISABLED)

    def send_message(self):
        #message = message_textbox.get()
        message = input("Message >")
        if message != '':
            self.client.sendall(message.encode())
            # message_textbox.delete(0, len(message))
        else:
            print("Empty Message")
    
    def listen_for_messages_from_server(self):
        while 1:

            message = self.client.recv(2048).decode('utf-8')
            if message != '':
                username = message.split("~")[0]
                content = message.split('~')[1]

                print("[{username}] {content}")
                #add_message(f"[{username}] {content}")
                
            else:
                print("Error")
