#-----------------------------------------------------------------------------#
#   LogInWindow.py                                                            #
#   Author: Logan Pierceall                                                   #
#   Date: March 8, 2022                                                       #
#                                                                             #
#   This file contains the user interface that allows a user to log in,       #
#       create a new user account, or reset a forgotten password. The code    #
#       handling the JSON interactions that are initiated in this window is   #
#       found in the LogInLogic.py file.                                      #
#-----------------------------------------------------------------------------#


import tkinter as tk
from tkinter import messagebox
from tkinter import Tk

import LogInLogic
import MainWindow
import WidgetCreation



class LogInWindow(Tk):

    def __init__(self, *args, **kwargs):
    
        super().__init__(*args, **kwargs)
        
        self.WIN_HEIGHT = 300                   # Window height
        self.WIN_WIDTH = 400                    # Window width
        
        self.username = tk.StringVar()          # Stores text for the Username
                                                #   field
        self.password = tk.StringVar()          # Stores text for the Password
                                                #   field
        self.confirm_pass = tk.StringVar()      # Stores text for the Confirm
                                                #   Password field
        
        self.CreateWindow()
    
    
    
    # CheckLogin() is called by the 'Log In' button. It validates the user
    #   credentials by passing them to the CheckLogin() function found in 
    #   LoginLogic.py. If the credentials are correct, the Log In window is
    #   destroyed and the Main Window is initialized.
    # Args:     none
    # Returns:  none
    def CheckLogin(self, *args):
        
        username = self.username.get().rstrip()
        password = self.password.get().rstrip()
        
        # If 'check' is False, msg will contain an error message
        check, msg = LogInLogic.CheckLogin(username, password)
        
        if check:
            # Retrieve the most recent log-in date
            login_date = LogInLogic.GetLastLogIn(username)
        
            # Log the user in and load the main program
            MainWindow.MainWindow(username, login_date)    
            self.destroy()
        else:
            tk.messagebox.showerror('Error', msg)
    
    
    
    # CreateAccount() is called by the 'Create New Account' button. It destroys
    #   the current window widgets and creates the widgets used to create a new
    #   user account
    # Args:     none
    # Returns:  none
    def CreateAccount(self, *args):
    
        # Flag to track if a new user account was created. This will help clear
        #   the 'username' and 'password' fields if the user opts to not log in
        #   to a newly created user account
        self.created_account = False
    
        self.top_frame.forget()
        self.bottom_frame.forget()
        
        self.CreateFrames()
        self.CreateUserPassFields()
        self.CreateAccountCreateFields()
    
    
    
    # CreateAccountCreateFields() initializes the following widgets:
    #   A 'Confirm Password' label and text entry field
    #   A label that helps track whether the 'Password' and 'Confirm
    #       Password' fields contain matching text or not
    #   A button to create the new account
    #   A button to return to the main 'Log In' screen
    # Args:     none
    # Returns:  none
    def CreateAccountCreateFields(self):
    
        confirm_frame = WidgetCreation.CreateFrame(self.bottom_frame)
        confirm_frame.pack(fill = 'both', expand = 'true')
        
        # Create a frame to hold the 'Confirm Password' label and a label
        #   to indicate if the password fields have identical contents
        labels_frame = WidgetCreation.CreateFrame(confirm_frame)
        labels_frame.pack(side = 'top', fill = 'both', expand = 'true')
        
        # Create the 'Confirm Password' label
        confirm_label = WidgetCreation.CreateLabel(labels_frame,
                                                   'Confirm Password:')
        confirm_label.pack(side = 'left', fill = 'x', expand = 'true')
        
        # Create the password tracking label
        self.pass_match_label = WidgetCreation.CreateLabel(labels_frame, "",
                                                           ('georgia', 8))
        self.pass_match_label.pack(side = 'right', fill = 'x')
        
        # Create the 'Confirm Password' text entry box
        self.confirm_entry = WidgetCreation.CreateEntry(confirm_frame,
                                                        self.confirm_pass)
        self.confirm_entry.pack(side = 'bottom', fill = 'x', expand = 'true')
        
        # Set the two password fields to monitor if the contents match
        self.password.trace('w', self.PasswordMatch)
        self.confirm_pass.trace('w', self.PasswordMatch)
        self.PasswordMatch()
        
        # Create a frame to hold the confirm and return to main screen buttons
        create_return_frame = WidgetCreation.CreateFrame(self.bottom_frame)
        create_return_frame.pack(side = 'bottom', fill = 'both', expand = 'true')
        
        # Create a button to confirm account creation
        create_button = WidgetCreation.CreateButton(create_return_frame,
                                                    'Create Account',
                                                    self.FinalizeAccount)
        create_button.pack(side = 'left', fill = 'both', expand = 'true')
        
        # Create a button to return to the main log in window
        return_button = WidgetCreation.CreateButton(create_return_frame,
                                                    'Return to\nMain Screen',
                                                    self.ResetWindow)
        return_button.pack(side = 'right', fill = 'both', expand = 'true')
    
    
    
    # CreateFrames() initalizes the following widgets:
    #   A frame to hold the 'Username' and 'Password' fields
    #   A frame that holds the 'Log In' and 'Create New Account' buttons on the
    #       initial Log In screen, and the 'Confirm Password',
    #       'Create Account', and 'Return to Main Screen' buttons on the Create
    #       Account screen
    # Args:     none
    # Returns:  none
    def CreateFrames(self):
    
        self.top_frame = WidgetCreation.CreateFrame(self)
        self.top_frame.pack(side = 'top', fill = 'both', expand = 'true')
        
        self.bottom_frame = WidgetCreation.CreateFrame(self)
        self.bottom_frame.pack(side = 'bottom', fill = 'both', expand = 'true')
    
    
    
    # CreateLogInFields() initializes the following widgets:
    #   A clickable label used to reset a password
    #   A button to log in to the program
    #   A button to create a new user account
    # Args:     none
    # Returns:  none
    def CreateLogInFields(self):
    
        # Create a clickable label to allow a user to reset a forgotten password
        reset_pass_label = WidgetCreation.CreateLabel(self.pass_label_frame,
                                                      'Forgot password?',
                                                      ('georgia', 10))
        reset_pass_label.pack(side = 'right')
        
        # Bind a mouse-click event to the 'Forgot password?' label in order to
        #   launch the appropriate function when clicked
        reset_pass_label.bind('<Button-1>', lambda e:self.ResetPassword())
        
        # Create the log in and create account buttons
        login_create_frame = WidgetCreation.CreateFrame(self.bottom_frame)
        login_button = WidgetCreation.CreateButton(login_create_frame,
                                                   'Log In',
                                                   self.CheckLogin)
        create_button = WidgetCreation.CreateButton(login_create_frame,
                                                    'Create New\nAccount',
                                                    self.CreateAccount)
        
        login_create_frame.pack(side = 'top', fill = 'both', expand = 'true')
        login_button.pack(side = 'left', fill = 'both', expand = 'true')
        create_button.pack(side = 'right', fill = 'both', expand = 'true')
    
    
    
    # CreateUserPassFields() initializes the following widgets:
    #   A label and text entry box for the 'Username' field
    #   A label and text entry box for the 'Password' field
    # Args:     none
    # Returns:  none
    def CreateUserPassFields(self):
    
        # Create a username label and text entry box
        user_frame = WidgetCreation.CreateFrame(self.top_frame)
        user_frame.pack(side = 'top', fill = 'both', expand = 'true')
        
        user_label = WidgetCreation.CreateLabel(user_frame, 'Username:')
        user_label.pack(side = 'top', fill = 'x', expand = 'true')
        
        self.user_entry = WidgetCreation.CreateEntry(user_frame, self.username)
        self.user_entry.pack(side = 'bottom', fill = 'x', expand = 'true')
        
        # Create a password label and text entry box
        password_frame = WidgetCreation.CreateFrame(self.top_frame)
        password_frame.pack(side = 'bottom', fill = 'both', expand = 'true')
        
        self.pass_label_frame = WidgetCreation.CreateFrame(password_frame)
        self.pass_label_frame.pack(side = 'top', fill = 'x', expand = 'true')
        
        password_label = WidgetCreation.CreateLabel(self.pass_label_frame,
                                                    'Password:')
        password_label.pack(side = 'left', fill = 'x', expand = 'true')
        
        self.password_entry = WidgetCreation.CreateEntry(password_frame,
                                                         self.password)
        self.password_entry.pack(side = 'bottom', fill = 'x', expand = 'true')
    
    
    
    # CreateWindow() initializes the Log In window
    # Args:     none
    # Returns:  none
    def CreateWindow(self):
    
        # Obtain x&y coordinates to place window in center of screen
        y_pos = int((self.winfo_screenheight() / 2) - (self.WIN_HEIGHT / 2))
        x_pos = int((self.winfo_screenwidth() / 2) - (self.WIN_WIDTH / 2))
        
        # Title and size the main window
        self.title('Log In')
        self.geometry(f'{self.WIN_WIDTH}x{self.WIN_HEIGHT}+{x_pos}+{y_pos}')
        self.resizable(False, False)
        
        self.CreateFrames()             # Load the window frames
        self.CreateUserPassFields()     # Load the username/password widgets
        self.CreateLogInFields()        # Load the log in widgets
    
    
    
    # FinalizeAccount() is called by the 'Create Account' button. It passes the
    #   user-provided data to the CreateAccount() function found in the
    #   LoginLogic.py file. That function will store the new user info into the
    #   user info JSON file
    # Args:     none
    # Returns:  none
    def FinalizeAccount(self, *args):
    
        username = self.username.get().rstrip()
        password = self.password.get().rstrip()
        
        # Ensure the username field is populated
        if not username:
            tk.messagebox.showerror('ERROR', 'No username entered!')
        
        elif self.PasswordMatch():
            # 'create_results' holds boolean status for successful account
            #   creation
            # 'db_results' holds boolean status for successful addition
            #   to the previously opened files list (see MainLogic.py)
            # 'msg' holds the a string offering further info / error message
            create_results, db_results, msg = LogInLogic.CreateAccount(username,
                                                                       password)
            if create_results:
                # Give user the option to log in as the newly created user
                load = tk.messagebox.askyesno('Success', msg)
                
                # Update the created user flag
                self.created_account = True
                
                if load:
                    # If the previously opened files list was unable to be
                    #   accessed, files won't be saved in a listbox. Warn
                    #   the user before proceeding
                    if not db_results:
                        msg = f'Opened quiz files added to the selection ' \
                              f'list won\'t be able to be saved\nfor easier ' \
                              f'access in the future.'
                        tk.messagebox.showwarning('Warning', msg)
                    
                    login_date = LogInLogic.GetLastLogIn(username)
                    MainWindow.MainWindow(username, login_date)
                    self.destroy()
                else:
                    # Return to the main Log In window
                    self.ResetWindow()
            
            else:
                tk.messagebox.showerror('ERROR', msg)
                
        # If the passwords don't match, alert the user
        else:
            tk.messagebox.showerror('ERROR', 'Password fields don\'t match.')
    
    
    
    # PasswordMatch() is used to monitor if the text entered into the 'Password'
    #   field matches the text entered into the 'Confirm Password' field.
    #   Returns are only utilized by FinalizeAccount() to create a new account
    # Args:     none
    # Returns:  True if the passwords match
    #           False if they don't
    def PasswordMatch(self, *args):
    
        pass1 = self.password.get().rstrip()
        pass2 = self.confirm_pass.get().rstrip()
        
        # Update a label, located above the 'Confirm Password' box, to inform
        #   the user of the status of the two fields
        if (pass1 != '' and pass1 == pass2):
            self.pass_match_label['text'] = 'Passwords match!'
            self.pass_match_label['fg'] = 'green'
            return True
        else:
            self.pass_match_label['text'] = 'Passwords don\'t match'
            self.pass_match_label['fg'] = 'red'
            return False
    
    
    
    # Reset() is called by the 'Reset' button on the 'Reset Password' screen.
    #   It sends the contents of both password fields to the ChangePassword()
    #   function found within LogInLogic.py. That function will update the
    #   password stored in the user info JSON file
    # Args:     none
    # Returns:  none
    def Reset(self, *args):
    
        result, msg = LogInLogic.ChangePassword(self.username.get(),
                                                self.new_pass.get(),
                                                self.confirm_new_pass.get())
        
        # If the password fields matched, the user info is updated and the
        #   'Reset Password' window will be destroyed
        if result:
            tk.messagebox.showinfo('', msg)
            self.new_win.destroy()
        else:
            tk.messagebox.showerror('', msg)
            
            # Brings the Reset Password window back to the forefront of screen
            self.new_win.attributes('-topmost', True)
            self.new_win.attributes('-topmost', False)
        
    
    
    # RestPassword() is called by the 'Forgot password?' button. It creates a
    #   pop-up window that initializes the following widgets:
    #       A label and text entry box for the 'Username' field
    #       A label and text entry box for the 'New Password' field
    #       A label and text entry box for the 'Confirm New Password' field
    #       A button to finalize the password reset
    # Args:     none
    # Returns:  none
    def ResetPassword(self, *args):
    
        self.new_pass = tk.StringVar()          # Retrieves text from the
                                                #   'Enter new password' field
        self.confirm_new_pass = tk.StringVar()  # Retrieves text from the
                                                #   'Confirm new password'
                                                #   field
    
        # Create the new password window as a child of the main window
        self.new_win = tk.Toplevel(self)
        width = 300
        height = 250
        y_pos = int((self.winfo_screenheight() / 2) - (height / 2))
        x_pos = int((self.winfo_screenwidth() / 2) - (width / 2))
        self.new_win.geometry(f'{width}x{height}+{x_pos}+{y_pos}')
        self.new_win.title('Change password')
        
        # Frame to hold the new widgets
        new_frame = WidgetCreation.CreateFrame(self.new_win)
        new_frame.pack(fill = 'both', expand = 'true')
        
        # Username label and text entry box
        user_label = WidgetCreation.CreateLabel(new_frame, 'Enter username:')
        user_label.pack(fill = 'x', expand = 'true')
        
        user_entry = WidgetCreation.CreateEntry(new_frame, self.username)
        user_entry.pack(fill = 'x', expand = 'true')
        
        # New Password label and text entry box
        pass_label = WidgetCreation.CreateLabel(new_frame,
                                                'Enter new password:')
        pass_label.pack(fill = 'x', expand = 'true')
        
        pass_entry = WidgetCreation.CreateEntry(new_frame, self.new_pass)
        pass_entry.pack(fill = 'x', expand = 'true')
        
        # Confirm New Password label and text entry box
        confirm_label = WidgetCreation.CreateLabel(new_frame,
                                                   'Confirm new password:')
        confirm_label.pack(fill = 'x', expand = 'true')
        
        confirm_entry = WidgetCreation.CreateEntry(new_frame, self.confirm_new_pass)
        confirm_entry.pack(fill = 'x', expand = 'true')
        
        # Button to confirm the password reset
        new_button = WidgetCreation.CreateButton(new_frame, 'Reset', self.Reset)
        new_button.pack(fill = 'x', expand = 'true')
    
    
    
    # ResetWindow() is called by the 'Return to Main Screen' button. It destroys
    #   the current widgets and creates the widgets used by the main Log In
    #   screen
    # Args:     none
    # Returns:  none
    def ResetWindow(self, *args):
    
        self.top_frame.forget()
        self.bottom_frame.forget()
        
        self.CreateFrames()
        self.CreateUserPassFields()
        self.CreateLogInFields()
        
        # If a user created a new account but didn't want to log in as that
        #   account, clear the username and password fields
        if self.created_account:
            self.user_entry.delete(0, 'end')
            self.password_entry.delete(0, 'end')
            self.confirm_entry.delete(0, 'end')
        


if __name__ == '__main__':

    app = LogInWindow()
    app.mainloop()