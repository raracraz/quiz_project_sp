import os
import re
import base64
import datetime

def aclchecker(rowid, aclcheck):
    aclraw = UserDB.find('users', 'acl', 'raw',rowid)
    try:
        acl = str(base64.b64decode(aclraw[0].split('_')[2]))[1:]
        if acl[aclcheck] == '1':
            return True
        else:
            return False
    except:
        return False

def adminMenu(rowid):
    print('Welcome to the admin menu')
    print('1. Create/Modify user/password')
    print('2. Delete user')
    print('5. Exit')

def menu(rowid):
    print('\n\n+==================================+')
    try:
        username = str(base64.b64decode(UserDB.find('users', 'username', 'raw', rowid)[0].split('_')[2]))[1:]
        print('Welcome to the The quiz [{}]'.format(username))
    except:
        print('Welcome to the The quiz')
    print('+==================================+')    
    print('1. Login')
    print('2. Register')
    print('3. Forget password')
    print('4. Exit')
    try:
        if aclchecker(rowid, 5) == True:
            print('5. Admin Menu')
    except ValueError:
        pass
    try:
        choice = int(input('Please enter your choice: '))
    except ValueError:
        print('Please enter a valid choice')
        menu(rowid)
    if choice == 1:
        login(rowid)
    elif choice == 2:
        registerUser(rowid)
    elif choice == 3:
        forgetPassword(rowid)
    elif choice == 4:
        os._exit(0)
    elif choice == 5:
        if aclchecker(rowid,5) == True:
            adminMenu(rowid)
        else:
            print('You do not have access to this menu')
            menu(rowid)
    else:
        print('Please enter a valid choice')
        menu(rowid)

def generateOTP():
    #get a random number then hash it to 8 digits
    randomNumber = os.urandom(16)
    randomNumber = abs(hash(randomNumber) % (10 ** 8))
    return randomNumber

def registerUser(rowid):
    #acl = '11111' #to create admin user
    acl = '00000'
    username = str(input('Please enter your username: '))
    password = str(input('Please enter your password: '))
    email = str(input('Please enter your email: '))
    otp = str(generateOTP())
    #first let's check if username is already taken
    if UserDB.find('users', 'username', 'bool', username) == True:
        print('Username already taken')
        registerUser(rowid)
    else:
        username_pass = True
    #now let's check if email is already taken
    if UserDB.find('users', 'email', 'bool', email) == True:
        print('Email already taken')
        registerUser(rowid)
    else:
        email_pass = True
    #now let's check if email is a valid email
    if re.match(r"[^@]+@[^@]+\.[^@]+", email) == None:
        print('Email is not valid')
        registerUser(rowid)
    else:
        email_pass = True
    if username_pass == True and email_pass == True:
        try:
            UserDB.create('users', 'acl', 's', rowid, acl)
            UserDB.create('users', 'username', 's', rowid, username)
            UserDB.create('users', 'password', 's', rowid, password)
            UserDB.create('users', 'otp', 's', rowid, str(otp))
            UserDB.create('users', 'email', 's', rowid, email)
            print('+==================================+\n')
            print('Registration successful,\nreturn to the menu to login!\n')
            print('your email is {}, recovery OTP is {}'.format(email,otp))
            print('+==================================+\n')
            menu(rowid)
        except:
            print('Error creating user')
            registerUser(rowid)


#function to login using DBcom find function with data
def login(rowid):
    results = []
        
    try:
        username = str(input('Please enter your username: '))

        #if there is no username entered.
        if username == '':
            print('+==================================+\n')
            print('Login terminated.!\n')
            print('+==================================+\n')
            menu(rowid)

        try:
            password = str(input('Please enter your password: '))
        except ValueError:
            print('Please enter a valid password')
            login(rowid)

        rowid = UserDB.find('users', 'username', 'arr', username)
        try:
            username = str(base64.b64decode(UserDB.find('users', 'username', 'raw', rowid)[0].split('_')[2]))[1:]
            password = UserDB.find('users', 'password', 'arr', password)

            print('username:{}/password:{}'.format(username,password))

            if len(username) > 0 and len(password) > 0:
                print('=============================')
                print('Login successful {}'.format(username))
                print('=============================')
                menu(rowid[0])
            else:
                print('a. Incorrect username or password')
                login(rowid)

        except:
            print('b. Incorrect username or password')
            login(rowid)

    except ValueError:
        print('Error : {}'.format(ValueError))
        os._exit(1)

#function to forget password using DBcom find function

def forgetPassword(rowid):
    email = str(input('Please enter your email: '))
    #check if email is valid

    if email == '':
        menu(rowid)

    if re.match(r"[^@]+@[^@]+\.[^@]+", email) == None:
        print('Email is not valid')
        forgetPassword(rowid)
    else:
        rowid = UserDB.find('users', 'email', 'arr', email)[0]
        if len(rowid) != '':
            #try:
            password = str(base64.b64decode(UserDB.find('users', 'password', 'raw', rowid[0])[0].split('_')[2]))[1:]
            
            print('+==================================+\n')
            print('We have sent the password is {} to your Email {}'.format(password,email))
            print('+==================================+\n')
            menu(rowid)
            #except:
            #    forgetPassword(rowid)
        else:
            print('Email not found')
            forgetPassword(rowid)

class UserDB():
    def create(tableName, colName, colType, rowid, data):
        path = ('jsonPython/db/' + tableName + '/' + colName)
        os.makedirs(path, exist_ok=True)
        data = data.encode('utf-8')
        data = base64.b64encode(data)
        filename = str(rowid) + '_' + str(colType) + '_' + str(data)[2:-1]
        with open(path +'/'+ filename, 'w+') as f:
            f.write(str(data))
        return rowid

    def find(tableName, colName, returnType, data):
        results = []

        #print('returnType:{}'.format(returnType))

        if returnType == 'id' or returnType == 'raw':
            regex = re.compile(str(data))
        else:
            data = (data.encode('utf-8'))
            data = str(base64.b64encode(data))[2:-3]
            regex = re.compile(data)
        for root, dirs, files in os.walk('jsonPython/db/'+ tableName+'/'+ colName):
            for file in files:
                if returnType == 'arr':
                    file_data = file.split('_')[2]
                else:
                    file_data = file
                if bool(re.match(regex, file_data)):
                    #print('>', file_data,'[',data,']'),
                    if returnType == 'bool':
                        results.append(True)
                    elif returnType == 'arr':
                        results.append(file.split('_')[0])
                    elif returnType == 'raw':
                        results.append(file)
        return results

    def read(tableName, colName, rowid):
        path = ('jsonPython/db/' + tableName + '/' + colName)
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.split('_')[0] == str(rowid):
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

    def delete(tableName, colName, rowid):
        path = ('jsonPython/db/' + tableName + '/' + colName + '/' + rowid)
        if os.path.exists(path):
            os.rmdir(path)
            print('Deleted' + path + 'successfully')
            return True
        else:
            print('This table does not exist...')
            return False
'''
    def delete(tableName, colName, colType, rowid, data):
        path = ('jsonPython/db/' + tableName + '/' + colName)
        filename = str(colType) + '_' + str(rowid) + '_' + str(data)
        if os.path.exists(path + '/' + filename):
            os.remove(path + '/' + filename)
            print('Deleted' + path + '/' + filename)
            return True
        else:
            print('This file does not exist...')
            return False
'''
'''
    def delete(tableName, colName, rowid):
        path = ('jsonPython/db/' + tableName + '/' + colName)
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.split('_')[0] == str(rowid):
                    os.remove(file)
                    print('Successfully deleted ' + file)
                    return True
                else:
                    print('Error, could not delete file...')
                    return False
'''