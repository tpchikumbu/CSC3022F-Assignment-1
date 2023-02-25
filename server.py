import os
import threading
from socket import *
from tqdm import tqdm

def upload (socket, address, name, size):
    #message = socket.recv(1024).decode("utf-8")

    bar = tqdm(range(size), f"Receiving {name}", unit="B", unit_scale=True, unit_divisor=1024)
    f = open(f"./serverfiles/recv_{name}", "wb")
    while True:
        message = socket.recv(4096)
        if not message:
            break
        f.write(message)
        
        bar.update(len(message))

    f.close    
    socket.close()

def file_handling (sock, addr):
    while True:
        message = sock.recv(1024).decode("utf-8")
        file_details = message.split("\t")
        f_name = file_details[1]
        f_size = int (file_details[2])

        if message.find("download") == 0:
            directive, filename = message.split(" ")
            print(f"downloading file: {filename}")
            # implement sending the file onto the socket
            print(f"Sending ... {filename}")

            cFile = open(f"./serverfiles/{filename}", "rb")
            data = cFile.read()

            sock.send(data)
            cFile.close()

            print("File sent!")

        elif message.find("upload") == 0:
            upload(sock, addr, f_name, f_size)
        
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
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

if __name__ == "__main__":
    main()
