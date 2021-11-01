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

    #password = str(input('Please enter your password: '))
    
    #def switch_demo():
    #    menu = int(input('Please choose a Option: '))
    #    switcher = {
    #        1: "Login",
    #        2: "Register",
    #        3: "Forget password",
    #    }
    #    print (switcher.get(menu, "Invalid Option" ))

    
