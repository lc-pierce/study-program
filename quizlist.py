import os
import random
import tkinter as tk
from tkinter import messagebox

import quizbank

class QuizList:

    def __init__ (self):
    
        self.__quiz_list = []
    
    
    
    def get_length (self):
    
        return len(self.__quiz_list)
    
    
    
    def get_quiz_entry (self):
    
        return self.__quiz_list.pop(random.randint(0, len(self.__quiz_list) - 1))
    
    
    
    def clear_entries (self):
    
        try:
            self.__quiz_list.clear()
            return True
        except:
            return False
    
    
    
    def populate_quizlist (self, filename):
    
        __first_entry_flag = True
    
        try:
            with open(filename) as __file:
                for __line in __file:
                    if __line == '\n' or __line == '':
                        pass
                    else:
                        __line_type = __line[:3]
                        __line_contents = __line[4:].rstrip()
                        
                        if __line_type == 'FIL':
                            __filename_key = __line_contents
                            
                        elif __line_type == 'TYP':
                            if not __first_entry_flag:
                                self.__quiz_list.append(__qb)
                            else:
                                __first_entry_flag = False
                            if __line_contents == 'single':
                                __qb = quizbank.SingleChoiceQB(__filename_key)
                            elif __line_contents == 'multi':
                                __qb = quizbank.MultiChoiceQB(__filename_key)
                        
                        elif __line_type == 'QST':
                            __qb.set_question_str(__line_contents)
                        
                        elif __line_type == 'ANS':
                            __qb.append_answers_list(__line_contents)
                            __qb.increase_answer_count()
                        else:
                            tk.messagebox.showerror('ERROR', 'Invalid data entry, process aborted.')
                            self.clear_entries()
                            
            self.__quiz_list.append(__qb)
            return True
                         
        except IOError:
            return False