# Use file system to store rows of data.
# Provides high concurrency and low latency only limited by the file system.
# does not have read/write locks.
# usage:
# create - create a new table with a column and row data returns unquie rowid
# find - find a matching data in table/column returns rowid
# read - read data from table/column/rowid returns data
# update - update data in table/column/rowid returns true/false
# delete - delete data from table/column/rowid returns true/false

import os #navigate file system
import base64 #ensures that each character is supported by the file system
import re #use to manipulate strings
class UserDB():
    def create(tableName, colName, colType, rowid, data):
        path = (tableName + '/' + colName)
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
        for root, dirs, files in os.walk(tableName+'/'+ colName):
            for file in files:
                file_data = file.split('_')[2]
                if bool(re.match(regex, file_data)):
                    #print('>', file_data,'[',data,']')
                    results.append(file.split('_')[0])
                    return True
        return False

    def find_rowid(tableName, colName, rowid):
        results = []
        regex = re.compile(rowid)
        path = (tableName + '/' + colName)
        for root, dirs, files in os.walk(path):
            for file in files:
                file_data = file.split('_')[0]
                if bool(re.match(regex, file_data)):
                    print('>', file_data, '[',rowid,']')
                    results = results.append(file.split('_')[0])
                    return True
        return False

    def read(tableName, colName, rowid):
        path = (tableName + '/' + colName)
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.split('_')[0] == str(rowid):
                    data = base64.b64encode(file.split('_')[2])
                    data = str(data)[2:-1]
                    return data     
    
    def update(tableName, colName, colType, rowid, data, colType2, rowid2, data2, userinput):
        path = (tableName + '/' + colName)
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
        path = (tableName + '/' + colName + '/' + rowid)
        if os.path.exists(path):
            os.rmdir(path)
            print('Deleted' + path + 'successfully')
            return True
        else:
            print('This table does not exist...')
            return False
'''
    def delete(tableName, colName, colType, rowid, data):
        path = ( tableName + '/' + colName)
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
        path = ( tableName + '/' + colName)
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
        