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
        
        self.__bg_color = 'PaleTurquoise2'
        self.__font_color = 'grey1'
        self.__font = 'georgia'
        self.__green = 'SpringGreen3'
        self.__red = 'firebrick1'
        self.__correct_color = 'SlateBlue1'
        
        # Used to offset the window creation by accounting for the presence of the desktop's taskbar
        self.__taskbar_size = 40
        
        self.create_window(root_window, screen_width, screen_height)
        self.create_frames()
        
        
    
    def create_window (self, main_win, width, height):
    
        self.__quiz_window = tk.Toplevel(master = main_win)
        self.__quiz_win_height = 700
        self.__quiz_win_width = 800
        self.__y_pos = int((height / 2) - (self.__quiz_win_height / 2) - self.__taskbar_size)
        self.__x_pos = int((width / 2) - (self.__quiz_win_width / 2))
        self.__quiz_window.geometry(f'{self.__quiz_win_width}x{self.__quiz_win_height}+{self.__x_pos}+{self.__y_pos}')
    
    
    
    def create_frames (self):
    
        self.__current_qb = self.__quiz_list.get_quiz_entry()
        self.__quiz_window.title('Question source: ' + self.__current_qb.get_filename())
        
        self.__question_frame = tk.Frame(self.__quiz_window,
                                         padx = 5,
                                         pady = 5,
                                         bg = self.__bg_color)
        self.__answers_frame = tk.Frame(self.__quiz_window,
                                        padx = 5,
                                        pady = 5,
                                        bg = self.__bg_color)
        self.__buttons_frame = tk.Frame(self.__quiz_window,
                                        padx = 5,
                                        pady = 5,
                                        bg = self.__bg_color)
        self.__check_next_button_frame = tk.Frame(self.__buttons_frame)
        self.__exit_button_frame = tk.Frame(self.__buttons_frame)
        
        self.__question_frame.pack(fill = 'both', expand = 'true')
        self.__answers_frame.pack(fill = 'both', expand = 'true')
        self.__buttons_frame.pack(fill = 'both', expand = 'true')
        self.__check_next_button_frame.pack(side = 'top', fill = 'both', expand = 'true')
        self.__exit_button_frame.pack(side = 'bottom', fill = 'both', expand = 'true')
        
        # Create the objects that populate the rest of the window
        self.create_question_widgets()
        if self.__current_qb.get_question_type() == 's':
            # Current question is single answer, call single answer function to create answer widgets
            self.create_single_answer()
        elif self.__current_qb.get_question_type() == 'm':
            # Create multi answer widgets
            self.create_multi_answer()
        self.create_button_widgets()
    
    
    
    # Creates the objects that hold the question for the current qb object
    def create_question_widgets (self):
    
        self.__question_number_label = tk.Label(self.__question_frame,
                                                text = 'QUESTION ' + str(self.__answered_questions + 1) 
                                                       + ' OF ' + str(self.__total_questions),
                                                pady = 5,
                                                font = (self.__font, 12, 'bold'),
                                                bg = self.__bg_color,
                                                fg = self.__font_color)
        self.__question_label = tk.Label(self.__question_frame,
                                         text = self.__current_qb.get_question(),
                                         wraplength = 775,
                                         justify = 'left',
                                         font = (self.__font, 14, 'bold'),
                                         bg = self.__bg_color,
                                         fg = self.__font_color)
        self.__question_result_label = tk.Label(self.__question_frame,
                                                text = 'NULL',
                                                font = (self.__font, 14, 'bold'),
                                                height = 1,
                                                bg = self.__bg_color,
                                                fg = self.__bg_color)
        self.__question_number_label.pack(side = 'top', fill = 'x')
        self.__question_label.pack(side = 'top', fill = 'both', expand = 'true')
        self.__question_result_label.pack(side = 'bottom', fill = 'x')
    
    
    
    # Creates the check button objects for a question with multiple answers
    def create_multi_answer (self):
    
        # List will hold the answer button objects to help process the user's chosen answer
        self.__answer_buttons_list = []
    
        self.__cb_vars_list = []
        self.__answers_index = 0
        
        while self.__answers_index < self.__current_qb.get_answer_count():
        
            self.__cb_var = tk.IntVar(self.__quiz_window)
            self.__cb_var.set(0)
            self.__cb_vars_list.append(self.__cb_var)
            
            # Check if the answer is a correct one so it can be added to the correct answers
            #   list and the special ending character can be stripped
            __answer_text = self.__current_qb.get_answer()
            if __answer_text[-1] == '@':
                self.__current_qb.set_correct_answer(self.__answers_index)
                __answer_text = __answer_text.strip('@')
            
            # Create the check button object for the answer
            self.__cb = tk.Checkbutton(self.__answers_frame,
                                           text = __answer_text,
                                           variable = self.__cb_var,
                                           font = (self.__font, 14, 'bold'),
                                           wraplength = 600,
                                           justify = 'left',
                                           anchor = 'w',
                                           bg = self.__bg_color,
                                           activebackground = self.__bg_color,
                                           fg = self.__font_color,
                                           activeforeground = self.__font_color,
                                           selectcolor = 'ghost white')
            self.__cb.pack(fill = 'both', expand = 'true')
            self.__answer_buttons_list.append(self.__cb)
            
            self.__answers_index += 1
    
    
    
    # Creates the radio button objects for a question with a single answer
    def create_single_answer (self):
    
        # List will hold the answer button objects to help process the user's chosen answer
        self.__answer_buttons_list = []
        
        self.__radio_var = tk.IntVar(self.__quiz_window)
        self.__radio_var.set(-1)
        self.__answers_index = 0
        
        while self.__answers_index < self.__current_qb.get_answer_count():
        
            # Check if the answer is a correct one so it can be added to the correct answers
            #   list and the special ending character can be stripped
            __answer_text = self.__current_qb.get_answer()
            if __answer_text[-1] == '@':
                self.__current_qb.set_correct_answer(self.__answers_index)
                __answer_text = __answer_text.strip('@')
            
            # Create the radio button object for the answer
            self.__rb = tk.Radiobutton(self.__answers_frame,
                                           text = __answer_text, 
                                           variable = self.__radio_var,
                                           value = self.__answers_index,
                                           font = (self.__font, 14, 'bold'),
                                           wraplength = 600,
                                           justify = 'left',
                                           anchor = 'w',
                                           bg = self.__bg_color,
                                           activebackground = self.__bg_color,
                                           fg = self.__font_color,
                                           activeforeground = self.__font_color,
                                           selectcolor = 'ghost white')
            self.__rb.pack(fill = 'both', expand = 'true')
            self.__answer_buttons_list.append(self.__rb)
                
            self.__answers_index += 1
    
    
    
    # Creates the action button widgets
    def create_button_widgets (self):
    
        self.__check_answer_button = tk.Button(self.__check_next_button_frame,
                                               text = 'CHECK ANSWER',
                                               command = self.check_answer,
                                               font = (self.__font, 16, 'bold'),
                                               bd = 0,
                                               bg = self.__bg_color,
                                               activebackground = self.__bg_color,
                                               activeforeground = self.__font_color,
                                               fg = self.__font_color)
        self.__next_question_button = tk.Button(self.__check_next_button_frame,
                                                text = 'NEXT QUESTION',
                                                command = self.load_next_question,
                                                font = (self.__font, 16, 'bold'),
                                                bd = 0,
                                                bg = self.__bg_color,
                                                activebackground = self.__bg_color,
                                                fg = self.__font_color,
                                                activeforeground = self.__font_color,
                                                disabledforeground ='grey25')
        self.__next_question_button['state'] = 'disabled'
        self.__exit_button = tk.Button(self.__exit_button_frame,
                                       text = 'GRADE & EXIT QUIZ',
                                       command = self.grade_quiz,
                                       font = (self.__font, 16, 'bold'),
                                       bg = self.__bg_color,
                                       activebackground = self.__bg_color,
                                       fg = self.__font_color,
                                       activeforeground = self.__font_color,
                                       bd = 0)
        self.__check_answer_button.pack(side = 'left', fill = 'both', expand = 'true')
        self.__next_question_button.pack(side = 'right', fill = 'both', expand = 'true')
        self.__exit_button.pack(fill = 'both', expand = 'true')
    
    
    
    # Checks the question type and loads the correct check answer function before updating objects
    #   to reflect the result
    def check_answer (self):
    
        self.__answered_questions += 1
        self.__check_answer_button['state'] = 'disabled'
        
        if self.__current_qb.get_question_type() == 's':
            self.check_single_answer()
        elif self.__current_qb.get_question_type() == 'm':
            self.check_multi_answer()
        
        # Check if there are any questions remaining and if so activate the button to continue.
        #   Otherwise inform the user and hide the processing widgets
        if self.__quiz_list.get_length() > 0:
            self.__next_question_button['state'] = 'active'
        else:
            self.__check_next_button_frame.forget()
            self.__quiz_over_label = tk.Label(self.__buttons_frame,
                                              text = "Quiz over! Click 'Grade & Exit Quiz'\nto get your results.",
                                              font = (self.__font, 20, 'bold'),
                                              bg = self.__bg_color,
                                              fg = self.__font_color)
            self.__quiz_over_label.pack(side = 'top', fill = 'both', expand = 'true')
    
    
    
    def check_single_answer (self):
    
        __user_answer = self.__radio_var.get()
        if __user_answer == self.__current_qb.get_correct_answer():
        
            self.__correct_answers += 1
            
            # Update the label with the results and color the chosen answer box green
            self.__question_result_label.config(text = 'CORRECT!',
                                                fg = self.__correct_color)
            self.__answer_buttons_list[__user_answer].config(bg = self.__green)
        else:
        
            # Update the label with the results, color the chosen answer box red, and color the
            #   correct option green
            self.__question_result_label.config(text = 'INCORRECT',
                                                fg = self.__correct_color)
            self.__answer_buttons_list[__user_answer].config(bg = self.__red)
            self.__answer_buttons_list[self.__current_qb.get_correct_answer()].config(bg = self.__green)
    
    
    
    def check_multi_answer (self):
    
        __index = 0
        __user_answer = ''
        for __entry in self.__cb_vars_list:
            if __entry.get() == 1:
                __user_answer += str(__index)
            __index += 1
        
        if __user_answer == self.__current_qb.get_correct_answer():
        
            self.__correct_answers += 1
            
            # Update the label with the results and color the chosen answer boxes green
            self.__question_result_label.config(text = 'CORRECT!',
                                                fg = self.__correct_color)
            for __char in __user_answer:
                self.__answer_buttons_list[int(__char)].config(bg = self.__green)
        else:
        
            self.__question_result_label.config(text = 'INCORRECT',
                                                fg = self.__correct_color)
            for __char in __user_answer:
                self.__answer_buttons_list[int(__char)].config(bg = self.__red)
                
            for __char in self.__current_qb.get_correct_answer():
                self.__answer_buttons_list[int(__char)].config(bg = self.__green)
    
    
    
    def load_next_question (self):
    
        self.__question_frame.forget()
        self.__answers_frame.forget()
        self.__buttons_frame.forget()
        
        self.create_frames()
    
    
    
    def grade_quiz (self):
    
        # If no questions were answered, skip grading. Otherwise calculate a score and show the user
        if self.__answered_questions == 0:
            pass
        else:
            __student_score = self.__correct_answers / self.__answered_questions
            tk.messagebox.showinfo('Quiz over! Here are your results.',
                                   f'You answered {self.__correct_answers} out of {self.__answered_questions}'
                                   + f' questions correct for a score of {__student_score:.2%}!')
        
        self.__quiz_window.destroy()