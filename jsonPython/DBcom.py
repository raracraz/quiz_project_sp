import json
import os
import uuid
import base64
class userDB():
    def create(tablename, colName, colType, rowid, data):
        path = ('db/' + tablename + '/' + colName)
        os.makedirs(path, exist_ok=True)
        data = base64.b64encode(data)
        
        
        


