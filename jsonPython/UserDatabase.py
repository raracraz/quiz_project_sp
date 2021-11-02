import os
import DBcom
import uuid
import re
import base64
rowid = hash(uuid.uuid4())
# function to show the main menu for the quiz app 
def menu(rowid):
    print('Welcome to the The quiz')
    print('1. Login')
    print('2. Register')
    print('3. Forget password')
    print('4. Exit')
    try:
        choice = int(input('Please enter your choice: '))
    except ValueError:
        print('Please enter a valid choice')
        menu(rowid)
    if choice == 1:
        data = ''
        data = (data.encode('utf-8'))
        data = base64.b64encode(data) 
        login(rowid, data)
    elif choice == 2:
        registerUser(rowid)
    elif choice == 3:
        forgetPassword(rowid)
    elif choice == 4:
        exit()
    else:
        print('Please enter a valid choice')
        menu(rowid)

    menu(rowid)

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

#function to login using DBcom find function with data
def login(rowid, data):
    results = []
    colType = 's'
    DBcom.UserDB.find_rowid('users', 'username', rowid)
    if DBcom.UserDB.find_rowid('users', 'username', rowid) == True:
        
        try:
            data = str(input('Please enter your username: '))
        except ValueError:
            print('Please enter a valid username')
            login(rowid, data)
        try:
            data = str(input('Please enter your password: '))
        except ValueError:
            print('Please enter a valid password')
            login(rowid, data)

        filename = str(results) + '_' + str(colType) + '_' + str(data)[2:-1]
        if DBcom.UserDB.find('users', 'username', filename) == True:
            if DBcom.UserDB.find('users', 'password', filename) == True:
                print('Login successful')
                #function to take quiz
            else:
                print('Incorrect password')
                login(rowid, data)
        else:
            print('Incorrect username')
            login(rowid, data)
    else:
        print('Incorrect username')
        login(rowid, data)

#function to forget password using DBcom find function

def forgetPassword(rowid):
    try:
        username = str(input('Please enter your username: '))
    except ValueError:
        print('Please enter a valid username')
        forgetPassword(rowid)
    if DBcom.UserDB.find('users', 'username', 's', username) == True:
        print('Your password is: ' + DBcom.UserDB.find('users', 'password', 's', username))
        menu(rowid)
    else:
        print('Incorrect username')
        forgetPassword(rowid)
#let the user choose to login, register or forget password



menu(rowid)


