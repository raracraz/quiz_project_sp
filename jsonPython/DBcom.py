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
        data = (data.encode('utf-8'))
        data = str(base64.b64encode(data))[2:-3]
        regex = re.compile(data)

        for root, dirs, files in os.walk('db/'+ tablename+'/'+ colName):
            for file in files:
                file_data = file.split('_')[2]
                if bool(re.match(regex, file_data)):
                    print('>', file_data,'[',data,']')
                    results.append(file.split('_')[0])
        return results

    def read(tablename, colName, rowid):
        path = ('db/' + tablename + '/' + colName)
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.split('_')[0] == str(rowid):
                    data = base64.b64encode(file.split('_')[2])
                    data = str(data)[2:-1]
                    return data     

    def update(tablename, colName, colType, rowid, data):
        path = ('db/' + tablename + '/' + colName)
        os.chdir(path)
        data = (data.encode('utf-8'))
        data = base64.b64encode(data)
        oldFileName = str(colType) + '_' + str(rowid) + '_' + str(data)
        newFileName = str(colType) + '_' + str(rowid) + '_' + str(data)
        
        #os.rename(oldName, newName)


        


