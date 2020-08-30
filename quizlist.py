# ------------------------------------------------------------------------------------------------- #
# quizlist.py is used to create a QuizList object. This object functions similarly to a regular     #
#   Python list, but it will be populated with QuizBank entries. The QuizBank object will be used   #
#   to populate the quiz assessment window and it holds information pulled from database files,     #
#   which will include:                                                                             #
#       The name of the file holding the quiz information                                           #
#       The type of question, which can be either single or multiple-choice answer                  #
#       The question itself                                                                         #
#       The answer options                                                                          #
#       The correct answer option(s)                                                                #
#                                                                                                   #
# Author: Logan Pierceall                                                                           #
# Last revision date: August 10, 2020                                                               #
# ------------------------------------------------------------------------------------------------- #

import os
import random
import tkinter as tk
from tkinter import messagebox

class QuizList:

    def __init__(self):

        self.__quiz_list = []


    # clear_entries() deletes all the QuizBank objects from the list
    def clear_entries(self):

        try:
            self.__quiz_list.clear()
            return True
        except:
            return False


    # get_length() returns the total number of QuizBank objects in the list
    def get_length(self):

        return len(self.__quiz_list)


    # get_quiz_entry() returns a randomly chosen QuizBank object from the list
    def get_quiz_entry(self):

        return self.__quiz_list.pop(random.randint(0, self.get_length() -1))


    # populate_quizlist() opens the file passed as an argument and uses the information within to
    #   create a QuizBank object for each question and stores them into a QuizList object
    def populate_quizlist(self, filename):

        try:
            with open(filename) as __file:
                for __line in __file:

                    # the first 3 characters of every line will be the type of info provided by the line
                    #   and the rest of the line will be the useful information for the quiz
                    __line_type = __line[:3]
                    __line_contents = __line[4:].rstrip()

                    if __line_type == 'FIL':
                        # the line contains the filename that will be added to every QuizBank object
                        __filename_key = __line_contents

                    elif __line_type == 'TYP':
                        # the line contains the answer type of question and represents the beginning
                        #   of a new question entry
                        __qb = QuizBank(__filename_key)
                        __qb.add_key('QuestionType', __line_contents)

                    elif __line_type == 'QST':
                        # the line contains the text for the question itself
                        __qb.add_key('Question', __line_contents)

                    elif __line_type == 'ANS':
                        # each answer is appended with a sequential number and the total number of
                        #   answers found is collected and stored
                        __qb.add_key('Answer' + str(__qb.get_answer_count()), __line_contents)
                        __qb.increase_answer_count()

                    elif __line_type == 'COR':
                        # the correct answer line will be an index or indices indicating which of
                        #   the answers in the list of answers is the correct answer. it represents
                        #   the end of the block containing information for a question so the question
                        #   will be stored into the list
                        __temp_list = []
                        for __char in __line_contents:
                            __temp_list.append(int(__char))
                        __qb.add_key('CorrectAnswer', __temp_list)
                        self.__quiz_list.append(__qb)
                    else:
                        # if invalid data is encountered then the program will alert the user and
                        #   delete all previously gathered data
                        tk.messagebox.showinfo('ERROR', 'Invalid data entry, process aborted.')
                        self.clear_entries()
                        
            return True

        except IOError:

            return False



class QuizBank:

    def __init__(self, filename):

        self.__question_dict = {'Filename': filename}
        self.__answer_count = 0


    # add_key() adds key-value pairs pulled from the file to the current object's dictionary
    def add_key(self, key, value):

        self.__question_dict[key] = value


    # check_answer() determines if the answer string passed as an argument matches the answer(s)
    #   whose index/indices will be stored in the CorrectAnswer key
    def check_answer(self, user_answer):

        if self.__question_dict['CorrectAnswer'] == user_answer:
            return True
        else:
            return False


    # get_answer_count() returns the number of possible answers for the current question
    def get_answer_count(self):

        return self.__answer_count


    # get_entry() returns the value associated with the key passed as an argument
    def get_entry(self, key):

        return self.__question_dict[key]


    # increase_answer_count() increases the number of answers found while processing a question
    def increase_answer_count(self):

        self.__answer_count += 1