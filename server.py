import os
import threading
from socket import *
import serv_utils
CURRENT_USERS = []

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
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}\n")

def file_handling(conn, addr):
    with conn:
        print(f"Connected by {addr}")
        loggedIn = False
        handshake = False
        
        #logging in
        # should receive msg like LOGIN\tusername\tpassword
        for i in range(1,4):
            # the first message from the client should be a login message
            recv_msg = conn.recv(1024).decode()
            recv_args = recv_msg.split("\t")

            # if the message received is not a login 
            if recv_args[0] != "LOGIN":
                send_msg = "ERROR\tUser must login first"
                conn.send(send_msg.encode())
            else:
                username, password, log = str(recv_args[1]), str(recv_args[2]), str(recv_args[3])
                print(log)
                response = serv_utils.login(username, password)
                loggedIn = response[0]
                conn.send(response[1].encode())
                if loggedIn:
                    CURRENT_USERS.append(username)
                    break
        

        if loggedIn:
            print(f"user {username} has been successfully logged in")
        else:
            print("user is not logged in and interaction was unsucessful")
        
        recv_msg = conn.recv(1024).decode()
        print(recv_msg)
                    



if __name__ == "__main__":
    main()