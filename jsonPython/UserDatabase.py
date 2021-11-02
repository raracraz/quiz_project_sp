import os
import DBcom
import uuid
rowid = hash(uuid.uuid4())
def registerUser(rowid):
    acl = 0000
    try:
        username = str(input('Please enter your username: '))
    except ValueError:
        print('Please enter a valid username')
        registerUser(rowid, acl)
    try:
        password = str(input('Please enter your password: '))
    except ValueError:
        print('Please enter a valid password')
        registerUser(rowid, acl)
    DBcom.UserDB.create('users', 'acl', 'i', rowid, acl)
    DBcom.UserDB.create('users', 'username', 's', rowid, username)
    DBcom.UserDB.create('users', 'password', 's', rowid, password)

    #password = str(input('Please enter your password: '))
    


#let the user choose to login, register or forget password

def switchUser(rowid, login, registerUser, forgetPassword):
    print('Welcome to the The quiz')
    print('1. Login')
    print('2. Register')
    print('3. Forget password')
    print('4. Exit')
    try:
        choice = int(input('Please enter your choice: '))
    except ValueError:
        print('Please enter a valid choice')
        switchUser(rowid)
    if choice == 1:
        login(rowid)
    elif choice == 2:
        registerUser(rowid)
    elif choice == 3:
        forgetPassword(rowid)
    elif choice == 4:
        exit()
    else:
        print('Please enter a valid choice')
        switchUser(rowid)

    
