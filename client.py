import getpass
import os
import socket

def main():
    serverName = "localhost"
    serverPort = 4000
    
    ip = input("Enter \"IP port\" of server. Leave blank to use \'localhost\' and port 4000\n")
    if (ip):
        serverName, serverPort = ip.split(" ")
        serverPort = int(serverPort)

    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((serverName,serverPort))
    addr = socket.gethostbyname(socket.gethostname())
    message = clientSocket.recv(1024).decode()
    print(message)
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

    if loggedIn:
        print("interaction was successful and user logged in")
        x = input("Press 1 to proceed.")
        clientSocket.send(send_msg.encode())
        print(clientSocket.recv(1024).decode())

    else:
        print("user is not logged in and interaction was unsucessful")
    
    send_msg = f"Client {addr} now disconnecting"
    x = input("Press enter to exit.")
    clientSocket.send(send_msg.encode())
    clientSocket.close()














    # if ("not" not in return_message):
    #     down = input("Do you want to download the file (y/n)\n")
    #     if down:
    #         clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #         clientSocket.connect((serverName,serverPort))

    #         message = "hello " + filename
    #         clientSocket.send(message.encode())
            
            
    #         if not os.path.isdir("./downloads"): os.mkdir("./downloads")
    #         # implement getting file from the server
    #         file = open(f"./downloads/{filename}", "w")

    #         data = clientSocket.recv(1024).decode("utf-8")
    #         file.write(data)

    #         file.close()

    #         print("File received!")

    #         clientSocket.close()

if __name__ == "__main__":
    main()
