#from cryptography.fernet import Fernet
import os
import sys
from hashlib import md5

FORMAT = "utf-8"

def login(username, passwd):
    hashed = username + "," + passwd

    with open("./users.txt", "r") as users:
        for user in users:
            if user.strip() == hashed: return True

    return False
    #this implementation is put on hold until we can fix issues with new line issue
    """
    hashed = username + "," + passwd

    with open("./filekey.key", "rb") as filekey:
        key = filekey.read()

    fernet = Fernet(key)

    with open("./users.bin", "rb") as users:
        for user in users:
            x = fernet.decrypt(user).decode()
            #print(f"x\t= {x}")
            #print(f"hash\t= {hashed}")
            if x == hashed: return True

    return False
    """

def add_user(username, passwd):
    hashed = username + "," + passwd
    isIn = False
    with open("./users.txt", "r") as users:
        for user in users:
            if user.strip() == hashed: isIn = True
        
    if not isIn:
        with open("./users.txt", "a") as users:
            print("adding user")
            print(hashed, file=users)

    """
    hashed = username + "," + passwd
    
    with open("./filekey.key", "rb") as filekey:
        key = filekey.read()

    fernet = Fernet(key)
    x = fernet.encrypt(hashed.encode())

    # have to figure out how to write one user per line encrypted
    
    with open("./users.bin", "ab+") as users:
        print(f"user added: {x}")
        all_users = users.read()
        for i in users:
            print(i)

        if x not in all_users:
            users.write(x)
        else:
            print("user already in")
    """

print(login("tpchiks", "343f"))


def downloads(connection,address,textfileName):
    directory,textfile = textfileName.split(' ')
    print(f"Checking if the file with name {textfile} exists")
    if(os.path.exists(textfile)):
        print(f"File {textfile} exixts!")
        print(f"Downloading file {textfile} into directory {directory}")
        file = open(f"./serverfiles/{textfile}","r")
        data=file.read()
        connection.send(data.encode("utf-8"))
        file.close()
        print("File has been sent!")
    else:
        print(f"The file under the name {textfile} does not exist")

def viewFiles(connection):
        files = os.listdir("serverfiles")
        send_data = "OK@"
        if len(files) == 0:
            send_data += "The server directory is empty"
        else:
            send_data += "\n".join(f for f in files)
        connection.send(send_data.encode(FORMAT))


def md5sum(filename):
    hash = md5()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(128 * hash.block_size), b""):
            hash.update(chunk)
    return hash.hexdigest()