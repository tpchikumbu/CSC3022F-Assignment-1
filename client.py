import getpass
import os
import socket

def main():
    serverName = "localhost"
    serverPort = 50000
    
    ip = input("Enter \"IP port\" of server. Leave blank to use \'localhost\' and port 4000\n")
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
        user_input = input("Enter the number of the option: ")
        if user_input == "1":
            send_msg = "VIEW\t"
            clientSocket.send(send_msg.encode())
            
            recv_msg = clientSocket.recv(1024).decode()
            recv_args = recv_msg.split("@")
            if recv_args[0] == "OK":
                print(recv_args[1])
                send_msg = "OK@received files"
            else:
                send_msg = "NOTOK@file not received properly"
        else:
            continue

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
