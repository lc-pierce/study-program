import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

import createfile
import quizlist
import takequiz

class QuizApp:

    def __init__ (self):
    
        self.__quiz = quizlist.QuizList()
        
        self.__opened_quiz_files = 'openedfiles.txt'
        self.__opened_files = []
        
        self.__bg_color = 'PaleTurquoise2'
        self.__font_color = 'grey1'
        self.__font = 'georgia'
        
        # Call member functions to create and populate the program window
        self.create_main_window()
        self.create_layout_frames()
        self.create_file_list()
        self.create_action_buttons()
        self.__main_window.mainloop()
        
        
     
    def create_main_window (self):
    
        self.__main_window = tk.Tk()
        self.__main_window.title('Study Program')
        
        self.__main_height = 500
        self.__main_width = 800
        self.__screen_height = self.__main_window.winfo_screenheight()
        self.__screen_width = self.__main_window.winfo_screenwidth()
        self.__y_pos = int((self.__screen_height / 2) - (self.__main_height / 2))
        self.__x_pos = int((self.__screen_width / 2) - (self.__main_width / 2))
        self.__main_window.geometry(f'{self.__main_width}x{self.__main_height}+{self.__x_pos}+{self.__y_pos}')
    


    # Creates all of the frames to be used later by objects
    def create_layout_frames (self):

        # Frames for the listbox and associated buttons objects area
        self.__listbox_buttons_frame = tk.Frame(self.__main_window,
                                                padx = 5,
                                                pady = 5,
                                                bg = self.__bg_color)
        self.__listbox_frame = tk.Frame(self.__listbox_buttons_frame,
                                        padx = 5,
                                        pady = 5,
                                        bg = self.__bg_color)
        self.__listbox_labelframe = tk.LabelFrame(self.__listbox_frame,
                                                  text = 'SELECT FILES TO LOAD',
                                                  padx = 5,
                                                  pady = 5,
                                                  bd = 1,
                                                  relief = 'sunken',
                                                  font = (self.__font, 15, 'bold'),
                                                  bg = self.__bg_color,
                                                  fg = self.__font_color)
        self.__top_buttons_frame = tk.Frame(self.__listbox_buttons_frame,
                                            padx = 5,
                                            pady = 5,
                                            bg = self.__bg_color)
        
        # Frames for the action button objects area
        self.__action_buttons_frame = tk.Frame(self.__main_window,
                                               padx = 5,
                                               pady = 5,
                                               bg = self.__bg_color)
        
        # Pack the frames
        self.__listbox_buttons_frame.pack(side = 'top', fill = 'both', expand = 'true')
        self.__action_buttons_frame.pack(side = 'bottom', fill = 'both', expand = 'true')
        
        self.__listbox_frame.pack(side = 'left', fill = 'both', expand = 'true')
        self.__top_buttons_frame.pack(side = 'right', fill = 'both', expand = 'true')
        
        self.__listbox_labelframe.pack(fill = 'both', expand = 'true')
    
    
    
    # Creates a listbox containing all database files previously loaded into a quiz along with the
    #   buttons used to add a new file to the list, load the chosen files into a quiz, and clear
    #   any loaded files from the quiz
    def create_file_list (self):
    
        # Create the listbox object and a scrollbar
        self.__file_scrollbar = tk.Scrollbar(self.__listbox_labelframe,
                                             orient= 'vertical')
        self.__file_listbox = tk.Listbox(self.__listbox_labelframe,
                                         selectmode = 'multiple',
                                         yscrollcommand = self.__file_scrollbar.set,
                                         activestyle = 'dotbox',
                                         font = (self.__font, 13),
                                         bg = 'ghost white')
        self.__file_scrollbar.config(command = self.__file_listbox.yview)
        self.__file_scrollbar.pack(side = 'right', fill = 'y')
        self.__file_listbox.pack(fill = 'both', expand = 'true')
        
        # Populate the listbox
        try:
            with open(self.__opened_quiz_files) as __file:
                for __line in __file:
                    if __line == '\n' or __line == '':
                        pass
                    else:
                        self.__opened_files.append(__line.rstrip())
            
            for __item in self.__opened_files:
                self.__file_listbox.insert('end', os.path.basename(__item))
                
        except IOError:
            __f = open(self.__opened_quiz_files, 'a+')
            __f.close()
        
        # Create the listbox interactive buttons
        self.__add_file_button = tk.Button(self.__top_buttons_frame,
                                           text = 'Add A File To The List',
                                           command = self.add_file,
                                           font = (self.__font, 12, 'bold'),
                                           bd = 0,
                                           bg = self.__bg_color,
                                           activebackground = self.__bg_color,
                                           fg = self.__font_color)
        self.__load_files_button = tk.Button(self.__top_buttons_frame,
                                             text = 'Load Selections From List',
                                             command = self.load_files,
                                             font = (self.__font, 12, 'bold'),
                                             bd = 0,
                                             bg = self.__bg_color,
                                             activebackground = self.__bg_color,
                                             fg = self.__font_color)
        self.__empty_quiz_button = tk.Button(self.__top_buttons_frame,
                                             text = 'Clear Loaded Files From Quiz',
                                             command = self.empty_quiz,
                                             font = (self.__font, 12, 'bold'),
                                             bd = 0,
                                             bg = self.__bg_color,
                                             activebackground = self.__bg_color,
                                             fg = self.__font_color)
        self.__add_file_button.pack(side = 'top', expand = 'true', fill = 'both')
        self.__load_files_button.pack(side = 'top', expand = 'true', fill = 'both')
        self.__empty_quiz_button.pack(side = 'top', expand = 'true', fill = 'both')
    
    
    
    # Creates the buttons used to launch the quiz and to create a new database file
    def create_action_buttons (self):
    
        self.__take_quiz_button = tk.Button(self.__action_buttons_frame,
                                            text = 'Launch Quiz',
                                            command = self.launch_quiz,
                                            font = (self.__font, 18, 'bold'),
                                            height = 3,
                                            width = 9,
                                            bd = 0,
                                            bg = self.__bg_color,
                                            activebackground = self.__bg_color,
                                            fg = self.__font_color,
                                            disabledforeground = self.__font_color)
        self.__create_file_button = tk.Button(self.__action_buttons_frame,
                                              text = 'Create New \nDatabase File',
                                              command = self.create_file,
                                              font = (self.__font, 18, 'bold'),
                                              height = 3,
                                              width = 9,
                                              bd = 0,
                                              bg = self.__bg_color,
                                              activebackground = self.__bg_color,
                                              fg = self.__font_color,
                                              disabledforeground = self.__font_color)
        self.__take_quiz_button.pack(side = 'left', fill = 'both', expand = 'true')
        self.__create_file_button.pack(side = 'right', fill = 'both', expand = 'true')
    
    
    
    # Prompts the user to browse their computer for a new file to add to the listbox list
    def add_file (self):
        
        __file = filedialog.askopenfilename(title = 'Select file',
                                            filetypes = (('Text Files', '*.txt'),
                                                         ('All Files', '*.*')))
        if __file != '':
            
            # Add the opened file to the list of previously opened quiz files
            with open(self.__opened_quiz_files, 'a') as __f:
                __f.write(__file + '\n')
            
            # Add the file to the internal list of loaded files and add it to the listbox
            self.__opened_files.append(__file)
            __file = os.path.basename(__file)
            self.__file_listbox.insert('end', __file)
            
            # Notify the user the file was added to the quiz list
            tk.messagebox.showinfo('FILE ADDED',
                                   'Success! ' + __file + ' loaded into quiz.')
    
    
    
    # Launches the window used to create a new database file. See createfile.py for further information
    def create_file (self):
    
        __file = filedialog.asksaveasfilename(title = 'Save As...',
                                              defaultextension = '.txt')
        
        if __file != '':
        
            # If the file is being created for the first time, add the filename as the first line
            if not (os.path.isfile(__file) and os.path.getsize(__file) > 0):
                with open(__file, 'a+') as __f:
                    __f.write(f'FIL:{os.path.basename(__file)}\n')
        
            createfile.CreateFile(__file, self.__main_window,
                                  self.__screen_width, self.__screen_height)
    
    
    
    # Used by all other functions to easily create any needed error messages
    def display_error (self, message):
    
        tk.messagebox.showerror('ERROR', message)
    
    
    
    # Empties the internal quiz list of any previously loaded quiz entries
    def empty_quiz (self):
    
        self.__quiz.clear_entries()
    
    
    
    # Launches the window used to take a quiz. See takequiz.py for further information
    def launch_quiz (self):
    
        if self.__quiz.get_length() == 0:
            self.display_error('No quiz files loaded yet!')
        else:
            takequiz.Quiz(self.__quiz, self.__main_window,
                          self.__screen_width, self.__screen_height)
    
    
    
    # Pulls selections from the listbox and loads them into the quiz object
    def load_files (self):
    
        __loaded_str = ''
        __selection = self.__file_listbox.curselection()
        if __selection:
        
            # Load each file stored in opened files list and populate string containing filenames
            #   for confirmation message after operation
            for __index in __selection:
                __result = self.__quiz.populate_quizlist(self.__opened_files[__index])
                if __result:
                    __loaded_str += f'\t{os.path.basename(self.__opened_files[__index])}\n'
                else:
                    self.display_error(f'Error opening {os.path.basename(self.__opened_files[__index])}'
                                                     + ', operation aborted.')
                    self.__quiz.clear_entries()
                    break
            
            tk.messagebox.showinfo('SUCCESS!', 'Files successfully loaded:\n' + __loaded_str)
        else:
            self.display_error('No files selected!')



if __name__ == '__main__':
    QuizApp()