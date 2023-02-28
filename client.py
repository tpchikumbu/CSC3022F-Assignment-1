import getpass
import socket
import tqdm
import os


def main():
    serverName = "127.0.1.1"
    serverPort = 50000
    
    ip = input("Enter \"IP port\" of server. Leave blank to use \'localhost\' and port 50000\n")
    if (ip):
        serverName, serverPort = ip.split(" ")
        serverPort = int(serverPort)

    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((serverName,serverPort))
    addr = socket.gethostbyname(socket.gethostname())

    loggedIn = False
    handshake = False
    send_msg = "client ready"

    for i in range(1,4):
        username = input("Username: ")
        password = getpass.getpass(prompt="Password:")
        log = f"\tLogin attempt {i} by {addr}: u: {username} p: {password}"
        send_msg = "LOGIN\t" + username + "\t" + password + log
        clientSocket.send(send_msg.encode())

        recv_msg = clientSocket.recv(1024).decode()
        recv_args = recv_msg.split("\t")
        if recv_args[0] == "ERROR":
            print(f"{recv_args[0]}: {recv_msg[1]}")
            continue
        elif recv_args[0] == "NOTAUTH":
            print(recv_args[1])
            continue
        elif recv_args[0] == "AUTH":
            print(recv_args[1])
            loggedIn = True
            break
    
    # present the menu to client
    while loggedIn:
        print_menu()
        user_input = input("Enter the number of the option: \n")
        if user_input == "1": #view files
            send_msg = "VIEW\t"
            clientSocket.send(send_msg.encode())
            
            recv_msg = clientSocket.recv(1024).decode()
            recv_args = recv_msg.split("\t")
            if recv_args[0] == "OK":
                print(recv_args[1])
                send_msg = "OK\treceived files"
            else:
                send_msg = "NOTOK\tfile not received properly"
        elif user_input == "2": #download files
            filename = input("Enter the name of the file to be downloaded\n")
            send_msg = "DOWNLOAD\t"+filename
            clientSocket.send(send_msg.encode()) #implement specifying download directory

            #added stuff for progress bar and sending of all filetypes
            filesize = int(clientSocket.recv(1024).decode())
            bar = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
            in_file = open(f"./downloads/down_{filename}", "wb")
            while True:
                message = clientSocket.recv(4096) #can't tell when entire file has been downloaded
                end = bytes("EOF".encode())
                if message == end:
                    break

                in_file.write(message)
                bar.update(len(message))

            in_file.close()
            #send_msg = "Downloaded"

        elif user_input == 3:
            print("Upload")

        elif user_input == 4:
            print("Log Out")
        else:
            print("Invalid input")

        #clientSocket.send(send_msg.encode())

    if loggedIn:
        print("interaction was successful and user logged in")
    else:
        print("user is not logged in and interaction was unsucessful")
    
    send_msg = f"Client {addr} now disconnecting"
    x = input("Press enter to exit.")
    clientSocket.send(send_msg.encode())
    clientSocket.close()

    
def print_menu():
    print("1. View files\n2. Download file\n3. Upload file\n4. Logout")


if __name__=="__main__":
    main()
