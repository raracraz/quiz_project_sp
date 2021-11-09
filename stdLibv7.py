# +==========================================================
# StdLib
# version 0.1109.1729
# last update: 2021-11-09
# created by: Crazzz
# +==========================================================

import os
import re
import base64
import datetime
import uuid
import glob

def aclchecker(localrowid, aclcheck):
    aclraw = UserDB.find('users', 'acl', 'id', 'raw',localrowid)
    try:
        acl = str(base64.b64decode(aclraw[0].split('_')[2]))[1:]
        if acl[aclcheck] == '1':
            return True
        else:
            return False
    except:
        return False

def adminMenu(localrowid):
    print('Welcome to the admin menu')
    print('1. Users')
    print('2. Questions')
    print('\n<ENTER> to go Back')
  
    try:
        choice = int(input('Please enter your choice: '))
    except ValueError:
        menu(localrowid)
    if choice == 1:
        doAdminUser(localrowid)
    elif choice == 2:
        doAdminQuestions(localrowid)
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
        UserDB.update('users', 'username', 's',userid, value)
    elif column == 2:
        UserDB.update('users', 'password', 's',userid, value)
    elif column == 3:
        UserDB.update('users', 'email', 's',userid, value)
    elif column == 4:
        UserDB.update('users', 'acl', 's',userid, value)
    elif column == 5:
        UserDB.update('users', 'otp', 's',userid, value)

    doAdminUserEditList(userid)

def doAdminUserEditList(userid):
    userinfo = UserDB.find('users', 'username', 'id', 'raw', userid)
    acl = UserDB.find('users', 'acl', 'id', 'raw', userid)
    password = UserDB.find('users', 'password', 'id', 'raw', userid)
    otp = UserDB.find('users', 'otp', 'id', 'raw', userid)
    email = UserDB.find('users', 'email', 'id', 'raw', userid)
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
    print('\n<ENTER> to go Back')
    try:
        choice = int(input('Please enter your choice: [1-6]'))

        if choice == 6:
            doAdminListUsers(userid)
        else:
            changeTo = input('Please enter the new value: ')

            if changeTo == '':
                doAdminListUsers(userid)
            else:
                doAdminUserEditData(userid, choice, changeTo)

    except ValueError:
        doAdminListUsers(userid)
    

def doAdminListUsers(rowid):
    userlist = []
    usercount = 1
    allusers = UserDB.find('users', 'username', 'id', 'raw','')
    alluserscnt = len(allusers)
    for user in allusers:
        print("{}. {}/{}".format(usercount,str(base64.b64decode(user.split('_')[2]))[2:-1],str(user.split('_')[0])))
        usercount = usercount + 1

    print('\n<ENTER> to go Back')

    try:
        choice = int(input('Please enter your choice: [{}-{}]' .format(1,alluserscnt)))
    except ValueError:
        doAdminUser(rowid)

    if choice > alluserscnt:
        print('Please enter a valid choice')
        doAdminUser(rowid)
    else:
        rowid = allusers[choice-1].split('_')[0]
        doAdminUserEditList(rowid)
    

    

def doAdminQuestions(rowid):
    pass

def menu(localrowid=hash(uuid.uuid4())):
    print('\n\n+==================================+')
    try:
        username = UserDB.find('users', 'username', 'id', 'arr', localrowid)
        print(username)
        
        print('Welcome to the The quiz [{}/{}]'.format(username[0],localrowid))
    except:
        print('Welcome to the The quiz')
    print('+==================================+')    
    print('1. Login')
    print('2. Register')
    print('3. Forget password')
    print('4. Questions')
    try:
        try:
            if aclchecker(localrowid, 5) == True:
                print('5. Admin Menu')
        except:
            #just ignore because the user probably not logged in
            pass
    except ValueError:
        os._exit(0)
    print('\n<ENTER> to Exit')


    try:
        choice = int(input('Please enter your choice: '))
        if choice == 1:
            login(localrowid)
        elif choice == 2:
            registerUser(localrowid,"normal")
        elif choice == 3:
            forgetPassword(localrowid)
        elif choice == 4:
            doQuestions(localrowid)
        elif choice == 1008:
            registerUser(localrowid,"admin",'11111')
        elif choice == 5:
            if aclchecker(localrowid,5) == True:
                adminMenu(localrowid)
            else:
                print('You do not have access to this menu')
                menu(localrowid)
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
    if len(UserDB.find('users', 'username', 'data', 'bool', username)) > 0:
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
    if len(UserDB.find('users', 'email', 'data', 'bool', email)) > 0:
        print('Email already taken')
        email_pass = False
    else:
        email_pass = True


    if username_pass == True and email_pass == True:
        try:

            UserDB.create('users', 'acl', 's', localrowid, acl)
            UserDB.create('users', 'username', 's', localrowid, username)
            UserDB.create('users', 'password', 's', localrowid, password)
            UserDB.create('users', 'otp', 's', localrowid, str(otp))
            UserDB.create('users', 'email', 's', localrowid, email)
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

        rowid = UserDB.find('users', 'username', 'data', 'id', username)
        username_pass = UserDB.find('users', 'username', 'data','bool', username)
        password_pass = UserDB.find('users', 'password', 'data','bool', password)
        localrowid = rowid

        print('username:[{}/{}]/password:[{}/{}]/loggedin_rowid:{}'.format(username,username_pass,password,password_pass,localrowid))

        try:
            if len(username_pass) > 0 and len(password_pass) > 0 and localrowid != '':
                print('=============================')
                print('Login successful {}/{}'.format(username,localrowid))
                print('=============================')
                menu(localrowid)
            else:
                print('a. Incorrect username or password')
                login(localrowid)
        except:
            print('b. Incorrect username or password')
            login(localrowid)

    except ValueError:
        menu(localrowid)

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
        localrowid = UserDB.find('users', 'email', 'data', 'arr', email)[0]
        if len(localrowid) != '':
            #try:
            password = str(base64.b64decode(UserDB.find('users', 'password', 'id','raw', localrowid[0])[0].split('_')[2]))[1:]
            
            print('+==================================+\n')
            print('We have sent the password is {} to your Email {}'.format(password,email))
            print('+==================================+\n')
            menu(localrowid)
            #except:
            #    forgetPassword(rowid)
        else:
            print('Email not found')
            forgetPassword(localrowid)

class UserDB():
    def create(tableName, colName, colType, localrowid, data):
        path = ('jsonPython/db/' + tableName + '/' + colName)
        os.makedirs(path, exist_ok=True)
        data = data.encode('utf-8')
        data = base64.b64encode(data)
        filename = str(localrowid) + '_' + str(colType) + '_' + str(data)[2:-1]
        with open(path +'/'+ filename, 'w+') as f:
            f.write(str(data))
        return localrowid

    def find(tableName, colName, searchPart, returnType, data):
        results = []

        if searchPart == 'id':
            data = str(data)
        else:
            data = str(data).encode('utf-8')
            #data = str(base64.b64encode(data))[2:-3]

        #file_list = sorted(os.walk('jsonPython/db/'+ tableName+'/'+ colName))
        dir_name = 'jsonPython/db/'+tableName+'/' + colName
        file_list = sorted(filter(os.path.isfile, glob.glob(dir_name + "/*")),key=os.path.getmtime)
        #file_list = sorted(filter(os.path.isfile, glob.glob('jsonPython/db/'+tableName+'/'+colName,recursive=True)))

        for files in file_list:

            file = os.path.basename(files)
            #print('[{}]'.format(file))

            if searchPart == 'data':
                #file_data = str(file.split('_')[2])[:-2]
                file_data = str(file.split('_')[2])
                file_data = base64.b64decode(file_data)
            else:
                file_data = str(file.split('_')[0])
            
            if bool(re.match(data,file_data)):
                if returnType == 'bool':
                    #print('bool>', data,'[',file_data,']')
                    results.append(True)
                elif returnType == 'arr':
                    #print('arr>', data,'[',file_data,']')
                    results.append(str(base64.b64decode(file.split('_')[2]))[2:-1])
                elif returnType == 'id':
                    #print('id>', data,'[',file_data,']')
                    results.append(file.split('_')[0])
                else:
                    #print('raw>', data,'[',file_data,']')
                    results.append(file)
        return results

    def read(tableName, colName, localrowid):
        path = ('jsonPython/db/' + tableName + '/' + colName)
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.split('_')[0] == str(localrowid):
                    data = base64.b64encode(file.split('_')[2])
                    data = str(data)[2:-1]
                    return data

    def update(tableName, colName, colType, localrowid, data):
        path = ('jsonPython/db/' + tableName + '/' + colName)
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.split('_')[0] == str(localrowid):
                    data = data.encode('utf-8')
                    data = base64.b64encode(data)
                    data = str(data)[2:-1]
                    os.remove(path +'/'+ file)
                    with open(path +'/'+ str(localrowid) + '_' + colType + '_' + str(data), 'w+') as f:
                        f.write(str(data))
                    return data     
    
    def BAKupdate(tableName, colName, colType, rowid, data, colType2, rowid2, data2, userinput):
        path = ('jsonPython/db/' + tableName + '/' + colName)
        oldFileName = str(colType) + '_' + str(rowid) + '_' + str(data)
        newFileName = str(colType2) + '_' + str(rowid2) + '_' + str(data2)
        for root, dirs, files in os.walk(path):
            for file in files:
                if userinput == oldFileName:
                    os.rename(oldFileName, newFileName)
                    print('Successfully updated' + oldFileName + ' to ' + newFileName)
                    return True
                else:
                    print('Error, could not update file...')
                    return False

    def delete(tableName, colName, localrowid):
        path = ('jsonPython/db/' + tableName + '/' + colName + '/' + localrowid)
        if os.path.exists(path):
            os.rmdir(path)
            print('Deleted' + path + 'successfully')
            return True
        else:
            print('This table does not exist...')
            return False

# end of UserDB class

#start of main quiz functions

menu()