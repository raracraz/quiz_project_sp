import os
import stdLibv8
import uuid
import re
import hashlib
import base64
############################################################################################
'''
Functions of this QUIZ APPICATION:
'''
# This Quiz is a simple quiz that will ask the user a series of questions after login.
# The user will be able to register an account
# The user will be able to login to their account
# The user will be able to recover their password using the email they registered with

# The user will be able to answer the questions with a single character.
# The user will be able to quit the quiz at any time.
# The user will be able to see their score at the end of the quiz.
# The user's results will be saved to a file and additionally in a csv file.

# The admin will be able to add questions to the quiz.
# The admin will be able to remove questions from the quiz.
# The admin will be able to view and change the current list of questions.
# The admin will be able to randomize the order of the questions.
# The admin will be able to change the account details of any user.

global rowid, username, loggedin_rowid
# function to show the main menu for the quiz app 
#let the user choose to login, register, forget password and exit
rowid = hash(uuid.uuid4())
loggedin_rowid = rowid
stdLibv8.menu(rowid)
#stdLibv8.takeQuiz(rowid, username='craz')
#stdLibv8.checkAnswer(rowid, username='craz', resultList=['a', 'b', 'c', 'd', 'c'], Qnsno = 5, allQns, attCount, count)
#stdLibv8.adminCreateQuestionPool(rowid)
#stdLibv8.doAdminQuestions(rowid, username='craz')










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

