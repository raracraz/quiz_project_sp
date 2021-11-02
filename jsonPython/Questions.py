#function to write questions to a text file
#function to read questions from a text file to a list and return the list
#function to check if the answer is correct from the list




import os
import uuid
import base64

def write_questions(questions):
    """
    Write questions to a text file
    """
    #create a unique file name
    file_name = str(uuid.uuid4()) + ".txt"
    #open the file
    with open(file_name, "w") as file:
        #write the questions to the file
        for question in questions:
            file.write(question + "\n")
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

