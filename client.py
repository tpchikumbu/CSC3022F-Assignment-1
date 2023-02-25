import os
import socket

serverName = socket.gethostbyname(socket.gethostname())
serverPort = 50000

while True:
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((serverName,serverPort))

    filename = input("Enter the name of the file you want to search for:\n")
    clientSocket.send(filename.encode())

    confirmation = clientSocket.recv(1024)
    return_message = confirmation.decode()
    print(return_message)
    clientSocket.close()

    if ("not" not in return_message):
        down = input("Do you want to download the file (y/n)\n")
        if down:
            clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            clientSocket.connect((serverName,serverPort))

            message = "hello " + filename
            clientSocket.send(message.encode())
            
            
            if not os.path.isdir("./downloads"): os.mkdir("./downloads")
            # implement getting file from the server
            file = open(f"./downloads/{filename}", "w")

            data = clientSocket.recv(1024).decode("utf-8")
            file.write(data)

            file.close()

            print("File received!")

            clientSocket.close()