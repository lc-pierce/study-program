import json
from json.decoder import JSONDecodeError
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import Tk

import CreateDBWindow
import LogInWindow
import QuizWindow
import Widgets


class MainWindow():

    def __init__(self, root_window, username, login_date):
    
        self.root = root_window
        self.current_user = username
        self.last_login = login_date
        
        # Button height and width constants
        self.button_height = 3
        self.button_width = 30
        
        # Load the user files info
        self.DB_FILE = 'previousfiles.json'
        self.user_files = self.LoadDatabase()
        
        # Function to save user data if the window is exited
        self.root.protocol('WM_DELETE_WINDOW', self.OnClose)
        
        # Load the window and widgets
        self.InitializeWindow()
    
    
    def AddFile(self):
        """Add a new quiz file to the user's file list.
        
        This function is called by the 'Add New File' button.
        """
        
        new_file = filedialog.askopenfilename(title='Select a file...',
                                          filetypes=[('JSON Files', '*.json')])
        if not new_file:
            return
        
        # Verify the file isn't already in the user's list
        for file in self.user_files:
            if file == new_file:
                messagebox.showerror('Error', 'File already present.')
                return
        
        self.user_files.append(new_file)
        self.listbox.insert('end', os.path.basename(new_file))
    
    
    def CreateNewDatabaseFile(self):
        """Launch a window to create a new quiz database file.
        
        This function is called by the 'Create New Database File' button.
        """
        
        CreateDBWindow.CreateDBWindow(root_window=self.root,
                                      user_files=self.user_files,
                                      parent_listbox=self.listbox)
    
    
    def InitializeListbox(self, parent_frame):
    
        """Initialize the Listbox widget and populate it with quiz files.
        
        The Listbox widget holds a user's quiz database files. The files
            selected before launching the quiz will be used to populate the
            quiz. Once a file has been loaded once, it will be saved to the
            user's file list and automatically loaded into the Listbox on
            subsequent logins.
        
        Arguments:
            parent_frame: the Frame that holds the Listbox widget
        """
        
        def BindMouseWheel(event):
            """Bind the mouse wheel to scroll through the Listbox."""
            
            self.listbox.bind_all('<MouseWheel>', Scroll)
        
        def Scroll(event):
            """Set the parameters for the mouse wheel to scroll."""
            
            self.listbox.yview_scroll(int(-1*(event.delta/120)), 'units')
        
        
        labelframe = Widgets.CreateLabelFrame(parent_frame,
                                              _text='Select Files To Load')
        labelframe.pack(fill = 'both', expand = 'true')
        
        scrollbar = Widgets.CreateScrollbar(labelframe)
        self.listbox = Widgets.CreateListbox(labelframe, _scrollbar=scrollbar)
        scrollbar.config(command=self.listbox.yview,
                         scrollregion=self.listbox.bbox('end'))
        scrollbar.pack(side='right', fill='y')
        self.listbox.pack(fill='both', expand='true')
        
        # Bind the mouse wheel to scroll the scrollbar whenever the mouse is
        #   within the listbox boundaries
        self.listbox.bind('<Enter>', BindMouseWheel)
        self.listbox.bind('<Leave>',
                          lambda e: self.listbox.unbind_all('<MouseWheel>'))
        
        # Fill the Listbox with the user's previously opened files
        for file in self.user_files:
            self.listbox.insert('end', os.path.basename(file))
    
    
    def InitializeListboxButtons(self, parent_frame):
        """Initialize buttons to add/remove quiz files within the Listbox.
        
        Arguments:
            parent_frame: the Frame that holds the Buttons
        """
        
        def RemoveFile():
            """Call the function to remove a file from the user's list.
            
            This function is called by the 'Remove Selected Files' button.
            """
            
            if self.RemoveFile():
                # Re-populate the listbox with the updated file list
                self.listbox.delete(0, 'end')
                for file in self.user_files:
                    self.listbox.insert('end', os.path.basename(file))
        
        
        # Create a button to add files to the listbox
        add_button = Widgets.CreateButton(parent_frame,
                                          _text='Add\nNew File',
                                          _cmd=self.AddFile,
                                          _height=self.button_height)
        add_button.pack(side='left', expand='true')
        
        # Create a button to remove a file from the listbox
        remove_button = Widgets.CreateButton(parent_frame,
                                             _text='Remove\n Selected File(s)',
                                             _cmd=RemoveFile,
                                             _height=self.button_height)
        remove_button.pack(side='right', expand='true')
    
    
    def InitializeMainButtons(self, parent_frame):
        """Initialize buttons to launch a quiz and create a new quiz file.
        
        Arguments:
            parent_frame: the Frame that holds the buttons.
        """
        
        def Load():
            """Call the function to load selected quiz files and launch quiz.
        
            This function is called by the 'Load Files & Launch Quiz' button.
            """
            result, quiz = self.LoadQuizFiles()
            if result:
                self.SaveData()
                QuizWindow.QuizWindow(self.root, quiz)
        
        
        launch_button = Widgets.CreateButton(parent_frame,
                                             _text='Load Files & Launch Quiz',
                                             _cmd=Load,
                                             _height=self.button_height,
                                             _width=self.button_width)
        launch_button.pack(expand='true')
        create_button = Widgets.CreateButton(parent_frame,
                                             _text='Create New Database File',
                                             _cmd=self.CreateNewDatabaseFile,
                                             _height=self.button_height,
                                             _width=self.button_width)
        create_button.pack(expand='true')
    
    
    def InitializeWelcomeMessage(self, parent_frame):
        """Initialize a label welcoming the user to the program.
        
        Arguments:
            parent_frame: the Frame that holds the welcome label and logout
                          button.
        """
        
        def Logout():
            """Log the current user out of the program.
            
            This function is called by the 'Log Out' button.
            """
            
            self.SaveData()
            self.root.destroy()
            LogInWindow.LogInWindow()
        
        
        welcome_str = f'\nWelcome, {self.current_user}!'
        if self.last_login:
            welcome_str += f'\n\nLast seen {self.last_login}'
        welcome_label = Widgets.CreateLabel(parent_frame, _text=welcome_str)
        welcome_label.pack(fill='both', expand='true')
        
        # Create a logout button
        logout_frame = Widgets.CreateFrame(parent_frame)
        logout_frame.pack(side='bottom', fill='x')
        logout_button = Widgets.CreateButton(logout_frame, _text='Log Out',
                                             _cmd=Logout,
                                             _height=1)
        logout_button.pack()
    
    
    def InitializeWindow(self):
        """Initialize the main program window and load widgets."""
        
        self.root.title('')
        self.main_frame = Widgets.CreateFrame(self.root)
        self.main_frame.pack(fill='both', expand='true')
        self.main_canvas = Widgets.CreateCanvas(self.main_frame)
        self.main_canvas.pack(fill='both', expand='true')
        
        white = '#f8f8ff'
        # Create and populate the Listbox widget
        topx = topy = 5
        botx = boty = 445
        self.main_canvas.create_rectangle(topx, topy, botx, boty,
                                          fill=white)
        listbox_frame = Widgets.CreateFrame(self.main_canvas)
        self.main_canvas.create_window(topx + 2, topy + 2, anchor='nw',
                                       height=boty - topy - 2,
                                       width=botx - topx - 2,
                                       window=listbox_frame)
        self.InitializeListbox(listbox_frame)
        
        # Create the Listbox interaction buttons
        topx = 5
        topy = 460
        botx = 445
        boty = 570
        self.main_canvas.create_rectangle(topx, topy, botx, boty,
                                          fill=white)
        listbox_buttons_frame = Widgets.CreateFrame(self.main_canvas)
        self.main_canvas.create_window(topx + 2, topy + 2, anchor='nw',
                                       height=boty - topy - 2,
                                       width=botx - topx - 2,
                                       window=listbox_buttons_frame)
        self.InitializeListboxButtons(listbox_buttons_frame)
        
        # Create the welcome message label and logout button
        topx = 455
        topy = 5
        botx = 885
        boty = 155
        self.main_canvas.create_rectangle(topx, topy, botx, boty,
                                          fill=white)
        welcome_frame = Widgets.CreateFrame(self.main_canvas)
        self.main_canvas.create_window(topx + 2, topy + 2, anchor='nw',
                                       height=boty - topy - 2,
                                       width=botx - topx - 2,
                                       window=welcome_frame)
        self.InitializeWelcomeMessage(welcome_frame)
        
        # Create the main program buttons
        topx = 455
        topy = 267
        botx = 885
        boty = 492
        self.main_canvas.create_rectangle(topx, topy, botx, boty,
                                          fill=white)
        main_buttons_frame = Widgets.CreateFrame(self.main_canvas)
        self.main_canvas.create_window(topx + 2, topy + 2, anchor='nw',
                                       height=boty - topy - 2,
                                       width=botx - topx - 2,
                                       window=main_buttons_frame)
        self.InitializeMainButtons(main_buttons_frame)
    
    
    def LoadDatabase(self):
        """Load the user's quiz file history from the database file.
        
        This function opens the file containing the quiz database files each
            user has utilized in the past and loads the files associated with
            the current user into a list. If any changes are made to this list,
            they will be saved back to the file once a quiz begins.
        """
        
        db_data = []
        try:
            with open(self.DB_FILE, 'r') as infile:
                db_data = json.load(infile)
            db_data = db_data[self.current_user]
        except IOError:
            # The database file is nonexistent or corrupt and should be
            #   created as a fresh file
            with open(self.DB_FILE, 'w') as infile:
                pass
        except JSONDecodeError:
            tk.messagebox.showerror('Error',
                                    f'Unable to load data from {self.DB_FILE}')
        except:
            tk.messagebox.showerror('Error', 'Unexpected error encountered')
        
        return db_data
    
    
    def LoadQuizFiles(self):
        """Load the selected quiz files into a list.
        
        Returns:
            'True' and a list containing file contents if files were selected
                and at least one file was able to be loaded.
            'False' and 'None' if no files were selected, no files could be
                accessed, or the user chose not to proceed after encountering
                errors loading the files.
        """
        
        selections = self.listbox.curselection()
        if not selections:
            tk.messagebox.showerror('Error', 'No files selected!\nSelect ' \
                                             'files from the listbox prior ' \
                                             'to launching a quiz.')
            return False, None
        
        # Load the contents of selected files
        quiz = []
        error_msg = 'Error accessing the following files:\n'
        errors_flag = False
        for index in selections:
            try:
                with open(self.user_files[index], 'r') as infile:
                    quiz.extend(json.load(infile))
            except:
                # Create a composite error message for inaccessible files
                errors_flag = True
                error_msg += f'{os.path.basename(self.user_files[index])}\n'
        
        if not quiz:
            tk.messagebox.showerror('Error', 'No files could be accessed')
            return False, None
        
        if errors_flag:
            error_msg += 'Contents from those files won\'t be added. Continue?'
            ask = tk.messagebox.askyesno('Error', error_msg)
            if not ask:
                return False, None
        
        return True, quiz
    
    
    def OnClose(self):
        """Save user file data before exiting the program."""
        
        self.SaveData()
        self.root.destroy()
    
    
    def RemoveFile(self):
        """Remove selected file(s) from the user's file list.
        
        Files must be selected in the Listbox prior to clicking the button.
        
        Returns:
            'True' if files were selected and removed from the list.
            'False' if no files from the Listbox were selected or files weren't
                able to be removed from the list.
        """
        
        selections = self.listbox.curselection()
        if not selections:
            messagebox.showerror('Error', 'Select one or more files first')
            return False
        
        new_files = []
        for i, file in enumerate(self.user_files, 0):
            if i in selections:
                continue
            new_files.append(file)
        if new_files == self.user_files:
            messagebox.showerror('Error', 'Files were not able to be removed.')
            return False
        self.user_files = new_files
        return True
    
    
    def SaveData(self):
        """Save the user's file information to the database file."""
        
        try:
            with open(self.DB_FILE, 'r+') as outfile:
                existing_data = json.load(outfile)
                existing_data[self.current_user] = self.user_files
                outfile.seek(0)
                json.dump(existing_data, outfile, indent=4)
                outfile.truncate()
        except:
            tk.messagebox.showerror('Error',
                                    f'{self.DB_FILE} could not be accessed.' \
                                    'Altered file information won\'t be saved')