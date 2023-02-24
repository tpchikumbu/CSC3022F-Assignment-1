#from cryptography.fernet import Fernet

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


def transfer(filename):
    f = open(f"./serverfiles/{filename}", "rb")
    content = f.read()
    print("file downloaded...")
    f.close()

    fw = open(f"./downloads/{filename}", "wb")
    fw.write(content)
    fw.close()
    print("file sent")


print(login("tpchiks", "343f"))
