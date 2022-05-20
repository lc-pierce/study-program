import json
from json.decoder import JSONDecodeError
import os
from datetime import date
import tkinter as tk
from tkinter import messagebox
from tkinter import Tk

import MainWindow
import Widgets


class LogInWindow(Tk):

    def __init__(self, *args, **kwargs):
    
        super().__init__(*args, **kwargs)
        
        # Constant height for all Button widgets
        self.button_height = 3
        
        # Variables used to retrieve Entry box contents
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.confirm_pass = tk.StringVar()
        
        # Load the user accounts info
        self.users_file = 'users.json'
        self.user_db = self.LoadDatabase()
        
        # Load the window and the initial 'Log In' widgets
        self.InitializeWindow()
        self.LoadLogInWindow()
    
    
    def ChangePassword(self):
        """Update a user's password using the user-provided information.
        
        Returns:
            'True' if the password is successfully changed.
            'False' if any fields are left blank, the password fields don't
                match, the new password is identical to the old password, or
                the user isn't found in the database.
        """
        
        username = self.username.get().lstrip().rstrip()
        if not username:
            messagebox.showerror('Error', 'No username entered.')
            return False
        
        if not self.PasswordMatch():
            messagebox.showerror('Error', 'Password fields do not match.')
            return False
        password = self.password.get().lstrip().rstrip()
        
        for user in self.user_db:
            if user['User'] == username:
                if user['Password'] == password:
                    messagebox.showerror('Error',
                                         'New password unchanged from the ' \
                                         'old password.')
                    return False
                user['Password'] = password
                messagebox.showinfo('Success!', 'Password updated!')
                return True
        
        messagebox.showerror('Error', f'{username} not found in database.')
        return False
    
    
    def CheckLogin(self):
        """Verify the user-provided credentials and retrieve last log-in date.
        
        Returns:
            'True', the username, and the date of the user's last login if the
                provided information is valid.
            'False', 'None', and 'None' if the username or password fields
                aren't populated, the password is incorrect, or the user
                wasn't found in the database.
        """
        
        username = self.username.get().lstrip().rstrip()
        if not username:
            messagebox.showerror('Error', 'No username entered.')
            return False, None, None
        
        password = self.password.get().lstrip().rstrip()
        if not password:
            messagebox.showerror('Error', 'No password entered.')
            return False, None, None
        
        for user in self.user_db:
            if user['User'] == username:
                if user['Password'] == password:
                    # Retrive the last log-in date, then update value to now
                    prev_login = user['LastLogIn']
                    user['LastLogIn'] = date.today().strftime('%B %d, %Y')
                    return True, username, prev_login
                else:
                    messagebox.showerror('Error',
                                         'The provided password is incorrect.')
                    return False, None, None
        
        messagebox.showerror('Error', f'User {username} does not exist.')
        return False, None, None
    
    
    def CreateAccount(self):
        """Add a new user account to the database list.
        
        Returns:
            'True' if the user provided a valid username and the passwords
                are identical.
            'False' if no username was provided, no password was provided,
                or the passwords don't match.
        """
        
        username = self.username.get().lstrip().rstrip()
        if not username:
            messagebox.showerror('Error', 'No username entered!')
            return False
        for user in self.user_db:
            if user['User'] == username:
                messagebox.showerror('Error', f'{username} already exists!')
                return False
        
        if not self.PasswordMatch():
            messagebox.showerror('Error', 'Passwords must match!')
            return False
        password = self.password.get().lstrip().rstrip()
        
        user_data = {
            'User': username,
            'Password': password,
            'CreationDate': date.today().strftime('%B %d, %Y'),
            'LastLogIn': ''
        }
        self.user_db.append(user_data)
        return True
    
    
    def InitializeWindow(self):
        """Initialize the main program window."""
        
        win_height = 600
        win_width = 900
        
        # 'x' and 'y' coordinates place window in the center of the screen
        y = int((self.winfo_screenheight() / 2) - (win_height / 2))
        x = int((self.winfo_screenwidth() / 2) - (win_width / 2))
        self.geometry(f'{win_width}x{win_height}+{x}+{y}')
        self.resizable(False, False)
        self.title('Log In')
        
        # Initialize the background template frame and canvas
        self.main_frame = Widgets.CreateFrame(self)
        self.main_frame.pack(fill='both', expand='true')
        self.main_canvas = Widgets.CreateCanvas(self.main_frame)
        self.main_canvas.pack(fill='both', expand='true')
        
        # Create a window in the center of the screen to hold widgets
        top_left_x = win_width / 4
        top_left_y = win_height / 4
        bottom_right_x = win_width - top_left_x
        bottom_right_y = win_height - top_left_y
        self.main_canvas.create_rectangle(top_left_x, top_left_y,
                                          bottom_right_x, bottom_right_y,
                                          fill='#f8f8ff')
        self.canvas_window = self.main_canvas.create_window(win_width / 2,
                                                            win_height / 2)
        
        # Function to save user data if the window is exited
        self.protocol('WM_DELETE_WINDOW', self.OnClose)
    
    
    def LoadCreateAccountWindow(self):
        """Initialize the widgets used to create a new user account.
        
        This function is called by the 'Create New Account' button on the
            'Log In' window.
        """
        
        def CreateAccount():
            """Call the function to create a new account and log in.
            
            This function is called by the 'Create Account' button. If the
                user provided a valid username and the password fields match,
                the account will be created and the user will be asked to log
                into the account. If the user declines, the window resets back
                to the initial 'Log In' window.
            """
            
            if not self.CreateAccount():
                return
            
            # Offer to log the new user account in
            ask = messagebox.askyesno('Success!',
                                     f'Account created. Log in as {username}?')
            if ask:
                # Save data to the file and load the main program
                self.SaveData()
                self.main_frame.destroy()
                MainWindow.MainWindow(self, username, login_date=None)
            else:
                # Clear variable fields and return to initial 'Log In' window
                self.username.set('')
                self.password.set('')
                self.confirm_pass.set('')
                Return()
        
        def Return():
            """Erase 'Account Creation' widgets to load 'Log In' widgets.
            
            This function is called by the 'Return To Log In' button.
            """
            confirm_frame.forget()
            self.LoadLogInWindow()
        
        confirm_frame = Widgets.CreateFrame(self.main_canvas)
        self.main_canvas.itemconfigure(self.canvas_window,
                                       window=confirm_frame)
        
        # Create a button to create the account and a button to return to
        #   the 'Log In' window
        button_frame = Widgets.CreateFrame(confirm_frame)
        button_frame.pack(side='bottom')
        
        create_button = Widgets.CreateButton(button_frame,
                                             _text='Create Account',
                                             _cmd=CreateAccount,
                                             _height=self.button_height)
        create_button.pack(side='left')
        return_button = Widgets.CreateButton(button_frame,
                                             _text='Return To\nLog In',
                                             _cmd=Return,
                                             _height=self.button_height)
        return_button.pack(side='right')
        
        # Set the password fields to monitor if they match and update a label
        #   to show their status
        self.pass_match_label = Widgets.CreateLabel(confirm_frame, _text='',
                                                    _font=('georgia', 8))
        self.pass_match_label.pack(side='bottom')
        self.password.trace('w', self.PasswordMatch)
        self.confirm_pass.trace('w', self.PasswordMatch)
        self.PasswordMatch()
        
        # Create the 'Confirm Password', 'Password', and 'Username' fields
        widget_list = []
        confirm_entry = Widgets.CreateEntry(confirm_frame,
                                            _var=self.confirm_pass, _show='*')
        confirm_entry.pack(side='bottom')
        widget_list.append(confirm_entry)
        confirm_label = Widgets.CreateLabel(confirm_frame,
                                            _text='Confirm Password:')
        confirm_label.pack(side='bottom')
        
        pass_entry = Widgets.CreateEntry(confirm_frame,
                                         _var=self.password, _show='*')
        pass_entry.pack(side='bottom')
        widget_list.append(pass_entry)
        pass_label = Widgets.CreateLabel(confirm_frame, _text='Password:')
        pass_label.pack(side='bottom')
        
        user_entry = Widgets.CreateEntry(confirm_frame, _var=self.username)
        user_entry.pack(side='bottom')
        widget_list.append(user_entry)
        user_label = Widgets.CreateLabel(confirm_frame, _text='Username:')
        user_label.pack(side='bottom')
        
        # Entry fields are created bottom-to-top and their order in the window
        #   stack needs to be reversed and lifted so that 'Tab' navigates from
        #   top-to-bottom
        widget_list.reverse()
        for widget in widget_list:
            widget.lift()
    
    
    def LoadDatabase(self):
        """Load the user accounts information from the database file.
        
        This function opens the file containing user account information and
            loads the contents into a list. In the event that a new user is
            created or a user's password is updated, the information will be
            saved back to the database either before the main program launches
            or before the window is closed.
        
        Returns:
            db_data: If the user accounts file exists and is accessible, this
                        list contains the contents
                     If the file doesn't exist or is inaccessible, this list
                        is empty
        """
        
        db_data = []
        try:
            with open(self.users_file, 'r') as infile:
                db_data = json.load(infile)
        except IOError:
            # The database file is nonexistent or corrupt and should be
            #   created as a fresh file
            try:
                with open(self.users_file, 'x') as infile:
                    pass
            except:
                messagebox.showerror('Error', 'File creation operations not ' \
                                              'allowed in the current ' \
                                              'directory.\n User account ' \
                                              'information will not be saved.')
        except JSONDecodeError:
            messagebox.showerror('Error',
                                 f'Unable to load data from {self.users_file}')
        except:
            messagebox.showerror('Error', 'Unexpected error encountered.')
        
        return db_data
    
    
    def LoadForgotPasswordWindow(self):
        """Initialize the widgets used to change a user's password.
        
        This function is called by clicking on the 'Forgot Password?' label
            located on the 'Log In' window.
        """
        
        def ChangePassword():
            """Call the function to change the user's password.
            
            This function is called by the 'Change Password' button.
            """
            if self.ChangePassword():
                # Update successful, return to main screen
                self.confirm_pass.set('')
                self.password.set('')
                Return()
            else:
                return
        
        def Return():
            """Erase 'Forgot Password' widgets to load 'Log In' widgets.
            
            This function is called by the 'Return To Log In' button.
            """
            forgot_frame.forget()
            self.LoadLogInWindow()
        
        forgot_frame = Widgets.CreateFrame(self.main_canvas)
        self.main_canvas.itemconfigure(self.canvas_window, window=forgot_frame)
        
        # Create a button to change the password and a button to return to
        #   the initial 'Log In' window
        button_frame = Widgets.CreateFrame(forgot_frame)
        button_frame.pack(side='bottom')
        
        change_button = Widgets.CreateButton(button_frame,
                                             _text='Change Password',
                                             _cmd=ChangePassword,
                                             _height=self.button_height)
        change_button.pack(side='left')
        return_button = Widgets.CreateButton(button_frame,
                                             _text='Return To\nLog In',
                                             _cmd=Return,
                                             _height=self.button_height)
        return_button.pack(side='right')
        
        # Set the password fields to monitor if they match and update a label
        #   to show their status
        self.pass_match_label = Widgets.CreateLabel(forgot_frame, _text='',
                                                    _font=('georgia', 8))
        self.pass_match_label.pack(side='bottom')
        self.password.trace('w', self.PasswordMatch)
        self.confirm_pass.trace('w', self.PasswordMatch)
        self.PasswordMatch()
        
        # Create the 'Confirm Password', 'New Password', and 'Username' fields
        widget_list = []
        confirm_entry = Widgets.CreateEntry(forgot_frame,
                                            _var=self.confirm_pass,
                                            _show='*')
        confirm_entry.pack(side='bottom')
        widget_list.append(confirm_entry)
        confirm_label = Widgets.CreateLabel(forgot_frame,
                                            _text='Confirm Password:')
        confirm_label.pack(side='bottom')
        
        new_pass_entry = Widgets.CreateEntry(forgot_frame, _var=self.password,
                                             _show='*')
        new_pass_entry.pack(side='bottom')
        widget_list.append(new_pass_entry)
        new_pass_label = Widgets.CreateLabel(forgot_frame,
                                             _text='New Password:')
        new_pass_label.pack(side='bottom')
        
        user_entry = Widgets.CreateEntry(forgot_frame, _var=self.username)
        user_entry.pack(side='bottom')
        widget_list.append(user_entry)
        user_label = Widgets.CreateLabel(forgot_frame, _text='Username:')
        user_label.pack(side='bottom')
        
        # Entry fields are created bottom-to-top and their order in the window
        #   stack needs to be reversed and lifted so that 'Tab' navigates from
        #   top-to-bottom
        widget_list.reverse()
        for widget in widget_list:
            widget.lift()
    
    
    def LoadLogInWindow(self):
        """Initialize the widgets used to log in to an account."""
        
        def CreateAccount():
            """Erase 'Log In' widgets to load 'Account Creation' widgets.
            
            This function is called by the 'Create New Account' button.
            """
            login_frame.forget()
            self.LoadCreateAccountWindow()
        
        def ForgotPassword():
            """Erase 'Log In' widgets to load 'Forgot Password' widgets.
            
            This function is called by clicking on the 'Forgot Password' label.
            """
            login_frame.forget()
            self.LoadForgotPasswordWindow()
        
        def LogIn():
            """Verify the user's credentials and load the main program.
            
            This function is called by the  'Log In' button.
            """
            result, user, date = self.CheckLogin()
            if result:
                # Save the database file and load the program
                self.SaveData()
                self.main_frame.destroy()
                MainWindow.MainWindow(self, user, login_date=date)
        
        login_frame = Widgets.CreateFrame(self.main_canvas)
        self.main_canvas.itemconfigure(self.canvas_window, window=login_frame)
        
        # Create a button to log in and a button to create a new account
        button_frame = Widgets.CreateFrame(login_frame)
        button_frame.pack(side='bottom')
        login_button = Widgets.CreateButton(button_frame,
                                            _text='Log In',
                                            _cmd=LogIn,
                                            _height=self.button_height)
        login_button.pack(side='left')
        create_button = Widgets.CreateButton(button_frame,
                                             _text='Create\nNew Account',
                                             _cmd=CreateAccount,
                                             _height=self.button_height)
        create_button.pack(side='right')
        
        # Create a clickable label to reset a user's password
        reset_label = Widgets.CreateLabel(login_frame,
                                          _text='Forgot Password?',
                                          _font=('georgia', 10))
        reset_label.pack(side='bottom')
        reset_label.bind('<Button-1>', lambda e:ForgotPassword())
        
        # Create the 'Password' and 'Username' fields
        widget_list = []
        pass_entry = Widgets.CreateEntry(login_frame, _var=self.password,
                                         _show='*')
        pass_entry.pack(side='bottom')
        widget_list.append(pass_entry)
        pass_label = Widgets.CreateLabel(login_frame, _text='Password:')
        pass_label.pack(side='bottom')
        
        user_entry = Widgets.CreateEntry(login_frame, _var=self.username)
        user_entry.pack(side='bottom')
        widget_list.append(user_entry)
        user_label = Widgets.CreateLabel(login_frame, _text='Username:')
        user_label.pack(side='bottom')
        
        # Entry fields are created bottom-to-top and their order in the window
        #   stack needs to be reversed and lifted so that 'Tab' navigates from
        #   top-to-bottom
        widget_list.reverse()
        for widget in widget_list:
            widget.lift()
    
    
    def OnClose(self):
        """Save user account data before exiting the program."""
        self.SaveData()
        self.destroy()
    
    
    def PasswordMatch(self, *args):
        """Verify that the 'Password' and 'Confirm Password' fields match.
        
        This function is called whenever the contents of either of the password
            entry fields changes. It updates the text on a label to reflect
            the matching status to the user.
        
        Returns:
        'True' if the fields contain identical contents.
        'False' if they don't.
        """
        pass1 = self.password.get().lstrip().rstrip()
        pass2 = self.confirm_pass.get().lstrip().rstrip()
        
        if (pass1 and pass1 == pass2):
            self.pass_match_label['text'] = 'Passwords match'
            self.pass_match_label['fg'] = 'green'
            return True
        else:
            self.pass_match_label['text'] = 'Password don\'t match'
            self.pass_match_label['fg'] = 'red'
            return False
    
    
    def SaveData(self):
        """Save user account information to the database file."""
        
        try:
            with open(self.users_file, 'r+') as outfile:
                json.dump(self.user_db, outfile, indent=4)
                outfile.truncate()
        except:
            messagebox.showerror('Error',
                                 f'{self.users_file} could not be accessed.' \
                                 'New user information won\'t be saved')