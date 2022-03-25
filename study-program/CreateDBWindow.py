#-----------------------------------------------------------------------------#
# CreateDBWindow.py                                                           #
# Author: Logan Pierceall                                                     #
# Date: March 14, 2022                                                        #
#-----------------------------------------------------------------------------#

import tkinter as tk
from tkinter import messagebox
from tkinter import Tk

import CreateDBLogic
import WidgetCreation



class CreateDBWindow(Tk):

    def __init__(self, user, *args, **kwargs):
    
        super().__init__(*args, **kwargs)
        
        self.WIN_HEIGHT = 600           # Window height
        self.WIN_WIDTH = 1100           # Window width
        self.ANS_PAD = 1                # Padding used for answer box frames
        self.ANS_TEXT_HEIGHT = 2        # Height used for answer entry boxes
        self.FONT = ('georgia', 12)     # Default font used by all widgets
        self.ANS_LIMIT = 7              # Ceiling for number of answer options
        self.INITIAL_ANS_TEXT = 'Enter answer here...'  # Initial text inserted
                                                        #   into 'Answer' entry
                                                        #   boxes
                                                        
        self.INITIAL_Q_TEXT = 'Enter question here...'  # Initial text inserted
                                                        #   into the 'Question'
                                                        #   entry box
        
        self.finish_flag = False        # Flag to ensure the final question
                                        #   gets added to the file
        
        self.current_user = user
        self.question_num = 0           # Tracks current question number for
                                        #   display purposes
        
        # Bind the 'Tab' keyboard button to move between Text entry objects
        self.bind_class("Text", "<Tab>", self.FocusNextWidget)
        
        self.CreateWindow()
    
    
    
    # AddAnswer() calls CreateAnswerField() to add an additional label and
    #   text entry box for an answer option. An upper limit to the amount
    #   of answer options is given by self.ANS_LIMIT
    # Args:     none
    # Returns:  none
    def AddAnswer(self, *args):
        
        if self.ans_index < self.ANS_LIMIT:
            self.CreateAnswerField(self.ans_frame)
        else:
            tk.messagebox.showerror('ERROR', 'Answer limit reached.')
    
    
    
    # ClearField() is an event method bound to <FocusIn> on the text entry
    #   boxes used for the question and answer fields. It clears out the text
    #   initially placed into the field when created if it is still present.
    # Args:     event = the event that invokes the function
    # Returns:  none
    def ClearField(self, event):
        text = event.widget.get('1.0', 'end').rstrip()
        if (text == self.INITIAL_Q_TEXT or text == self.INITIAL_ANS_TEXT):
            event.widget.delete('1.0', 'end')
    
    
    
    # CreateAnswerField() initializes the following widgets:
    #   A frame to hold the label and checkbox
    #   A frame to hold the text entry box
    #   A label to indicate the answer option number
    #   A checkbox to indicate the answer option is a correct answer
    #   A text entry box to provide the answer option's content
    # Args:     parent = the widget's parent object
    # Returns:  none
    def CreateAnswerField(self, parent):
    
        self.ans_index += 1
    
        # Create a frame to hold the label and correct answer checkbox and a
        #   frame to hold the text entry box
        label_frame = WidgetCreation.CreateFrame(parent, self.ANS_PAD,
                                                 self.ANS_PAD)
        label_frame.pack(fill = 'x')
        
        text_frame = WidgetCreation.CreateFrame(parent, self.ANS_PAD,
                                                self.ANS_PAD)
        text_frame.pack(fill = 'x')
        
        # Create the numbered answer label
        label_str = 'Answer ' + str(self.ans_index)
        ans_label = WidgetCreation.CreateLabel(label_frame, label_str,
                                               self.FONT)
        ans_label.pack(side = 'left')
        
        # Create a checkbox to mark an answer as the correct option
        cb_var = tk.IntVar(self)
        self.cb_list.append(cb_var)
        ans_cb = WidgetCreation.CreateCheckButton(label_frame,
                                                  'Correct Answer', cb_var,
                                                  self.FONT)
        ans_cb.pack(side = 'right')
        
        # Create the text entry box
        ans_text = WidgetCreation.CreateText(text_frame, self.FONT,
                                             self.ANS_TEXT_HEIGHT)
        ans_text.insert('1.0', self.INITIAL_ANS_TEXT)
        ans_text.pack(fill = 'x')
        
        # Bind the <FocusIn> event to remove the INITIAL_ANS_TEXT string
        ans_text.bind('<FocusIn>', self.ClearField)
        
        # Bind the <FocusOut> event to restore the INITIAL_ANS_TET string
        #   if no other text was entered into the field
        ans_text.bind('<FocusOut>', self.RestoreAnswerField)
        
        # Store the box into a list for later retrieval
        self.ans_box_list.append(ans_text)
    
    
    
    # CreateButtonFields() initializes the following widgets:
    #   A button to add an additional answer field
    #   A button to save the current data and load a fresh screen
    #   A button to save the current data and record all the data to a file
    # Args:     parent = the widget's parent object
    # Returns:  none
    def CreateButtonFields(self, parent):
    
        # Create a button that calls AddAnswer() to add an additional set of
        #   answer entry fields
        add_ans_button = WidgetCreation.CreateButton(parent,
                                                     'Add answer box',
                                                     self.AddAnswer)
        add_ans_button.pack(side = 'left', fill = 'x', expand = 'true')
        
        # Create a button that calls NextQuestion() to save the currently
        #   entered data and create a fresh screen
        next_q_button = WidgetCreation.CreateButton(parent, 'Next question',
                                                    self.NextQuestion)
        next_q_button.pack(side = 'left', fill = 'x', expand = 'true')
        
        # Create a button that calls SerializeDB() to save the currently
        #   entered data and write it to a file
        finish_button = WidgetCreation.CreateButton(parent, 'Save & Finish',
                                                    self.SerializeDB)
        finish_button.pack(side = 'right', fill = 'x', expand = 'true')
    
    
    
    # CreateFrames() initalizes the following widgets:
    #   A frame to hold the question entry field
    #   A frame to hold the answer entry fields
    #   A frame to hold the window's buttons
    # It also calls the functions to initialize the question fields, the answer
    #   fields, and the button fields
    # Args:     none
    # Returns:  none
    def CreateFrames(self):
    
        self.question_num += 1
        self.ans_box_list = []          # Stores all answer entry boxes so the
                                        #   contents can be retrieved later
        self.ans_index = 0              # Tracks answer option number for
                                        #   display purposes
        self.cb_list = []               # Stores all checkbuttons so their
                                        #   contents can be retrieved later
        
        # Create the 'Question' label frame
        q_str = 'Question ' + str(self.question_num)
        self.question_frame = WidgetCreation.CreateLabelFrame(self, q_str,
                                                              self.FONT)
        self.question_frame.pack(side = 'left', fill = 'both', expand = 'true')
        self.question_frame.pack_propagate(0)
        
        # Create the 'Answer' and button frames
        self.answers_buttons_frame = WidgetCreation.CreateFrame(self)
        self.answers_buttons_frame.pack(side = 'right', fill = 'both',
                                        expand = 'true')
        self.answers_buttons_frame.pack_propagate(0)
        
        self.ans_frame = WidgetCreation.CreateFrame(self.answers_buttons_frame)
        self.ans_frame.pack(side = 'top', fill = 'both', expand = 'true')
        
        but_frame = WidgetCreation.CreateFrame(self.answers_buttons_frame)
        but_frame.pack(side = 'bottom', fill = 'x')
        
        # Create the 'Question' fields
        self.CreateQuestionFields(self.question_frame)
        
        # Create the 4 initial 'Answer' fields
        while self.ans_index < 4:
            self.CreateAnswerField(self.ans_frame)
            
        # Create the button fields
        self.CreateButtonFields(self.answers_buttons_frame)
    
    
    
    # CreateQuestionFields() initializes the following widgets:
    #   A text entry box to enter the question content
    # Args:     parent = the widget's parent object
    # Returns:  none
    def CreateQuestionFields(self, parent):
    
        self.question_entry = WidgetCreation.CreateText(parent, self.FONT)
        self.question_entry.pack(fill = 'both', expand = 'true')
        
        # Insert the initial entry box contents
        self.question_entry.insert('1.0', self.INITIAL_Q_TEXT)
        
        # Bind the <FocusIn> event to remove the INITIAL_Q_TET string
        self.question_entry.bind('<FocusIn>', self.ClearField)
        
        # Bind the <FocusOut> event to restore the INITIAL_Q_TET string
        #   if no other text was entered into the field
        self.question_entry.bind('<FocusOut>', self.RestoreQuestionField)
    
    
    
    # CreateWindow() initializes the Create DB window
    # Args:     none
    # Returns:  none
    def CreateWindow(self):
    
        # Obtain x&y coordinates to place window in center of screen
        y_pos = int((self.winfo_screenheight() / 2) - (self.WIN_HEIGHT / 2))
        x_pos = int((self.winfo_screenwidth() / 2) - (self.WIN_WIDTH / 2))
        
        self.title(f'New database file for {self.current_user}')
        self.geometry(f'{self.WIN_WIDTH}x{self.WIN_HEIGHT}+{x_pos}+{y_pos}')
        self.resizable(False, False)
        
        # Create the window frames
        self.CreateFrames()
    
    
    
    # FocusNextWidget() allows the 'Tab' keyboard button to shift focus between
    #   widgets rather than insert space into an entry widget
    # Args:     event = the event that invokes the function
    # Returns:  none
    def FocusNextWidget(self, event):
    
        event.widget.tk_focusNext().focus()
    
    
    
    # NextQuestion() is called by the 'Next question' button. It retrieves the
    #   contents from all of the window's widgets and passes them to
    #   CheckFields() in CreateDBLogic.py so the contents can be validated and
    #   stored before refreshing the widgets for the next question
    # Args:     none
    # Returns:  none
    def NextQuestion(self, *args):
        
        # Retrieve the text from the quest entry box
        q_str = self.question_entry.get('1.0', 'end').rstrip()
        
        # Retrieve the text from the answer entry boxes
        ans_entries = []
        for box in self.ans_box_list:
            ans_entries.append(box.get('1.0', 'end').rstrip())
        
        # Retrieve the values from the check buttons
        cb_checked_list = []
        for cb in self.cb_list:
            cb_checked_list.append(cb.get())
        
        # Pass all collected info to CheckFields() in CreateDBLogic for
        #   verification. If all info is valid, it will be placed into
        #   a JSON-ready format
        result, msg = CreateDBLogic.CheckFields(q_str, self.INITIAL_Q_TEXT,
                                                ans_entries,
                                                self.INITIAL_ANS_TEXT,
                                                cb_checked_list,
                                                self.finish_flag)
        
        # If there was an error in reading the info, inform the user
        if not result:
            tk.messagebox.showerror('ERROR', msg)
        
        # If this function wasn't called by SerializeDB(), refresh the screen
        #   for a new question
        elif not self.finish_flag:
            self.question_frame.forget()
            self.answers_buttons_frame.forget()
            self.CreateFrames()
    
    
    
    # RestoreAnswerField() re-populates answer entry boxes with the initial
    #   content string if the user shift focus off of an answer entry field
    #   without entering any contents
    # Args:     event = the event that invokes the function
    # Returns:  none
    def RestoreAnswerField(self, event):
        if (event.widget.get('1.0', 'end').rstrip() == ''):
            event.widget.insert('1.0', self.INITIAL_ANS_TEXT)
    
    
    
    # RestoreQuestionField() re-populates answer entry boxes with the initial
    #   content string if the user shift focus off of the question entry field
    #   without entering any contents
    # Args:     event = the event that invokes the function
    # Returns:  none
    def RestoreQuestionField(self, event):
        if event.widget.get('1.0', 'end').rstrip() == '':
            event.widget.insert('1.0', self.INITIAL_Q_TEXT)
    
    
    
    # SerializeDB() is called by the 'Save & Finish' button. It calls
    #   NextQuestion() to retrieve the info currently present in the widgets
    #   before calling SerializeDB() in CreateDBLogic.py. That function saves
    #   the collected info to a file
    # Args:     none
    # Returns:  none
    def SerializeDB(self, *args):
    
        # Capture the current data before finalizing
        self.finish_flag = True
        self.NextQuestion()
        
        # Confirm the user is finished before finalizing all the data
        ask = tk.messagebox.askyesno('Finished?',
                                     f'Write {self.question_num} questions to file?')
        if ask:
            files = [('JSON Files', '*.json'), ('All files', '*.*')]
            file = tk.filedialog.asksaveasfilename(title = 'Save as...',
                                                   filetypes = files,
                                                   defaultextension = '.json')
            
            # 'result' indicates the success of the function call. If False,
            #   'msg' will contain an error message
            result, msg = CreateDBLogic.SerializeDB(file)
            
            if result:
                tk.messagebox.showinfo('SUCCESS', msg)
                self.destroy()
            else:
                tk.messagebox.showerror('ERROR', msg)