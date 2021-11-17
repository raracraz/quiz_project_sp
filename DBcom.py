from datetime import datetime
import os
import base64
import hashlib
import glob
import shutil
import re
class UserDB():
    def create(tableName, colName, colType, localrowid, data):
        path = ('jsonPython/db/' + tableName + '/' + colName)
        os.makedirs(path, exist_ok=True)
        if colType == 's':
            data = data.encode('utf-8')
            data = str(base64.b64encode(data))
        
        #filename = str(localrowid) + '_' + str(colType) + '_' + str(data)[2:-1]
        if colType == 'r':
            filename = str(localrowid) + '_' + str(colType) + '_' + str(data)[2:-1]
        if colType == 'q':
            filename = str(localrowid) + '_' + str(colType) + '_' + str(data)
        #date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(path+'/'+filename, 'w+') as f:
            #f.write(date+'_'+str(data))
            f.write(str(data))
        return localrowid
    
    def createQn(tableName, colName, colType, localrowid, data):
        path = ('jsonPython/db/' + tableName + '/' + colName)
        os.makedirs(path, exist_ok=True)
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        date = date.encode('utf-8')
        date = str(base64.b64encode(date))
        data = str(date) + '_' + str(data)
        filename = str(localrowid) + '_' + str(colType) + '_' + str(data)[2:-1]
        with open(path+'/'+filename, 'w+') as f:
            f.write(str(data))
        return localrowid

    def find(tableName, colName, searchPart, searchMethod, returnType, data):
        results = []

        if searchPart == 'id':
            data = str(data)
        else:
            data = str(data).encode('utf-8')
            #data = str(base64.b64encode(data))[2:-3]

        #file_list = sorted(os.walk('jsonPython/db/'+ tableName+'/'+ colName))
        dir_name = 'jsonPython/db/'+tableName+'/' + colName
        file_list = sorted(filter(os.path.isfile, glob.glob(dir_name + "/*")),key=os.path.getmtime)
        #file_list = sorted(filter(os.path.isfile, glob.glob('jsonPython/db/'+tableName+'/'+colName,recursive=True)))

        for files in file_list:

            file = os.path.basename(files)
            #print('[{}]'.format(file))

            if searchPart == 'data':
                #file_data = str(file.split('_')[2])[:-2]
                file_data = str(file.split('_')[2])
                file_data = base64.b64decode(file_data + '==')
                #print(str(data).replace(" ", ""), str(file_data).replace(" ", ""))
                #print(type(str(data)), type(str(file_data)))
            else:
                file_data = str(file.split('_')[0])
            if searchMethod == 're':
                if bool(re.match(str(data).replace(" ", ""),str(file_data).replace(" ", ""))):
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
            else:    
                if str(data) == str(file_data):
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

    def update(tableName, colName, colType, localrowid, data):
        path = ('jsonPython/db/' + tableName + '/' + colName)
        for root, dirs, files in os.walk(path):
            for file in files:
                if colType == 's':
                    if file.split('_')[0] == str(localrowid):
                        data = data.encode('utf-8')
                        data = base64.b64encode(data)
                        data = str(data)[2:-1]
                        os.remove(path +'/'+ file)
                        with open(path +'/'+ str(localrowid) + '_' + colType + '_' + str(data), 'w+') as f:
                            f.write(str(data))
                        return data   
                else:
                    if file.split('_')[0] == str(localrowid):
                        os.remove(path +'/'+ file)
                        with open(path +'/'+ str(localrowid) + '_' + colType + '_' + str(data), 'w+') as f:
                            f.write(str(data))
                        return data  
    
    def BAKupdate(tableName, colName, colType, rowid, data, colType2, rowid2, data2, userinput):
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

    def delete(tableName):
        path = ('jsonPython/db/' + tableName )
        if os.path.exists(path):
            shutil.rmtree(path)
            print('Deleted\t' + path + '\tsuccessfully')
            return True
        else:
            print('This table does not exist...')
            return False
        
    def deleteUser(tableName, colName, localrowid):
        
      #  print(localrowid)
        find_result = UserDB.find(tableName, colName, 'id', 'raw', localrowid[0])
        path = ('jsonPython/db/' + tableName + '/' + colName + '/' + find_result[0])
        os.remove(path)