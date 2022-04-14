#-----------------------------------------------------------------------------#
#   File:   LogInLogic.py                                                     #
#   Author: Logan Pierceall                                                   #
#                                                                             #
#   This module contains the backend code utilized by the Log In window. The  #
#       frontend code can be found in LogInWindow.py                          #
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

# Helps to format all JSON-serialized data
JSON_INDENT = 4



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
    if not confirm_password:
        return False, 'Please confirm the password.'
    
    # Ensure that the passwords match
    if password != confirm_password:
        return False, 'Passwords must match.'
    
    # Update the user's password
    try:
        with open(USER_INFO, 'r+') as file:
            existing_data = json.load(file)
            for entry in existing_data:
                if entry['User'] == username:
                    entry['Password'] = password
                    file.seek(0)
                    json.dump(existing_data, file, indent = JSON_INDENT)
                    file.truncate()
                    return True, 'Password successfully changed!'
        
        # Returns if the username isn't found within USER_INFO
        return False, f'{username} not found.'
    
    except IOError:
        # USER_INFO is non-existent or otherwise inaccessible
        return False, f'Unable to access {USER_INFO}'
    
    except JSONDecodeError:
        # USER_INFO is empty
        return False, f'No data found in {USER_INFO}'
    
    except:
        return False, 'Unexpected error encountered'



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
                        return True, None
                    else:
                        return False, 'Invalid password'
        
        # Return False if the username isn't found
        return False, f'{username} is not a valid account'
    
    except IOError:
        # USER_INFO is non-existent or otherwise inaccessible
        return False, f'Unable to access {USER_INFO}'
    
    except JSONDecodeError:
        # USER_INFO is empty
        return False, f'No data found in {USER_INFO}'
    
    except:
        return False, 'Unexpected error encountered'



# CreateAccount() prepares a new user dictionary object to add to the
#   USER_INFO database file.
# Args:     username = the new user's username
#           password = the new user's password
# Returns:  
def CreateAccount(username, password):

    # Prepare the user info for JSON
    user = {
        'User': username,
        'Password': password,
        'CreationDate': date.today().strftime('%B %d, %Y'),
        'LastLogIn': ''
    }
    
    try:
        with open(USER_INFO, 'r+') as outfile:
            existing_data = json.load(outfile)
            existing_data.append(user)
            outfile.seek(0)
            json.dump(existing_data, outfile, indent = JSON_INDENT)
            outfile.truncate()
    
    except (IOError, JSONDecodeError):
        # User file doesn't exist or is corrupted/empty. Open in 'w+' mode to
        #   create a fresh file
        new_list = [user]
        
        try:
            with open(USER_INFO, 'w+') as outfile:
                json.dump(new_list, outfile, indent = JSON_INDENT)
                outfile.truncate()
        
        except:
            # Further errors indicate the user can't be added
            return False, 'Unexpected error encountered. Account not created.'
            
    except:
        # Any other errors likely resulted in the user not being added
        return False, 'Unexpected error encountered. Account not created.'
    
    # Send the username to the AddNewUser() function in MainLogic.py to add
    #   the user to a file containing each user's quiz database files
    result, msg = MainLogic.AddNewUser(username)
    return True, None



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
                    # Retrieve the last log-in date, then update the last date
                    #   to reflect the current activity
                    previous_login = entry['LastLogIn']
                    entry['LastLogIn'] = date.today().strftime('%B %d, %Y')
            file.seek(0)
            json.dump(existing_data, file, indent = JSON_INDENT)
            file.truncate()
            
            return previous_login

    except:
        return None