#function to write questions to a text file
#function to read questions from a text file to a list and return the list
#function to check if the answer is correct from the list



import json
import os
import uuid
import base64
def write_questions(questions):
    """
    Write questions to a text file
    """
    #create a unique file name
    file_name = "QuestionPool" + ".txt"
    #open the file
    with open(file_name, "w") as file:
        #write the questions to the file
        for question in questions:
            file.write(json.dumps(question) + "\n")
    return file_name

def read_questions(file_name):
    """
    Read questions from a text file and return a list
    """
    #open the file
    with open(file_name, "r") as file:
        #read the questions from the file
        questions = file.readlines()
    #remove the \n from each question
    questions = [question.rstrip("\n") for question in questions]
    return questions

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
#each question created should have 4 options (A, B, C, D) with the correct answer being A, B, C, or D
#add the question to a dictionary
#write the question to a text file
def replace_question_pool():
    """
    Replace question pool
    """
    questionList = []
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
    def replaceQnCheckpoint():
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
        
        return questionList
    replaceQnCheckpoint()


def main():
    """
    Main function
    """
    #ask user if they want to create a new question pool or use the existing question pool
    print("Welcome to the question pool creator")
    print("Would you like to create a new question pool or use the existing question pool?")
    print("1. Create a new question pool")
    print("2. Use an existing question pool")
    #get user input
    try:
        user_input = int(input("Enter 1 or 2: "))
    except ValueError:
        print("Please enter a number")
        main()
    #if user chooses to create a new question pool, ask user to enter questions to replace the question pool.
    #each question created should have 4 options (A, B, C, D) with the correct answer being A, B, C, or D
    #add the question to a dictionary
    #write the question to a text file
    if user_input == 1:
        questions = []
        questions = replace_question_pool(questions)
        file_name = write_questions(questions)
        print("The questions have been written to the file: " + file_name)
    #if user chooses to use an existing question pool, ask user to enter the file name of the question pool
    #read the questions from the file and return a list
    elif user_input == 2:
        file_name = input("Enter the file name of the question pool: ")
        questions = read_questions(file_name)
    #ask user to enter a question
    while True:
        question = input("Enter a question: ")
        if question == "":
            break
        #ask user to enter the options for the question
        options = input("Enter the options for the question (A, B, C, D): ")
        #ask user to enter the correct answer for the question
        answer = input("Enter the correct answer: ")
        #create a unique id for the question
        id = str(uuid.uuid4())
        #create a question with the unique id, question, options, and answer
    
replace_question_pool()