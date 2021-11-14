# +==========================================================
# StdLib
# version 0.1109.1729
# last update: 2021-11-11
# created by: Crazzz
# +==========================================================

import os
import re
import base64
import json
import datetime
import uuid
import glob
import shutil
import DBcom
def aclchecker(localrowid, aclcheck):
    #rowid = DBcom.UserDB.find('users', 'username', 'data', 'id', username)
    aclraw = DBcom.UserDB.find('users', 'acl', 'id', 'raw', localrowid)
    print(aclraw)
    print(localrowid)

    acl = str(base64.b64decode(aclraw[localrowid].split('_')[2]))[1:]
    print(acl)
    if acl[aclcheck] == '1':
        return True
    else:
        return False
    

def adminMenu(localrowid):
    print('Welcome to the admin menu')
    print('1. Users')
    print('2. Questions')
    print('\n<ENTER> to go Back')
    try:
        choice = int(input('Please enter your choice: '))
    except ValueError:
        doUserQuestions(localrowid)
    if choice == 1:
        doAdminUser(localrowid)
    elif choice == 2:
        doAdminQuestions(localrowid, '')
    elif choice == 3:
        menu(localrowid)
    else:
        menu(localrowid)

def doAdminUser(localrowid):
    print('Welcome to the user admin menu [{}]'.format(localrowid))
    print('1. Create new user')
    print('2. List Users to Update/Delete')
    print('\n<ENTER> to go Back')
    try:
        choice = int(input('Please enter your choice: '))
    except ValueError:
        print('Please enter a valid choice')
        menu(localrowid)
    if choice == 1:
        registerUser(localrowid,"admin")
    elif choice == 2:
        doAdminListUsers(localrowid)
    else:
        menu(localrowid)

def doAdminUserEditData(userid,column, value):
    if column == 1:
        DBcom.UserDB.update('users', 'username', 's',userid, value)
    elif column == 2:
        DBcom.UserDB.update('users', 'password', 's',userid, value)
    elif column == 3:
        DBcom.UserDB.update('users', 'email', 's',userid, value)
    elif column == 4:
        DBcom.UserDB.update('users', 'acl', 's',userid, value)
    elif column == 5:
        DBcom.UserDB.update('users', 'otp', 's',userid, value)

    doAdminUserEditList(userid)

def doAdminUserDelData(userid):
    DBcom.UserDB.delete('users', 'username',userid)
    DBcom.UserDB.delete('users', 'password',userid)
    DBcom.UserDB.delete('users', 'email', userid)
    DBcom.UserDB.delete('users', 'acl', userid)
    DBcom.UserDB.delete('users', 'otp', userid)

    doAdminUserDelData(userid)

def doAdminUserEditList(userid):
    userinfo = DBcom.UserDB.find('users', 'username', 'id', 'raw', userid)
    acl = DBcom.UserDB.find('users', 'acl', 'id', 'raw', userid)
    password = DBcom.UserDB.find('users', 'password', 'id', 'raw', userid)
    otp = DBcom.UserDB.find('users', 'otp', 'id', 'raw', userid)
    email = DBcom.UserDB.find('users', 'email', 'id', 'raw', userid)
    username = str(base64.b64decode(userinfo[0].split('_')[2]))[2:-1]
    password = str(base64.b64decode(password[0].split('_')[2]))[2:-1]
    otp = str(base64.b64decode(otp[0].split('_')[2]))[2:-1]
    email = str(base64.b64decode(email[0].split('_')[2]))[2:-1]
    acl = str(base64.b64decode(acl[0].split('_')[2]))[2:-1]
    print('1. username:{}'.format(username))
    print('2. password:{}'.format(password))
    print('3. email:{}'.format(email))
    print('4. acl:{}'.format(acl))
    print('5. otp:{}'.format(otp))
    print('6. DELETE USER')
    print('\n<ENTER> to go Back')
    try:
        choice = int(input('Please enter your choice [1-5]: '))

        if choice == 7:
            doAdminListUsers(userid)
        elif choice == 6:
            allusers = DBcom.UserDB.find('users', 'username', 'id', 'raw','')
            rowid = allusers[choice-1].split('_')[0]
            doAdminUserDelData(rowid, 6)
        else:
            changeTo = input('Please enter the new value: ')

            if changeTo == '':
                doAdminListUsers(userid)
            else:
                doAdminUserEditData(userid, choice, changeTo)

    except ValueError:
        doAdminListUsers(userid)
    
####################################################################################################################################


def doAdminListUsers(rowid):
    userlist = []
    usercount = 1
    allusers = DBcom.UserDB.find('users', 'username', 'id', 'raw','')
    alluserscnt = len(allusers)
    for user in allusers:
        print("{}. Username: {} / UserID: {}".format(usercount,str(base64.b64decode(user.split('_')[2]))[2:-1],str(user.split('_')[0])))
        usercount = usercount + 1

    print('\n<ENTER> to go Back')

    try:
        choice = int(input('Please enter your choice [{}-{}]: '.format(1,alluserscnt)))
    except ValueError:
        doAdminUser(rowid)

    if choice > alluserscnt:
        print('Please enter a valid choice')
        doAdminUser(rowid)
    else:
        rowid = allusers[choice-1].split('_')[0]
        doAdminUserEditList(rowid)
    

    

def doAdminQuestions(rowid, questionid):
    print('Welcome to the question admin menu')
    print('1. Create new question pool ')
    print('2. List Question Pools to Update/Delete')
    print('\n<ENTER> to go Back')
    try:
        choice = int(input('Please enter your choice: '))
    except ValueError:
        adminMenu(rowid)
    if choice == 1:
        adminCreateQuestionPool(rowid)
    elif choice == 2:
        listQuestionPool(rowid, questionid)
    else:
        pass

####################
def menu(localrowid):
    print('\n\n+==================================+')
    print('Welcome to the The quiz')
    print('+==================================+')    
    print('1. Login')
    print('2. Register')
    print('3. Forget password')
    print('\n<ENTER> to Exit')


    try:
        choice = int(input('Please enter your choice: '))
        if choice == 1:
            login(localrowid)
        elif choice == 2:
            registerUser(localrowid,"normal")
        elif choice == 3:
            forgetPassword(localrowid)
        elif choice == 1008:
            registerUser(localrowid,"admin",'11111')
        else:
            menu(localrowid)
    except ValueError:
        os._exit(0)
    menu()

def generateOTP():
    #get a random number then hash it to 8 digits
    randomNumber = os.urandom(16)
    randomNumber = abs(hash(randomNumber) % (10 ** 8))
    return randomNumber

def registerUser(rowid,fromwhere, acl = '00000'):
    username_pass = False
    password_pass = False
    email_pass = False
    #acl = '00000'
    #acl = '11111' #to create admin user
    #regenerate rowid to ensure each record is unique
    
    localrowid = str(abs(hash(os.urandom(16)) % (10 ** 8)))

    if fromwhere == 'admin':
        print('+==================================+')
        print('Create User / Admin User Menu')
        print('+==================================+')
    else:
        print('+==================================+')
        print('Create User Menu')
        print('+==================================+')        

    username = str(input('Please enter your username: '))

    #if username is empty go back
    if username == '':
        if fromwhere == 'admin':
            doAdminUser(localrowid)
        else:
            menu(localrowid)

    password = str(input('Please enter your password: '))
    email = str(input('Please enter your email: '))
    otp = str(generateOTP())

    #first let's check if username is already taken
    if len(DBcom.UserDB.find('users', 'username', 'data', 'bool', username)) > 0:
        print('Username already taken')
    else:
        username_pass = True

    #now let's check if email is a valid email
    if re.match(r"[^@]+@[^@]+\.[^@]+", email) == None:
        print('Email is not valid')
        email_pass = False
    else:
        email_pass = True

    #now let's check if email is already taken
    if len(DBcom.UserDB.find('users', 'email', 'data', 'bool', email)) > 0:
        print('Email already taken')
        email_pass = False
    else:
        email_pass = True


    if username_pass == True and email_pass == True:
        try:
            DBcom.UserDB.create('users', 'acl', 's', localrowid, acl)
            DBcom.UserDB.create('users', 'username', 's', localrowid, username)
            DBcom.UserDB.create('users', 'password', 's', localrowid, password)
            DBcom.UserDB.create('users', 'otp', 's', localrowid, str(otp))
            DBcom.UserDB.create('users', 'email', 's', localrowid, email)
            print('+==================================+')
            print('Registration successful,\nreturn to the menu to login!\n')
            print('your email is {}, recovery OTP is {}'.format(email,otp))
            print('+==================================+\n')
            if fromwhere == "admin":
                doAdminUser(rowid)
            else:
                menu(rowid)
        except:
            print('Error creating user')
            registerUser(localrowid,fromwhere)
    else:
        registerUser(localrowid,fromwhere)

#allows the the user to take a quiz
def doQuestions(localrowid):

    pass

#function to login using DBcom find function with data
def login(localrowid):
    results = []
    username = ""
    password = ""
    username_pass = False
    password_pass = False
        
    try:
        username = str(input('Please enter your username: '))
    
        #if there is no username entered.
        if username == '':
            print('+==================================+\n')
            print('Login terminated.!\n')
            print('+==================================+\n')
            menu(localrowid)

        try:
            password = str(input('Please enter your password: '))
        except ValueError:
            print('Please enter a valid password')
            login(localrowid)

        rowid = DBcom.UserDB.find('users', 'username', 'data', 'id', username)
        username_pass = DBcom.UserDB.find('users', 'username', 'data','bool', username)
        password_pass = DBcom.UserDB.find('users', 'password', 'data','bool', password)
        userid = DBcom.UserDB.find('users', 'username', 'id', 'id', username)
        print(localrowid)
        print(userid)
        print(rowid)
        localrowid = rowid

        print('username:[{}/{}]/password:[{}/{}]/loggedin_rowid:{}'.format(username,username_pass,password,password_pass,localrowid))

        try:
            if len(username_pass) > 0 and len(password_pass) > 0 and localrowid != '':
                print('=============================')
                print('Login successful {}/{}'.format(username,localrowid))
                print('=============================')
                doUserQuestions(localrowid,'' , userid)
            else :
                print('a. Incorrect username or password')
                login(localrowid)
        except ValueError:
            print('b. Incorrect username or password')
            login(localrowid)

    except ValueError:
        login(localrowid)

#function to forget password using DBcom find function

def forgetPassword(localrowid):
    email = str(input('Please enter your email: '))
    #check if email is valid

    if email == '':
        menu(localrowid)

    if re.match(r"[^@]+@[^@]+\.[^@]+", email) == None:
        print('Email is not valid')
        forgetPassword(localrowid)
    else:
        localrowid = DBcom.UserDB.find('users', 'email', 'data', 'id', email)[0]
        print(localrowid)
        if len(localrowid) != '':
            #try:
            #password = str(base64.b64decode(DBcom.UserDB.find('users', 'password', 'id','raw', localrowid[0])[0].split('_')[2]))[1:]
            password = str(DBcom.UserDB.find('users', 'password', 'id','raw', localrowid)).split('_')[2][0:-2]
            print(password)
            print('+==================================+\n')
            print('We have sent the password {} to your Email {}'.format(password,email))
            print('+==================================+\n')
            menu(localrowid)
            #except:
            #    forgetPassword(rowid)
        else:
            print('Email not found')
            forgetPassword(localrowid)

#start of main quiz functions

#function to use UserDB.create() to create the question pool with different rowids only if acl is 11111.
#function to use UserDB.create() to create the question pool with different rowids only if acl is 11111.
def adminCreateQuestionPool(localrowid):
    print('+==================================+\n')
    print('Creating Question Pool...')
    print('+==================================+\n')
    #create the question pool
    #delete current questions
    
    DBcom.UserDB.delete('questions')
    print('How many questions do you want to have in the quiz?')
    print('(max 10)')
    print('Press <Enter> to go back\n')
    
    try:
        questionCount = int(input('> '))
    except ValueError:
        adminMenu(localrowid)
    if questionCount < 1 or questionCount > 10:
        print('Invalid number of questions...')
        adminMenu(localrowid)
    else:
        for i in range(1,questionCount+1):
            options = []
            questionid = hash(uuid.uuid4())
            print('\nCreating Question {}'.format(i))
            print('What is the question?')
            question = input('> ')
            question+str(i)
            #question = question.encode('utf-8')
            for j in range(1,5):
                print('What is option {}?'.format(j))
                inputOptions = input('> ')
                #inputOptions = inputOptions.encode('utf-8')
                options.append(inputOptions)
            print('What is the correct answer?')
            correctAnswer = input('> ')
            #correctAnswer = correctAnswer.encode('utf-8')
            if correctAnswer not in options:
                print('Error, the correct answer is not in the options...')
                adminCreateQuestionPool(localrowid)
            DBcom.UserDB.create('questions','options','r',questionid,[options])
            DBcom.UserDB.create('questions','correctAnswers','r',questionid,correctAnswer)
            DBcom.UserDB.create('questions', 'questions', 'r', questionid, question)
            print('Question {} created successfully'.format(i))
        print('+==================================+\n')
        print('\n')
        print('+==================================+\n')
    adminMenu(localrowid)
    
##
def listQuestionPool(localrowid, questionid):
    print('+==================================+\n')
    print('Listing Question Pool...')
    print('+==================================+\n')
    #list the question pool
    allQns = DBcom.UserDB.find('questions', 'questions', 'id', 'raw','')
    print(allQns)
    allQnscnt = len(allQns)
    allQnsnum = len(allQns)
    Qnscnt = 1
    for allQnscnt in allQns:
        print("{}. Question: {}/QuestionID: {}".format(Qnscnt,str((allQnscnt.split('_')[2])),str(allQnscnt.split('_')[0])))
        Qnscnt = Qnscnt + 1
    print('+==================================+\n')
    print('Which question do you want to modify?: ')
    
    print('\nPress <Enter> to go back\n')
    try:
        questionNumber = int(input('Please enter from [{}-{}]: '.format(1,allQnsnum)))
        adminModifyQuestion(localrowid, questionNumber, questionid)
    except ValueError:
        doAdminQuestions(localrowid, questionid)


def adminModifyQuestion(localrowid, questionNumber, questionid):
    print('+==================================+\n')
    print('Modifying Question...')
    print('+==================================+\n')
    if questionNumber < 1 or questionNumber > 10:
        print('Invalid number of questions...')
        adminMenu(localrowid)
    else:
        questionNumber = questionNumber - 1
        question = DBcom.UserDB.find('questions', 'questions', 'id', 'raw', '')
        question = question[questionNumber]
        options = DBcom.UserDB.find('questions', 'options', 'id', 'raw', '')
        options = options[questionNumber]
        correctAnswer = DBcom.UserDB.find('questions', 'correctAnswers', 'id', 'raw', '')
        correctAnswer = correctAnswer[questionNumber]
        print('Question: {}'.format(question.split('_')[2]))
        print('Options: {}'.format(options.split('_')[2][2:-2]))
        print('Correct Answer: {}'.format(correctAnswer.split('_')[2]))
        print('+==================================+\n')
        print('What do you want to modify?')
        print('1. Question')
        print('2. Options')
        print('3. Correct Answer')
        print('\nPress <Enter> to go back')
        print('+==================================+\n')
        try:
            modifyChoice = int(input('> '))
        except ValueError:
            adminMenu(localrowid)
        if modifyChoice == 1:
            print(question)
            questionid = question.split('_')[0]
            question = question.split('_')[2]
            print(question)
            print(questionid)
            print('What is the new question?')
            newQuestion = input('> ')
            print(question)
            DBcom.UserDB.update('questions', 'questions', 'r', questionid, newQuestion)
            print('Question successfully modified')
            listQuestionPool(localrowid, questionid)
        elif modifyChoice == 2:
            print('These are the current options: ')
            print(options.split('_')[2][2:-2])
        
            print('What are the new options?: ')
            questionid = question.split('_')[0]
            options = options.split('_')[2]
            options = []
            try:
                for i in range(1,5):
                    newOption = input('Enter the new option {}: '.format(i))
                    options.append(newOption)
                    print(options)
            except ValueError:
                adminModifyQuestion(localrowid, questionNumber, questionid)
            print(options)
            DBcom.UserDB.update('questions', 'options', 'r', questionid, [options])
            print('Option successfully modified')
            listQuestionPool(localrowid, questionid)
        elif modifyChoice == 3:
            print(correctAnswer.split('_')[2])
            print('What is the new correct answer?')
            questionid = question.split('_')[0]
            try:
                print('<Enter> to go back')
                newCorrectAnswer = input('What is the correct answer?: ')
            except ValueError:
                adminModifyQuestion(localrowid, questionNumber, questionid)
            
            if newCorrectAnswer not in options:
                print('Error, the correct answer is not in the options...')
                print('Answer not changed.')
                adminModifyQuestion(localrowid, questionNumber, questionid)
            else:
                DBcom.UserDB.update('questions', 'correctAnswers', 'r', questionid, newCorrectAnswer)
                print('Correct answer successfully modified')
                listQuestionPool(localrowid, questionid)
    listQuestionPool(localrowid, questionid)

#userMenu
def doUserQuestions(localrowid, questionid, userid):
    print(userid)
    userid = DBcom.UserDB.find('users', 'username', 'id', 'raw', localrowid)
    print(userid)
    #userid = userid.split('_')[2]
    userid = base64.b64decode(userid[0].split('_')[2]).decode('utf-8')
    username = DBcom.UserDB.find('users', 'username', 'id', 'id', localrowid)
    print(username)
    print(userid)
    print('+==================================+\n')
    print('User Question Menu...')
    print('UserID: {}'.format(userid))
    print('+==================================+\n')
    print('1. List Question Pool')
    print('2. Take Quiz')
    print('\nPress <Enter> to go back to login page')
    print('(You will be logged out)')
    print('+==================================+\n')
    try:
        userChoice = int(input('> '))
    except ValueError:
        menu(localrowid)
    if userChoice == 1:
        listQuestionPool(localrowid, questionid)
    elif userChoice == 2:
        #takeQuiz(localrowid, questionid)
        pass
    elif userChoice == 5:
        try:
            if aclchecker(localrowid, 5) == True:
                adminMenu(localrowid)
            else:
                print('You do not have access to this menu')
                menu(localrowid)
        except ValueError:
            pass
    else:
        print('Invalid choice...')
        doUserQuestions(localrowid, questionid, userid)
    #try:
        #try:
        #    if aclchecker(username, 5) == True:
        #            print('5. Admin Menu')
       # except:
     #          #just ignore because the user probably not logged in
     #       pass
   # except ValueError:
    

#adminMenu('85324259')
#doUserQuestions('85324259', '', '85324259')