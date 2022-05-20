import json
from json.decoder import JSONDecodeError
import os
import tkinter as tk
from tkinter import messagebox

import Widgets

class CreateDBWindow():
    
    def __init__(self, root_window, user_files, parent_listbox):
        
        self.root = root_window
        self.user_files = user_files
        self.listbox = parent_listbox
        
        self.question_num = 1
        self.file_data  = []
        self.init_q_text = 'Enter question here...'
        self.init_a_text = 'Enter answer here...'
        
        self.InitializeWindow()
    
    
    def AddAnswerBox(self):
        """Initialize the widgets for a single answer entry set.
        
        This function is called 4 times when initializing the window and by
            the 'Add Answer Box' button.
        """
        
        def ClearField(event):
            """Clear the contents of the answer text box."""
            if text.get('1.0', 'end').rstrip() == self.init_a_text:
                text.delete('1.0', 'end')
        
        def RestoreField(event):
            """Restore the contents of the answer text box."""
            if not text.get('1.0', 'end').rstrip():
                text.insert('1.0', self.init_a_text)
        
        
        self.ans_index += 1
        
        label_frame = Widgets.CreateFrame(self.answers_frame, _padx=1, _pady=1)
        label_frame.pack(fill='x', expand='true')
        label = Widgets.CreateLabel(label_frame,
                                    _text='Answer ' + str(self.ans_index))
        label.pack(side='left')
        
        # Create a Checkbutton to mark options as correct answers
        cb_var = tk.IntVar(self.window)
        self.cb_list.append(cb_var)
        cb = Widgets.CreateCheckButton(label_frame, _text='Correct Answer',
                                       _var = cb_var)
        cb.pack(side='left')
        
        text_frame = Widgets.CreateFrame(self.answers_frame, _padx=1, _pady=1)
        text_frame.pack(fill='x', expand='true')
        text = Widgets.CreateText(text_frame)
        text.insert('1.0', self.init_a_text)
        text.pack()
        self.ans_box_list.append(text)
        
        text.bind('<FocusIn>', ClearField)
        text.bind('<FocusOut>', RestoreField)
    
    
    def BindMouseWheel(self, event):
        """Bind the mouse wheel to scroll through the answers Canvas."""
        
        def MouseWheelScroll(event):
            self.ans_canvas.yview_scroll(int(-1*(event.delta/120)), 'units')
        
        if self.ans_index < 8:
            # If the current widgets don't fill the window, scrolling upward
            #   scrolls above the first widget into empty white space
            return
        self.ans_canvas.bind_all('<MouseWheel>', MouseWheelScroll)
    
    
    def CreateAnswers(self):
        """Initialize the widgets to provide the answer texts."""
        
        def FrameConfigure(event):
            self.ans_canvas.configure(scrollregion=self.ans_canvas.bbox('all'))
        
        def BindMouseWheel(event):
            if self.ans_index < 8:
                return
            self.ans_canvas.bind_all('<MouseWheel>', Scroll)
        
        def Scroll(event):
            self.ans_canvas.yview_scroll(int(-1*(event.delta/120)), 'units')
        
        white = '#f8f8ff'
        self.ans_canvas = Widgets.CreateCanvas(self.a_frame, _bg=white)
        self.ans_canvas.pack(fill='both', expand='true')
        self.answers_frame = Widgets.CreateFrame(self.ans_canvas)
        self.answers_frame.pack(fill='both', expand='true')
        self.ans_canvas.create_window(0, 0, anchor='nw', width=620,
                                      window=self.answers_frame)
        scrollbar = Widgets.CreateScrollbar(self.ans_canvas)
        scrollbar.configure(command=self.ans_canvas.yview)
        self.ans_canvas.configure(yscrollcommand=scrollbar.set,
                                  scrollregion=self.ans_canvas.bbox('all'))
        scrollbar.pack(side='right', fill='y')
        
        # Bind the mouse wheel to only scroll the Canvas when hovering over it
        self.ans_canvas.bind('<Enter>', BindMouseWheel)
        self.ans_canvas.bind('<Leave>',
                             lambda e: self.ans_canvas.unbind('<MouseWheel>'))
        
        # Bind the answers frame to update the Canvas' scrollregion
        self.answers_frame.bind('<Configure>', FrameConfigure)
        
        # Lists hold each answer option's widgets for retrieving later
        self.ans_index = 0
        self.cb_list = []
        self.ans_box_list = []
        for i in range(4):
            self.AddAnswerBox()
    
    
    def CreateQuestion(self):
        """Initialize the widgets to provide the question text."""
        
        def ClearField(event):
            """Clear the contents of the question text box."""
            if self.q_text.get('1.0', 'end').rstrip() == self.init_q_text:
                self.q_text.delete('1.0', 'end')
        
        def RestoreField(event):
            """Restore the contents of the question text box."""
            if not self.q_text.get('1.0', 'end').rstrip():
                self.q_text.insert('1.0', self.init_q_text)
        
        
        q_str = 'Question ' + str(self.question_num)        
        
        self.q_lframe = Widgets.CreateLabelFrame(self.q_frame, _text=q_str)
        self.q_lframe.pack(fill='both', expand='true')
        
        self.q_text = Widgets.CreateText(self.q_lframe)
        self.q_text.pack(fill='both', expand='true')
        self.q_text.insert('1.0', self.init_q_text)
        
        self.q_text.bind('<FocusIn>', ClearField)
        self.q_text.bind('<FocusOut>', RestoreField)
    
    
    def CreateQuizEntry(self):
        """Verify widgets were appropriately populated and build a quiz entry.
        
        Returns:
            'True' and the quiz entry dictionary if all fields were populated
                and no errors were encountered.
            'False' and 'None' if the question field was left empty, no answer
                text was provided, no answers were marked as correct, or an
                answer was marked as correct but not populated.
        """
        
        question = self.q_text.get('1.0', 'end').lstrip().rstrip()
        if not question or question == self.init_q_text:
            tk.messagebox.showerror('Error', 'Question field left empty.',
                                    parent=self.window)
            return False, None
        
        answers = []
        answer_filled = False
        for index, widget in enumerate(self.ans_box_list, 0):
            text = widget.get('1.0', 'end').lstrip().rstrip()
            if text and text != self.init_a_text:
                answer_filled = True
            answers.append(text)
        if not answer_filled:
            tk.messagebox.showerror('Error', 'Fill at least one answer field.',
                                    parent=self.window)
            return False, None
        
        answer_checks = []
        for cb in self.cb_list:
            answer_checks.append(cb.get())
        if not sum(answer_checks):
            tk.messagebox.showerror('Error', 'No answers were marked correct.',
                                    parent=self.window)
            return False, None
        
        # Ensure no answer fields were marked as correct but not populated
        for index, cb in enumerate(answer_checks, 0):
            if cb == 1:
                if not answers[index] or answers[index] == self.init_a_text:
                    msg = f'Answer {index+1} left empty but marked correct.'
                    tk.messagebox.showerror('Error', msg, parent=self.window)
                    return False, None
        
        # Translate valid information into a dictionary
        new_entry = {}
        correct_answers = sum(answer_checks)
        if correct_answers > 1:
            q_type = 'multi'
        else:
            q_type = 'single'
        new_entry.update({'Type': q_type})
        new_entry.update({'Question': question})
        
        ans_count = 0
        char_count = 0
        index = 1
        for answer in answers:
            if not answer or answer == self.init_a_text:
                # Skip answer fields left unaltered by user
                continue
            ans_count += 1
            char_count += len(answer)
            new_entry.update({'Answer'+str(index): answer})
            index += 1
        new_entry.update({'NumOfAnswers': ans_count})
        new_entry.update({'CharCount': char_count})
        
        ans_list = []
        for index, cb in enumerate(answer_checks, 0):
            if cb == 1:
                if correct_answers == 1:
                    new_entry.update({'Correct': answers[index]})
                    break
                else:
                    ans_list.append(answers[index])
        if ans_list:
            new_entry.update({'Correct': ans_list})
        
        return True, new_entry
    
    
    def InitializeButtons(self):
        """Initialize the main program interaction buttons."""
        
        left_frame = Widgets.CreateFrame(self.b_frame)
        left_frame.pack(side='left', fill='both', expand='true')
        middle_frame = Widgets.CreateFrame(self.b_frame)
        middle_frame.pack(side='left', fill='both', expand='true')
        right_frame = Widgets.CreateFrame(self.b_frame)
        right_frame.pack(side='left', fill='both', expand='true')
        
        # Create a button to save the file and close the window
        finish_button = Widgets.CreateButton(left_frame,
                                             _text='Save\n& Finish',
                                             _cmd=self.SerializeDB,
                                             _height=5)
        finish_button.pack()
        
        # Create a button to refresh the widgets for the next question
        next_button = Widgets.CreateButton(middle_frame,
                                           _text='Next\nQuestion',
                                           _cmd=self.NextQuestion,
                                           _height=5)
        next_button.pack()
        
        # Create a button to add an additional answer box
        add_button = Widgets.CreateButton(right_frame,
                                          _text='Add\nAnswer Box',
                                          _cmd=self.AddAnswerBox,
                                          _height=5)
        add_button.pack()
    
    
    def InitializeWindow(self):
        """Initialize the 'Create Database File' window."""
        
        self.window = tk.Toplevel(self.root)
        
        height = 600
        width = 1300
        y = int((self.window.winfo_screenheight() / 2) - (height / 2))
        x = int((self.window.winfo_screenwidth() / 2) - (width / 2))
        self.window.geometry(f'{width}x{height}+{x}+{y}')
        self.window.resizable(False, False)
        self.window.title('New database file')
        
        self.main_frame = Widgets.CreateFrame(self.window)
        self.main_frame.pack(fill='both', expand='true')
        self.main_canvas = Widgets.CreateCanvas(self.main_frame)
        self.main_canvas.pack(fill='both', expand='true')
        
        white = '#f8f8ff'
        
        # Create a window to hold the question widgets
        self.main_canvas.create_rectangle(5, 5, 635, 480, fill=white)
        self.q_frame = Widgets.CreateFrame(self.main_canvas)
        self.main_canvas.create_window(7, 7, anchor='nw', height=473,
                                       width=628, window=self.q_frame)
        self.CreateQuestion()
        
        # Create a window to hold the buttons
        self.main_canvas.create_rectangle(5, 490, 635, 585, fill=white)
        self.b_frame = Widgets.CreateFrame(self.main_canvas)
        self.main_canvas.create_window(7, 492, anchor='nw', height=93,
                                       width=628, window=self.b_frame)
        self.InitializeButtons()
        
        # Create a window to hold the answer widgets
        self.main_canvas.create_rectangle(655, 5, 1285, 585, fill=white)
        self.a_frame = Widgets.CreateFrame(self.main_canvas)
        self.main_canvas.create_window(657, 7, anchor='nw', height=578,
                                       width=628, window=self.a_frame)
        self.CreateAnswers()
        
        # Bind the 'Tab' button to cycle through text entry widgets
        self.window.bind_class('Text', '<Tab>',
                               lambda e: e.widget.tk_focusNext().focus())
    
    
    def NextQuestion(self):
        """Verify widget contents and refresh them to their initial state.
        
        This function is called by the 'Next Question' button.
        """
        
        # Validate the widget contents and construct a new quiz entry
        result, entry = self.CreateQuizEntry()
        if not result:
            return
        self.file_data.append(entry)
        ask = tk.messagebox.askyesno('Continue?',
                                     'Reset fields for a new question?',
                                     parent=self.window)
        if not ask:
            self.SerializeDB()
            return
        
        # Reset the screen for a new question
        self.question_num += 1
        self.q_lframe['text'] = 'Question ' + str(self.question_num)
        self.q_text.delete('1.0', 'end')
        self.q_text.insert('1.0', self.init_q_text)
        self.ans_canvas.forget()
        self.CreateAnswers()

    
    def SerializeDB(self):
        file = tk.filedialog.asksaveasfilename(defaultextension='.json',
                                    filetypes=[('JSON', '*.json')],
                                    initialdir='./database',
                                    title='Save database file as...',
                                    parent=self.window)
        if not file:
            return
        
        try:
            with open(file, 'w') as outfile:
                json.dump(self.file_data, outfile, indent=4)
                outfile.truncate()
        except IOError:
            msg = f'Unable to create the {os.path.basename(file)} file.'
            tk.messagebox.showerror('Error', msg, parent=self.window)
            return
        
        tk.messagebox.showinfo('Success',
                               f'{os.path.basename(file)} created.',
                               parent=self.window)
        
        # Add the file to the files list and listbox and exit the window
        self.listbox.insert('end', os.path.basename(file))
        self.user_files.append(file)
        self.window.destroy()