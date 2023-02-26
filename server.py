import os
import threading
from socket import *
import sys
from hashlib import md5
from tqdm import tqdm
#from . import serv_utils

FORMAT = "utf-8"
server_data_files = "serverfiles"
serverPort = 4000

def md5sum(filename):
    hash = md5()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(128 * hash.block_size), b""):
            hash.update(chunk)
    return hash.hexdigest()

def file_handling (sock, addr):
    # Send the starting message from the server to the user
    sock.send("OK@Welcome to the File Sever.\n Enter your Username and Password seperated by a space:".encode(FORMAT))
    # this part will detect if the user is in the server
    message = sock.recv(1024).decode(FORMAT)
    message =  message.split("\n")
    print(message[0])
    proceed = "OKAY"







    # the name and the password will be uploaded onto the metadata file that will consist of the data of the user
    # their logging name and their password



    # data send to the user 

    if(proceed =="OK"):
        data = "OK@"
        data += "1: List all the files from the server.\n"
        data += "2 <path>: Upload a file to the server.\n"
        data += "3 <filename>: Delete a file from the server.\n"
        data += "LOGOUT: Disconnect from the server.\n"
        data += "HELP: List all the commands."

        sock.send(data.encode(FORMAT))

        while True:
            data = sock.recv(1024).decode(FORMAT)
            data =  data.split("@")
            command = data[0]

            if command == "1":
                files = os.listdir(server_data_files)
                send_data_user = "OK@" # this will be a decoding mechanism that the user will use
                if len(files) == 0:
                    send_data_user += "The server directory is empty"
                else:
                    send_data_user += "\n".join(f for f in files) # listing the files in the directory 
                sock.send(send_data_user.encode(FORMAT))
            if command == "2":
                name,text = data[1],data[2] # the name of the file and the context of the 
                bar = tqdm(range(1000), f"Receiving {name}", unit="B", unit_scale=True, unit_divisor=1024)
                f = open(f"./serverfiles/recv_{name}", "wb")
                while True:
                    if not text:
                        break
                    f.write(text)
                    bar.update(len(text))
                f.close()  
            if command == "3":
                files = os.listdir(server_data_files)
                send_data = "OK@"
                filename = data[1]

                if len(files) == 0:
                    send_data += "The server directory is empty"
                else:
                    if filename in files:
                        os.system(f"rm {server_data_files}/{filename}")
                        send_data += "File deleted successfully."
                    else:
                        send_data += "File not found."

                sock.send(send_data.encode(FORMAT))
            sock.close()

def main () : 
    print("Starting...")
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind((gethostbyname(gethostname()),serverPort))
    serverSocket.listen(1)
    print("The server is ready to connect.\n")
    while True:
        connectSocket, addr = serverSocket.accept()
        cThread = threading.Thread(target=file_handling, args=(connectSocket, addr))
        cThread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

if __name__ == "__main__":
    main()