#-----------------------------------------------------------------------------#
#   File:   QuizWindow.py                                                     #
#   Author: Logan Pierceall                                                   #
#   Date:   March 8, 2022                                                     #
#                                                                             #
#   This module contains the functions that interact directly with the quiz   #
#       information. Each quiz question is a self-contained dictionary object #
#       that is retrieved from a JSON database file. A list object is used to #
#       hold all of the quiz entry objects.                                   #
#                                                                             #
#   Each quiz entry utilizes the following keys:                              #
#       Type:           A given entry may have 1 or more correct answers      #
#                           Questions with one answer will have type          #
#                           "single", and multiple answers will be designated #
#                           type "multi"                                      #
#       Question:       Contains the question text                            #
#       NumOfAnswers:   Contains the integer count of answer options          #
#       Answer#:        Each answer key is numbered sequentially, starting at #
#                           1, and contains the text for one answer option    #
#       Correct:        Contains the text matching the correct answer string  #
#                           For multiple choice questions, all correct        #
#                           answers will be collected into a list             #
#-----------------------------------------------------------------------------#

import json
from json.decoder import JSONDecodeError
import random
import tkinter as tk
from tkinter import messagebox

class QuizList:

    def __init__(self):
    
        self.quiz = []              # Holds all list objects after serializing
        self.total_questions = 0    # Total number of questions in the quiz
        self.correct_answers = 0    # Total questions answered correctly
    
    
    
    # GetCorrectAnswer() retrieves the correct answer for a given quiz entry
    # Args:     entry = the current quiz question object
    # Returns:  the string containing the question's correct answer
    def GetCorrectAnswer(self, entry):
    
        return entry['Correct']
    
    
    
    # GetAnswer() retrieves an answer string for a given quiz entry. Answers
    #   are listed sequentially within the quiz object, e.g., Answer1, Answer2
    # Args:     index = the specific numbered answer to retrieve
    #           entry = the current quiz question object
    # Returns:  the string containing the specified answer
    def GetAnswer(self, index, entry):
    
        return entry['Answer' + str(index)]
    
    
    
    # GetAnswerCount() retrieves the number of answer options for a given quiz
    #   entry
    # Args:     entry = the current quiz question object
    # Returns:  the integer number of possible answers
    def GetAnswerCount(self, entry):
    
        return entry['NumOfAnswers']
    
    
    
    # GetEntry() retrieves a randomly selected quiz entry from the quiz list.
    # Args:     none
    # Returns:  a dict object containing all of the needed info for one quiz
    #           question
    def GetEntry(self):
        
        # If an entry exists in the list, return one at random
        if self.GetLength() != 0:
            return True, self.quiz.pop(random.randint(0, len(self.quiz) - 1))
        else:
            return False, 0
    
    
    
    # GetEntryType() is used to determine if a given quiz entry has a single
    #   answer or multiple answers
    # Args:     entry = the current quiz question object
    # Returns:  a string indicating "single" for single answer or "multi" for
    #               multiple answers
    def GetEntryType(self, entry):
    
        return entry['Type']
    
    
    
    # GetLength() retrieves the current number of quiz entries in the quiz list
    # Args:     none
    # Returns:  the integer number of items in the quiz list
    def GetLength(self):

        return len(self.quiz)
    
    
    
    # GetNumberOfCorrects() retrieves the number of questions the user has
    #   correctly answered
    # Args:     none
    # Returns:  the integer number of correctly answered questions
    def GetNumberOfCorrects(self):
    
        return self.correct_answers
    
    
    
    # GetQuestion() retrieves the question text for a given quiz entry
    # Args:     entry = the current quiz question object
    # Returns:  the string containing the question
    def GetQuestion(self, entry):
    
        return entry['Question']
    
    
    
    # GetTotalQuestions() retrieves the total number of quiz entries in the
    #   list after initial creation
    # Args:     none
    # Returns:  the integer number of total quiz entries
    def GetTotalQuestions(self):
    
        return self.total_questions
    
    
    
    # IncrementCorrectAns() increments the number of correctly answered
    #   questions by one
    # Args:     none
    # Returns:  none
    def IncrementCorrectAns(self):
    
        self.correct_answers += 1
    
    
    
    # PopulateQuiz() loads a given JSON file as a list of dict objects. Each
    #   object represents a single quiz entry
    # Args:     filename = the JSON file containing quiz info
    # Returns:  True and an empty string if the file is loaded successfully
    #           False and an error message otherwise
    def PopulateQuiz(self, filename):
    
        try:
            with open(filename, 'r') as file:
                self.quiz.extend(json.load(file))
            self.total_questions = len(self.quiz)
            return True, ''
        
        # Exception catches a file that can't be opened
        except IOError:
            return False, f'Unable to open {filename}'
        
        # Exception catches an empty file
        except JSONDecodeError:
            return False, f'Unable to load info from {filename}'
        
        # Exception catches all other unexpected errors
        except:
            return False, 'Unexpected error ocurred'