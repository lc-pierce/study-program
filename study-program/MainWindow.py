#-----------------------------------------------------------------------------#
#   File:   Main.py                                                           #
#   Author: Logan Pierceall                                                   #
#   Date:   March 8, 2022                                                     #
#-----------------------------------------------------------------------------#

import os
import tkinter as tk
from tkinter import messagebox
from tkinter import Tk

import CreateDBWindow
import LogInWindow
import MainLogic
import QuizList
import QuizWindow
import WidgetCreation



class MainWindow(Tk):

    def __init__(self, username, login_date, *args, **kwargs):
    
        super().__init__(*args, **kwargs)
        
        # 'current_user' is used to create a custom welcome screen and to load
        #   a user-specific list of database files into a listbox widget
        self.current_user = username
        
        # 'login_date' contains the last recorded log-in date for the user. If
        #   they've never logged in prior, the argument will be an empty string
        if login_date == '':
            self.last_login = 'Never!'
        else:
            self.last_login = login_date
        
        self.WIN_HEIGHT = 600           # Window height
        self.WIN_WIDTH = 900            # Window width
        
        self.CreateWindow()
    
    
    
    # AddFile() is called by the 'Add file to the list' button. It calls the
    #   AddQuizFile() function in MainLogic.py, which allows a user to select
    #   a new file to add to the listbox widget
    # Args:     none
    # Returns:  none
    def AddFile(self, *args):
    
        # 'result' will indicate success status, 'msg' will contain an error
        #   message if applicable
        result, msg = MainLogic.AddQuizFile(self.listbox, self.current_user)
        if not result:
            tk.messagebox.showerror('Error', msg)
    
    
    
    # CreateDBFile() is called by the 'Create new database file' button. It
    #   calls the CreateDBWindow() function in CreateDBWindow.py, which
    #   allows a user to create a new quiz database file
    # Args:     none
    # Returns:  none
    def CreateDBFile(self, *args):
    
        CreateDBWindow.CreateDBWindow(self.current_user)
    
    
    
    # CreateFrames() initalizes the following widgets:
    #   Frames to hold the listbox and accompanying button
    #   Frames to hold a welcome label and several function buttons
    # Args:     none
    # Returns:  none
    def CreateFrames(self):
        
        self.left_frame = WidgetCreation.CreateFrame(self)
        self.left_frame.pack(side = 'left', fill = 'both', expand = 'true')
        
        self.right_frame = WidgetCreation.CreateFrame(self)
        self.right_frame.pack(side = 'right', fill = 'both', expand = 'true')
        
        # Create frames to hold the listbox and associated button
        self.listbox_frame = WidgetCreation.CreateLabelFrame(self.left_frame,
                                            'Select files to load...')
        self.listbox_frame.pack(side = 'top', fill = 'both', expand = 'true')
        
        self.add_button_frame = WidgetCreation.CreateFrame(self.left_frame)
        self.add_button_frame.pack(side = 'bottom', fill = 'x')
        
        # Create frames to separate the labels and buttons on the right side
        #   of the screen
        self.labels_frame = WidgetCreation.CreateFrame(self.right_frame)
        self.labels_frame.pack(fill = 'both', expand = 'true')
        
        self.buttons_frame = WidgetCreation.CreateFrame(self.right_frame)
        self.buttons_frame.pack(fill = 'both', expand = 'true')
    
    
    
    # CreateInteractiveSide() initalizes the following widgets: 
    #   A welcome label
    #   A button that loads the selected listbox files into a quiz and launches
    #       that quiz
    #   A button that launches a new window to create a new quiz database file
    #   A button to remove a selected file from the listbox
    # Args:     none
    # Returns:  none
    def CreateInteractiveSide(self):
    
        # Create a welcome label displaying the username and last log-in date
        welcome_str = f'\nWelcome, {self.current_user}!\n' \
                      f'Last log-in: {self.last_login}'
        welcome_label = WidgetCreation.CreateLabel(self.labels_frame,
                                                   welcome_str)
        welcome_label.pack(fill = 'both', expand = 'true')
    
        # Create a button to load selected files and launch the quiz
        launch_button = WidgetCreation.CreateButton(self.buttons_frame,
                                                    'Load files & launch quiz',
                                                    self.LaunchQuiz)
        launch_button.pack(fill = 'x')
        
        # Create a button to create a new database file
        new_db_file_button = WidgetCreation.CreateButton(self.buttons_frame,
                                                         'Create new database file',
                                                         self.CreateDBFile)
        new_db_file_button.pack(fill = 'x')
        
        # Create a button to remove a file from the listbox
        remove_file_button = WidgetCreation.CreateButton(self.buttons_frame,
                                                         'Remove selected file(s)',
                                                         self.RemoveFile)
        remove_file_button.pack(fill = 'x')
    
    
    
    # CreateListboxSide() initializes the listbox widget, which contains a list
    #   of files previously opened by the current user, and a button to add
    #   new files to the list
    # Args:     none
    # Returns:  none
    def CreateListboxSide(self):
    
        # Create the listbox widget and a scrollbar to attach to it
        scrollbar = tk.Scrollbar(self.listbox_frame, orient = 'vertical')
        self.listbox = WidgetCreation.CreateListbox(self.listbox_frame,
                                                    scrollbar)
        scrollbar.config(command = self.listbox.yview)
        
        scrollbar.pack(side = 'right', fill = 'y')
        self.listbox.pack(fill = 'both', expand = 'true')
        
        # Create a button to add a file to the listbox
        add_file_button = WidgetCreation.CreateButton(self.add_button_frame,
                                                      'Add a file to the list',
                                                      self.AddFile)
        add_file_button.pack(side = 'bottom', fill = 'x', expand = 'true')
    
    
    
    # CreateWindow() initializes the Main Window
    # Args:     none
    # Returns:  none
    def CreateWindow(self):
        
        # Obtain x&y coordinates to place window in center of screen
        y_pos = int((self.winfo_screenheight() / 2) - (self.WIN_HEIGHT / 2))
        x_pos = int((self.winfo_screenwidth() / 2) - (self.WIN_WIDTH / 2))
        
        # Title and size the main window
        self.title("Study Program")
        self.geometry(f'{self.WIN_WIDTH}x{self.WIN_HEIGHT}+{x_pos}+{y_pos}')
        self.resizable(False, False)
        
        # Create the window frames
        self.CreateFrames()
        
        # Create the Listbox widget and accompanying button
        self.CreateListboxSide()
        
        # Create a welcome label and the interactive buttons
        self.CreateInteractiveSide()
        
        # Load the previously opened database files into the listbox
        self.PopulateListbox()
    
    
    
    # LaunchQuiz() is called by the 'Load selections and launch quiz' button.
    #   It retrieves the files selected in the Listbox widget and passes those
    #   selections to the LoadQuiz() function in MainLogic.py. That function is
    #   used to initalize the quiz window
    # Args:     none
    # Returns:  none
    def LaunchQuiz(self, *args):
    
        selections = self.listbox.curselection()
        
        if selections:
            # 'result' will indicate success status, 'msg' will contain an error
            #   message if applicable, 'quiz' holds the loaded quiz list
            result, msg, quiz = MainLogic.LoadQuiz(selections,
                                                   self.current_user)
            
            if result:
                QuizWindow.QuizWindow(quiz, self)
            else:
                tk.messagebox.showerror('Error', msg)
                
        # Throw error if no files were selected
        else:
            tk.messagebox.showerror('Error', 'No files selected!')
    
    
    
    # PopulateListbox() calls the PopulateListbox() function in MainLogic.py.
    #   That function opens a JSON file containing the previously loaded quiz
    #   files for all users and loads the files specific to the current user
    #   into the listbox widget
    # Args:     none
    # Returns:  none
    def PopulateListbox(self):
    
        # If 'result' is False, 'msg' will contain an error message
        result, msg = MainLogic.PopulateListbox(self.current_user,
                                                self.listbox)
        
        if not result:
            tk.messagebox.showerror('Error', msg)
    
    
    
    # RemoveFile() retrieves the currently selected file(s) in the listbox and
    #   removes it from the user's previously opened files. The listbox is then
    #   repopulated
    # Args:     none
    # Returns:  none
    def RemoveFile(self):
    
        selections = self.listbox.curselection()
        
        if selections:
            # Build a list of the filenames:
            files_list = []
            for choice in selections:
                result, file = MainLogic.GetFilename(choice, self.current_user)
                if result:
                    files_list.append(file)
                # If the previously opened files file couldn't be accessed,
                #   'result' will be false and 'file' will contain an error
                #   message
                else:
                    tk.messagebox.showerror('Error', file)
                    return
                
            # Prompt the user for confirmation before removing each file
            for file in files_list:
                ask_text = f'Remove {os.path.basename(file)}?'
                ask = tk.messagebox.askyesno('Remove file?', ask_text)
                
                if ask:
                    result, msg = MainLogic.RemoveFile(file, self.current_user)
                    if not result:
                        tk.messagebox.showerror('Error', msg)
        
            # Rebuild the listbox
            self.listbox.delete(0, 'end')
            self.PopulateListbox()
        
        else:
            tk.messagebox.showerror('Error', 'Select one or more files first')