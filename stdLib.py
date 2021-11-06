# Use file system to store rows of data.
# Provides high concurrency and low latency only limited by the file system.
# does not have read/write locks.
# usage:
# create - create a new table with a column and row data returns unquie rowid
# find - find a matching data in table/column returns rowid
# read - read data from table/column/rowid returns data
# update - update data in table/column/rowid returns true/false
# delete - delete data from table/column/rowid returns true/false
import json
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
#database functions finished

#start of quiz functions
#write_questions - write questions to a file
#read_questions - read questions from a file
#Question - create a question
#replace_question_pool - replace the question pool with a new set of questions

def write_questions(questions):
    """
    Write questions to a text file
    """
    #create a unique file name
    file_name = "QuestionPool.txt"
    #open the file
    with open(file_name, "w+") as file:
        #write the questions to the file
        for question in questions:
            file.write(json.dumps(question) + "\n" )
    return file_name
#read_questions - read json questions from QuestionPool.txt into a dictionary and prints the questions from the dictionary, prints 3 lines, id, question, options, options must be labeled as a, b, c, d
#wait for user input before printing the next question
def read_questions(file_name):
    """
    Read questions from a text file
    """
    #create a unique file name\
    #open the file
    optionsList = ['a)', 'b)', 'c)', 'd)']
    optionsList2 = ['a', 'b', 'c', 'd']
    global userAnswerList
    userAnswerList = []
    with open(file_name, 'r') as file:
        #read the questions from the file
        questions = file.readlines()
        #print the questions
        for q in questions:
            q = json.loads(q)
            id = q['id']+1
            question = q['question']
            print('id: ', id)
            print('Question: ', question)
            #print one option from the options list
            for option in q['options']:
                print(optionsList[q['options'].index(option)], option)
            #wait for user input before printing the next question
            
            userAnswer = str(input('Press enter a answer(a, b , c , d): '))
            if userAnswer not in optionsList2:
                print('Invalid answer')
                read_questions(file_name)
            else:
                userAnswerList.append(userAnswer)

            
            #print(userAnswerList)
            print('\n')

#function to check if the user answer is correct and print the correct answer and print the score of the user and the total number of questions
def check_answer(file_name):
    global userAnswerList
    global num_questions
    num_questions = 2
    correctAnswerList = []
    #get the correct answer from the json file
    with open(file_name, 'r') as file:
        #read the questions from the file
        questions = file.readlines()
        for q in questions:
            q = json.loads(q)
            correctAnswerList.append(q['answer'])
        print(correctAnswerList)
        score = 0
        total = num_questions
        for i in range(len(userAnswerList)):
            if userAnswerList[i] == correctAnswerList[i]:
                score += 1
        print('Your score is: ', score)
        print('Total number of questions: ', total)
        percentage = (score/total)*100
        print('Your percentage score is: ', percentage)
        #give the user the option to retake the quiz ?
        #do later





        print('\n')
        userAnswerList = []

def Question(id, question, options, answer):
    """
    Create a question
    """
    #create a question with the unique id, question, options, and answer
    question = {
        "id": id,
        "question": question,
        "options": options,
        "answer": answer
    }
    return question
#if user chooses to create a new question pool, ask user to enter questions to replace the question pool.
#the replaceQnCheckpoint function will loop until the number of questions is equal to num_questions
#each question created should have 4 options (A, B, C, D) with the correct answer being A, B, C, or D
#add the question to a dictionary
#write the question to a text file
def replace_question_pool():
    """
    Replace question pool
    """
    questionList = []
    global num_questions
    #ask user how many questions they want to add to the question pool, not more then 10 questions
    try:
        num_questions = int(input("How many questions do you want to add to the question pool? "))
        if num_questions > 10:
            print("You can only add 10 questions maximum")
            replace_question_pool()
    except ValueError:
        print("Please enter a number")
        replace_question_pool()
    
    #ask user to enter questions to replace the question pool
    #loop until the number of questions is equal to num_questions
    def replaceQnCheckpoint(questionList, num_questions):
        for id in range(num_questions):
            #ask user to enter a question
            question = input("Enter a question: ")
            #ask user to enter the options
            optionA = str(input("Enter an option for A: "))
            optionB = str(input("Enter an option for B: "))
            optionC = str(input("Enter an option for C: "))
            optionD = str(input("Enter an option for D: "))
            if optionA == "" or optionB == "" or optionC == "" or optionD == "":
                print("option cannot be empty")
                replaceQnCheckpoint(questionList, num_questions)
            #ask user to enter the correct answer
            answer = str(input("Enter the correct answer: "))
            #if answer in optionA or optionB or optionC or optionD:
               # print("Please enter a valid answer")
               # replaceQnCheckpoint(questionList, num_questions)
            #create a question
            question = Question(id, question, [optionA, optionB, optionC, optionD], answer)
            #add the question to a list
            questionList.append(question)
            #write the questionList to QuestionPool.txt
            write_questions(questionList)
    replaceQnCheckpoint(questionList, num_questions)
    return questionList

    '''
    def replaceQnCheckpoint(num_questions):
        while len(questionList) <= num_questions:
            question = input("Enter a question: ")
            if question == "":
                print("question cannot be empty")
                replaceQnCheckpoint()
            #ask user to enter wrong answers for the question
            while len(questionList) <= num_questions:
                optionA = input("Enter an option for A: ")
                optionB = input("Enter an option for B: ")
                optionC = input("Enter an option for C: ")
                optionD = input("Enter an option for D: ")
                if optionA == "" or optionB == "" or optionC == "" or optionD == "":
                    print("option cannot be empty")
                    replaceQnCheckpoint()
                #ask user to enter the correct answer for the question
                while len(questionList) <= num_questions:
                    answer = input("Enter the correct answer for the question: ")
                    if answer == "":
                        print("answer cannot be empty")
                        replaceQnCheckpoint()
                    #create a question
                    id = 1
                    id =+ 1
                    question = Question(id, question, [optionA, optionB, optionC, optionD], answer)
                    #add the question to a list
                    questionList.append(question)
                    #write the question to a text file
                    file_name = "QuestionPool.txt"
                    file_name = write_questions(questionList)
                    print("Question added to the question pool")
                    return file_name
        replaceQnCheckpoint(num_questions)   
    replaceQnCheckpoint(num_questions) 
    return questionList
    '''

#function to read questions from QuestionPool.txt and print them to the screen

#the score will be calculated by taking the number of questions correct and dividing it by the number of questions in the question pool
#the score will be displayed to the user




def main():
    """
    Main function
    """
    #ask user if they want to create a new question pool or add to the existing question pool
    print("Welcome to the question pool creator")
    print("Would you like to create a new question pool or use the existing question pool?")
    print("1. Create a new question pool")
    print("2. Add to existing question pool")
    #get user input
    try:
        user_input = int(input("Enter 1 or 2: "))
    except ValueError:
        print("Please enter either 1 or 2")
        main()
    #if user chooses to create a new question pool, ask user to enter questions to replace the question pool.
    #each question created should have 4 options (A, B, C, D) with the correct answer being A, B, C, or D
    #add the question to a dictionary
    #write the question to a text file
    if user_input == 1:
        questions = replace_question_pool()
        file_name = write_questions(questions)
    #if user chooses to use an existing question pool, ask user to enter the file name of the question pool
    #read the questions from the file and return a list
    elif user_input == 2:
        print("You chose to use an existing Question Pool\n")
        questions = read_questions('QuestionPool.txt')
    #ask user to enter a question
    else:
        print("Please enter 1 or 2")
        main()

read_questions('QuestionPool.txt')
check_answer('QuestionPool.txt')