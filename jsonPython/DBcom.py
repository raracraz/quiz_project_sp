import json
import os #navigate file system
import base64 #ensures that each character is supported by the file system
import re #use to manipulate strings
class UserDB():
    def create(tableName, colName, colType, rowid, data):
        path = ('./db/' + tableName + '/' + colName)
        
        os.makedirs(path, exist_ok=True)
        data = (data.encode('utf-8'))
        data = base64.b64encode(data)
        filename = str(rowid) + '_' + str(colType) + '_' + str(data)[2:-1]
        with open(path +'/'+ filename, 'w+') as f:
            f.write(str(data))
        return rowid

    def find(tableName, colName, data):
        results = []
        data = (data.encode('utf-8'))
        data = str(base64.b64encode(data))[2:-3]
        regex = re.compile(data)
        for root, dirs, files in os.walk('db/'+ tableName+'/'+ colName):
            for file in files:
                file_data = file.split('_')[2]
                if bool(re.match(regex, file_data)):
                    print('>', file_data,'[',data,']')
                    results.append(file.split('_')[0])
        return results

    def find_rowid(tableName, colName, rowid):
        results = []
        regex = re.compile(rowid)
        path = ('db/' + tableName + '/' + colName)
        for root, dirs, files in os.walk(path):
            for file in files:
                file_data = file.split('_')[0]
                if bool(re.match(regex, file_data)):
                    print('>', file_data, '[',rowid,']')
                    results.append(file.split('_')[0])
        return results

    def read(tableName, colName, rowid):
        path = ('db/' + tableName + '/' + colName)
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.split('_')[0] == str(rowid):
                    data = base64.b64encode(file.split('_')[2])
                    data = str(data)[2:-1]
                    return data     

    def update(tableName, colName, colType, rowid, data, colType2, rowid2, data2, userinput):
        path = ('db/' + tableName + '/' + colName)
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

    def delete(tableName, colName, colType, rowid, data):
        path = ('db/' + tableName + '/' + colName)
        filename = str(colType) + '_' + str(rowid) + '_' + str(data)
        if os.path.exists(path + '/' + filename):
            os.remove(path + '/' + filename)
            print('Deleted' + path + '/' + filename)
            return True
        else:
            print('This file does not exist...')
            return False

        