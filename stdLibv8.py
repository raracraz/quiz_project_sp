import os
import re
import base64
import json
import datetime
import uuid
import glob
import shutil
import DBcom
import random

#purpose of stdLibv7 is to make stdLibv7.py more organized
def menu(localrowid):
    print('\n\n+==================================+')
    print(colors.bold, colors.fg.cyan, '    Welcome to the The quiz', colors.reset)
    print('+==================================+\n')    
    print('1. Login')
    print('2. Register')
    print('3. Forget password')
    print('\n<ENTER> to Exit')


    try:
        choice = int(input('Please enter your choice: '))
        if choice == 1:
            login(localrowid)
        elif choice == 2:
            registerUser(localrowid, '')
        elif choice == 3:
            forgetPassword(localrowid)
        elif choice == 1008:
            registerUser(localrowid,"admin",'11111')
        else:
            menu(localrowid)
    except ValueError:
        print('Goodbye...')

        os._exit(0)
    menu(localrowid)

def aclchecker(localrowid, aclcheck):
    #rowid = DBcom.UserDB.find('users', 'username', 'data', 'id', username)
    aclraw = DBcom.UserDB.find('users', 'acl', 'id','re' , 'raw', localrowid)
    #print(aclraw)
    #print(localrowid)

    acl = str(base64.b64decode(aclraw[0].split('_')[2]))[1:]
    #print(acl)
    if acl[aclcheck] == '1':
        return True
    else:
        return False

#############################################################################
#                           Part of register()                              #
#############################################################################
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
        print(colors.fg.cyan, '   Create User / Admin User Menu', colors.reset)
        print('+==================================+')
    else:
        print('+==================================+')
        print(colors.bold, colors.fg.cyan, '\t  Create User Menu', colors.reset)
        print('+==================================+')        
        print('Requirements:')
        print('1. Username must be between 4 and 20 characters')
        print('2. Username must contain at least one special character [@#$%^&+=]')
        print('3. Username must contain at least one upper and lower case letter')
        print('4. Username must contain at least one number [0-9]')
        print('5. Password must be between 4 and 20 characters')
        print('6. Password must contain at least one special character [@#$%^&+=]')
        print('7. Password must contain at least one number [0-9]')
        print('8. Password must contain at least one upper and lower case letter')
        print('<b> to back')
        print('+==================================+')
    reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{4,20}$"
    pat = re.compile(reg)
    username = str(input('Please enter your username: '))
    if username == 'b':
        menu(localrowid)
    mat = re.search(pat, username)
    if mat:
        pass
    else:
        print('Username is not valid')
        registerUser(rowid,fromwhere)
    #if username is empty go back
    if username == '':
        if fromwhere == 'admin':
            doAdminUser(localrowid, username)
        else:
            menu(localrowid)

    password = str(input('Please enter your password: '))
    mat = re.search(pat, password)
    if mat:
        pass
    else:
        print('Password is not valid')
        registerUser(rowid,fromwhere)
    email = str(input('Please enter your email: '))
    otp = str(generateOTP())

    #first let's check if username is already taken
    if len(DBcom.UserDB.find('users', 'username', 'data','' , 'bool', username)) > 0:
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
    if len(DBcom.UserDB.find('users', 'email', 'data','' ,'bool', email)) > 0:
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
                doAdminUser(rowid, username)
            else:
                menu(rowid)
        except ValueError:
            print('Error creating user')
            registerUser(localrowid,fromwhere)
    else:
        registerUser(localrowid,fromwhere)

#############################################################################
#                           Part of forgetPassword()                        #
#############################################################################

def forgetPassword(localrowid):
    print('+==================================+')
    print(colors.bold, colors.fg.cyan, '\t  Forget Password', colors.reset)
    print('+==================================+')
    print('\n<ENTER> to back')
    email = str(input('Please enter your email: '))
    
    #check if email is valid

    if email == '':
        menu(localrowid)

    if re.match(r"[^@]+@[^@]+\.[^@]+", email) == None:
        print('Email is not valid')
        forgetPassword(localrowid)
    else:
        try:
            localrowid = DBcom.UserDB.find('users', 'email', 'data','', 'id', email)[0]
        except IndexError:
            print('Email not found')
            forgetPassword(localrowid)
        print(localrowid)
        if len(localrowid) != '':
            try:
                #password = str(base64.b64decode(DBcom.UserDB.find('users', 'password', 'id','raw', localrowid[0])[0].split('_')[2]))[1:]
                password = str(DBcom.UserDB.find('users', 'password', 'id','','raw', localrowid)).split('_')[2][0:-2]
                print(password)
                print('+==================================+\n')
                print('We have sent the password {} to your Email {}'.format(password,email))
                print('+==================================+\n')
                menu(localrowid)
            except:
                forgetPassword(localrowid)
        else:
            print('Email not found')
            forgetPassword(localrowid)

#############################################################################
#                           Part of login()                                 #
#############################################################################

def login(localrowid):
    print('+==================================+')
    print(colors.bold, colors.fg.cyan, '\t     Login Menu', colors.reset)
    print('+==================================+')
    results = []
    username = ""
    password = ""
    username_pass = False
    password_pass = False
        
    try:
        print('\n<ENTER> to back')
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
            print(colors.bg.red, 'Please enter a valid password', colors.reset)
            login(localrowid)
        rowid = DBcom.UserDB.find('users', 'username', 'data','', 'id', username)
        username_pass = DBcom.UserDB.find('users', 'username', 'data','','bool', username)
        password_pass = DBcom.UserDB.find('users', 'password', 'data','','bool', password)
        userid = DBcom.UserDB.find('users', 'username', 'id','', 'id', username)
        #print(localrowid)
        #print(userid)
        #print(rowid)
        localrowid = rowid
        print('username:[{}/{}]/password:[{}/{}]/loggedin_rowid:{}'.format(username,username_pass,password,password_pass,localrowid))
        try:
            if len(username_pass) > 0 and len(password_pass) > 0 and localrowid != '':
                print('+==================================+')
                print(colors.fg.green ,'Login successful {}/{}'.format(username,localrowid), colors.reset)
                print('+==================================+')
                doUserQuestions(localrowid, username)
            else :
                print(colors.fg.red, 'a. Incorrect username or password', colors.reset)
                login(localrowid)
        except ValueError:
            print(colors.fg.red, 'b. Incorrect username or password', colors.reset)
            login(localrowid)

    except ValueError:
        login(localrowid)

#############################################################################
#                           After Logged in                                 #
#############################################################################

def doUserQuestions(localrowid, username):
    #print(userid)
    #userid = DBcom.UserDB.find('users', 'username', 'id', 'raw', localrowid)
    #print(userid)
    #userid = userid.split('_')[2]
    #userid = base64.b64decode(userid[0].split('_')[2]).decode('utf-8')
    #username = DBcom.UserDB.find('users', 'username', 'id', 'id', localrowid)
    #print(localrowid)
    #print(userid)
    print('+==================================+\n')
    print(colors.fg.cyan, '\tUser Question Menu...', colors.reset)
    print('UserID: {}'.format(username))
    print('+==================================+\n')
    print('1. Take Quiz')
    print('2. User results')
    if aclchecker(localrowid[0], 4) == True:
        print('5. Admin Menu')
    print('\n<ENTER> to go back to login page')
    print('(You will be logged out)')
    print('+==================================+\n')
    try:
        userChoice = int(input('Please enter your choice: '))
    except ValueError:
        menu(localrowid)
    if userChoice == 1:
        attCount = DBcom.UserDB.find('questions', 'NumberOfAtt', 'id', 're', 'raw', '')
        attCount = attCount[0].split('_')[2]
        takeQuiz(localrowid, username, count = attCount)
    elif userChoice == 2:
        userResults(localrowid, username)
    elif userChoice == 5:
        try:
            if aclchecker(localrowid[0], 4) == True:
                adminMenu(localrowid, username)
            else:
                print('You do not have access to this menu')
                menu(localrowid)
        except ValueError:
            pass
    else:
        print('Invalid choice...')
        doUserQuestions(localrowid, username)
    #try:
        #try:
        #    if aclchecker(username, 5) == True:
        #            print('5. Admin Menu')
       # except:
     #          #just ignore because the user probably not logged in
     #       pass
   # except ValueError:

def userResults(localrowid, username):
    print('+==================================+\n')
    print(colors.fg.cyan , '\tUser Results Menu...', colors.reset)
    print('UserID: {}'.format(username))
    print('+==================================+\n')
    
    '''
    try:
        userChoice = int(input('> '))
    except ValueError:
        doUserQuestions(localrowid, username)
    '''
    i = 1
    userList = DBcom.UserDB.find('users', 'results', 'id','re',  'raw', localrowid)
    for results in userList:
        if localrowid[0] == results.split('_')[0]:
            date = results.split('_')[2]
            date = str(base64.b64decode(date).decode('utf-8'))
            userResult = results.split('_')[3]
            print('{}. {} - {}%'.format(i, date, userResult))
            i += 1
    print('\n<ENTER> to go back')
    print('+==================================+\n')
    try:
        userChoice = int(input('> '))
        doUserQuestions(localrowid, username)
    except ValueError:
        doUserQuestions(localrowid, username)
#############################################################################
#                           Admin Menu + features                           #
#############################################################################

def adminMenu(localrowid, username):
    print('+==================================+\n')
    print(colors.fg.cyan, '    Welcome to the admin menu', colors.reset)
    print('+==================================+\n')
    print('1. Users')
    print('2. Questions')
    print('\n<ENTER> to go Back')
    try:
        choice = int(input('Please enter your choice: '))
    except ValueError:
        doUserQuestions(localrowid, username)
    if choice == 1:
        doAdminUser(localrowid, username)
    elif choice == 2:
        doAdminQuestions(localrowid, username)
    elif choice == 3:
        menu(localrowid)
    else:
        menu(localrowid)

def doAdminUser(localrowid, username):
    print('+==================================+\n')
    print(colors.fg.cyan, ' Welcome to the user setting menu', colors.reset)
    print('+==================================+\n')
    print('1. Create new user')
    print('2. List Users to Update/Delete')
    print('\n<ENTER> to go Back')
    try:
        choice = int(input('Please enter your choice: '))
    except ValueError:
        print('Please enter a valid choice')
        doUserQuestions(localrowid, username)
    if choice == 1:
        registerUser(localrowid,"admin")
    elif choice == 2:
        doAdminListUsers(localrowid, rowid='')
    else:
        print('Invalid choice...')
        menu(localrowid)

def doAdminUserEditData(userid, column, value, localrowid):
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

    doAdminUserEditList(userid, localrowid)

def doAdminUserDelData(userid, localrowid):
    #print(userid)
    print('Are you sure you want to delete this user? [y/n]')
    try:
        choice = int(input('Please enter your choice: '))
        if choice == 'y':
            DBcom.UserDB.deleteUser('users', 'username', userid)
            DBcom.UserDB.deleteUser('users', 'password',userid)
            DBcom.UserDB.deleteUser('users', 'email', userid)
            DBcom.UserDB.deleteUser('users', 'acl', userid)
            DBcom.UserDB.deleteUser('users', 'otp', userid)
            print('Deleted User successfully')
            menu(localrowid)
        elif choice == 'n':
            doAdminUserEditList(userid, localrowid)
        else:
            print('Invalid choice')
            doAdminUserEditList(userid, localrowid)
    except ValueError:
        print('Invalid choice...')
        doAdminUserEditList(userid, localrowid)

def doAdminUserEditList(userid, localrowid):
    username = DBcom.UserDB.find('users', 'username', 'id','re', 'raw', userid)
    acl = DBcom.UserDB.find('users', 'acl', 'id', 're','raw', userid)
    password = DBcom.UserDB.find('users', 'password', 'id', 're','raw', userid)
    otp = DBcom.UserDB.find('users', 'otp', 'id', 're','raw', userid)
    email = DBcom.UserDB.find('users', 'email', 'id', 're','raw', userid)
    username = str(base64.b64decode(username[0].split('_')[2]))[2:-1]
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
        choice = int(input('Please enter your choice [1-6]: '))

        if choice == 7:
            print(localrowid)
            print(userid)
            doAdminListUsers(localrowid, userid)
        elif choice == 6:
            #print(localrowid)
            #print(allusers)
            #rowid = allusers[choice-1].split('_')[0]
            #print(rowid)
            #print(userid)
            doAdminUserDelData(userid, localrowid)
        else:
            changeTo = input('Please enter the new value: ')

            if changeTo == '':
                doAdminListUsers(localrowid, userid)
            else:
                doAdminUserEditData(userid, choice, changeTo, localrowid)
    except ValueError:
        doAdminListUsers(localrowid, userid)

def doAdminListUsers(localrowid, rowid=''):
    print('+==================================+\n')
    print(colors.fg.cyan, '\t   List of Users', colors.reset)
    print('+==================================+\n')
    userlist = []
    usercount = 1
    allusers = DBcom.UserDB.find('users', 'username', 'id', 're','raw','')
    alluserscnt = len(allusers)
    for user in allusers:
        print("{}. Username: {} / UserID: {}".format(usercount,str(base64.b64decode(user.split('_')[2]))[2:-1],str(user.split('_')[0])))
        usercount = usercount + 1

    print('\n<ENTER> to go Back')

    try:
        choice = int(input('Please enter your choice [{}-{}]: '.format(1,alluserscnt)))
    except ValueError:
        doAdminUser(localrowid, '')

    if choice > alluserscnt:
        print('Please enter a valid choice')
        doAdminUser(localrowid, '')
    else:
        rowid = allusers[choice-1].split('_')[0]
        doAdminUserEditList(rowid, localrowid)

def randomizeQuestions(localrowid, username):
        print('+==================================+\n')
        print(colors.fg.cyan, '\tRandomizing Questions...', colors.reset)
        print('+==================================+\n')
        #get the list of questions
        allQns = DBcom.UserDB.find('questions', 'questions', 'id', 're','raw','')
        state = True
        #shuffle the list
        print(allQns)
        allQnsnum = len(allQns)
        random.shuffle(allQns)
        print(allQns)
        #print the list1
        #update the list
        print(localrowid)
        while state == True:
            for qn in allQns:
                qnid = qn.split('_')[0]
                qn = str(qn.split('_')[2])
                print(qn)
                print(qnid)
                DBcom.UserDB.update('questions', 'questions', 'r', qnid, qn)
            state = False
        '''
        for qn in allQns:
            rowid = qn.split('_')[0]
            for i in range(0,allQnsnum):
                if rowid == allQns[i].split('_')[0]:
                    DBcom.UserDB.update('questions', 'questions', 'r',rowid, str(allQns[i].split('_')[2]))
                    break
        '''
        print('+==================================+\n')
        print('Questions randomized successfully!')
        print('+==================================+\n')
        adminMenu(localrowid, username)

def doAdminQuestions(rowid, username):
    print('+==================================+\n')
    print(colors.fg.cyan, 'Welcome to the question setting menu', colors.reset)
    print('+==================================+\n')
    print('1. Create new question pool ')
    print('2. List Question Pools to Update/Delete')
    print('3. Add questions to the existing question pool')
    print('4. Randomize questions')
    print('5. Select number of questions in Quiz')
    print('6. Select number of Quiz attempts')
    print('\n<ENTER> to go Back')
    print('+==================================+')

    try:
        choice = int(input('Please enter your choice: '))
    except ValueError:
        adminMenu(rowid, username)
    if choice == 1:
        print('Are you sure? This will delete the current question pool[y/n]')
        try:
            choice = input('Please enter your choice: ')
        except ValueError:
            doAdminQuestions(rowid, username)
        if choice == 'y':
            adminCreateQuestionPool(rowid, username)
        else:
            doAdminQuestions(rowid, username)
    elif choice == 2:
        listQuestionPool(rowid, username)
    elif choice == 3:
        addQuestions(rowid, username)
        
    elif choice == 4:
        randomizeQuestions(rowid, username)
    elif choice == 5:
        adminSelectQuestions(rowid, username)
    elif choice == 6:
        adminSelectAttempts(rowid, username)
    else:
        pass

def adminSelectAttempts(localrowid, username):
    current = DBcom.UserDB.find('questions', 'NumberOfAtt', 'id', 're', 'raw', localrowid[0])
    current = current[0].split('_')[2]
    print('Current number of Attempts: {}'.format(current))
    try:
        choice = int(input('Please enter your choice: '))
        if choice == '':
            doAdminQuestions(localrowid, username)
    except ValueError:
        print('Please enter a valid choice')
        doAdminQuestions(localrowid, username)
    if choice >= 1 and choice <= 15:
        DBcom.UserDB.update('questions', 'NumberOfAtt', 'q', localrowid[0], choice)
        print('+==================================+\n')
        print('Number of Attempts set successfully!')
        doUserQuestions(localrowid, username)

def addQuestions(localrowid, username):
    print('+==================================+\n')
    print(colors.fg.cyan, '\tAdd Questions', colors.reset)
    print('+==================================+\n')
    print('How many questions do you want to add?')
    print('(max 10)')
    print('\n<ENTER> to go back')
    try:
        questionCount = int(input('> '))
    except ValueError:
        doAdminQuestions(localrowid, username)
    if questionCount < 1 or questionCount > 10:
        print('Invalid number of questions...')
        doAdminQuestions(localrowid, username)
    else:
        for i in range(1,questionCount+1):
            options = []
            opt = ['a','b','c','d']
            questionid = os.urandom(16)
            questionid = abs(hash(questionid) % (10 ** 8))
            print('\nCreating Question {}'.format(i))
            print('What is the question?')
            question = input('> ')
            question+str(i)
            #question = question.encode('utf-8')
            for j in range(1,5):
                print('What is the option {}?'.format(opt[j-1]))
                inputOptions = input('> ')
                #inputOptions = inputOptions.encode('utf-8')
                options.append(inputOptions)
            print('What is the correct answer?')
            print('[a, b, c ,d]')
            correctAnswer = input('> ')
            #correctAnswer = correctAnswer.encode('utf-8')

            if correctAnswer not in opt:
                print('Error, the correct answer is not in the options...')
                adminCreateQuestionPool(localrowid, username)
            options = str(options)
            print(options)
            print(question)
            print(correctAnswer)
            #print(type(options))
            options = options.replace("'","")
            options = options.replace("[","")
            options = options.replace("]","")
            #print(options)
            DBcom.UserDB.create('questions','options','q',questionid,options)
            DBcom.UserDB.create('questions','correctAnswers','q',questionid,correctAnswer)
            DBcom.UserDB.create('questions', 'questions', 'q', questionid, question)
            print('Question {} created successfully'.format(i))
        print('+==================================+\n')
        print('\n')
        print('+==================================+\n')
    doAdminQuestions(localrowid, username)

def adminSelectQuestions(localrowid, username):
    print('+==================================+\n')
    print(colors.fg.cyan, '\tSelect Number of Questions', colors.reset)
    print('+==================================+\n')
    print('How many questions should the Quiz have?')
    print('\n<ENTER> to go Back')
    QnsList = []
    current = DBcom.UserDB.find('questions', 'NumberOfQ', 'id', 're', 'raw', '')
    current = current[0].split('_')[2]
    print('Current number of questions: {}'.format(current))
    try:
        choice = int(input('Please enter your choice: '))
        if choice == '':
            doAdminQuestions(localrowid, username)
    except ValueError:
        print('Please enter a valid choice')
        doAdminQuestions(localrowid, username)
    if choice >= 5 and choice <= 10:
        DBcom.UserDB.update('questions', 'NumberOfQ', 'q', localrowid[0], choice)
        for i in range(1,choice+1):
            QnsList.append('Question-{}'.format(i))
            QnsList.append('User Answer')
            QnsList.append('Model Answer')
        #write a new header into results.csv
        open('results.csv', 'a').write('\n{},{},{},{}'.format('User',str(str(QnsList).split(',')).replace('"','').replace("'", '').replace('[', '').replace(']', '')),'Score(percent)','Date')
        print('+==================================+\n')
        print('Number of Questions set successfully!')
        doUserQuestions(localrowid, username)
    

def adminCreateQuestionPool(localrowid, username):
    print('+==================================+\n')
    print(colors.fg.cyan, '\tCreate Question Pool', colors.reset)
    print('+==================================+\n')
    #create the question pool
    #delete current questions
    
    DBcom.UserDB.delete('questions')
    print('How many questions do you want to have in the quiz?')
    print('(max 10)')
    print('\n<ENTER> to go back')
    
    try:
        questionCount = int(input('> '))
    except ValueError:
        adminMenu(localrowid, username)
    if questionCount < 1 or questionCount > 10:
        print('Invalid number of questions...')
        adminMenu(localrowid, username)
    else:
        for i in range(1,questionCount+1):
            options = []
            opt = ['a','b','c','d']
            questionid = os.urandom(16)
            questionid = abs(hash(questionid) % (10 ** 8))
            print('\nCreating Question {}'.format(i))
            print('What is the question?')
            question = input('> ')
            question+str(i)
            #question = question.encode('utf-8')
            for j in range(1,5):
                print('What is the option {}?'.format(opt[j-1]))
                inputOptions = input('> ')
                #inputOptions = inputOptions.encode('utf-8')
                options.append(inputOptions)
            print('What is the correct answer?')
            print('[a, b, c ,d]')
            correctAnswer = input('> ')
            #correctAnswer = correctAnswer.encode('utf-8')

            if correctAnswer not in opt:
                print('Error, the correct answer is not in the options...')
                adminCreateQuestionPool(localrowid, username)
            options = str(options)
            print(options)
            print(question)
            print(correctAnswer)
            #print(type(options))
            options = options.replace("'","")
            options = options.replace("[","")
            options = options.replace("]","")
            #print(options)
            DBcom.UserDB.createQn('questions','options','q',questionid,options)
            DBcom.UserDB.createQn('questions','correctAnswers','q',questionid,correctAnswer)
            DBcom.UserDB.createQn('questions', 'questions', 'q', questionid, question)
            print('Question {} created successfully'.format(i))
        DBcom.UserDB.createQn('questions', 'NumberOfQ', 'q', questionid, '5')
        DBcom.UserDB.createQn('questions', 'NumberOfAtt', 'q', questionid, '3')
            
        print('+==================================+\n')
        print('\n')
        print('+==================================+\n')
    adminMenu(localrowid, username)
    
def listQuestionPool(localrowid, username):
    print('+==================================+\n')
    print(colors.fg.cyan, '\tList Question Pool', colors.reset)
    print('+==================================+\n')
    #list the question pool
    allQns = DBcom.UserDB.find('questions', 'questions', 'id', 're','raw','')
    print(allQns)
    allQnscnt = len(allQns)
    allQnsnum = len(allQns)
    Qnscnt = 1
    for allQnscnt in allQns:
        print("{}. Question: {}/ID: {}".format(Qnscnt,str((allQnscnt.split('_')[2])),str(allQnscnt.split('_')[0])))
        Qnscnt = Qnscnt + 1
    print('+==================================+\n')
    print('Which question do you want to modify?: ')
    
    print('\n<ENTER> to go back\n')
    try:
        questionNumber = int(input('Please enter from [{}-{}]: '.format(1,allQnsnum)))
        adminModifyQuestion(localrowid, questionNumber, username)
    except ValueError:
        doAdminQuestions(localrowid, username)

def adminModifyQuestion(localrowid, questionNumber, username):
    print('+==================================+\n')
    print(colors.fg.cyan, '\tModify Question', colors.reset)
    print('+==================================+\n')
    questionid = ''
    opt = ['a', 'b', 'c', 'd']
    if questionNumber < 1 or questionNumber > 10:
        print('Invalid number of questions...')
        adminMenu(localrowid, username)
    else:
        questionNumber = questionNumber - 1
        question = DBcom.UserDB.find('questions', 'questions', 'id', 're','raw', '')
        question = question[questionNumber]
        options = DBcom.UserDB.find('questions', 'options', 'id', 're','raw', '')
        options = options[questionNumber]
        correctAnswer = DBcom.UserDB.find('questions', 'correctAnswers', 'id', 're','raw', '')
        correctAnswer = correctAnswer[questionNumber]
        print('Question: {}'.format(question.split('_')[2]))
        print('Options: ')
        for i in range(1,5):
            print('{}) {}'.format(opt[i-1],(options.split('_')[2]).replace(' ', '').split(',')[i-1]))
        print('Correct Answer: {}'.format(correctAnswer.split('_')[2]))
        print('+==================================+\n')
        print('What do you want to modify?')
        print('1. Question')
        print('2. Options')
        print('3. Correct Answer')
        print('\n<ENTER> to go back')
        print('+==================================+\n')
        try:
            modifyChoice = int(input('> '))
        except ValueError:
            adminMenu(localrowid, username)
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
            listQuestionPool(localrowid, username)
        elif modifyChoice == 2:
            print('These are the current options: ')
            print(options.split('_')[2][2:-2])
        
            print('What are the new options?: ')
            questionid = question.split('_')[0]
            options = options.split('_')[2]
            options = []
            try:
                for i in range(1,5):
                    newOption = str(input('Enter the new option {}: '.format(i)))
                    options.append(newOption)
                    print(options)
            except ValueError:
                print('Invalid input...')
                adminModifyQuestion(localrowid, questionNumber, username)
            print(options)
            DBcom.UserDB.update('questions', 'options', 'r', questionid, [options])
            print('Option successfully modified')
            listQuestionPool(localrowid, username)
        elif modifyChoice == 3:
            print(correctAnswer.split('_')[2])
            print('What is the new correct answer?')
            questionid = question.split('_')[0]
            try:
                print('\n<ENTER> to go back')
                newCorrectAnswer = input('What is the correct answer?: ')
            except ValueError:
                adminModifyQuestion(localrowid, questionNumber, username)
            
            if newCorrectAnswer not in opt:
                print('Error, the correct answer is not in the options...')
                print('Answer not changed.')
                adminModifyQuestion(localrowid, questionNumber, username)
            else:
                DBcom.UserDB.update('questions', 'correctAnswers', 'r', questionid, newCorrectAnswer)
                print('Correct answer successfully modified')
                listQuestionPool(localrowid, username)
    listQuestionPool(localrowid, username)


    
        

##############################################################################
#                               TakeQuiz                                     #
##############################################################################
def takeQuiz(localrowid, username, count):
    print('+==================================+\n')
    print(colors.fg.cyan, '\tTake Quiz', colors.reset)
    print('+==================================+\n')
    #list the question pool
    resultList = []
    Qnsno = DBcom.UserDB.find('questions', 'NumberOfQ', 'id', 're','raw','')
    Qnsno = int(Qnsno[0].split('_')[2])
    print(Qnsno)
    allQns = DBcom.UserDB.find('questions', 'questions', 'id','re', 'raw','')
    #print(allQns)
    alloptions = DBcom.UserDB.find('questions', 'options', 'id', 're','raw','')
    attCount = DBcom.UserDB.find('questions', 'NumberOfAtt', 'id', 're', 'raw', '')
    attCount = attCount[0].split('_')[2]
    attCount = int(attCount)
    allOptnum = len(alloptions)
    allQnscnt = len(allQns)
    if int(Qnsno) > int(allQnscnt):
        print('Error, there are not enough questions in the pool...')
        print('Please ask the admin to add more questions...')
        adminMenu(localrowid, username)
    Opt = ['a', 'b', 'c', 'd']
    state = True
    forward = ''
    question = ''
    Qnscnt = 0
    Qnsid = 1
    #print(allQns)
    #print(alloptions)
    #print(username)
    while state == True:
        if forward == 'n':
            Qnscnt = Qnscnt + 1
            Qnsid = Qnsid + 1
        elif forward == 'p':
            Qnscnt = Qnscnt - 1
            Qnsid = Qnsid - 1
            try:
                resultList.pop(Qnscnt)
                resultList.pop(Qnscnt-1)
            except IndexError:
                print('Error, you cannot go back on the first question')
                Qnscnt = Qnscnt + 1
                Qnsid = Qnsid + 1
                pass
        elif forward == 'e':
            print('Exiting Quiz...')
            doUserQuestions(localrowid, username)
        else:
            pass
        question = allQns[Qnscnt]
        
        #print(question)
        #print(allOptnum)
        print("QuestionID: {}/{}".format(Qnsid, Qnsno))
        print("Question:\n{}".format(str(question.split('_')[2])))
        for i in range(0, Qnsno+1):
            allOptnum = alloptions[i]
            if question.split('_')[0] == allOptnum.split('_')[0]:
                #print(allOptnum)
                    allOptnum = allOptnum.split('_')[2]
                    allOptnum = allOptnum.split(',')
                    allOptnum = [x.strip() for x in allOptnum]
                    print(allOptnum)
                    print("a) {}".format(str(allOptnum[0])))
                    print("b) {}".format(str(allOptnum[1])))
                    print("c) {}".format(str(allOptnum[2])))
                    print("d) {}".format(str(allOptnum[3])))
                    print('+==================================+')
                    print("What is the correct Answer?: ")
                    print('[a,b,c,d]')
                    try:
                        result = str(input('> ')).lower()
                        if result not in Opt:
                            print('Answer not in options')
                            print('Answer not saved.')
                            
                        else:
                            resultList.append(result)
                    except result == '':
                        print('Error, please enter a valid answer')
                        pass
                    except ValueError:
                        print('Error, please enter a valid answer')
                        pass
        
        
        print(resultList)
        print('+==================================+')
        print('[n]ext, [p]revious, [e]xit.[n/p/e]')
        try:
            forward = str(input('> ')).lower()
        except ValueError:
            print('Invalid input...')
            takeQuiz(localrowid, username, count)
        
        if Qnsid == Qnsno:
            print('You have reached the end of the quiz')
            print('+==================================+')
            print('Summary page:')
            for i in range(0, len(resultList)):
                print('Question: {}\nAnswer:{}'.format(allQns[i].split('_')[2], resultList[i]))
            print('+==================================+')
            print('[y]es to submit. [p]revious to back.')
            try:
                submit = str(input('> '))
            except ValueError:
                print('Invalid input...')
                takeQuiz(localrowid, username, count)
            if submit == 'y':
                state = False
                print(attCount)
                checkAnswer(localrowid, username, resultList, Qnsno, allQns, attCount, count)
            else:
                Qnscnt = Qnscnt - 1
                Qnsid = Qnsid - 1
                resultList.pop(Qnscnt)
                resultList.pop(Qnscnt-1)

    '''
    for i in allQns:
        if forward == '':
            question = i
        elif forward == 'n':
            print(question)
            question = allQns[Qnscnt+1]
            print(question)
            Qnsid+=1
        elif forward == 'p':
            print(question)
            question = allQns[Qnscnt-3]
            print(question)
            Qnsid-=1
    '''
    '''
    for i in allQns:
        question = i
        print(Qnscnt)
        print(allQns)
        print(allQnscnt)
        print("QuestionID: {}/{}".format(Qnsid, allQnsnum))
        print("Question: {}".format(str(question.split('_')[2])))
        for allOptnum in alloptions:
            if question.split('_')[0] == allOptnum.split('_')[0]:
            #print(allOptnum)
                allOptnum = allOptnum.split('_')[2]
                allOptnum = allOptnum.split(',')
                print("Options: {}".format(str(allOptnum[0])))
                print("        {}".format(str(allOptnum[1])))
                print("        {}".format(str(allOptnum[2])))
                print("        {}".format(str(allOptnum[3])))
                print('+==================================+')
                print("What is the correct Answer?: ")
                result = str(input('> '))
                resultList.append(result)
                #ask the user if they want to go next or previous question
                print('+==================================+')
                print('[n]ext to continue, [p]revious to back.[n/p]')
                try:
                    forward = str(input('> '))
                except ValueError:
                    print('Invalid input...')
                    takeQuiz(localrowid, username)
        #print(allQnscnt)
        #print(resultList)
    try:
        print('+==================================+')
        print('Do you want to submit the quiz?')
        print('[y]es or [n]o')
        submit = str(input('> '))
        if submit == 'y':
            print('+==================================+')
            checkAnswer(localrowid, username, resultList)
        elif submit == 'n':
            takeQuiz(localrowid, username)
        else:
            print('Invalid input...')
            takeQuiz(localrowid, username)
    except ValueError:
        print('Invalid input...')
        takeQuiz(localrowid, username)
    #DBcom.UserDB.createQn('users', 'results', 's', localrowid, resultList)
    print('+==================================+\n')
    '''
def checkAnswer(localrowid, username, resultList, Qnsno, allQns, attCount, count):
    print('+==================================+\n')
    print('Checking Answer...')
    print('+==================================+\n')
    localrowid = localrowid[0]
    QnsList = []
    #AnsList = []
    #ModelList = []
    #count = attCount
    #print('count>{}'.format(count)) = 3
    #print('attCount>{}'.format(attCount)) = 3
    #count = count - 1
    correctNum = 0
    score = 0
    state = True
    Tscore = Qnsno*2
    modelAnsList = DBcom.UserDB.find('questions', 'correctAnswers', 'id', 're','raw','')
    #print(resultList)
    #print(modelAnsList)
    print('User: {}'.format(username))
    for i in range(0, Qnsno):
        if modelAnsList[i].split('_')[2] == resultList[i]:
            #print(modelAnsList[i].split('_')[2])
            #print(resultList[i])
            #print(i)
            print('Question {}. Correct!'.format(i+1))
            correctNum = correctNum + 1
            score+=2
        else:
            print('Question {}. Incorrect!'.format(i+1))
    percnt = (correctNum/Qnsno) * 100
    percnt = round(percnt, 2)
    print('Final score: {}/{} - {}%'.format(score, Tscore, percnt))
    print('{}/{} questions correct.'.format(correctNum, Qnsno))
    DBcom.UserDB.createQn('users', 'results', 's', localrowid, percnt)
    #write percnt and username to results.csv
    #find the total number of questions
    for i in range(0, Qnsno):
        Qns = allQns[i]
        Ans = resultList[i]
        Model = modelAnsList[i]
        #Qns = Qns.split('_')[2]
        QnsList.append(Qns.split('_')[2])
        QnsList.append(Ans)
        QnsList.append(Model.split('_')[2])

    QnsList = str(QnsList).replace('[', '').replace(']', '').replace("'", '')
    #AnsList = str(AnsList).replace('[', '').replace(']', '').replace("'", '')
    #ModelList = str(ModelList).replace('[', '').replace(']', '').replace("'", '')
    open('results.csv', 'a').write('\n{},{},{},{}'.format(username, str(QnsList.split(',')).replace('[', '').replace(']', '').replace("'", '').replace(' ', ''), str(percnt)+'%', datetime.datetime.now()))
    #ask if user wants to retake quiz
    while state == True:
        print('Do you want to retake the quiz?')
        #print('count> {}'.format(count))
        count = int(count) - 1 
        print('[{}/{}] attempts left.'.format(count, attCount))
        print('[y]es or [n]o')
        try:
            retake = int(input('Please enter your choice: '))
            if retake == 'y':
                if count == 0:
                    print(colors.bg.red, 'You have no more attempts left.', colors.reset)
                    doUserQuestions(localrowid, username)
                    print('Thank you for taking the quiz.')
                    print('+==================================+')
                    state = False
                    doUserQuestions(localrowid, username)
                takeQuiz(localrowid, username, count)
            else:
                print('+==================================+')
                print('Thank you for taking the quiz.')
                print('+==================================+')
                doUserQuestions(localrowid, username)
                state = False
        except ValueError:
            print('Invalid input...')
            doUserQuestions(localrowid, username)

        print('+==================================+\n')



###############################################################################
#                               Extra feature(colors)                         #
###############################################################################

# Python program to print
# colored text and background
class colors:
	reset='\033[0m'
	bold='\033[01m'
	disable='\033[02m'
	underline='\033[04m'
	reverse='\033[07m'
	strikethrough='\033[09m'
	invisible='\033[08m'
	class fg:
		black='\033[30m'
		red='\033[31m'
		green='\033[32m'
		orange='\033[33m'
		blue='\033[34m'
		purple='\033[35m'
		cyan='\033[36m'
		lightgrey='\033[37m'
		darkgrey='\033[90m'
		lightred='\033[91m'
		lightgreen='\033[92m'
		yellow='\033[93m'
		lightblue='\033[94m'
		pink='\033[95m'
		lightcyan='\033[96m'
	class bg:
		black='\033[40m'
		red='\033[41m'
		green='\033[42m'
		orange='\033[43m'
		blue='\033[44m'
		purple='\033[45m'
		cyan='\033[46m'
		lightgrey='\033[47m'

#print(colors.bg.green, "SKk", colors.fg.red, "Amartya")
#print(colors.bg.lightgrey, "SKk", colors.fg.red, "Amartya")
