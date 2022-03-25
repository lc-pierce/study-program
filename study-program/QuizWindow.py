#-----------------------------------------------------------------------------#
#   QuizWindow.py                                                             #
#   Author: Logan Pierceall                                                   #
#   Date: March 11, 2022                                                      #
#-----------------------------------------------------------------------------#

import tkinter as tk

import QuizLogic
import WidgetCreation

class QuizWindow:

    def __init__(self, quiz, parent_window):
    
        self.quiz = quiz
        self.green = 'SpringGreen4'
        self.red = 'firebrick2'
        self.correct_ans_color = 'SlateBlue1'
        self.questions_answered = 0
        self.question_number = 1
        
        self.CreateWindow(parent_window)
    
    
    
    def CheckAnswer(self):
    
        if self.entry_type == 'single':
            radio_choice = self.radio_var.get()
            
            # Ensure the user chose an answer
            if radio_choice == 0:
                return
            else:
                self.questions_answered += 1
                self.check_ans_button['state'] = 'disabled'
                self.next_ques_button['state'] = 'normal'
                check_ans = QuizLogic.CheckRadio(radio_choice, self.quiz,
                                                 self.quiz_entry)
        else:
            chosen_answers = QuizLogic.GetCBVars(self.cb_vars,
                                                 self.shuffled_ans)
            
            # Ensure the user chose at least one answer
            if chosen_answers:
                self.questions_answered += 1
                self.check_ans_button['state'] = 'disabled'
                self.next_ques_button['state'] = 'normal'
                check_ans = QuizLogic.CheckCB(chosen_answers, self.quiz,
                                              self.quiz_entry)
            else:
                return
        
        if check_ans:
            QuizLogic.IncrementCorrectAns(self.quiz)
            self.result_label.config(text = 'CORRECT!', fg = self.green)
        else:
            self.result_label.config(text = 'INCORRECT', fg = self.red)
    
    
    
    def CreateAnswers(self, parent):
        
        answers_frame = WidgetCreation.CreateFrame(self.answers_buttons_frame)
        answers_frame.pack(side = 'top', fill = 'both', expand = 'true')
        
        self.entry_type = QuizLogic.GetEntryType(self.quiz, self.quiz_entry)
        self.shuffled_ans = QuizLogic.ShuffleAnswers(self.quiz,
                                                     self.quiz_entry)
        if self.entry_type == 'single':
            self.radio_var = tk.IntVar(self.window)
            for index in self.shuffled_ans:
                self.CreateRadio(index, self.quiz, self.quiz_entry,
                                 answers_frame)
            self.radio_var.set(0)
        else:
            self.cb_vars = []
            for index in self.shuffled_ans:
                self.CreateCheckbox(index, self.quiz, self.quiz_entry,
                                    answers_frame)
        
        # Create an empty label to update when an answer is checked
        self.result_label = WidgetCreation.CreateLabel(answers_frame, '')
        self.result_label.pack(fill = 'x')
    
    
    
    def CreateButtons(self, parent):
    
        check_next_frame = WidgetCreation.CreateFrame(parent)
        exit_frame = WidgetCreation.CreateFrame(parent)
        
        check_next_frame.pack(side = 'top', fill = 'x')
        exit_frame.pack(side = 'bottom', fill = 'x')
        
        self.check_ans_button = WidgetCreation.CreateButton(check_next_frame,
                                                            'Check Answer',
                                                            self.CheckAnswer)
        self.next_ques_button = WidgetCreation.CreateButton(check_next_frame,
                                                            'Next Question',
                                                            self.LoadNext)
        self.next_ques_button['state'] = 'disabled'
        exit_button = WidgetCreation.CreateButton(exit_frame,
                                                  'Grade Quiz & Exit',
                                                  self.GradeQuiz)
        
        self.check_ans_button.pack(side = 'left', fill = 'x', expand = 'true')
        self.next_ques_button.pack(side = 'right', fill = 'x',
                                       expand = 'true')
        exit_button.pack(fill = 'x', expand = 'true')
    
    
    
    def CreateCheckbox(self, index, quiz, entry, parent):
    
        cb_var = tk.IntVar(self.window)
        self.cb_vars.append(cb_var)
        ans_text = QuizLogic.GetAnswer(index, quiz, entry)
        cb = WidgetCreation.CreateCheckButton(parent, ans_text, cb_var)
        cb.pack(fill = 'x')
        
    
    
    def CreateFrames(self):
    
        # Delete the old frames, if present, before constructing new frames
        try:
            self.question_frame.forget()
            self.answers_buttons_frame.forget()
        except:
            pass
    
        lf_text = QuizLogic.GetQuestionNumber(self.question_number, self.quiz)
        self.question_frame = WidgetCreation.CreateLabelFrame(self.window,
                                                              lf_text)
        self.answers_buttons_frame = WidgetCreation.CreateFrame(self.window)
        
        # Pack the main frames and set propagate to 0 to keep frames at a
        #   constant size
        self.question_frame.pack(side = 'left', fill = 'both', expand = 'true')
        self.question_frame.pack_propagate(0)
        self.answers_buttons_frame.pack(side = 'right', fill = 'both',
                                        expand = 'true')
        self.answers_buttons_frame.pack_propagate(0)
        
        self.CreateQuestion(self.question_frame)        # Create question field
        self.CreateAnswers(self.answers_buttons_frame)  # Create answer fields
        self.CreateButtons(self.answers_buttons_frame)  # Create action buttons
    
    
    
    def CreateQuestion(self, parent):
    
        text = QuizLogic.GetQuestion(self.quiz, self.quiz_entry)
        question_label = WidgetCreation.CreateLabel(parent, text)
        question_label.pack(fill = 'x')
    
    
    
    def CreateRadio(self, index, quiz, entry, parent):
    
        ans_text = QuizLogic.GetAnswer(index, quiz, entry)
        rb = WidgetCreation.CreateRadioButton(parent, ans_text, self.radio_var,
                                              index)
        rb.pack(fill = 'x')
    
    
    
    def CreateWindow(self, parent):
    
        self.window = tk.Toplevel(parent)
        HEIGHT = 600
        WIDTH = 1100
        y_pos = int((self.window.winfo_screenheight() / 2) - (HEIGHT / 2))
        x_pos = int((self.window.winfo_screenwidth() / 2) - (WIDTH / 2))
        self.window.geometry(f'{WIDTH}x{HEIGHT}+{x_pos}+{y_pos}')
        
        self.GetQuizEntry()
    
    
    
    def GetQuizEntry(self):
    
        # Retrieve a question from the quiz list
        result, self.quiz_entry = QuizLogic.GetEntry(self.quiz)
        
        # If the list is empty, proceed to load results
        if result:
            self.CreateFrames()
        else:
            self.QuizResults()
    
    
    
    def GradeQuiz(self):
    
        result, msg = QuizLogic.GradeQuiz(self.questions_answered, self.quiz)
        if result:
            tk.messagebox.showinfo('', msg)
        else:
            tk.messagebox.showerror('ERROR', msg)
    
    
    
    def LoadNext(self):
    
        self.question_number += 1
        self.GetQuizEntry()
    
    
    
    # QuizResults() is called once all quiz questions have been answered.
    def QuizResults(self):
    
        self.GradeQuiz()
        self.window.destroy()