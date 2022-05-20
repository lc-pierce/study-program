import random
import tkinter as tk
from tkinter import messagebox

import Widgets

class QuizWindow():
    
    def __init__(self, root_window, quiz_list):
        
        self.root = root_window
        self.quiz = quiz_list
        
        self.answered_questions = 0
        self.correct = 0
        self.question_num = 0
        
        # Shuffle the quiz order so each quiz is unique
        random.shuffle(self.quiz)
        self.InitializeWindow()
    
    
    def CheckAnswer(self):
        """Check the chosen answer against the question's correct answer.
        
        This function is called by the 'Check Answer' button.
        """
        
        answer = False
        if self.quiz_entry['Type'] == 'single':
            user_choice = self.radio_var.get()
            if user_choice == 0:
                return
            
            user_answer = self.quiz_entry['Answer'+str(user_choice)]
            correct_answer = self.quiz_entry['Correct']
            if user_answer == correct_answer:
                answer = True
        else:
            # Convert the user's selected answers to text
            user_answer = []
            for index, cb_var in enumerate(self.cb_vars, 0):
                if cb_var.get() == 1:
                    answer_index = self.answer_indeces[index]
                    answer_str = self.quiz_entry['Answer'+str(answer_index)]
                    user_answer.append(answer_str)
            if not user_answer:
                return
            
            correct_answer = self.quiz_entry['Correct'].copy()
            correct_answer.sort()
            user_answer.sort()
            if user_answer == correct_answer:
                answer = True
        
        # Disable the 'Check Answer' button until a new question is loaded
        self.check_button['state'] = 'disabled'
        self.next_button['state'] = 'normal'
        self.answered_questions += 1
        if answer:
            self.correct += 1
            self.result_label.config(text='Correct!', bg='#000000',
                                     fg='#f8f8ff')
        else:
            self.result_label.config(text='Sorry, your answer is incorrect.',
                                     bg='#000000', fg='#f8f8ff')
            self.HighlightIncorrects(user_answer, correct_answer)
    
    
    def GradeQuiz(self):
        """Compute user's score and close the quiz window.
        
        This function is called either by the 'Grade Quiz & Exit' button or
            when the quiz list is empty.
        """
        
        if not self.answered_questions:
            msg = 'No questions have been answered.\n' \
                  'Are you sure you want to exit?'
        else:
            score = self.correct / self.answered_questions
            msg = f'You answered {self.correct} out of ' \
                  f'{self.answered_questions} questions correctly.\n' \
                  f'Your score is {score:.2%}.\n\nExit quiz?'
        
        ask = messagebox.askyesno('Exit', msg, parent=self.window)
        if ask:
            self.window.destroy()
    
    
    def HighlightIncorrects(self, user_answer, correct_answer):
        """Change answer label backgrounds to highlight incorrect answers.
        
        This function is called when a user answers a question incorrectly.
            Chosen answers that are incorrect are given a red background, and
            answers that are correct are given a green background.
        
        Arguments:
            user_answer: the text string(s) for the user's answer(s)
            correct_answer: the text string(s) for the correct answer(s)
        """
        
        green = '#00cc66'
        red = '#f25a5a'
        if self.quiz_entry['Type'] == 'single':
            for rb in self.rb_list:
                if rb['text'] == user_answer:
                    rb['bg'] = red
                if rb['text'] == correct_answer:
                    rb['bg'] = green
        else:
            for cb in self.cb_list:
                for answer in user_answer:
                    if cb['text'] == answer:
                        cb['bg'] = red
                        break
                for answer in correct_answer:
                    if cb['text'] == answer:
                        cb['bg'] = green
                        break
    
    
    def InitializeWindow(self):
        """Initialize the 'Quiz' window."""
        
        self.window = tk.Toplevel(self.root)
        height = 600
        width = 1300
        y = int((self.window.winfo_screenheight() / 2) - (height / 2))
        x = int((self.window.winfo_screenwidth() / 2) - (width / 2))
        self.window.geometry(f'{width}x{height}+{x}+{y}')
        self.window.resizable(False, False)
        
        self.main_frame = Widgets.CreateFrame(self.window)
        self.main_frame.pack(fill='both', expand='true')
        self.main_canvas = Widgets.CreateCanvas(self.main_frame)
        self.main_canvas.pack(fill='both', expand='true')
        
        white = '#f8f8ff'
        # Create the question widgets
        self.main_canvas.create_rectangle(5, 5, 635, 480, fill=white)
        q_frame = Widgets.CreateFrame(self.main_canvas)
        self.main_canvas.create_window(7, 7, anchor='nw', height=473,
                                       width=628, window=q_frame)
        self.question_label = Widgets.CreateLabel(q_frame, _text='')
        self.question_label.pack(fill='x')
        self.result_label = Widgets.CreateLabel(q_frame, _text='',
                                                _font=('georgia', 18),
                                                _anchor='center')
        self.result_label.pack(side='bottom', fill='x')
        
        # Create a window to hold the action buttons
        self.main_canvas.create_rectangle(5, 490, 635, 585, fill=white)
        b_frame = Widgets.CreateFrame(self.main_canvas)
        self.main_canvas.create_window(7, 492, anchor='nw', height=93,
                                       width=628, window=b_frame)
        
        # Create the buttons
        b_height = 5
        left_frame = Widgets.CreateFrame(b_frame)
        left_frame.pack(side='left', fill='both', expand='true')
        middle_frame = Widgets.CreateFrame(b_frame)
        middle_frame.pack(side='left', fill='both', expand='true')
        right_frame = Widgets.CreateFrame(b_frame)
        right_frame.pack(side='left', fill='both', expand='true')
        
        grade_button = Widgets.CreateButton(left_frame,
                                            _text='Grade Quiz\n& Exit',
                                            _cmd=self.GradeQuiz,
                                            _height=b_height)
        grade_button.pack()
        self.check_button = Widgets.CreateButton(middle_frame,
                                                 _text='Check\nAnswer',
                                                 _cmd=self.CheckAnswer,
                                                 _height=b_height)
        self.check_button.pack()
        self.next_button = Widgets.CreateButton(right_frame,
                                                _text='Next\nQuestion',
                                                _cmd=self.LoadNext,
                                                _height=b_height)
        self.next_button.pack()
        
        # Create a Frame to hold the answers Canvas
        self.main_canvas.create_rectangle(655, 5, 1285, 585, fill=white)
        self.a_frame = Widgets.CreateFrame(self.main_canvas)
        self.main_canvas.create_window(657, 7, anchor='nw', height=578,
                                       width=628, window=self.a_frame)
        
        # Begin populating the window
        self.quiz_entry = self.quiz.pop()
        self.PopulateWindow()
    
    
    def LoadNext(self):
        """Erase current widget contents to prepare for a new question.
        
        This function is called by the 'Next Question' button.
        """
        
        if not self.quiz:
            self.GradeQuiz()
            return
        
        # Disable 'Next Question' button until the answer has been checked
        self.next_button['state'] = 'disabled'
        self.check_button['state'] = 'normal'
        self.result_label.config(text='', bg='#f8f8ff')
        self.ans_canvas.forget()
        self.widget_frame.forget()
        if self.quiz_entry['Type'] == 'multi':
            for cb in self.cb_list:
                cb.forget()
        else:
            for rb in self.rb_list:
                rb.forget()
        
        self.quiz_entry = self.quiz.pop()
        self.PopulateWindow()
        
    
    def PopulateWindow(self):
        """Use the current quiz question to populate the window widgets. """
        
        def FrameConfigure(event):
            """Recalculate the answer canvas scroll region."""
            
            self.ans_canvas.configure(scrollregion=self.ans_canvas.bbox('all'))
        
        
        # Update the question label
        self.question_num += 1
        q_text = f'Question {self.question_num}\n\n' \
                 f'{self.quiz_entry["Question"]}'
        self.question_label.config(text=q_text)
        
        # Shuffle the order in which answers will appear
        self.answer_indeces = []
        for i in range(1, self.quiz_entry['NumOfAnswers']+1):
            self.answer_indeces.append(i)
        random.shuffle(self.answer_indeces)
        
        # Create the answers Canvas
        white = '#f8f8ff'
        self.ans_canvas = Widgets.CreateCanvas(self.a_frame, _bg=white)
        self.ans_canvas.pack(fill='both', expand='true')
        self.widget_frame = Widgets.CreateFrame(self.ans_canvas)
        self.widget_frame.pack(fill='both', expand='true')
        self.ans_canvas.create_window(0, 0, anchor='nw', width=620,
                                      window=self.widget_frame)
        
        scrollbar = Widgets.CreateScrollbar(self.ans_canvas)
        scrollbar.config(command=self.ans_canvas.yview)
        self.ans_canvas.configure(yscrollcommand=scrollbar.set,
                                  scrollregion=self.ans_canvas.bbox('all'))
        scrollbar.pack(side='right', fill='y')
        
        # Update the scroll region each time a new answer is added
        self.ans_canvas.bind('<Configure>', FrameConfigure)
        if self.quiz_entry['Type'] == 'multi':
            self.cb_list = []
            self.cb_vars = []
            for index in self.answer_indeces:
                cb_var = tk.IntVar(self.window)
                ans_text = self.quiz_entry['Answer'+str(index)]
                cb = Widgets.CreateCheckButton(self.widget_frame,
                                               _text=ans_text, _var=cb_var)
                cb.pack(fill='x')
                self.cb_list.append(cb)
                self.cb_vars.append(cb_var)
        else:
            self.rb_list = []
            self.radio_var = tk.IntVar(self.window)
            for index in self.answer_indeces:
                ans_text = self.quiz_entry['Answer'+str(index)]
                rb = Widgets.CreateRadioButton(self.widget_frame,
                                               _text=ans_text,
                                               _var=self.radio_var,
                                               _index=index)
                rb.pack(fill='x')
                self.rb_list.append(rb)
            self.radio_var.set(0)