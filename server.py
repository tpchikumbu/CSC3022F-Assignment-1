import os
import threading
from socket import *
import serv_utils
CURRENT_USERS = {}


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
    try:
        with conn:
            # isAdmin = False
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
                    send = response[1] + "\t" + response[2]
                    conn.send(send.encode())
                    if loggedIn:
                        isAdmin = (response[2] == "ADMIN")
                        if username in CURRENT_USERS:
                            CURRENT_USERS[username].append(addr)
                        else:
                            CURRENT_USERS[username] = [addr]
                        break
            

            # MAIN FUNCTIONALITY
            while loggedIn:
                
                # recieving the data from the client 
                # this is one of the options offered
                # VIEW DOWNLOAD UPLOAD LOGOUT
                data = str(conn.recv(1024).decode())
                data = data.split("\t")

            # VIEW FUNCTIONALITY
                if data[0] == "VIEW":
                    print("View files")
                    file_request = serv_utils.viewFiles(server_data_files="serverfiles")
                    
                    # sends the file list or the error message
                    send_msg = file_request[1]
                    conn.send(send_msg.encode())

                    if file_request[0]:
                        #if we've actually gotten something without a hitch
                        print(f"Successfully sent file list to {addr}")
                    else:
                        print("Error encounted acquiring file list")

            # DOWNLOAD FUNCTIONALITY
                elif data[0]=="DOWNLOAD":
                    print("Download Files")
                    #data[1] : the user file name
                    # download function now returns the filesize and -1 if the file was not found
                    file_request = serv_utils.check_for_file(data[1])
                    
                    if file_request[0]:
                        file_password = file_request[1][1]
                        if file_password:
                            conn.send(f"LOCKED\tThe file: {file_request[1][0]} is password protected".encode())
                            recv_msg = conn.recv(1024).decode()
                            recv_args = recv_msg.split("\t")
                            if recv_args[0] == "PASSWORD":
                                if recv_args[1] != file_password:
                                    conn.send("NOTOK\tPassword incorrect. Request terminated.".encode())
                                    continue

                    out_file_size, hashed = serv_utils.download(conn, data[1])

                    # if the file was not found it just continues
                    if out_file_size != -1:
                        if not hashed:
                            print("ERROR: Different hash")
                            conn.send("NOTOK".encode())
                            break
                        else:
                            conn.send("OK".encode())
                        recv_msg = conn.recv(1024).decode()
                        recv_args = recv_msg.split("\t")

                        if(recv_args[0]=="RECEIVED"):
                            in_file_size = int(recv_args[1])
                            send_msg = "OK\t"
                            if in_file_size==out_file_size:
                                send_msg += "File was fully sent"
                                print(f"File {data[1]} was sent to {addr}")
                            else:
                                send_msg += "File was sent partially"
                                print(f"File {data[1]} was sent to {addr} partially")
                            
                            conn.send(send_msg.encode())
                        else:
                            send_msg = "NOTOK\tFile might have been lost"
                            conn.send(send_msg.encode())

            # UPLOAD
                elif data[0] == "UPLOAD":
                    # recv_msg = conn.recv(1024).decode()
                    # uploading files onto the server
                    print("UPLOADING FILE TO THE SERVER")
                    # recieving the message from the user 
                    filename = data[1]
                    password = data[2]
                    filesize = int(data[3])

                    if (serv_utils.check_for_file(filename))[0]:
                        send_msg = f"NOTOK\tFile: {filename} already exists on server. Process ended."
                        conn.send(send_msg.encode())
                        continue
                    else:
                        send_msg = "OK\tServer ready to receive the file"
                        conn.send(send_msg.encode())

                    # expects a messages like UPLOAD\tfilename\tpassword\tfilesize
                    serv_utils.upload(conn, filename, password, filesize)
            
                elif data[0] == "LOGOUT":
                    CURRENT_USERS[username].remove(addr)
                    conn.send("LOGOUT\tUser successfully logged out".encode())
                    conn.close()
                    break

                elif data[0] == "ADMIN":
                    status_of_user_added, add_msg = serv_utils.add_user(data[1],data[2], eval(data[3]))
                    print(add_msg)
                    if(status_of_user_added):
                        conn.send(f"SUCCESS\t{add_msg}".encode())
                    else:
                        conn.send(f"FAILURE\t{add_msg}".encode())
        
    except ConnectionError as e:
        print(e)
        return


if __name__ == "__main__":
    main()