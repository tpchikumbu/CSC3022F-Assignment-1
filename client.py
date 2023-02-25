import os
import socket
from tqdm import tqdm

serverName = socket.gethostbyname(socket.gethostname())
serverPort = 12000
i = 0

while i == 0:
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((serverName,serverPort))

    operation = input("Choose an operation:\n1. [u]pload\n2. [d]ownload\n")
    #clientSocket.send(operation.encode())

    #confirmation = clientSocket.recv(1024)
    #return_message = confirmation.decode()
    #print(return_message)

    #if ("not" not in return_message):
    match operation[0]:
        case "u":
            print ("\nuploading file\n")
            file_name = input("Enter the file to be uploaded.\n")
            file_size = os.path.getsize(file_name)
            message = f"upload\t{file_name }\t{file_size}"
            clientSocket.send(message.encode("utf-8"))

            bar = tqdm(range(file_size), f"Sending {file_name}", unit ="B", unit_scale=True, unit_divisor = 1024)
            f = open(file_name, "rb")
            while True:
                message = f.read(4096)

                if not message:
                    break

                clientSocket.sendall(message)
                #msg = clientSocket.recv(1024).decode("utf-8")
                bar.update(len(message))

            f.close
            clientSocket.close()
        case "d":
            print ("\ndownloading file\n")
        case _:
            print ("\nERROR: closing connection\n")
            clientSocket.close()
    i += 1
    

    """if ("not" not in return_message):
        down = input("Do you want to download the file (y/n)\n")
        if down:
            clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            clientSocket.connect((serverName,serverPort))

            message = "download " + filename 
            clientSocket.send(message.encode())
            

            if not os.path.isdir("./downloads"): os.mkdir("./downloads")
            # implement getting file from the server
            file = open(f"./downloads/{filename}", "w")

            data = clientSocket.recv(1024).decode("utf-8")
            file.write(data)

            file.close()

            print("File received!")

            clientSocket.close()"""
