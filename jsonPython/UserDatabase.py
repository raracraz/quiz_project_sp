import os
import DBcom
import uuid
rowid = hash(uuid.uuid4())
username = str(input('Please enter your username: '))
def registerUser(rowid, username):
    
    DBcom.UserDB.create('users', 'username', 's', rowid, username)

    #password = str(input('Please enter your password: '))
    
def switch_demo(argument):
    switcher = {
        1: "Login",
        2: "Register",
        3: "Forget password",
    }
    print (switcher.get(argument, "Invalid Option"))


