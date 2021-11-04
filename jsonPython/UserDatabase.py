import os
import DBcom
import uuid
import re
import base64

# function to show the main menu for the quiz app 
def menu():
    rowid = hash(uuid.uuid4())
    print('\nWelcome to the The quiz')
    print('1. Login')
    print('2. Register')
    print('3. Forget password')
    print('4. Exit')
    try:
        choice = int(input('Please enter your choice: '))
    except ValueError:
        print('Please enter a valid choice')
        menu()
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
        menu()

    menu()

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
def login(dataUser, dataPass):
    try:
        dataUser = str(input('Please enter your username: '))
    except ValueError:
        print('Please enter a valid username')
        login(dataUser)
    except KeyboardInterrupt:
        print('\nGoodbye...')
        exit()
    #if there is no username entered.
    if dataUser =='':
        print('Please enter a valid username')
        login(dataUser)

    try:
        dataPass = str(input('Please enter your password: '))
    except ValueError:
        print('Please enter a valid password')
        login(dataUser, dataPass)
    except KeyboardInterrupt:
        print('\nGoodbye...')
        exit()
    if DBcom.UserDB.find('users', 'username', dataUser) == True:
        if DBcom.UserDB.find('users', 'password', dataPass) == True:
            print('Login successful')
            menu()
        else:
            print('Incorrect password')
            login(dataUser, dataPass)
    else:
        print('Incorrect username')
        login(dataUser, dataPass)
   

#function to forget password using DBcom find function

def forgetPassword(rowid):
    try:
        username = str(input('Please enter your username: '))
    except ValueError:
        print('Please enter a valid username')
        forgetPassword(rowid)
    if DBcom.UserDB.find('users', 'username', 's', username) == True:
        print('Your password is: ' + DBcom.UserDB.find('users', 'password', 's', username))
        menu()
    else:
        print('Incorrect username')
        forgetPassword(rowid)
#let the user choose to login, register or forget password



menu()


