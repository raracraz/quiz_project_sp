import json
import DBcommands
import os
#User data has id, email, password and accesslevel.
def current_path():
    print("Current working directory")
    print(os.getcwd())
    print()
current_path()

os.makedirs('quiz_app/db/users/password')
     
current_path()
