#-----------------------------------------------------------------------------#
#   LogInWindow.py                                                            #
#   Author: Logan Pierceall                                                   #
#                                                                             #
#   This module creates an initial log-in window. This window allows a user   #
#       to log in, create a new user account, or reset a forgotten password.  #
#       After providing valid login information, control is passed to the     #
#       main window, whose code can be found in MainWindow.py.                #
#                                                                             #
#   The supporting backend code for this module is found in LogInLogic.py.    #
#-----------------------------------------------------------------------------#

import os
import tkinter as tk
from tkinter import messagebox
from tkinter import Tk

import LogInLogic
import MainWindow
import Widgets



class LogInWindow(Tk):

    def __init__(self, *args, **kwargs):
    
        super().__init__(*args, **kwargs)
        
        # Create the folder to store quiz database files if not already present
        try:
            os.mkdir('database')
        except:
            pass
        
        # Window dimensions
        self.WIN_HEIGHT = 600
        self.WIN_WIDTH  = 900
        
        # Widget option constants
        self.BUT_HEIGHT = 3
        self.WHITE      = '#f8f8ff'
        
        self.username     = tk.StringVar()      # Stores 'Username'
        self.password     = tk.StringVar()      # Stores 'Password'
        self.confirm_pass = tk.StringVar()      # Stores 'Confirm Password'
        
        # Flag that tracks if the user clicks on the 'Forgot password' label.
        #   Helps designate which widgets to erase when the 'Return to Log In'
        #   button is clicked
        self.forgot_flag = False
            
        self.CreateWindow()
    
    
    
    # ChangePassword() is called by the 'Change password' button. This function
    #   sends the username, new password, and confirmed new password to the
    #   ChangePassword() function in LogInLogic.py to update the user's
    #   password
    # Args:     none
    # Returns:  none
    def ChangePassword(self):
    
        # Retrieve the username and passwords
        username = self.username.get().rstrip()
        password = self.new_pass.get().rstrip()
        confirm  = self.conf_new.get().rstrip()
        
        # 'result' is a boolean for successful password update and 'msg'
        #   contains either a success message or error message
        result, msg = LogInLogic.ChangePassword(username, password, confirm)
        
        if result:
            tk.messagebox.showinfo('Success', msg)
            self.Return()
        else:
            tk.messagebox.showerror('Error', msg)
    
    
    
    # CheckLogin() is called by the 'Log In' button. It validates the user
    #   credentials by passing them to the CheckLogin() function found in 
    #   LoginLogic.py. If the credentials are correct, the Log In window is
    #   destroyed and the Main Window is initialized.
    # Args:     none
    # Returns:  none
    def CheckLogin(self):
        
        username = self.username.get().rstrip()
        password = self.password.get().rstrip()
        
        # Validate the information. If 'check' is False, msg will contain an
        #   error message
        result, msg = LogInLogic.CheckLogin(username, password)
        
        if result:
            # Retrieve the most recent log-in date
            login_date = LogInLogic.GetLastLogIn(username)
        
            # Delete this window and load the main program
            self.main_frame.forget()
            MainWindow.MainWindow(self, username, login_date)
        else:
            tk.messagebox.showerror('Error', msg)
    
    
    
    # CreateAccount() is called by the 'Create New Account' button. It destroys
    #   the log in widgets and creates the widgets used to create a new user
    #   account
    # Args:     none
    # Returns:  none
    def CreateAccount(self):
    
        # Erase the initial log in widgets and load the account creation ones
        self.main_canvas.delete(self.loginw)
        
        # Widgets are created from the bottom of the screen, which causes the
        #   'Tab' button to traverse them in that order. This list helps
        #   to reverse that and return 'Tab' to expected behavior
        widget_list = []
        
        confirm_frame = Widgets.CreateFrame(self.main_canvas)
        self.acctw = self.main_canvas.create_window(self.WIN_WIDTH / 2,
                                                    self.WIN_HEIGHT / 2,
                                                    window = confirm_frame)
        
        # Create a frame to hold the buttons
        button_frame = Widgets.CreateFrame(confirm_frame)
        button_frame.pack(side = 'bottom')
        
        # Create a button two finalize the account
        finalize_button = Widgets.CreateButton(button_frame, 'Create Account',
                                            self.FinalizeAccount,
                                            self.BUT_HEIGHT)
        finalize_button.pack(side = 'left')
        
        # Create a button to return to the main screen
        return_button = Widgets.CreateButton(button_frame, 'Return to\nLog In',
                                          self.Return, self.BUT_HEIGHT)
        return_button.pack(side = 'right')
        
        # Create a label to monitor whether the contents of both password
        #   fields match or not
        self.pass_match_label = Widgets.CreateLabel(confirm_frame, '',
                                                    _font = ('georgia', 8))
        self.pass_match_label.pack(side = 'bottom')
        
        # Set the two password fields to monitor their contents and call it
        #   to initialize the label's text
        self.password.trace('w', self.PasswordMatch)
        self.confirm_pass.trace('w', self.PasswordMatch)
        self.PasswordMatch()
        
        # Create an entry box and label for password confirmation
        self.confirm_entry = Widgets.CreateEntry(confirm_frame,
                                                 self.confirm_pass, '*')
        self.confirm_entry.pack(side = 'bottom')
        widget_list.append(self.confirm_entry)
        
        confirm_label = Widgets.CreateLabel(confirm_frame, 'Confirm Password:')
        confirm_label.pack(side = 'bottom')
        
        # Create an entry box and label for the password
        self.pass_entry = Widgets.CreateEntry(confirm_frame, self.password, 
                                              '*')
        self.pass_entry.pack(side = 'bottom')
        widget_list.append(self.pass_entry)
        
        pass_label = Widgets.CreateLabel(confirm_frame, 'Password:')
        pass_label.pack(side = 'bottom')
        
        # Create an entry box and label for the username
        self.user_entry = Widgets.CreateEntry(confirm_frame, self.username)
        self.user_entry.pack(side = 'bottom')
        widget_list.append(self.user_entry)
        
        user_label = Widgets.CreateLabel(confirm_frame, 'Username:')
        user_label.pack(side = 'bottom')
        
        # Reverse the 'Tab' navigation
        widget_list.reverse()
        for widget in widget_list:
            widget.lift()
    
    
    
    # CreateBackground() initializes a frame and canvas that cover the entire
    #   window and places a white box in the middle of the window
    # Args:     none
    # Returns:  none
    def CreateBackground(self):
    
        # Create the frame and canvas
        self.main_frame = Widgets.CreateFrame(self)
        self.main_frame.pack(fill = 'both', expand = 'true')
        
        self.main_canvas = Widgets.CreateCanvas(self.main_frame)
        self.main_canvas.pack(fill = 'both', expand = 'true')
        
        # Draw a rectangle in the middle of the window
        top_left_x = self.WIN_WIDTH / 4
        top_left_y = self.WIN_HEIGHT / 4
        bottom_right_x = self.WIN_WIDTH - top_left_x
        bottom_right_y = self.WIN_HEIGHT - top_left_y
        self.main_canvas.create_rectangle(top_left_x, top_left_y,
                                          bottom_right_x, bottom_right_y,
                                          fill = self.WHITE)
    
    
    
    # CreateLogInFields() initializes the widgets used to log in
    # Args:     none
    # Returns:  none
    def CreateLogInFields(self):
    
        # Widgets are created from the bottom of the screen, which causes the
        #   'Tab' button to traverse them in that order. This list helps
        #   to reverse that and return 'Tab' to expected behavior
        widget_list = []
    
        # Create a frame within the canvas to hold the widgets
        self.login_frame = Widgets.CreateFrame(self.main_canvas)
        self.loginw = self.main_canvas.create_window(self.WIN_WIDTH / 2,
                                                     self.WIN_HEIGHT / 2,
                                                     window = self.login_frame)
        
        # Create a frame to hold buttons
        button_frame = Widgets.CreateFrame(self.login_frame)
        button_frame.pack(side = 'bottom')
        
        # Create a button to log in
        login_button = Widgets.CreateButton(button_frame, 'Log In',
                                            self.CheckLogin, self.BUT_HEIGHT)
        login_button.pack(side = 'left')
        
        # Create a button to make a new user account
        create_button = Widgets.CreateButton(button_frame,
                                             'Create\nNew Account',
                                             self.CreateAccount,
                                             self.BUT_HEIGHT)
        create_button.pack(side = 'right')
        
        # Create a clickable label to reset a password
        reset_label = Widgets.CreateLabel(self.login_frame, 'Forgot Password?',
                                         _font = ('georgia', 10))
        reset_label.pack(side = 'bottom')
        
        # Bind a mouse-click event to the 'Forgot password?' label
        reset_label.bind('<Button-1>', lambda e:self.ForgotPassword())
        
        # Create an entry box and label for the password
        pass_entry = Widgets.CreateEntry(self.login_frame, self.password, '*')
        pass_entry.pack(side = 'bottom')
        widget_list.append(pass_entry)
        
        pass_label = Widgets.CreateLabel(self.login_frame, 'Password:')
        pass_label.pack(side = 'bottom')
        
        # Create an entry box and label for the username
        user_entry = Widgets.CreateEntry(self.login_frame, self.username)
        user_entry.pack(side = 'bottom')
        widget_list.append(user_entry)
        
        user_label = Widgets.CreateLabel(self.login_frame, 'Username:')
        user_label.pack(side = 'bottom')
        
        # Reverse the 'Tab' navigation
        widget_list.reverse()
        for widget in widget_list:
            widget.lift()
    
    
    
    # CreateWindow() initializes the window
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
        
        self.CreateBackground()
        self.CreateLogInFields()
    
    
    
    # FinalizeAccount() is called by the 'Create Account' button. This function
    #   collects the username and password fields and passes them to the
    #   CreateAccount() function in LogInLogic.py to add the new account to the
    #   users database
    # Args:     none
    # Returns:  none
    def FinalizeAccount(self):
    
        username = self.username.get().rstrip()
        password = self.password.get().rstrip()
        
        # Ensure the username field is populated
        if not username:
            tk.messagebox.showerror('ERROR', 'No username entered.')
            return
        
        # Ensure the password fields match
        if not self.PasswordMatch():
            tk.messagebox.showerror('ERROR', 'Passwords must match.')
            return
        
        result, msg = LogInLogic.CreateAccount(username, password)
        if result:
        
            # Prompt the user to log in as the new account
            load_txt = 'Account successfully created. Log in as ' \
                       f'{username} now?'
            load = tk.messagebox.askyesno('Success', load_txt)
            
            if load:
                # Destroy the main frame to erase the current window
                self.main_frame.destroy()
            
                # MainWindow() takes a last log-in date as an argument. Since
                #   this is a new account, pass 'None' instead
                MainWindow.MainWindow(self, username, None)
            else:
                # If a user created a new account but didn't want to log in as
                #   that account, clear the username and password fields
                self.user_entry.delete(0, 'end')
                self.pass_entry.delete(0, 'end')
                self.confirm_entry.delete(0, 'end')
                self.Return()
        else:
            tk.messagebox.showerror('Error', msg)
    
    
    
    # ForgotPassword() is called by the 'Forgot password?' label. It destroys
    #   the main log in widgets and rebuilds the window with fields used to
    #   change a user's password
    # Args:     none
    # Returns:  none
    def ForgotPassword(self):
    
        # Update the window flag
        self.forgot_flag = True
    
        self.new_pass = tk.StringVar()      # Stores 'New password' field
        self.conf_new = tk.StringVar()      # Stores 'Confirm password' field
        
        # Delete the log in widgets
        self.main_canvas.delete(self.loginw)
        
        # Widgets are created from the bottom of the screen, which causes the
        #   'Tab' button to traverse them in that order. This list helps
        #   to reverse that and return 'Tab' to expected behavior
        widget_list = []
        
        forgot_frame = Widgets.CreateFrame(self.main_canvas)
        self.forgotw = self.main_canvas.create_window(self.WIN_WIDTH / 2,
                                                      self.WIN_HEIGHT / 2,
                                                      window = forgot_frame)
        
        # Create a frame to hold the buttons
        button_frame = Widgets.CreateFrame(forgot_frame)
        button_frame.pack(side = 'bottom')
        
        # Create a button to change the password
        change_button = Widgets.CreateButton(button_frame, 'Change password',
                                             self.ChangePassword,
                                             self.BUT_HEIGHT)
        change_button.pack(side = 'left')
        
        # Create a button to return to the main screen
        return_button = Widgets.CreateButton(button_frame, 'Return to\nLog In',
                                             self.Return, self.BUT_HEIGHT)
        return_button.pack(side = 'right')
        
        # Create a password confirmation entry box and label
        confirm_entry = Widgets.CreateEntry(forgot_frame, self.conf_new, '*')
        confirm_entry.pack(side = 'bottom')
        widget_list.append(confirm_entry)
        
        confirm_label = Widgets.CreateLabel(forgot_frame, 'Confirm password:')
        confirm_label.pack(side = 'bottom')
        
        # Create a new password entry box and label
        new_pass_entry = Widgets.CreateEntry(forgot_frame, self.new_pass, '*')
        new_pass_entry.pack(side = 'bottom')
        widget_list.append(new_pass_entry)
        
        new_pass_label = Widgets.CreateLabel(forgot_frame, 'New password:')
        new_pass_label.pack(side = 'bottom')
        
        # Create a username entry box and label
        user_entry = Widgets.CreateEntry(forgot_frame, self.username)
        user_entry.pack(side = 'bottom')
        widget_list.append(user_entry)
        
        user_label = Widgets.CreateLabel(forgot_frame, 'Username:')
        user_label.pack(side = 'bottom')
        
        # Reverse the 'Tab' navigation
        widget_list.reverse()
        for widget in widget_list:
            widget.lift()
    
    
    
    # PasswordMatch()'s primary function is to constantly monitor the
    #   'Password' and 'Confirm Password' fields and provide a visual indicator
    #   of whether the two fields have identical contents or not
    # Return values are only utilized when creating a new user account
    # Args:     none
    # Returns:  True if the passwords match
    #           False if they don't
    def PasswordMatch(self, *args):
    
        pass1 = self.password.get().rstrip()
        pass2 = self.confirm_pass.get().rstrip()
        
        # Update a label, located above the 'Confirm Password' box, to inform
        #   the user of the status of the two fields
        if (pass1 and pass1 == pass2):
            self.pass_match_label['text'] = 'Passwords match!'
            self.pass_match_label['fg'] = 'green'
            return True
        else:
            self.pass_match_label['text'] = 'Password don\'t match'
            self.pass_match_label['fg'] = 'red'
            return False
    
    
    
    # Return() is called by the 'Return to Log In' button present on both the
    #   account creation and change of password windows. This function deletes
    #   the widgets used by either of those two windows and loads the initial
    #   log in widgets
    # Args:     none
    # Returns:  none
    def Return(self):
    
        # If the forgot flag is True, that window called the function and those
        #   widgets should be deleted. If not, then the account creation window
        #   called the function
        if self.forgot_flag:
            self.main_canvas.delete(self.forgotw)
            self.forgot_flag = False
        else:
            self.main_canvas.delete(self.acctw)
        
        self.CreateLogInFields()