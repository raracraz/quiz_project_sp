import json
import os
import uuid
import base64
import re
class userDB():
    def create(tablename, colName, colType, rowid, data):
        path = ('db/' + tablename + '/' + colName)
        os.makedirs(path, exist_ok=True)
        data = (data.encode('utf-8'))
        data = base64.b64encode(data)
        filename = str(colType) + '_' + str(rowid) + '_' + str(data)
        with open(path +'/'+ filename + '_' + data) as f:
            f.write(str(data))
        return rowid
        
    def find(tablename, colName, data):
        results = []
        data = str(base64.b64encode(data))[2:-3]
        regex = re.compile(data)
        
        


