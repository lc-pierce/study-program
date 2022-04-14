#-----------------------------------------------------------------------------#
#   QuizWindow.py                                                             #
#   Author: Logan Pierceall                                                   #
#                                                                             #
#   This module creates the quiz window.
#-----------------------------------------------------------------------------#

import random
import tkinter as tk
from tkinter import Tk

import QuizLogic
import Widgets


class QuizWindow():

    def __init__(self, root_window, quiz):
    
        self.root = root_window
        self.quiz = quiz
        
        # Window dimensions
        self.WIN_HEIGHT = 600
        self.WIN_WIDTH  = 1300
        
        # Widget option constants
        self.BUT_HEIGHT = 5
        self.GREEN      = '#00cc66'
        self.RED        = '#f25a5a'
        self.WHITE      = '#f8f8ff'

        self.canvas_flag        = False
        self.correct_answers    = 0
        self.question_number    = 0
        self.questions_answered = 0
        
        # Shuffle the question order before loading the quiz
        random.shuffle(self.quiz)
        
        self.CreateWindow()
    
    
    
    # BindMouseWheel() is an event that triggers when the mouse hovers over the
    #   answer widget frame. It calls MouseWheelScroll() to allow the mouse
    #   wheel to scroll through the answer widget canvas
    # Args:     event = the event that invokes the function
    # Returns:  none
    def BindMouseWheel(self, event):
        
        self.ans_canvas.bind_all('<MouseWheel>', self.MouseWheelScroll)
    
    
    
    # CheckAnswer() is called by the 'Check Answer' button. This function
    #   retrieves the user's chosen answer(s) from the answer widgets and
    #   passes them to either the CheckRadio() or CheckCB() function in
    #   QuizLogic.py, depending on the question type
    def CheckAnswer(self):
    
        if self.quiz_entry['Type'] == 'single':
            radio_choice = self.radio_var.get()
            
            # If the user didn't choose an answer yet, cancel the operation
            if radio_choice == 0:
                return
            
            # Disable the 'Check Answer' button and enable 'Next Question'
            self.check_button['state'] = 'disabled'
            self.next_button['state']  = 'normal'
            
            self.questions_answered += 1
            check_ans = QuizLogic.CheckRadio(radio_choice, self.quiz_entry)
        
        else:
            chosen_answers = QuizLogic.GetCBVars(self.cb_vars,
                                                 self.shuffled_ans)
            
            # If the user didn't choose any answers yet, cancel the operation
            if not chosen_answers:
                return
                
            # Disable the 'Check Answer' button and enable 'Next Question'
            self.check_button['state'] = 'disabled'
            self.next_button['state']  = 'normal'
            
            self.questions_answered += 1
            check_ans, ans_list = QuizLogic.CheckCB(chosen_answers,
                                                    self.quiz_entry)
        
        if check_ans:
            self.correct_answers += 1
            self.result_label.config(text = 'Correct!')
        else:
            self.result_label.config(text = 'Sorry, your answer is incorrect.')
            
            # Highlight the incorrect answers chosen and the correct answers
            if self.quiz_entry['Type'] == 'single':
                self.HighlightRadioAnswers(radio_choice)
            else:
                self.HighlightCheckAnswers(ans_list)
    
    
    
    # CreateAnswers() initializes the answer widgets
    # Args:     _parent = the widgets' parent object
    # Returns:  none
    def CreateAnswers(self, _parent = None):
    
        if not _parent:
            _parent = self.a_frame
        
        # Shuffle the order the answers will be created
        self.shuffled_ans = QuizLogic.ShuffleAnswers(self.quiz_entry)
        
        if self.quiz_entry['Type'] == 'single':
            self.radio_var = tk.IntVar(self.window)
            for index in self.shuffled_ans:
                self.CreateRadio(index, self.quiz_entry, _parent)
            self.radio_var.set(0)
        else:
            self.cb_vars = []
            for index in self.shuffled_ans:
                self.CreateCheckbox(index, self.quiz_entry, _parent)
    
    
    
    # CreateAnswersCanvas() creates a scrollable canvas to place the answer
    #   widgets in. A canvas is necessary if the total count of characters
    #   in all of the answer options is > 1800.
    # Args:     none
    # Returns:  none
    def CreateAnswersCanvas(self):
    
        self.canvas_flag = True
    
        # Create a canvas and place a frame into it to pack the widgets
        self.ans_canvas = Widgets.CreateCanvas(self.a_frame)
        self.ans_canvas.pack(fill = 'both', expand = 'true')
        
        self.widget_frame = Widgets.CreateFrame(self.ans_canvas)
        self.widget_frame.pack(fill = 'both', expand = 'true')
        
        self.ans_canvas.create_window(0, 0, anchor = 'nw', width = 620,
                                      window = self.widget_frame)
        
        # Create a scrollbar to attach to the canvas
        scrollbar = Widgets.CreateScrollbar(self.ans_canvas)
        scrollbar.config(command = self.ans_canvas.yview)
        self.ans_canvas.configure(yscrollcommand = scrollbar.set,
                                  scrollregion = self.ans_canvas.bbox('all'))
        scrollbar.pack(side = 'right', fill = 'y')
        
        # Create canvas bind to update the scroll region each time an answer
        #   is created
        self.widget_frame.bind('<Configure>', self.FrameConfigure)
        
        # Create scrollbar bind to scroll only when mouse is over the canvas
        self.widget_frame.bind('<Enter>', self.BindMouseWheel)
        self.widget_frame.bind('<Leave>', self.UnbindMouseWheel)
        
        # Create the answer widgets
        self.CreateAnswers(self.widget_frame)
    
    
    
    # CreateButtons() initializes the buttons used to check the selected
    #   answer, load the next question, and grade and exit the quiz
    # Args:     none
    # Returns:  none
    def CreateButtons(self):
    
        left_frame = Widgets.CreateFrame(self.b_frame)
        left_frame.pack(side = 'left', fill = 'both', expand = 'true')
        
        middle_frame = Widgets.CreateFrame(self.b_frame)
        middle_frame.pack(side = 'left', fill = 'both', expand = 'true')
        
        right_frame = Widgets.CreateFrame(self.b_frame)
        right_frame.pack(side = 'left', fill = 'both', expand = 'true')
        
        # Create a button to grade the quiz and exit
        grade_button = Widgets.CreateButton(left_frame, 'Grade Quiz\n& Exit',
                                            self.GradeQuiz, self.BUT_HEIGHT)
        grade_button.pack()
        
        # Create a button to check the user's answer
        self.check_button = Widgets.CreateButton(middle_frame, 'Check\nAnswer',
                                                 self.CheckAnswer,
                                                 self.BUT_HEIGHT)
        self.check_button.pack()
        
        # Create a button to load the next question
        self.next_button = Widgets.CreateButton(right_frame, 'Next\nQuestion',
                                                self.LoadNext, self.BUT_HEIGHT)
        self.next_button.pack()
    
    
    
    # CreateCheckbox() initializes a single check button answer option
    # Args:     index  = the answer option number to create
    #           entry  = the current quiz question
    #           parent = the radio button's parent object
    # Returns:  none
    def CreateCheckbox(self, index, entry, parent):
    
        cb_var = tk.IntVar(self.window)
        ans_text = QuizLogic.GetAnswer(index, entry)
        cb = Widgets.CreateCheckButton(parent, ans_text, cb_var)
        cb.pack(fill = 'x')
        self.cb_vars.append(cb_var)
        self.cb_list.append(cb)
    
    
    
    # CreateMainFrames() initializes a canvas that covers the entire window, a
    #   frame that holds the question, and a frame that holds the answer 
    #   options
    def CreateMainFrames(self):
        
        # Create a rectangle, frame, and window for the question
        self.main_canvas.create_rectangle(5, 5, 635, 480, fill = self.WHITE)
        self.q_frame = Widgets.CreateFrame(self.main_canvas)
        self.main_canvas.create_window(7, 7, anchor = 'nw',
                                       height = 473, width = 628,
                                       window = self.q_frame)
        
        # Create a rectangle, frame, and window for the answers
        self.main_canvas.create_rectangle(655, 5, 1285, 585, fill = self.WHITE)
        self.a_frame = Widgets.CreateFrame(self.main_canvas)
        self.main_canvas.create_window(657, 7, anchor = 'nw',
                                       height = 578, width = 628,
                                       window = self.a_frame)
        
    
    
    # CreateQuestion() initializes the label containing the question text
    # Args:     none
    # Returns:  none
    def CreateQuestion(self):
        
        # Retrieve the question from the quiz entry
        question = QuizLogic.GetQuestion(self.quiz_entry)
        text = f'Question {self.question_number}\n\n{question}'
        
        self.question_label = Widgets.CreateLabel(self.q_frame, text)
        self.question_label.pack(fill = 'x')
        
        # Create an empty label to update when an answer is checked
        self.result_label = Widgets.CreateLabel(self.q_frame, '',
                                                _font = ('georgia', 18),
                                                _anchor = 'center')
        self.result_label.pack(side = 'bottom', fill = 'x')
    
    
    
    # CreateRadio() initializes a single radio button answer option
    # Args:     index  = the answer option number to create
    #           entry  = the current quiz question
    #           parent = the radio button's parent object
    # Returns:  none
    def CreateRadio(self, index, entry, parent):
    
        ans_text = QuizLogic.GetAnswer(index, entry)
        rb = Widgets.CreateRadioButton(parent, ans_text, self.radio_var, index)
        rb.pack(fill = 'x')
        self.rb_list.append(rb)
    
    
    
    # CreateWindow() initializes the main window and creates a main frame and
    #   canvas that encompass the entire screen. This function also initializes
    #   the frame and canvas that hold the action buttons. Finally, it calls
    #   the function to retrieve the first quiz question.
    # Args:     none
    # Returns:  none
    def CreateWindow(self):
    
        self.window = tk.Toplevel(self.root)
    
        # Obtain x&y coordinates to place window in center of screen
        y_pos = int((self.window.winfo_screenheight() / 2) -
                    (self.WIN_HEIGHT / 2))
        x_pos = int((self.window.winfo_screenwidth() / 2) -
                    (self.WIN_WIDTH / 2))
        
        dimensions = f'{self.WIN_WIDTH}x{self.WIN_HEIGHT}+{x_pos}+{y_pos}'
        self.window.geometry(dimensions)
        self.window.title('Study Program')
        self.window.resizable(False, False)
        
        # Create a main frame and canvas
        self.main_frame = Widgets.CreateFrame(self.window)
        self.main_frame.pack(fill = 'both', expand = 'true')
        
        self.main_canvas = Widgets.CreateCanvas(self.main_frame)
        self.main_canvas.pack(fill = 'both', expand = 'true')
        
        # Create a rectangle, frame, and window for the question
        self.main_canvas.create_rectangle(5, 5, 635, 480, fill = self.WHITE)
        self.q_frame = Widgets.CreateFrame(self.main_canvas)
        self.main_canvas.create_window(7, 7, anchor = 'nw',
                                       height = 473, width = 628,
                                       window = self.q_frame)
        
        # Create a rectangle, frame, and window for the action buttons
        self.main_canvas.create_rectangle(5, 490, 635, 585, fill = self.WHITE)
        self.b_frame = Widgets.CreateFrame(self.main_canvas)
        self.main_canvas.create_window(7, 492, anchor = 'nw',
                                       height = 93, width = 628,
                                       window = self.b_frame)
        
        # Create a rectangle, frame, and window for the answers
        self.main_canvas.create_rectangle(655, 5, 1285, 585, fill = self.WHITE)
        self.a_frame = Widgets.CreateFrame(self.main_canvas)
        self.main_canvas.create_window(657, 7, anchor = 'nw',
                                       height = 578, width = 628,
                                       window = self.a_frame)
        
        # Create the buttons
        self.CreateButtons()
        
        # Obtain an initial quiz entry object
        self.GetQuizEntry()
    
    
    
    # FrameConfigure() is an event that re-calculates the scroll region of the
    #   answers canvas whenever an answer option is added.
    # Args:     event = the event that invokes the function
    # Returns:  none
    def FrameConfigure(self, event):
    
        self.ans_canvas.configure(scrollregion = self.ans_canvas.bbox('all'))
    
    
    
    # GetQuizEntry() attempts to retrieve a new quiz question. If one exists,
    #   this function calls the functions to generate the window widgets. If
    #   no more questions exist, the function to grade and exit the quiz gets
    #   called
    # Args:     none
    # Returns:  none
    def GetQuizEntry(self):
    
        # Retrieve a question from the quiz list
        self.quiz_entry = QuizLogic.GetEntry(self.quiz)
        
        # If all questions have been asked, proceed to the results
        if not self.quiz_entry:
            self.GradeQuiz()
            return
        
        # Increment the current question number
        self.question_number += 1
            
        # Disable the 'Next Question' button
        self.next_button['state'] = 'disabled'
            
        # Enable the 'Check Answer' button
        self.check_button['state'] = 'normal'
        
        # Initialize lists to hold radiobuttons and checkbuttons
        self.rb_list = []
        self.cb_list = []
            
        # Load the widgets
        self.CreateQuestion()
            
        if ((QuizLogic.GetCharCount(self.quiz_entry) > 1800) or
           (QuizLogic.GetAnswerCount(self.quiz_entry) > 10)):
            # Answer options will likely exceed window space, so the
            #   widgets should be in a scrollable canvas
            self.CreateAnswersCanvas()
        else:
            self.CreateAnswers()
    
    
    
    # GradeQuiz() is called by the 'Grade Quiz & Exit' button. It creates a
    #   pop-up window to display the user's score (if applicable) and prompts
    #   the user to exit the quiz.
    # Args:     none
    # Returns:  none
    def GradeQuiz(self):
    
        if not self.questions_answered:
            close_msg = 'Exit quiz?'
        else:
            score = self.correct_answers / self.questions_answered
            close_msg = f'You answered {self.correct_answers} out of ' \
                        f'{self.questions_answered} questions correctly\n' \
                        f'for a score of {score:.2%}\nExit quiz?'
        
        close = tk.messagebox.askyesno('Exit', close_msg)
        if close:
            self.window.destroy()
    
    
    
    # HighlightCheckAnswers() is called if the user gets a multiple answer
    #   question wrong. This function highlights the user's incorrect answers
    #   with a red background and the correct answers with a green background
    # Args:     user_answer = the list of answer strings chosen by the user
    # Returns:  none 
    def HighlightCheckAnswers(self, user_answers):
        
        # Remove the user-chosen answers that were correct from the list of
        #   user answers
        for correct_ans in self.quiz_entry['Correct']:
            index = 0
            found = False
            for answer in user_answers:
                if answer == correct_ans:
                    found = True
                    break
                index += 1
            
            if found:
                user_answers.pop(index)
        
        # Change the button background to red for incorrect answers
        for cb in self.cb_list:
            for answer in user_answers:
                if cb['text'] == answer:
                    cb['bg'] = self.RED

        # Change the button background to green for correct answers
        for cb in self.cb_list:
            for answer in self.quiz_entry['Correct']:
                if cb['text'] == answer:
                    cb['bg'] = self.GREEN
    
    
    
    # HighlightRadioAnswers() is called if the user gets a single answer
    #   question wrong. This function highlights the user's answer with a red
    #   background and the correct answer with a green background
    # Args:     user_answer = the radiobutton value of the user's answer
    # Returns:  none
    def HighlightRadioAnswers(self, user_answer):
        
        for rb in self.rb_list:
            # Change the button background to red for the incorrect answer
            if rb['value'] == user_answer:
                rb['bg'] = self.RED
            
            # Change the button background to green for the correct answer
            if rb['text'] == self.quiz_entry['Correct']:
                rb['bg'] = self.GREEN
    
    
    
    # LoadNext() is called by the 'Next Question' button. This function erases
    #   the current question and answer frames in preparation for the next
    #   question
    # Args:     none
    # Returns:  none
    def LoadNext(self):
        
        # Erase the question and results labels
        self.question_label.forget()
        self.result_label.forget()
        
        # Erase the answer widgets
        if self.canvas_flag:
            self.canvas_flag = False
            self.ans_canvas.forget()
            self.widget_frame.forget()
        
        if self.quiz_entry['Type'] == 'single':
            for rb in self.rb_list:
                rb.forget()
        else:
            for cb in self.cb_list:
                cb.forget()
        
        # Retrieve the next quiz question
        self.GetQuizEntry()
    
    
    
    # MouseWheelScroll() allows the mouse wheel to scroll through the answer
    #   widgets field if it grows beyond the height of the window
    # Args:     event = the event that invokes the function
    # Returns:  none
    def MouseWheelScroll(self, event):
    
        self.ans_canvas.yview_scroll(int(-1 * (event.delta / 120)), 'units')
    
    
    
    # UnbindMouseWheel() is an event that triggers when the mouse moves away
    #   from the answer widget frame. It unbinds the mouse wheel so that
    #   scrolling won't scroll through the widgets
    # Args:     event = the event that invokes the function
    # Returns:  none
    def UnbindMouseWheel(self, event):
    
        self.ans_canvas.unbind_all('<MouseWheel>')