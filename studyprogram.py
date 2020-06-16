import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

import createfile
import quizlist
import takequiz

class QuizApp:

    def __init__(self):

        # Initialize QuizList object that will hold all quiz entries
        self.__quiz = quizlist.QuizList()

        # File that holds the list of previously seen quiz files
        self.__quizzes_file = 'openedfiles.txt'

        # String to hold the filename used to store missed questions (if desired by user)
        self.__missed_questions_file = ''

        # Initialize main program interface and position it in the middle of the screen
        self.__root = tk.Tk()
        self.__root.title('Study Program')
        __root_height = 235
        __root_width = 375
        self.__screen_width = self.__root.winfo_screenwidth()
        self.__screen_height = self.__root.winfo_screenheight()
        __x_pos = int((self.__screen_width / 2) - (__root_width / 2))
        __y_pos = int((self.__screen_height / 2) - (__root_height / 2))
        self.__root.geometry(f'{__root_width}x{__root_height}+{__x_pos}+{__y_pos}')

        # Load the program's interface objects
        self.create_file_list()
        self.create_buttons()
        self.create_help()
        self.create_menu()
        self.grid_items()

        self.__root.mainloop()



    def create_file_list(self):

        # Create a listbox to show all files that have been opened in prior instances for user ease
        #   in loading into a new quiz
        self.__listbox_frame = tk.LabelFrame(self.__root,
                                             text = 'Previously loaded files',
                                             padx = 5,
                                             pady = 5)
        self.__listbox = tk.Listbox(self.__listbox_frame,
                                    selectmode = 'EXTENDED',
                                    height = 12)

        # A list containing all files that have been loaded into the program in order to add them to
        #   the list box and to later load them into the quiz
        self.__opened_files = []

        # Try to open the file holding the list of previously opened list files. If unsuccuessful,
        #   assume no files have been opened previously and create an empty list box. Otherwise,
        #   populate the list box with those previously seen files
        try:
            # Lines in the file will have an abridged name to be displayed in the list box, followed
            #   by their absolute pathname for program use in the next line
            with open(self.__quizzes_file) as __file:
                for __line1 in __file:
                    if __line1 == '\n':
                        # If the line is blank but exists, skip processing
                        pass
                    else:
                        __line2 = next(__file)
                        __temp_obj = [__line1.rstrip(), __line2.rstrip()]
                        self.__opened_files.append(__temp_obj)

            for __item in self.__opened_files:
                self.__listbox.insert('end', __item[0])

        except IOError:
            pass



    # create_buttons() creates the buttons to add new files to the file list, load selected files
    #   into a quiz, take a quiz over the loaded questions, and create a new quiz file
    def create_buttons(self):

        self.__button_frame = tk.Frame(self.__root,
                                       padx = 5,
                                       pady = 5)
        self.__new_file_btn = tk.Button(self.__button_frame,
                                        text = 'Add new file \nto list',
                                        command = self.open_file)
        self.__load_files_btn = tk.Button(self.__button_frame,
                                           text = 'Load selected files',
                                           command = self.populate_quiz)
        self.__take_quiz_btn = tk.Button(self.__button_frame,
                                         text = 'Take quiz',
                                         command = self.take_quiz)
        self.__create_file_btn = tk.Button(self.__button_frame,
                                           text = 'Create new \ndatabase file',
                                           command = self.create_file)



    # create_help() creates a help frame explaining the functionality of the program's buttons
    def create_help(self):

        self.__help_frame = tk.LabelFrame(self.__root,
                                          text = 'Help',
                                          pady = 2)
        self.__new_file_lbl = tk.Label(self.__help_frame,
                                       text = 'Add: adds a file to the list')
        self.__load_file_lbl = tk.Label(self.__help_frame,
                                        text = 'Load: create a quiz from selected files')
        self.__take_quiz_lbl = tk.Label(self.__help_frame,
                                        text = 'Take: take quiz after loading')
        self.__create_file_lbl = tk.Label(self.__help_frame,
                                          text = 'Create: use form to create new quiz file')



    # create_menu() is used to create a menu bar
    def create_menu(self):

        self.__menubar = tk.Menu(self.__root)

        # Creates the menu holding basic program functions
        self.__filemenu = tk.Menu(self.__menubar,
                                  tearoff = 0)
        self.__filemenu.add_command(label = 'Add quiz file',
                                    command = self.open_file)
        self.__filemenu.add_command(label = 'Create new quiz file',
                                    command = self.create_file)
        self.__filemenu.add_command(label = 'Take quiz',
                                    command = self.take_quiz)
        self.__filemenu.add_separator()
        self.__filemenu.add_command(label = 'Clear loaded questions',
                                    command = self.clear_quiz)
        self.__filemenu.add_command(label = 'Exit',
                                    command = self.exit)
        self.__menubar.add_cascade(label = 'File',
                                   menu = self.__filemenu)



    # grid_items() collects all of the object placement calls in one central place for convenience
    def grid_items(self):
        
        self.__listbox_frame.grid(row = 0, column = 0, rowspan = 6)
        self.__listbox.grid(row = 0, column = 0)

        self.__button_frame.grid(row = 0, column = 1, rowspan = 2, pady = 3)
        self.__new_file_btn.grid(row = 0, column = 1, sticky = 'nsew')
        self.__load_files_btn.grid(row = 0, column = 2, sticky = 'nsew')
        self.__take_quiz_btn.grid(row = 1, column = 1, sticky = 'nsew')
        self.__create_file_btn.grid(row = 1, column = 2, sticky = 'nsew')

        self.__help_frame.grid(row = 2, column = 1, rowspan = 4, padx = 5)
        self.__new_file_lbl.grid(row = 0, sticky = 'w')
        self.__load_file_lbl.grid(row = 1, sticky = 'w')
        self.__take_quiz_lbl.grid(row = 2, sticky = 'w')
        self.__create_file_lbl.grid(row = 3, sticky = 'w')

        self.__root.config(menu = self.__menubar)



    def create_file(self):

        __filename = filedialog.asksaveasfilename(title = 'Save As...',
                                                  defaultextension = '.txt')
        
        # If a file was created, initialize the window to populate that file
        if __filename != '':
            createfile.CreateFile(__filename, self.__root,
                                  self.__screen_width, self.__screen_height)



    # open_file() is used to add a new file to the list of previously seen quiz database files
    def open_file(self):

        __filename = filedialog.askopenfilename(title = 'Select file',
                                                filetypes = (('Text Files', '*.txt'), ('All Files', '*.*')))

        # If a file was chosen, add it to the list file, the listbox entries, and to
        #   the open_files list
        if __filename != '':
            # Retrieve the filename without directories for display purposes
            __f_shortened = os.path.basename(__filename)
            __temp_obj = [__f_shortened, __filename]

            self.__listbox.insert('end', __f_shortened)
            self.__opened_files.append(__temp_obj)

            with open(self.__quizzes_file, 'a') as f:
                f.write('\n' + __f_shortened + '\n')
                f.write(__filename)


    # populate_quiz() is used to fill the quiz list with entries built out of the selected quiz files
    def populate_quiz(self):

        # Retrieve the list of indeces and load the corresponding file stored in the second entry of
        #   the opened_files list
        __selected_items = self.__listbox.curselection()
        for __index in __selected_items:
            self.__quiz.populate_quizlist(self.__opened_files[__index][1])



    # take_quiz() loads the takequiz module to quiz the user over questions loaded from files
    def take_quiz(self):

        # If no files have been loaded, inform the user. Otherwise initiate the quiz
        if self.__quiz.get_length() == 0:
            tk.messagebox.showerror('ERROR', 'No files loaded yet!')
        else:
            takequiz.Quiz(self.__quiz, self.__root,
                          self.__screen_width, self.__screen_height)



    # clear_quiz() deletes all of the contents of the quiz list
    def clear_quiz(self):

        if self.__quiz.clear_entries():
            tk.messagebox.showinfo('Success!', 'Quiz entries cleared.')
        else:
            tk.messagebox.showerror('ERROR', 'Error deleting entries.')



    # exit() contains all of the cleanup utilities to properly exit the program
    def exit(self):

        # PLANS: If create file or quiz window open, ask again to exit to be safe

        self.__root.quit()



if __name__ == '__main__':
    QuizApp()
