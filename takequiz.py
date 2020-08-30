# ------------------------------------------------------------------------------------------------- #
# takequiz.py is used to create a new window that will allow the user to take a quiz over the files #
#   they've loaded.                                                                                 #
#                                                                                                   #
# Author: Logan Pierceall                                                                           #
# Last revision date: August 10, 2020                                                               #
# ------------------------------------------------------------------------------------------------- #

import os
import tkinter as tk
from tkinter import messagebox

import quizlist

class Quiz:

    def __init__ (self, quiz_list, root_window, screen_width, screen_height):
    
        self.__quiz_list = quiz_list
        self.__total_questions = self.__quiz_list.get_length()
        self.__answered_questions = 0
        self.__correct_answers = 0
        self.__incorrect_list = []
        
        self.__quiz_window = tk.Toplevel(master = root_window)
        self.__quiz_win_height = 600
        self.__quiz_win_width = 700
        self.__y_pos = int((screen_height / 2) - (self.__quiz_win_height / 2))
        self.__x_pos = int((screen_width / 2) - (self.__quiz_win_width / 2))
        self.__quiz_window.geometry(f'{self.__quiz_win_width}x{self.__quiz_win_height}+{self.__x_pos}+{self.__y_pos}')

        self.create_frames()



    def create_frames (self):
    
        self.__current_qb = self.__quiz_list.get_quiz_entry()
        
        self.__quiz_window.title('Question source: ' + self.__current_qb.get_entry('Filename'))
        
        self.__question_frame = tk.Frame(self.__quiz_window,
                                         padx = 5,
                                         pady = 5,
                                         bg = 'dodger blue')
        self.__answers_frame = tk.Frame(self.__quiz_window,
                                        padx = 5,
                                        pady = 5,
                                        bg = 'dodger blue')
        self.__buttons_frame = tk.Frame(self.__quiz_window,
                                        padx = 5,
                                        pady = 5,
                                        bg = 'dodger blue')
        self.__check_next_button_frame = tk.Frame(self.__buttons_frame)
        self.__exit_button_frame = tk.Frame(self.__buttons_frame)
        
        self.__question_frame.pack(fill = 'both', expand = 'true')
        self.__answers_frame.pack(fill = 'both', expand = 'true')
        self.__buttons_frame.pack(fill = 'both', expand = 'true')
        self.__check_next_button_frame.pack(side = 'top', fill = 'both', expand = 'true')
        self.__exit_button_frame.pack(side = 'bottom', fill = 'both', expand = 'true')
        
        self.create_question_widgets()
        self.create_answer_widgets(self.__current_qb.get_entry('QuestionType'))
        self.create_button_widgets()



    def create_question_widgets (self):
    
        self.__question_number_label = tk.Label(self.__question_frame,
                                                text = 'QUESTION ' + str(self.__answered_questions + 1) 
                                                       + ' OF ' + str(self.__total_questions),
                                                pady = 5,
                                                font = ('times', 12, 'bold'),
                                                bg = 'dodger blue',
                                                fg = 'mint cream')
        self.__question_label = tk.Label(self.__question_frame,
                                         text = self.__current_qb.get_entry('Question'),
                                         wraplength = 650,
                                         justify = 'left',
                                         font = ('times', 14, 'bold'),
                                         bg = 'dodger blue',
                                         fg = 'mint cream')
        self.__question_result_label = tk.Label(self.__question_frame,
                                                text = 'PLACEHOLDER',
                                                font = ('times', 14, 'bold'),
                                                height = 1,
                                                bg = 'dodger blue',
                                                fg = 'dodger blue')
        self.__question_number_label.pack(side = 'top', fill = 'x')
        self.__question_label.pack(side = 'top', fill = 'both', expand = 'true')
        self.__question_result_label.pack(side = 'bottom', fill = 'x')



    def create_answer_widgets (self, question_type):
    
        self.__answer_buttons_list = []
        
        if question_type == 'multi':
        
            self.__cb_vars_list = []
            self.__answers_index = 0
            while self.__answers_index < self.__current_qb.get_answer_count():
            
                self.__cb_var = tk.IntVar(self.__quiz_window)
                self.__cb_var.set(0)
                self.__cb_vars_list.append(self.__cb_var)
                
                self.__cb = tk.Checkbutton(self.__answers_frame,
                                           text = self.__current_qb.get_entry('Answer' + 
                                                  str(self.__answers_index)),
                                           variable = self.__cb_var,
                                           font = ('times', 14, 'bold'),
                                           wraplength = 600,
                                           justify = 'left',
                                           anchor = 'w',
                                           bg = 'dodger blue',
                                           activebackground = 'dodger blue',
                                           fg = 'mint cream',
                                           activeforeground = 'mint cream',
                                           selectcolor = 'black')
                self.__cb.pack(fill = 'both', expand = 'true')
                self.__answer_buttons_list.append(self.__cb)
                
                self.__answers_index += 1
                
        elif question_type == 'single':
            self.__radio_var = tk.IntVar(self.__quiz_window)
            self.__radio_var.set(-1)
            self.__answers_index = 0
            
            while self.__answers_index < self.__current_qb.get_answer_count():
            
                self.__rb = tk.Radiobutton(self.__answers_frame,
                                           text = self.__current_qb.get_entry('Answer' + 
                                                  str(self.__answers_index)), 
                                           variable = self.__radio_var,
                                           value = self.__answers_index,
                                           font = ('times', 14, 'bold'),
                                           wraplength = 600,
                                           justify = 'left',
                                           anchor = 'w',
                                           bg = 'dodger blue',
                                           activebackground = 'dodger blue',
                                           fg = 'mint cream',
                                           activeforeground = 'mint cream',
                                           selectcolor = 'black')
                self.__rb.pack(fill = 'both', expand = 'true')
                self.__answer_buttons_list.append(self.__rb)
                
                self.__answers_index += 1



    def create_button_widgets (self):
    
        self.__check_answer_button = tk.Button(self.__check_next_button_frame,
                                               text = 'CHECK ANSWER',
                                               command = self.check_answer,
                                               font = ('times', 16, 'bold'),
                                               bd = 0,
                                               bg = 'dodger blue',
                                               activebackground = 'dodger blue',
                                               activeforeground = 'mint cream',
                                               fg = 'mint cream')
        self.__next_question_button = tk.Button(self.__check_next_button_frame,
                                                text = 'NEXT QUESTION',
                                                command = self.load_next_question,
                                                font = ('times', 16, 'bold'),
                                                bd = 0,
                                                bg = 'dodger blue',
                                                activebackground = 'dodger blue',
                                                fg = 'mint cream',
                                                activeforeground = 'mint cream',
                                                disabledforeground ='grey25')
        self.__next_question_button['state'] = 'disabled'
        self.__exit_button = tk.Button(self.__exit_button_frame,
                                       text = 'GRADE & EXIT QUIZ',
                                       command = self.grade_quiz,
                                       font = ('times', 16, 'bold'),
                                       bg = 'dodger blue',
                                       activebackground = 'dodger blue',
                                       fg = 'mint cream',
                                       activeforeground = 'mint cream',
                                       bd = 0)
        self.__check_answer_button.pack(side = 'left', fill = 'both', expand = 'true')
        self.__next_question_button.pack(side = 'right', fill = 'both', expand = 'true')
        self.__exit_button.pack(fill = 'both', expand = 'true')



    def check_answer (self):
    
        self.__answered_questions += 1
        self.__check_answer_button['state'] = 'disabled'
        self.__user_answer = []

        if (self.__current_qb.get_entry('QuestionType')) == 'single':
            self.__user_answer.append(self.__radio_var.get())   
        elif (self.__current_qb.get_entry('QuestionType')) == 'multi':
            __cb_index = 0
            for __entry in self.__cb_vars_list:
                if __entry.get() == 1:
                    self.__user_answer.append(__cb_index)
                __cb_index += 1
        
        if self.__current_qb.check_answer(self.__user_answer):
            self.__correct_answers += 1
            self.__question_result_label.config(text = 'CORRECT', fg = 'mint cream')
            for __index in self.__user_answer:
                self.__answer_buttons_list[__index].config(bg = 'SpringGreen3')
        else:
            self.__question_result_label.config(text = 'INCORRECT', fg = 'mint cream')
            for __index in self.__user_answer:
                self.__answer_buttons_list[__index].config(bg = 'firebrick1')
            for __index in self.__current_qb.get_entry('CorrectAnswer'):
                self.__answer_buttons_list[__index].config(bg = 'SpringGreen3')

        if self.__quiz_list.get_length():
            self.__next_question_button['state'] = 'active'
        else:
            self.__check_next_button_frame.forget()
            self.__exit_button_frame
            self.__quiz_over_label = tk.Label(self.__buttons_frame,
                                              text = "Quiz over! Click 'Grade & Exit Quiz' to get your results.",
                                              font = ('times', 20, 'bold'),
                                              bg = 'dodger blue',
                                              fg = 'mint cream')
            self.__quiz_over_label.pack(fill = 'both', expand = 'true')



    def load_next_question (self):
    
        self.__question_frame.forget()
        self.__answers_frame.forget()
        self.__buttons_frame.forget()
        
        self.create_frames()



    def grade_quiz (self):
    
        if not self.__answered_questions:
            pass
        else:
            __student_score = self.__correct_answers / self.__answered_questions
            tk.messagebox.showinfo('Quiz over! Here are your results.',
                                   f'You answered {self.__correct_answers} out of {self.__answered_questions}'
                                   + f' questions correct for a score of {__student_score:.2%}!')

        self.__quiz_window.destroy()