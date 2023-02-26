import socket

IP = socket.gethostbyname(socket.gethostname())
PORT = 4000
ADDR = (IP, PORT)
FORMAT = "utf-8"
SIZE = 1024

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR) # create a connection with the server 

    while True:
        server_message = client.recv(SIZE).decode(FORMAT) # recieve the data from the server
        cmd, msg = server_message.split("@")
    
        # # break of the server was not connected at the time 
        if cmd == "DISCONNECTED":
            print(f"[SERVER]: {msg}")
            break
        elif cmd == "OK": # testing the state of the server 
            print(f"{msg}")

        # taking in the user input 
        data = input("> ")
        data = data.split(" ")
        username = data[0]
        password = data[1]
        client_login = username +"\n"+password
        client.send(client_login.encode(FORMAT))



      
        if cmd == "LOGOUT":
            client.send(cmd.encode(FORMAT))
            break
        elif cmd == "LIST":
            client.send(cmd.encode(FORMAT))
        elif cmd == "DELETE":
            client.send(f"{cmd}@{data[1]}".encode(FORMAT))
        elif cmd == "UPLOAD":
            path = data[1]

            with open(f"{path}", "r") as f:
                text = f.read()

            filename = path.split("/")[-1]
            send_data = f"{cmd}@{filename}@{text}"
            client.send(send_data.encode(FORMAT))

    print("Disconnected from the server.")
    client.close()

if __name__ == "__main__":
    main()























# import os
# import socket

# serverName = socket.gethostbyname(socket.gethostname())
# serverPort = 4000

# while True:
#     clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     clientSocket.connect((serverName,serverPort))



    # filename = input("Enter the name of the file you want to search for:\n")
    # clientSocket.send(filename.encode())

    # confirmation = clientSocket.recv(1024)
    # return_message = confirmation.decode()
    # clientSocket.close()

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
    #         clientSocket.send("recieved".encode())
    #         dataHash = clientSocket.recv(1024).decode("utf-8")
    #         print(dataHash)
    #         file.write(data)
    #         file.close()
            

    #         print("File received!")

    #         clientSocket.close()