import os
import DBcom
import uuid
rowid = hash(uuid.uuid4())
def registerUser(rowid):
    acl = '0000'
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
    DBcom.UserDB.create('users', 'acl', 's', rowid, acl)
    DBcom.UserDB.create('users', 'username', 's', rowid, username)
    DBcom.UserDB.create('users', 'password', 's', rowid, password)
    print('Registration successful, return to the menu to login!')

    #password = str(input('Please enter your password: '))

#function to login using DBcom find function
def login(rowid):
    try:
        username = str(input('Please enter your username: '))
    except ValueError:
        print('Please enter a valid username')
        login(rowid)
    try:
        password = str(input('Please enter your password: '))
    except ValueError:
        print('Please enter a valid password')
        login(rowid)
    if DBcom.UserDB.find('users', 'username', rowid, username, password) == True:
        if DBcom.UserDB.find('users', 'password', 's', password) == True:
            print('Login successful')
            switchUser(rowid)
        else:
            print('Incorrect password')
            login(rowid)
    else:
        print('Incorrect username')
        login(rowid)

#function to forget password using DBcom find function
def forgetPassword(rowid):
    try:
        username = str(input('Please enter your username: '))
    except ValueError:
        print('Please enter a valid username')
        forgetPassword(rowid)
    if DBcom.UserDB.find('users', 'username', 's', username) == True:
        print('Your password is: ' + DBcom.UserDB.find('users', 'password', 's', username))
        switchUser(rowid)
    else:
        print('Incorrect username')
        forgetPassword(rowid)
#let the user choose to login, register or forget password

def switchUser(rowid):
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

    switchUser(rowid)

switchUser(rowid)


