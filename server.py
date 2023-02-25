import os
import threading
from socket import *
#from . import serv_utils

def main () : 
    #IP = gethostbyname(gethostname())
    serverPort = 50000
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