#-----------------------------------------------------------------------------#
#   File:   Main.py                                                           #
#   Author: Logan Pierceall                                                   #
#                                                                             #
#   This module creates the main program window. This window allows a user to #
#       add quiz database files to a listbox in order to load them into a     #
#       quiz. The quiz window logic can be found in QuizWindow.py. Users are  #
#       also able to create a new quiz database file using an interactive     #
#       template window. That window's code is found in CreateDBWindow.py.    #
#                                                                             #
#   The supporting backend code for this module can be found in MainLogic.py  #
#-----------------------------------------------------------------------------#

import os
import tkinter as tk
from tkinter import messagebox
from tkinter import Tk

import CreateDBWindow
import LogInWindow
import MainLogic
import QuizWindow
import Widgets



class MainWindow():

    def __init__(self, root_window, username, login_date):
    
        self.root         = root_window
        self.current_user = username
        
        # 'login_date' contains the last recorded log-in date for the user. If
        #   they've never logged in prior, the argument will be an empty string
        if not login_date:
            self.last_login = 'Never!'
        else:
            self.last_login = login_date
        
        # Widget option constants
        self.BUT_HEIGHT = 3
        self.BUT_WIDTH  = 30
        self.WHITE      = '#f8f8ff'
        
        self.CreateWindow()
    
    
    
    # AddFile() is called by the 'Add New File' button. It calls
    #   AddQuizFile() function in MainLogic.py, which allows a user to select
    #   a new file to add to the listbox widget
    # Args:     none
    # Returns:  none
    def AddFile(self):
    
        # If 'result' is False, 'msg' contains an error message
        result, msg = MainLogic.AddQuizFile(self.listbox, self.current_user)
        if not result:
            tk.messagebox.showerror('Error', msg)
    
    
    
    def BindMouseWheel(self, event):
    
        self.listbox.bind_all('<MouseWheel>', self.MouseWheelScroll)
    
    
    
    # CreateDBFile() is called by the 'Create New Database File' button. It
    #   calls the CreateDBWindow() function in CreateDBWindow.py, which
    #   allows a user to use a template to create a new quiz database
    # Args:     none
    # Returns:  none
    def CreateDBFile(self):
    
        CreateDBWindow.CreateDBWindow(self.root, self.current_user,
                                      self.listbox)
    
    
    
    # CreateFilesButtons() initializes the two buttons used to interact with
    #   the listbox widget. These allow a user to add a new file to the listbox
    #   or remove an existing file from the listbox
    # Args:     none
    # Returns:  none
    def CreateFilesButtons(self):
    
        # Window coordinates
        topx = 5
        topy = 460
        botx = 445
        boty = 570
    
        # Create a rectangle to hold listbox interaction buttons
        self.main_canvas.create_rectangle(topx, topy, botx, boty,
                                          fill = self.WHITE)
    
        # Create a frame within the given rectangle
        buttons_frame = Widgets.CreateFrame(self.main_canvas)
        self.main_canvas.create_window(topx + 2, topy + 2, anchor = 'nw',
                                       height = boty - topy - 2,
                                       width = botx - topx - 2,
                                       window = buttons_frame)
        
        # Create a button to add files to the listbox
        add_button = Widgets.CreateButton(buttons_frame, 'Add\nNew File',
                                          self.AddFile, self.BUT_HEIGHT)
        add_button.pack(side = 'left', expand = 'true')
        
        # Create a button to remove a file from the listbox
        remove_button = Widgets.CreateButton(buttons_frame,
                                             'Remove\n Selected File(s)',
                                             self.RemoveFile, self.BUT_HEIGHT)
        remove_button.pack(side = 'right', expand = 'true')
    
    
    
    # CreateFilesListbox() initializes the listbox widget that holds the quiz
    #   database files that the user has previously opened.
    # Args:     none
    # Returns:  none     
    def CreateFilesListbox(self):
    
        # Window coordinates
        topx = topy = 5
        botx = boty = 445
    
        # Create a rectangle to hold the listbox
        self.main_canvas.create_rectangle(topx, topy, botx, boty,
                                          fill = self.WHITE)
        
        # Create a frame within that rectangle
        listbox_frame = Widgets.CreateFrame(self.main_canvas)
        self.main_canvas.create_window(topx + 2, topy + 2, anchor = 'nw',
                                       height = boty - topy - 2,
                                       width = botx - topx - 2,
                                       window = listbox_frame)
        
        # Create a labelframe for the listbox
        labelframe = Widgets.CreateLabelFrame(listbox_frame, 'Select Files')
        labelframe.pack(fill = 'both', expand = 'true')
        
        # Create the listbox and a scrollbar
        self.scrollbar = Widgets.CreateScrollbar(labelframe)
        self.listbox = Widgets.CreateListbox(labelframe, self.scrollbar)
        self.scrollbar.config(command = self.listbox.yview,
                              scrollregion = self.listbox.bbox('end'))
        
        self.scrollbar.pack(side = 'right', fill = 'y')
        self.listbox.pack(fill = 'both', expand = 'true')
        
        # Bind the mouse wheel to scroll the scrollbar whenever the mouse is
        #   within the listbox boundaries
        self.listbox.bind('<Enter>', self.BindMouseWheel)
        self.listbox.bind('<Leave>', self.UnbindMouseWheel)
    
    
    
    # CreateMainButtons() initializes a button that allows a user to load
    #   quiz database files and launch a quiz and a button that allows a user
    #   to create a new quiz database file
    # Args:     none
    # Returns:  none
    def CreateMainButtons(self):
    
        # Window coordinates
        topx = 455
        topy = 267
        botx = 885
        boty = 492
    
        # Create a rectangle to hold the main buttons
        self.main_canvas.create_rectangle(topx, topy, botx, boty,
                                          fill = self.WHITE)
    
        # Create a frame within the given rectangle
        buttons_frame = Widgets.CreateFrame(self.main_canvas)
        self.main_canvas.create_window(topx + 2, topy + 2, anchor = 'nw',
                                       height = boty - topy - 2,
                                       width = botx - topx - 2,
                                       window = buttons_frame)
        
        # Create a button to load selections and launch the quiz
        launch_button = Widgets.CreateButton(buttons_frame,
                                             'Load Files & Launch Quiz',
                                             self.LaunchQuiz,
                                             self.BUT_HEIGHT,
                                             self.BUT_WIDTH)
        launch_button.pack(expand = 'true')
        
        # Create a button to create a new database file
        create_button = Widgets.CreateButton(buttons_frame,
                                             'Create New Database File',
                                             self.CreateDBFile,
                                             self.BUT_HEIGHT,
                                             self.BUT_WIDTH)
        create_button.pack(expand = 'true')
    
    
    
    # CreateWelcomeMessage() initializes a label that welcomes the user to the
    #   program and displays the last date that they logged in
    # Args:     none
    # Returns:  none
    def CreateWelcomeMessage(self):
    
        # Window coordinates
        topx = 455
        topy = 5
        botx = 885
        boty = 155
        
        # Create a rectangle to hold the welcome message
        self.main_canvas.create_rectangle(topx, topy, botx, boty,
                                          fill = self.WHITE)
    
        # Create a frame within the given rectangle
        welcome_frame = Widgets.CreateFrame(self.main_canvas)
        self.main_canvas.create_window(topx + 2, topy + 2, anchor = 'nw',
                                       height = boty - topy - 2,
                                       width = botx - topx - 2,
                                       window = welcome_frame)
        
        welcome_str = f'\n\nWelcome, {self.current_user}!\n\n' \
                      f'Last Seen {self.last_login}'
        welcome_label = Widgets.CreateLabel(welcome_frame, welcome_str)
        welcome_label.pack(fill = 'both', expand = 'true')
    
    
    
    # CreateWindow() initializes a main frame and canvas that cover the entire
    #   window. The function also calls the functions responsible for
    #   populating the window with widgets
    # Args:     none
    # Returns:  none
    def CreateWindow(self):
    
        self.main_frame = Widgets.CreateFrame(self.root)
        self.main_frame.pack(fill = 'both', expand = 'true')
        
        self.main_canvas = Widgets.CreateCanvas(self.main_frame)
        self.main_canvas.pack(fill = 'both', expand = 'true')
        
        # Create and populate the listbox
        self.CreateFilesListbox()
        self.PopulateListbox()
        
        # Create the listbox interaction buttons
        self.CreateFilesButtons()
        
        # Create the welcome message
        self.CreateWelcomeMessage()
        
        # Create the main program buttons
        self.CreateMainButtons()
    
    
    
    # LaunchQuiz() is called by the 'Load Files & Launch Quiz' button. This
    #   function retrieves the files selected in the listbox widget and passes
    #   those selections to the LoadQuiz() function in MainLogic.py
    # Args:     none
    # Returns:  none
    def LaunchQuiz(self):
    
        selections = self.listbox.curselection()
        
        if selections:
            # 'result' will indicate success status, 'msg' will contain an error
            #   message if applicable, 'quiz' holds the loaded quiz list
            result, msg, quiz = MainLogic.LoadQuiz(selections,
                                                   self.current_user)
            if result:
                QuizWindow.QuizWindow(self.root, quiz)
            else:
                tk.messagebox.showerror('Error', msg)
                
        # Throw error if no files were selected
        else:
            tk.messagebox.showerror('Error', 'No files selected!')
    
    
    
    def MouseWheelScroll(self, event):
    
        self.listbox.yview_scroll(int(-1 * (event.delta / 120)), 'units')
    
    
    
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
    #   removes it from the user's previously opened files.
    # Args:     none
    # Returns:  none
    def RemoveFile(self):
    
        selections = self.listbox.curselection()
        
        if not selections:
            # No files have been selected, cancel operation
            tk.messagebox.showerror('Error', 'Select one or more files first')
            return
        
        files_list = []
        for item in selections:
            # Retrieve the full pathname for the file chosen
            result, file = MainLogic.GetFilename(item, self.current_user)
            
            if result:
                files_list.append(file)
            else:
                # If the operation failed, 'file' contains the error message
                tk.messagebox.showerror('Error', file)
        
        # Remove the chosen files from the user's file list
        result, msg = MainLogic.RemoveFile(files_list, self.current_user)
        if not result:
            tk.messagebox.showerror('Error', msg)
            return
        
        # Rebuild the listbox
        self.listbox.delete(0, 'end')
        self.PopulateListbox()
    
    
    
    def UnbindMouseWheel(self, event):
    
        self.listbox.unbind_all('<MouseWheel>')