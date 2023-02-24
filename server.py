import os
from socket import *
from . import serv_utils

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(("",serverPort))
serverSocket.listen(1)
print("The server is ready to receive")

while True:
    connectSocket, addr = serverSocket.accept()
    message = connectSocket.recv(1024).decode()
    if message.find("download") == 0:
        directive, filename = message.split(" ")
        print(f"downloading file: {filename}")
        # implement sending the file onto the socket
        print(f"Sending ... {filename}")

        file = open(f"./serverfiles/{filename}", "r")
        data = file.read()

        connectSocket.send(data.encode("utf-8"))
        file.close()

        print("File sent!")
    
    else:
        print(f"Request received for file with filename: {message}")
        x = os.path.isfile(f"./serverfiles/{message}")

        return_message = "File found" if x else "File not found"
        connectSocket.send(return_message.encode())

    connectSocket.close()
