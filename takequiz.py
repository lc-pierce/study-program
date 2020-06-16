import tkinter as tk
from tkinter import messagebox

import quizlist



class Quiz:

    def __init__(self, quiz_list, root_window, screen_width, screen_height):

        self.__quiz_list = quiz_list
        self.__total_questions = self.__quiz_list.get_length()
        self.__answered_questions = 0
        self.__correct_answers = 0
        self.__incorrect_list = []

        # Create the quiz window
        self.__quiz_window = tk.Toplevel(master = root_window)
        __quiz_win_height = 500
        __quiz_win_width = 600
        __x_pos = int((screen_width / 2) - (__quiz_win_width/ 2))
        __y_pos = int((screen_height / 2) - (__quiz_win_height / 2))
        self.__quiz_window.geometry(f'{__quiz_win_width}x{__quiz_win_height}+{__x_pos}+{__y_pos}')

        # Populate the window with quiz objects
        self.populate_window()



    # populate_window() gets a new QuizBank object and uses it to insert objects into the window
    def populate_window(self):

        self.__current_qb = self.__quiz_list.get_quiz_entry()
        
        self.__row_index = 0
        self.__quiz_window.title('Question source: ' + self.__current_qb.get_entry('Filename'))

        # Create the labels for the question number and question
        self.__question_num_lbl = tk.Label(self.__quiz_window,
                                           text = 'Question ' + str(self.__answered_questions + 1) + ' of ' + str(self.__total_questions),
                                           font = ('times', 14))
        self.__question_lbl = tk.Label(self.__quiz_window,
                                       text = self.__current_qb.get_entry('Question') + '\n',
                                       wraplength = 600,
                                       font = ('times', 14))
        self.__question_num_lbl.grid(row = self.__row_index, columnspan = 3)
        self.__row_index += 1
        self.__question_lbl.grid(row = self.__row_index, columnspan = 3)
        self.__row_index += 1

        # Create the buttons for the answers
        self.create_buttons(self.__current_qb.get_entry('QuestionType'))

        # Create the buttons to process the chosen answer(s), load the next question, and exit
        self.__check_button = tk.Button(self.__quiz_window,
                                        text = 'Check Answer',
                                        command = self.check_answer,
                                        font = ('times', 12))
        self.__next_button = tk.Button(self.__quiz_window,
                                       text = 'Next Question',
                                       command = self.remove_widgets,
                                       font = ('times', 12))
        self.__exit_button = tk.Button(self.__quiz_window,
                                       text = 'Exit Quiz',
                                       command = self.grade_quiz,
                                       font = ('times', 12))
        self.__check_button.grid(row = self.__row_index, column = 0)
        self.__next_button.grid(row = self.__row_index, column = 1)
        self.__exit_button.grid(row = self.__row_index, column = 2)
        self.__row_index += 1

        # Disable the next question button until the current question has been answered
        self.__next_button['state'] = 'disabled'



    # create_buttons() creates the response buttons appropriate to the question type. If the question
    #   has multiple answers, load check buttons. Otherwise load radio buttons
    def create_buttons(self, question_type):

        self.__buttons_frame = tk.Frame(self.__quiz_window)
        self.__rb_cb_list = []

        if question_type == 'multi':

            # Store all of the check button variables in a list to check the answer later
            self.__cb_vars_list = []

            # The number of answers can vary depending on the question so buttons are created until
            #   all of the answers have been exhausted
            __answers_index = 0
            while __answers_index < self.__current_qb.get_answer_count():
                
                self.__cb_var = tk.IntVar(self.__quiz_window)
                self.__cb_vars_list.append(self.__cb_var)
                self.__cb_var.set(0)

                self.__cb = tk.Checkbutton(self.__buttons_frame,
                                          text = self.__current_qb.get_entry('Answer' + str(__answers_index)),
                                          variable = self.__cb_var,
                                          font = ('times', 14),
                                          wraplength = 500)
                self.__cb.grid(row = __answers_index, sticky = 'w')
                self.__rb_cb_list.append(self.__cb)
                
                __answers_index += 1

        else:

            self.__radio_var = tk.IntVar(self.__quiz_window)
            self.__radio_var.set(-1)

            # The number of answers can vary depending on the question so buttons are created until
            #   all of the answers have been exhausted
            __answers_index = 0
            while __answers_index < self.__current_qb.get_answer_count():

                self.__rb = tk.Radiobutton(self.__buttons_frame,
                                           text = self.__current_qb.get_entry('Answer' + str(__answers_index)),
                                           variable = self.__radio_var,
                                           value = __answers_index,
                                           font = ('times', 14),
                                           wraplength = 500)
                self.__rb.grid(row = __answers_index, sticky = 'w')
                self.__rb_cb_list.append(self.__rb)

                __answers_index += 1

        self.__buttons_frame.grid(row = self.__row_index, columnspan = 3)
        self.__row_index += 1



    # check_answer() retrieves the answer chosen by the user and compares it to the correct answer
    def check_answer(self):

        self.__check_button['state'] = 'disabled'
        self.__answered_questions += 1

        # Either retrieve the single chosen answer or create a string containing all chosen answers
        if (self.__current_qb.get_entry('QuestionType')) == 'single':
            __user_answer = self.__current_qb.get_entry('Answer' + str(self.__radio_var.get()))
        else:
            __user_answer = ''
            __cb_index = 0
            for __entry in self.__cb_vars_list:
                if __entry.get() == 1:
                    __user_answer += self.__current_qb.get_entry('Answer' + str(__cb_index))
                __cb_index += 1

        # Check the user's answer against the correct one and create the response message
        if self.__current_qb.check_answer(__user_answer):
            self.__correct_answers += 1
            __response_message = 'Correct!'
        else:
            __response_message = f"Incorrect. The correct answer is {self.__current_qb.get_entry('CorrectAnswer')}"

        # Create the label for response message
        self.__response_label = tk.Label(self.__quiz_window,
                                         text = __response_message,
                                         wraplength = 450,
                                         font = ('times', 14))
        self.__response_label.grid(row = self.__row_index, ipady = 15, columnspan = 3)
        self.__row_index += 1

        # If further questions are available, activate the next question button. Otherwise prompt the
        #   user to exit and receive their grade
        if self.__quiz_list.get_length():
            self.__next_button['state'] = 'active'
        else:
            self.__quiz_over_label = tk.Label(self.__quiz_window,
                                              text = 'Quiz over!\nClick "Exit Quiz" for results.',
                                              font = ('times', 14))
            self.__quiz_over_label.grid(row = self.__row_index, columnspan = 3)



    # grade_quiz() calculates the user's score, presents it to the screen, and closes the window
    def grade_quiz(self):

        if not self.__answered_questions:
            pass
        else:
            __student_score = self.__correct_answers / self.__answered_questions
            tk.messagebox.showinfo('Quiz over! Here are your results.',
                                   f'You answered {self.__correct_answers} out of {self.__answered_questions}'
                                   + f' questions correct for a score of {__student_score:.2%}!')

        self.__quiz_window.destroy()



    # remove_widgets() is used to destroy the currently active widgets so they can be updated
    def remove_widgets(self):

        self.__question_num_lbl.grid_remove()
        self.__question_lbl.grid_remove()
        self.__check_button.grid_remove()
        self.__next_button.grid_remove()
        self.__exit_button.grid_remove()
        for __button in self.__rb_cb_list:
            __button.grid_remove()

        # Try clauses are for widgets that may or may not be present
        try:
            self.__response_label.grid_remove()
        except:
            pass
        try:
            self.__quiz_over_label.grid_remove()
        except:
            pass

        # Load the next question
        self.populate_window()
