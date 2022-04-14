#-----------------------------------------------------------------------------#
# CreateDBWindow.py                                                           #
# Author: Logan Pierceall                                                     #
# Date: March 14, 2022                                                        #
#-----------------------------------------------------------------------------#

import os
import tkinter as tk
from tkinter import messagebox
from tkinter import Tk

import CreateDBLogic
import MainLogic
import Widgets


class CreateDBWindow():

    def __init__(self, root_window, user, parent_listbox):
    
        self.root         = root_window
        self.current_user = user
        self.listbox      = parent_listbox
        
        # Window dimensions
        self.WIN_HEIGHT = 600
        self.WIN_WIDTH  = 1300
        
        # Widget option constants
        self.BUT_HEIGHT       = 5
        self.INITIAL_ANS_TEXT = 'Enter answer here'
        self.INITIAL_Q_TEXT   = 'Enter question here...'
        self.WHITE            = '#f8f8ff'
        
        # Initial text entry box contents constants
        self.INITIAL_Q_TEXT   = 'Enter question here...'
        self.INITIAL_ANS_TEXT = 'Enter answer here...'
        
        # Ensures final form gets added to the file
        self.finish_flag = False

        # Tracks current question number
        self.question_num = 1
        
        # Tracks the number of answer text entry boxes
        self.ans_index = 0
        
        self.CreateWindow()
    
    
    
    # AddAnswerBox() initializes all of the widgets required for a single
    #   answer entry option. This function is also called by the 'Add Answer
    #   Box' button
    # Args:     none
    # Returns:  none
    def AddAnswerBox(self):
    
        self.ans_index += 1
        
        # Create a frame to hold the label and correct answer checkbox
        label_frame = Widgets.CreateFrame(self.answers_frame, 1, 1)
        label_frame.pack(fill = 'x', expand = 'true')
        
        # Create the answer label
        label_str = 'Answer ' + str(self.ans_index)
        ans_label = Widgets.CreateLabel(label_frame, label_str)
        ans_label.pack(side = 'left')
        
        # Create a checkbox to mark an answer as the correct option
        cb_var = tk.IntVar(self.window)
        self.cb_list.append(cb_var)
        ans_cb = Widgets.CreateCheckButton(label_frame, 'Correct Answer', 
                                           cb_var)
        ans_cb.pack(side = 'left')
        
        # Create the text entry box
        text_frame = Widgets.CreateFrame(self.answers_frame,
                                      _padx = 1, _pady = 1)
        text_frame.pack(fill = 'x', expand = 'true')
        
        ans_text = Widgets.CreateText(text_frame)
        ans_text.insert('1.0', self.INITIAL_ANS_TEXT)
        ans_text.pack()
        self.ans_box_list.append(ans_text)
        
        # Create a binding to clear the initial text when the widget is
        #   selected
        ans_text.bind('<FocusIn>', self.ClearField)
        
        # Create a binding to re-insert the initial text if the widget
        #   isn't populated after clearing the contents
        ans_text.bind('<FocusOut>', self.RestoreAnswerField)
    
    
    
    # BindMouseWheel() allows the mouse wheel to scroll through the answers
    #   canvas if the mouse is within the canvas field
    # Args:     event = the invoking event
    # Returns:  none
    def BindMouseWheel(self, event):
    
        # The scroll wheel has undesired behavior if the answer widget side
        #   isn't yet fully populated
        if self.ans_index > 7:
            self.ans_canvas.bind_all('<MouseWheel>', self.MouseWheelScroll)
    
    
    
    # ClearField() is an event bound to <FocusIn> on the question and answer
    #   text entry boxes. This function clears out the text initially inserted
    #   into the widget when created.
    # Args:     event = the invoking event
    # Returns:  none
    def ClearField(self, event):
        contents = event.widget.get('1.0', 'end').rstrip()
        if (contents == self.INITIAL_Q_TEXT or
            contents == self.INITIAL_ANS_TEXT):
            event.widget.delete('1.0', 'end')
    
    
    
    # CreateAnswers() initializes the scrollable canvas and frame that will
    #   hold the answer entry widgets. This function also calls the
    #   AddAnswerBox() function 4 times to create the initial answer widgets
    # Args:     none
    # Returns:  none
    def CreateAnswers(self):
    
        # Create a canvas within the answers frame to place the widgets
        self.ans_canvas = Widgets.CreateCanvas(self.a_frame, self.WHITE)
        self.ans_canvas.pack(fill = 'both', expand = 'true')
    
        # Place a frame for the widgets inside the answer canvas
        self.answers_frame = Widgets.CreateFrame(self.ans_canvas)
        self.answers_frame.pack(fill = 'both', expand = 'true')
        self.ans_canvas.create_window(0, 0, anchor = 'nw', width = 620,
                                      window = self.answers_frame)
        
        # Create a scrollbar for the canvas
        scrollbar = Widgets.CreateScrollbar(self.ans_canvas)
        scrollbar.configure(command = self.ans_canvas.yview)
        self.ans_canvas.configure(yscrollcommand = scrollbar.set,
                                  scrollregion = self.ans_canvas.bbox('all'))
        scrollbar.pack(side = 'right', fill = 'y')
        
        # Bind the frame to update the scrollregion every time an answer is
        #   added to the window
        self.answers_frame.bind('<Configure>', self.FrameConfigure)
        
        # Bind the mouse wheel to scroll the scrollbar whenever the mouse is
        #   within the canvas boundaries
        self.answers_frame.bind('<Enter>', self.BindMouseWheel)
        self.answers_frame.bind('<Leave>', self.UnbindMouseWheel)
        
        # Initialize the list to hold checkbutton variables
        self.cb_list = []
        
        # Initialize the list to hold answer text entry boxes
        self.ans_box_list = []
        
        # Create 4 initial answer fields
        for i in range(4):
            self.AddAnswerBox()
    
    
    
    # CreateButtons() initializes the main window buttons that allow the user
    #   to add an additional answer entry box, save the current data and
    #   refresh the screen, and finish up creation by saving the file
    # Args:     none
    # Returns:  none
    def CreateButtons(self):
    
        # Create frames to hold the buttons
        left_frame = Widgets.CreateFrame(self.b_frame)
        left_frame.pack(side = 'left', fill = 'both', expand = 'true')
        
        middle_frame = Widgets.CreateFrame(self.b_frame)
        middle_frame.pack(side = 'left', fill = 'both', expand = 'true')
        
        right_frame = Widgets.CreateFrame(self.b_frame)
        right_frame.pack(side = 'left', fill = 'both', expand = 'true')
        
        # Create a button to exit creation and save the file
        finish_button = Widgets.CreateButton(left_frame, 'Save\n& Finish',
                                             self.SerializeDB, self.BUT_HEIGHT)
        finish_button.pack()
        
        # Create a button to save current data and refresh the screen
        next_button = Widgets.CreateButton(middle_frame, 'Next\nQuestion',
                                           self.NextQuestion, self.BUT_HEIGHT)
        next_button.pack()
        
        # Create a button to add an additional answer box
        add_answer_button = Widgets.CreateButton(right_frame,
                                                 'Add\nAnswer Box',
                                                 self.AddAnswerBox,
                                                 self.BUT_HEIGHT)
        add_answer_button.pack()
    
    
    
    # CreateQuestion() initializes a labelframe and text entry box to enter
    #   the question contents.
    # Args:     none
    # Returns:  none
    def CreateQuestion(self):
    
        # Create a labeled frame to hold the text entry box
        q_str = 'Question ' + str(self.question_num)
        self.question_lframe = Widgets.CreateLabelFrame(self.q_frame, q_str)
        self.question_lframe.pack(fill = 'both', expand = 'true')
        
        # Create the text entry box and fill with placeholder text
        self.question_text = Widgets.CreateText(self.question_lframe)
        self.question_text.pack(fill = 'both', expand = 'true')
        self.question_text.insert('1.0', self.INITIAL_Q_TEXT)
        
        # Create a binding to clear the initial text when the widget is
        #   selected
        self.question_text.bind('<FocusIn>', self.ClearField)
        
        # Create a binding to re-insert the initial text if the widget
        #   isn't populated after clearing the contents
        self.question_text.bind('<FocusOut>', self.RestoreQuestionField)
    
    
    
    # CreateWindow() initializes the Create DB window
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
        self.window.title(f'New database file for {self.current_user}')
        self.window.resizable(False, False)
        
        # Bind the 'Tab' keyboard button to move between Text entry objects
        self.window.bind_class("Text", "<Tab>", self.FocusNextWidget)
        
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
        
        # Create the question widgets
        self.CreateQuestion()
        
        # Create the button widgets
        self.CreateButtons()
        
        # Create the answer widgets
        self.CreateAnswers()
    
    
    
    # FocusNextWidget() allows the 'Tab' keyboard to shift focus between
    #   widgets instead of inserting a tab into a text entry box
    # Args:     event = the invoking event
    # Returns:  none
    def FocusNextWidget(self, event):
    
        event.widget.tk_focusNext().focus()
    
    
    
    # FrameConfigure() is an event that re-calculates the scroll region of the
    #   canvas every time a new answer box is added
    # Args:     event = the invoking event
    # Returns:  none
    def FrameConfigure(self, event):
    
        self.ans_canvas.configure(scrollregion = self.ans_canvas.bbox('all'))
    
    
    
    # MouseWheelScroll() allows the mouse wheel to scroll through the answers
    #   canvas
    # Args:     event = the invoking event
    # Returns:  none
    def MouseWheelScroll(self, event):
    
        self.ans_canvas.yview_scroll(int(-1 * (event.delta / 120)), 'units')
    
    
    
    # NextQuestion() is called by the 'Next Question' button. This function
    #   collects all of the user-provided information from the widgets and
    #   passes them to the CheckFields() function in CreateDBLogic.py. If all
    #   of the information passes, it's converted to a JSON format.
    # Args:     none
    # Returns:  none
    def NextQuestion(self):
    
        # Retreve the question text
        question_str = self.question_text.get('1.0', 'end').rstrip()
        
        # Retrieve the answer texts
        answer_strs = []
        for widget in self.ans_box_list:
            answer_strs.append(widget.get('1.0', 'end').rstrip())
        
        # Retrieve the check button values
        check_list = []
        for cb in self.cb_list:
            check_list.append(cb.get())
        
        # Pass the info off for validation and storage
        result, msg = CreateDBLogic.CheckFields(question_str,
                                                self.INITIAL_Q_TEXT,
                                                answer_strs,
                                                self.INITIAL_ANS_TEXT,
                                                check_list)
        if not result:
            tk.messagebox.showerror('Error', msg)
            
            # Bring the creation window back to the forefront of screen
            self.window.attributes("-topmost", True)
            self.window.attributes("-topmost", False)
            return
        
        # Refresh the widgets
        self.question_lframe.forget()
        self.ans_canvas.forget()
        
        self.question_num += 1
        self.ans_index = 0
        
        self.CreateQuestion()
        self.CreateAnswers()
    
    
    
    # RestoreAnswerField() re-inserts the initial answer text entry box
    #   string if the text was cleared but the user didn't populate the field
    # Args:     event = the invoking event
    # Returns:  none
    def RestoreAnswerField(self, event):
        if (event.widget.get('1.0', 'end').rstrip() == ''):
            event.widget.insert('1.0', self.INITIAL_ANS_TEXT)
    
    
    
    # RestoreQuestionField() re-inserts the initial question text entry box
    #   string if the text was cleared but the user didn't populate the field
    # Args:     event = the invoking event
    # Returns:  none
    def RestoreQuestionField(self, event):
        if event.widget.get('1.0', 'end').rstrip() == '':
            event.widget.insert('1.0', self.INITIAL_Q_TEXT)
    
    
    
    # SerializeDB() is called by the 'Save & Finish' button. This function
    #   makes one final check for data to record before prompting the user for
    #   a filename that gets passed to the SerializeDB() function in
    #   CreateDBLogic.py. Finally, the new file is passed to the AddQuizFile()
    #   in MainLogic.py to add the file to the user's listbox
    # Args:     none
    # Returns:  none
    def SerializeDB(self):
    
        # Confirm the user is finished before finalizing all the data
        ask = tk.messagebox.askyesno('Finish & Save',
                                     'Ready to save the file?')
        if not ask:
            return
    
        # Perform a final check of the widgets
        # Retreve the question text
        question_str = self.question_text.get('1.0', 'end').rstrip()
        
        # Retrieve the answer texts
        answer_strs = []
        for widget in self.ans_box_list:
            answer_strs.append(widget.get('1.0', 'end').rstrip())
        
        # Retrieve the check button values
        check_list = []
        for cb in self.cb_list:
            check_list.append(cb.get())
        
        result = CreateDBLogic.FinalCheck(question_str, self.INITIAL_Q_TEXT,
                                          answer_strs, self.INITIAL_ANS_TEXT,
                                          check_list)
        if not result:
            # Data still needs to be recorded before finalizing
            result, msg = CreateDBLogic.CheckFields(question_str,
                                                    self.INITIAL_Q_TEXT,
                                                    answer_strs,
                                                    self.INITIAL_ANS_TEXT,
                                                    check_list)
            if not result:
                tk.messagebox.showerror('Error', msg)
                
                # Bring the creation window back to the forefront of screen
                self.window.attributes("-topmost", True)
                self.window.attributes("-topmost", False)
                return
        
        # Prompt the user to save the file
        files = [('JSON Files', '*.json'), ('All files', '*.*')]
        cwd = os.getcwd() + '//database'
        file = tk.filedialog.asksaveasfilename(title = 'Save as...',
                                               filetypes = files,
                                               defaultextension = '.json',
                                               initialdir = cwd)
        
        if not file:
            # Bring the creation window back to the forefront of screen
            self.window.attributes("-topmost", True)
            self.window.attributes("-topmost", False)
            return
        
        # Save the file to disk
        result, msg = CreateDBLogic.SerializeDB(file)
        if result:
            tk.messagebox.showinfo('Success', msg)
            result, msg = MainLogic.AddQuizFile(self.listbox,
                                                self.current_user, file)
            self.window.destroy()
        else:
            tk.messagebox.showerror('Error', msg)
    
    
    
    # UnbindMouseWheel() removes the mouse wheel's ability to scroll through
    #   the answers canvas once the mouse is no longer within the canvas field
    # Args:     event = the invoking event
    # Returns:  none
    def UnbindMouseWheel(self, event):
    
        self.ans_canvas.unbind_all('<MouseWheel>')