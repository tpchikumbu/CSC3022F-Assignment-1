import os
import threading
from socket import *
import serv_utils
CURRENT_USERS = []


def main () : 

    print("Starting...")
    serverPort = 50000
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

## HANDSHAKE PROTOCOL
        # receives handshaking protocol and sends back handshake protocol if everything is okay
        recv_msg = conn.recv(1024).decode()
        recv_args = recv_msg.split("\t")
        # if not handshaked properly the connection ends there and then
        if recv_args[0] != "HANDSHAKE":
            conn.send("ERROR\tHandshake protocol not obeyed; ending connection".encode())
            conn.close()
            return
        
        print(f"{addr}: {recv_args[1]}")
        send_msg = "HANDSHAKE\tConnection established securely."
        conn.send(send_msg.encode())


## LOG IN PROTOCOL
        loggedIn = False
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
        

        while loggedIn:
            
            # recieving the data from the client 
            data = str(conn.recv(1024).decode())
            data = data.split("\t")

            if data[0] == "VIEW":
                print("View files")
                serv_utils.viewFiles(conn,server_data_files="serverfiles")
                conn.recv(1024).decode() # getting the user input
                if(conn.recv(1024).decode().split("\t")[0]=="OK"):
                    conn.send("Process done.".encode())
                    print("View files: OK")
                else:
                    conn.send("Process failed.".encode())
                    print("View files: Failed")
            elif data[0]=="DOWNLOAD":
                print("Download Files")
                #data[1] : the user file name
                serv_utils.downloads(conn,data[1])
                if(conn.recv(1024).decode()=="SUCCESSFUL"):
                    print("File download onto clients side was successful")
                    conn.send("Process done.".encode())
            if data[0] == "UPLOAD":
                # uploading files onto the server
                print("UPLOADING FILE TO THE SERVER")
                # recieving the message from the user 
                conn.send("Uploading file to the server".encode())
                serv_utils.upload(conn,filename=recv_msg.split('\t')[2],filesize=int(recv_msg.split('\t')[3]))


if __name__ == "__main__":
    main()