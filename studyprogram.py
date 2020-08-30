# ------------------------------------------------------------------------------------------------- #
# studyprogram.py is the main program interface. It creates the main program GUI, which provides    #
#   a list of database files, a help menu, and buttons allowing the user to add files to the list,  #
#   load files from the list into a quiz, take a quiz, or create a new database file.               #
#                                                                                                   #
# Author: Logan Pierceall                                                                           #
# Last revision date: August 10, 2020                                                               #
# ------------------------------------------------------------------------------------------------- #

import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

import createfile
import quizlist
import takequiz

class QuizApp:

    def __init__ (self):
    
        # quizlist is a structure used to store information pulled from the database files
        #   see quizlist.py for further documentation
        self.__quiz = quizlist.QuizList()
        
        # the .txt file stores file paths for database files that have been previously loaded into
        #   the program so that they may be placed into a listbox for convenient access
        self.__past_quiz_files = 'openedfiles.txt'
        
        self.__main_window = tk.Tk()
        self.__main_window.title('Study Program')
        self.__main_height = 500
        self.__main_width = 900
        self.__screen_height = self.__main_window.winfo_screenheight()
        self.__screen_width = self.__main_window.winfo_screenwidth()
        self.__y_pos = int((self.__screen_height / 2) - (self.__main_height / 2))
        self.__x_pos = int((self.__screen_width / 2) - (self.__main_width / 2))
        self.__main_window.geometry(f'{self.__main_width}x{self.__main_height}+{self.__x_pos}+{self.__y_pos}')
        
        # the following frames create the basic layout of the window and will be used as master frames
        #   for all other window frames and widgets
        self.__box_button_frame = tk.Frame(self.__main_window,
                                           padx = 5,
                                           pady = 5,
                                           bg = 'dodger blue')
        self.__listbox_labelframe = tk.LabelFrame(self.__box_button_frame,
                                                  text = 'SELECT FILES TO LOAD',
                                                  padx = 5,
                                                  pady = 5,
                                                  bd = 0,
                                                  font = ('times', 15, 'bold'),
                                                  bg = 'dodger blue',
                                                  fg = 'mint cream')
        self.__help_frame = tk.Frame(self.__main_window,
                                     padx = 5,
                                     pady = 5,
                                     bg = 'dodger blue')
        self.__buttons_frame = tk.Frame(self.__box_button_frame,
                                        padx = 5,
                                        pady = 5,
                                        bg = 'dodger blue')
        self.__help_labelframe = tk.LabelFrame(self.__help_frame,
                                               text = 'HELP',
                                               bd = 1,
                                               font = ('times', 15, 'bold'),
                                               bg = 'dodger blue',
                                               fg = 'mint cream')
    
        self.__box_button_frame.pack(side = 'top', fill = 'both', expand = 'true')
        self.__help_frame.pack(side = 'bottom', fill = 'both', expand = 'true')
        self.__listbox_labelframe.pack(side = 'left', fill = 'both', expand = 'true')
        self.__buttons_frame.pack(side = 'right', fill = 'both', expand = 'true')
        self.__help_labelframe.pack(fill = 'both', expand = 'true')
        
        self.create_file_list()     # create the listbox containing database files
        self.create_buttons()       # create the main interface functionality buttons
        self.create_help_menu()     # create a menu to explain button usage
        
        self.__main_window.mainloop()


    # create_file_list() opens the .txt file containing previously loaded database files and
    #   uses them to populate a listbox. Any additional files opened after the program is running
    #   will also be added to the list. These files can then be selected in order to load them
    #   into the quizlist object
    def create_file_list (self):
    
        self.__file_scrollbar = tk.Scrollbar(self.__listbox_labelframe,
                                             orient = 'vertical')
        self.__file_listbox = tk.Listbox(self.__listbox_labelframe,
                                         selectmode = 'multiple',
                                         yscrollcommand = self.__file_scrollbar.set,
                                         activestyle = 'dotbox',
                                         font = ('times', 13),
                                         bg = 'mint cream')
        self.__file_scrollbar.config(command = self.__file_listbox.yview)
        self.__file_scrollbar.pack(side = 'right', fill = 'y')
        self.__file_listbox.pack(fill = 'both', expand = 'true')
        
        self.__opened_files = []
        try:
            with open(self.__past_quiz_files) as __file:
                for __line in __file:
                    if __line == '\n':
                        pass
                    else:
                        self.__opened_files.append(__line.rstrip())
                        
            for __item in self.__opened_files:
                self.__file_listbox.insert('end', os.path.basename(__item))
                
        except IOError:
            tk.messagebox.showerror('ERROR!', f'{self.__past_quiz_files} was unable to be opened')


    # create_buttons() creates the four buttons used to execute the program. These buttons have the
    #   following functionality:
    #       add_file:    add a database file to the list of files used to create a quiz
    #       load_file:   load all of the files selected in the list into a quizlist object
    #       take_quiz:   launches the quiz window
    #       create_file: launches a form to create a new database file
    def create_buttons (self):
    
        self.__left_button_frame = tk.Frame(self.__buttons_frame)
        self.__right_button_frame = tk.Frame(self.__buttons_frame)
        self.__add_file_button = tk.Button(self.__left_button_frame,
                                           text = 'ADD\nFILE TO LIST',
                                           command = self.open_file,
                                           font = ('times', 18, 'bold'),
                                           height = 3, width = 9,
                                           bd = 0,
                                           bg = 'dodger blue',
                                           activebackground = 'dodger blue',
                                           fg = 'mint cream')
        self.__load_files_button = tk.Button(self.__left_button_frame,
                                             text = 'LOAD\nSELECTED FILES',
                                             command = self.load_files,
                                             font = ('times', 18, 'bold'),
                                             height = 3, width = 9,
                                             bd = 0,
                                             bg = 'dodger blue',
                                             activebackground = 'dodger blue',
                                             fg = 'mint cream')
        self.__take_quiz_button = tk.Button(self.__right_button_frame,
                                            text = 'BEGIN\nQUIZ',
                                            command = self.load_quiz,
                                            font = ('times', 18, 'bold'),
                                            height = 3, width = 9,
                                            bd = 0,
                                            bg = 'dodger blue',
                                            activebackground = 'dodger blue',
                                            fg = 'mint cream',
                                            disabledforeground = 'mint cream')
        self.__create_file_button = tk.Button(self.__right_button_frame,
                                              text = 'CREATE\nNEW FILE',
                                              command = self.create_file,
                                              font = ('times', 18, 'bold'),
                                              height = 3, width = 9,
                                              bd = 0,
                                              bg = 'dodger blue',
                                              activebackground = 'dodger blue',
                                              fg = 'mint cream')
                                              
        self.__left_button_frame.pack(side = 'left', fill = 'both', expand = 'true')
        self.__right_button_frame.pack(side = 'right', fill = 'both', expand = 'true')
        self.__load_files_button.pack(side = 'top', fill = 'both', expand = 'true')
        self.__add_file_button.pack(side = 'bottom', fill = 'both', expand = 'true')
        self.__take_quiz_button.pack(side = 'top', fill = 'both', expand = 'true')
        self.__create_file_button.pack(side = 'bottom', fill = 'both', expand = 'true')


    # create_help_menu() creates a small label field in the main GUI that provides further elaboration
    #   on button functionality for the user
    def create_help_menu (self):
    
        self.__add_file_label = tk.Label(self.__help_labelframe,
                                         text = 'ADD: adds a file to the list box so it can be used for a quiz',
                                         font = ('times', 16),
                                         bg = 'dodger blue',
                                         fg = 'mint cream')
        self.__load_file_label = tk.Label(self.__help_labelframe,
                                          text = 'LOAD: create a quiz based on the selected files in the list box',
                                          font = ('times', 16),
                                          bg = 'dodger blue',
                                          fg = 'mint cream')
        self.__begin_quiz_label = tk.Label(self.__help_labelframe,
                                           text = 'BEGIN: start the quiz (note: files must be loaded first)',
                                           font = ('times', 16),
                                           bg = 'dodger blue',
                                           fg = 'mint cream')
        self.__create_file_label = tk.Label(self.__help_labelframe,
                                            text = 'CREATE: launch a form to create a new quiz database file',
                                            font = ('times', 16),
                                            bg = 'dodger blue',
                                            fg = 'mint cream')
        
        self.__load_file_label.pack(anchor = 'w', pady = 10)
        self.__add_file_label.pack(anchor = 'w', pady = 10)
        self.__begin_quiz_label.pack(anchor = 'w', pady = 10)
        self.__create_file_label.pack(anchor = 'w', pady = 10)


    # open_file() is used by the add_file_button to add a new file to the listbox entries and to
    #   the .txt file containing previously seen database files
    def open_file (self):
    
        __filename = filedialog.askopenfilename(title = 'Select file',
                                                filetypes = (('Text Files', '*.txt'), ('All Files', '*.*')))
        if __filename != '':
            
            with open (self.__past_quiz_files, 'a') as __f:
                __f.write(__filename + '\n')
                
            self.__opened_files.append(__filename)
            __filename = os.path.basename(__filename)
            self.__file_listbox.insert('end', __filename)


    # load_files() is used by the load_files_button to populate a quizlist object using the database
    #   files selected in the listbox
    def load_files (self):
    
        __selected_files = self.__file_listbox.curselection()
        
        if __selected_files:
            for __index in __selected_files:
                if not self.__quiz.populate_quizlist(self.__opened_files[__index]):
                    tk.messagebox.showerror('ERROR',
                                            'Error opening ' + os.path.basename(self.__opened_files[__index])
                                            + ', operation aborted.')
                    self.__quiz.clear_entries()
                    break
                    
        else:
            tk.messagebox.showerror('ERROR', 'No files selected!')


    # load_quiz() is used by the take_quiz_button to create a Quiz object, which will create a
    #   new window for the user to take a quiz over all loaded files.
    #   see takequiz.py for further documentation
    def load_quiz (self):
    
        if self.__quiz.get_length() == 0:
            tk.messagebox.showerror('ERROR', 'No files loaded yet!')
        else:
            takequiz.Quiz(self.__quiz, self.__main_window,
                          self.__screen_width, self.__screen_height)


    # create_file() is used by the create_file_button to create a CreateFile object, which will
    #   create a new window containing a form to aid in creating new database files
    #   see createfile.py for further documentation
    def create_file (self):
    
        __filename = filedialog.asksaveasfilename(title = 'Save As...',
                                                  defaultextension = '.txt')
        if __filename != '':
            createfile.CreateFile(__filename, self.__main_window,
                                  self.__screen_width, self.__screen_height)
        


if __name__ == '__main__':
    QuizApp()