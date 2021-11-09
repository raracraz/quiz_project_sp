import os
import re
import base64
import datetime

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
    print('3. Back')
  
    try:
        choice = int(input('Please enter your choice: '))
    except ValueError:
        print('Please enter a valid choice')
        menu(localrowid)
    if choice == 1:
        doAdminUser(localrowid)
    elif choice == 2:
        doAdminQuestions(localrowid)
    elif choice == 3:
        menu(localrowid)
    else:
        print('Please enter a valid choice')
        menu(localrowid)

def doAdminUser(localrowid):
    print('Welcome to the user admin menu [{}]'.format(localrowid))
    print('1. Create new user')
    print('2. List Users to Update/Delete')
    print('3. Back')
  
    try:
        choice = int(input('Please enter your choice: '))
    except ValueError:
        print('Please enter a valid choice')
        menu(localrowid)
    if choice == 1:
        registerUser(localrowid,"admin")
    elif choice == 2:
        doAdminListUsers(localrowid)
    elif choice == 3:
        menu(localrowid)
    else:
        print('Please enter a valid choice')
        menu(localrowid)

def doAdminListUsers(rowid):
    userlist = []
    usercount = 1
    allusers = UserDB.find('users', 'username', 'id', 'raw','')
    for user in allusers:
        print("{}. {}/{}".format(usercount,str(base64.b64decode(user.split('_')[2]))[2:-1],str(user.split('_')[0])))
        usercount = usercount + 1
    

def doAdminQuestions(rowid):
    pass

def menu(localrowid):
    print('\n\n+==================================+')
    try:
        username = UserDB.find('users', 'username', 'id', 'arr', localrowid)
        print('Welcome to the The quiz [{}/{}]'.format(username[0],localrowid[0]))
    except:
        print('Welcome to the The quiz')
    print('+==================================+')    
    print('1. Login')
    print('2. Register')
    print('3. Forget password')
    print('4. Questions')
    print('5. Exit')
    try:
        if aclchecker(localrowid, 5) == True:
            print('6. Admin Menu')
    except ValueError:
        pass
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
        elif choice == 5:
            os._exit(0)
        elif choice == 1008:
            registerUser(localrowid,"admin",'11111')
        elif choice == 6:
            if aclchecker(localrowid,5) == True:
                adminMenu(localrowid)
            else:
                print('You do not have access to this menu')
                menu(localrowid)
        else:
            print('Please enter a valid choice')
            menu(localrowid)


    except ValueError:
        print('Please enter a valid choice')
        menu(localrowid)

def generateOTP():
    #get a random number then hash it to 8 digits
    randomNumber = os.urandom(16)
    randomNumber = abs(hash(randomNumber) % (10 ** 8))
    return randomNumber

def registerUser(rowid,fromwhere, acl = '00000'):
    username_pass = False
    password_pass = False
    email_pass = False
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

        if username_pass[0] == True and password_pass[0] == True and localrowid != '':
            print('=============================')
            print('Login successful {}/{}'.format(username,localrowid))
            print('=============================')
            menu(localrowid)
        else:
            print('a. Incorrect username or password')
            login(localrowid)

    except ValueError:
        print('Error : {}'.format(ValueError))
        os._exit(1)

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

        for root, dirs, files in os.walk('jsonPython/db/'+ tableName+'/'+ colName):
            for file in files:
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
    
    def update(tableName, colName, colType, rowid, data, colType2, rowid2, data2, userinput):
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
