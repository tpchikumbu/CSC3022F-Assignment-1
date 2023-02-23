import os
import threading
from socket import *

def file_handling (sock, addr):
    while True:
        message = sock.recv(1024).decode()
        if message.find("download") == 0:
            directive, filename = message.split(" ")
            print(f"downloading file: {filename}")
            # implement sending the file onto the socket
            print(f"Sending ... {filename}")

            cFile = open(f"./serverfiles/{filename}", "r")
            data = cFile.read()

            sock.send(data.encode("utf-8"))
            cFile.close()

            print("File sent!")
        
        else:
            print(f"Request received for file with filename: {message}")
            x = os.path.isfile(f"./serverfiles/{message}")

            return_message = "File found" if x else "File not found"
            sock.send(return_message.encode())
            break
    print("closing")
    sock.close()

def main () : 
    #IP = gethostbyname(gethostname())
    serverPort = 12000
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