#-----------------------------------------------------------------------------#
#   LogInLogic.py                                                             #
#   Author: Logan Pierceall                                                   #
#   Date: March 9, 2022                                                       #
#                                                                             #
#   This file contains the backend code utilized by the Log In window. The    #
#       frontend code can be found within LogInWindow.py                      #
#                                                                             #
#   This code primarily maintains the file containing user information, which #
#       is saved as the variable USER_INFO. The USER_INFO file is a JSON file #
#       where every entry has the following format:                           #
#           User:           the account username for the given entry          #
#           Password:       the user's login password                         #
#           CreationDate:   the date the account was created                  #
#           LastLogIn:      the last known date that the account was used     #
#   All fields are strings, and all dates use the format 'Month DD, YYYY'     #
#-----------------------------------------------------------------------------#

from datetime import date
import json
from json.decoder import JSONDecodeError

import LogInWindow
import MainLogic

# The 'users.json' file contains a list of users and their passwords
USER_INFO = 'users.json'

JSON_INDENT = 4         # Helps to format all JSON-serialized data



# ChangePassword() is used to reset a user's password. It verifies that none of
#   the passed arguments are empty and that the passwords match before updating
#   the user's info within the USER_INFO file
# Args:     username = the user account to update
#           password = the desired new password
#           confirm_password = confirmation of the desired password
# Returns:  True and a confirmation if the password was successfully updated
#           False and an error message otherwise
def ChangePassword(username, password, confirm_password):

    # Ensure the username field isn't empty
    if not username:
        return False, 'No username entered!'

    # Ensure both password fields aren't empty
    if not password:
        return False, 'No password entered.'
    elif not confirm_password:
        return False, 'Please confirm the password.'
    
    # Ensure that the passwords match
    if password != confirm_password:
        return False, 'Passwords must match.'
    
    # Update the user's password
    try:
        with open(USER_INFO, 'w+') as file:
            existing_data = json.load(file)
            for entry in existing_data:
                if entry['User'] == username:
                    entry['Password'] = password
                    file.seek(0)
                    json.dump(existing_data, file, indent = JSON_INDENT)
                    file.truncate()
                    return True, 'Password successfully reset!'
        
        # Returns if the username isn't found within USER_INFO
        return False, f'{username} not found.'
    
    # Exception catches if the USER_INFO file doesn't exist
    except IOError:
        return False, GetErrorMessage('IOError')
    
    # Exception catches an empty or corrupted USER_INFO file
    except JSONDecodeError:
        return False, GetErrorMessage('JSONDecodeError')
    
    # Exception catches all other errors
    except:
        return False, GetErrorMessage('')



# CheckLogin() validates the user-provided username and password against info
#   stored in the USER_INFO database. If the username is found and the correct
#   password was supplied, the user will be logged in. A descriptive error
#   message will be returned otherwise
# Args:     username = the user-provided username string to check
#           password = the user-provided password string to check
# Returns:  True and an empty string if the info is valid
#           False and an error message otherwise
def CheckLogin(username, password):

    try:
        with open(USER_INFO) as file:
            existing_data = json.load(file)
            for entry in existing_data:
                if entry['User'] == username:
                    if entry['Password'] == password:
                        return True, ''
                    else:
                        return False, 'Incorrect password'
        
        # Return False if the username isn't found
        return False, f'{username} is not a valid account'
    
    # Exception catches a non-existent USER_INFO file
    except IOError:
        return False, GetErrorMessage('IOError')
    
    # Exception catches an empty or corrupted USER_INFO file
    except JSONDecodeError:
        return False, GetErrorMessage('JSONDecodeError')
    
    # Exception catches all other errors
    except:
        return False, GetErrorMessage('')



# CreateAccount() creates a new entry in the USER_INFO file containing the
#   given username and password combination, the date of account creation, and
#   a placeholder for the last log-in date
# Args:     username = the new account's username
#           password = the new account's password
# Returns:  True and a confirmation message if successful
#           False and an error message if unable to create the account
def CreateAccount(username, password):

    user = {
        'User': username,
        'Password': password,
        'CreationDate': date.today().strftime('%B %d, %Y'),
        'LastLogIn': ''
    }
    
    try:
        with open(USER_INFO, 'r+') as file:
            existing_data = json.load(file)
            existing_data.append(user)
            file.seek(0)
            json.dump(existing_data, file, indent = JSON_INDENT)
            file.truncate()
        
    # If the USER_INFO file exists but is not populated, JSON throws an error
    #   when trying to load data. Instead, dump data without attempting to load
    except JSONDecodeError:
        new_list = [user]
        with open(USER_INFO, 'r+') as file:
            json.dump(new_list, file, indent = JSON_INDENT)
            file.truncate()
    
    # If the USER_INFO file doesn't exist, an IOError is throw. Open the file
    #   in 'w+' mode so it gets created before opening
    except IOError:
        new_list = [user]
        with open(USER_INFO, 'w+') as file:
            json.dump(new_list, file, indent = JSON_INDENT)
            file.truncate()
        
    # Exception catches all other errors
    except:
        return False, False, 'Account unable to be created.'
    
    # If the account was created, send the username to the AddNewUser()
    #   function in MainLogic.py in order to add it to the database that
    #   tracks a user's quiz files
    result, msg = MainLogic.AddNewUser(username)
    
    if result:
        msg = f'Account created for {username}.\nLog in as {username}?'
    return True, result, msg



# GetErrorMessage() is used to return error messages for all errors associated
#   with operations involving USER_INFO
# Args:     error_type = a string indicating the error type
# Returns:  the specific error message string
def GetErrorMessage(error_type):
    # Error message for a non-existent USER_INFO file
    if error_type == 'IOError':
        return f'Error opening {USER_INFO}'
    
    # Error message for an empty or corrupted USER_INFO file
    elif error_type == 'JSONDecodeError':
        return f'Error loading information from {USER_INFO}'
    
    # Error message for all other unexpected errors
    else:
        return 'Unexpected error encountered'



# GetLastLogIn() retrieves the previous log-in date for the given user before
#   updating the entry for the current log-in action
# Args:     username = the user account to access
# Returns:  the 'LastLogIn' key value if the user data is found
#           an error message should an exception occur
def GetLastLogIn(username):

    try:
        with open(USER_INFO, 'r+') as file:
            existing_data = json.load(file)
            for entry in existing_data:
                if entry['User'] == username:
                    # Retrieve the last log-in date then update the last date
                    #   to reflect the current activity
                    previous_login = entry['LastLogIn']
                    entry['LastLogIn'] = date.today().strftime('%B %d, %Y')
            file.seek(0)
            json.dump(existing_data, file, indent = JSON_INDENT)
            file.truncate()

    except:
        previous_login = 'Error encountered'
    
    return previous_login