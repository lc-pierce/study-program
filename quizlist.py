import os
import random
from tkinter import messagebox



# The QuizList class holds all of the information on questions pulled from database files chosen
#   by the user. It contains a method for populating a list with QuizBank objects (defined below)
#   and additional methods to return a random entry in the list, clear the list, and get the total
#   number of QuizBank objects held in the list
class QuizList:

    def __init__(self):

        self.__quiz_list = []



    # clear_entries() is used to delete all the QuizBank objects from the list
    def clear_entries(self):

        try:
            self.__quiz_list.clear()
            return True
        except:
            return False



    # get_length() returns the total length of the current quiz list
    def get_length(self):

        return len(self.__quiz_list)



    # get_quiz_entry() returns a randomly generated quiz object from the list
    def get_quiz_entry(self):

        return self.__quiz_list.pop(random.randint(0, self.get_length() -1))



    def populate_quizlist(self, filename):

        try:
            with open(filename) as __file:
                for __line in __file:

                    # First 3 characters of every line will be the type of info provided by the line
                    #   and the rest of the line will be the useful information for the quiz
                    __line_type = __line[:3]
                    __line_contents = __line[4:].rstrip()

                    if __line_type == 'FIL':
                        # Line contains the filename that will be added to every QuizBank object
                        __filename_key = __line_contents

                    elif __line_type == 'TYP':
                        # Line contains the general type of question to follow and represents the
                        #   beginning of a new question
                        __qb = QuizBank(__filename_key)
                        __qb.add_key('QuestionType', __line_contents)

                    elif __line_type == 'QST':
                        __qb.add_key('Question', __line_contents)

                    elif __line_type == 'ANS':
                        # Each answer key is appended with a sequential number that must be retrieved
                        #   before incrementing the counter
                        __qb.add_key('Answer' + str(__qb.get_answer_count()), __line_contents)
                        __qb.increase_answer_count()

                    elif __line_type == 'COR':
                        # The line holding the correct answer will be the final line for any
                        #   question, meaning the QuizBank item is ready for the list
                        __qb.add_key('CorrectAnswer', __line_contents)
                        self.__quiz_list.append(__qb)
                    else:
                        # Invalid data has been encountered, so the program will alert the user and
                        #   delete all previously gathered data
                        tk.messagebox.showinfo('ERROR', 'Invalid data entry, process aborted.')
                        self.clear_entries()

        except IOError:
            tk.messagebox.showinfo('ERROR', f'{os.path.basename(filename)} unable to open.')



# Every entry in the QuizList list will be a QuizBank object, which is fundamentally just a dictionary
#   with methods to access the data within. A total count of the answers encountered while building
#   the entry is also maintained
class QuizBank:

    def __init__(self, filename):

        self.__question_dict = {'Filename': filename}
        self.__answer_count = 0



    # add_key() adds key-value pairs pulled from the file to the objects dictionary
    def add_key(self, key, value):

        self.__question_dict[key] = value



    # check_answer() determines if the passed answer matches the one recorded as correct
    def check_answer(self, user_answer):

        if self.__question_dict['CorrectAnswer'] == user_answer:
            return True
        else:
            return False



    # get_answer_count() returns the number of answers encountered while processing the file
    def get_answer_count(self):

        return self.__answer_count



    # get_entry() returns the value associated with the passed key
    def get_entry(self, key):

        return self.__question_dict[key]



    # increase_answer_count() increases the index of number of answers encountered in file reading
    def increase_answer_count(self):

        self.__answer_count += 1
