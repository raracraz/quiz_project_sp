import os
import stdLibv8
import uuid
import re
import hashlib
import base64
global rowid, username, loggedin_rowid
# function to show the main menu for the quiz app 
#let the user choose to login, register, forget password and exit
rowid = hash(uuid.uuid4())
loggedin_rowid = rowid
stdLibv8.menu(rowid)














'''
def menu():
    rowid = hash(uuid.uuid4())
    print('\n**Welcome to the The quiz**')
    print('1. Login')
    print('2. Register')
    print('3. Forget password')
    print('4. Exit')
    try:
        choice = int(input('Please enter your choice: '))
    except ValueError:
        print('Please enter a valid choice')
        menu()
    except KeyboardInterrupt:
        print('\nGoodbye...')
        exit()
    if choice == 1:
        dataUser = ''
        dataPass = ''
        login(dataUser, dataPass)
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
'''
'''
def registerUser(rowid):
    acl = '0000'
    try:
        username = str(input('Please enter your username: '))
    except ValueError:
        print('Please enter a valid username')
        registerUser(rowid, acl)
    except KeyboardInterrupt:
        print('\nGoodbye...')
        exit()
    try:
        password = str(input('Please enter your password: '))
    except ValueError:
        print('Please enter a valid password')
        registerUser(rowid, acl)
    except KeyboardInterrupt:
        print('\nGoodbye...')
        exit()
    stdLib.UserDB.create('users', 'acl', 's', rowid, acl)
    stdLib.UserDB.create('users', 'username', 's', rowid, username)
    stdLib.UserDB.create('users', 'password', 's', rowid, password)
    print('Registration successful, return to the menu to login!')

    #password = str(input('Please enter your password: '))
'''
'''
#function to login using DBcom find function with data
def login(dataUser, dataPass):
    
    try:
        print('**WARNING: Case Sensitive**')
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
    #if there is no password entered.
    if dataPass == '':
        print('Please enter a valid password')
        login(dataUser, dataPass)
    if stdLib.UserDB.find('users', 'username', dataUser) == True:
        if stdLib.UserDB.find('users', 'password', dataPass) == True:
            print('\nLogin successful')
            stdLib.main() #change to the take the quiz function
        else:
            print('Incorrect password')
            login(dataUser, dataPass)
    else:
        print('Incorrect username')
        login(dataUser, dataPass)
   
'''
#function to forget password using DBcom find function
'''
def forgetPassword(rowid):
    try:
        print('**WARNING: Case Sensitive**')
        username = str(input('Please enter your username: '))
    except ValueError:
        print('Please enter a valid username')
        forgetPassword(rowid)
    if stdLib.UserDB.find('users', 'username', 's', username) == True:
        print('Your password is: ' + stdLib.UserDB.find('users', 'password', 's', username))
        menu()
    else:
        print('Incorrect username')
        forgetPassword(rowid)
'''

