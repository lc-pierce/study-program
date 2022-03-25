#-----------------------------------------------------------------------------#
#   MainLogic.py                                                              #
#   Author: Logan Pierceall                                                   #
#   Date: March 11, 2022                                                      #
#-----------------------------------------------------------------------------#


import json
from json.decoder import JSONDecodeError
import os
from tkinter import filedialog

import QuizList

# File contains a dictionary object where each key value is a user who has
#   opened at least one database file. The value attached to that key is a
#   list of all database files that user has opened.
OPENED_DB_FILES = 'previousfiles.json'

JSON_INDENT = 4     # Helps to format all JSON-serialized data



# AddNewUser() is called by LogInLogic.py when a new user is created. This
#   user is added as a new key to the OPENED_DB_FILES database and given an
#   empty list as its value.
# Args:     username = the new user account
# Returns:  none
def AddNewUser(username):

    try:
        with open(OPENED_DB_FILES, 'r+') as file:
            existing_data = json.load(file)
            existing_data[username] = []
            file.seek(0)
            json.dump(existing_data, file, indent = JSON_INDENT)
            file.truncate()
        return True, ''
    
    # If the OPENED_DB_FILES file doesn't exist or isn't populated, open in
    #   'w+' mode to createthe file first and dump the user info without
    #   attempting to load it
    except (IOError, JSONDecodeError):
        new_data = {username : []}
        with open(OPENED_DB_FILES, 'w+') as file:
            json.dump(new_data, file, indent = JSON_INDENT)
            file.truncate()
        return True, ''
    
    # All other unexpected errors
    except:
        return False, GetErrorMessage('')



# AddQuizFile() allows the user to add a new database file to their listbox
#   widget. This file is also added to their list of previously opened files
#   in the OPENED_DB_FILES file.
# Args:     listbox = the current user's listbox widget
#           current_user = the currently logged-in user
# Returns:  True and a confirmation message if the operation was successful
#           False and an error message otherwise
def AddQuizFile(listbox, current_user):

    new_file = filedialog.askopenfilename(title = 'Select file...',
                                          filetypes = (('JSON Files', '*.json'),
                                                       ('All Files', '*.*')))

    if new_file:
        # Creates a new user entry for the OPENED_DB_FILES database 
        new_data = {
            current_user: [new_file]
        }
    
        try:
            with open(OPENED_DB_FILES, 'r+') as file:
                existing_data = json.load(file)
                
                # Check if the file is already in the list to avoid duplicates
                for entry in existing_data[current_user]:
                    if entry == new_file:
                        return False, 'File aleady exists'
                
                # Add the file to the list of files the current user has
                #   previously opened
                existing_data[current_user].append(new_file)
                file.seek(0)
                json.dump(existing_data, file, indent = JSON_INDENT)
                file.truncate()
                
            # Add the filename to the listbox
            listbox.insert('end', os.path.basename(new_file))
            return True, 'File added'
        
        # If the OPENED_DB_FILES file doesn't exist or isn't populated, open in
        #   'w+' mode to createthe file first and dump the user info without
        #   attempting to load it
        except JSONDecodeError:
            with open(OPENED_DB_FILES, 'w+') as file:
                json.dump(new_data, file, indent = JSON_INDENT)
                
            # Add the filename to the listbox
            listbox.insert('end', os.path.basename(new_file))
            return True, 'File added'
        
        # Exception catches all other unexpected errors
        except:
            return False, 'An unexpected error has ocurred'
    
    # If no file was selected, return with no message attached to prevent an
    #   error from being thrown
    else:
        return True, ''



# GetErrorMessage() is used to return error messages for all errors associated
#   with operations involving OPENED_DB_FILES
# Args:     error_type = a string indicating the error type
# Returns:  the specific error message string
def GetErrorMessage(error_type):

    # Error message for a non-existent OPENED_DB_FILES file
    if error_type == 'IOError':
        return f'Error opening {OPENED_DB_FILES}'
    
    # Error message for an empty or corrupted OPENED_DB_FILES file
    elif error_type == 'JSONDecodeError':
        return f'Error loading information from {OPENED_DB_FILES}'
    
    # Error message for all other unexpected errors
    else:
        return 'Unexpected error encountered'



# GetFilename() searches the list of previously opened files for the given user
#   and returns the filename at the given position
# Args:     file_selection = the list index of the filename to return
#           current_user = the currently logged-in user
# Returns:  True and a filename if successful
#           False and an error message otherwise
def GetFilename(file_selection, current_user):

    try:
        with open(OPENED_DB_FILES, 'r') as file:
            existing_data = json.load(file)
            user_files = existing_data[current_user]
            return True, user_files[file_selection]
    
    # Exception catches a non-existent OPENED_DB_FILES file
    except IOError:
        return False, GetErrorMessage('IOError')
    
    # Exception catches an empty or corrupted OPENED_DB_FILES file
    except JSONDecodeError:
        return False, GetErrorMessage('JSONDecodeError')
    
    # Exception catches all other errors
    except:
        return False, GetErrorMessage('')



# LoadQuiz() receives a list of user-selected listbox files and searches
#   through the given user's previously opened files to match the
#   selections and load the file's contents into a quiz list
# Args:     files_index_list = a list of int indeces representing the user's
#                              desired database files
#           current_user = the currently logged-in user
# Returns:  True, an empty string, and the quiz list object if successful
#           False, an error message, and an empty quiz otherwise
def LoadQuiz(files_index_list, current_user):

    # Create the QuizList object to hold the quiz information
    quiz = QuizList.QuizList()
    
    try:
        with open(OPENED_DB_FILES, 'r') as file:
            existing_data = json.load(file)
            for index in files_index_list:
                user_files = existing_data[current_user]
                result, msg = quiz.PopulateQuiz(user_files[index])
                if not result:
                    return False, msg, quiz
        
        return True, '', quiz
    
    # Exception catches a non-existent OPENED_DB_FILES file
    except IOError:
        return False, GetErrorMessage('IOError'), quiz
    
    # Exception catches an empty or corrupted OPENED_DB_FILES file
    except JSONDecodeError:
        return False, GetErrorMessage('JSONDecodeError'), quiz
    
    # Exception catches all other errors
    except:
        return False, GetErrorMessage(''), quiz



# PopulateListbox() accesses the OPENED_DB_FILES database file, finds the
#   given user, and fills the listbox with the given user's previously
#   opened files
# Args:     user = the currently logged-in user
#           listbox = the current user's listbox widget
# Returns:  none
def PopulateListbox(user, listbox):

    try:
        with open(OPENED_DB_FILES, 'r') as file:
            existing_data = json.load(file)
            for entry in existing_data[user]:
                listbox.insert('end', os.path.basename(entry))
        
        return True, ''
    
    # Exception catches a non-existent OPENED_DB_FILES file
    except IOError:
        return False, GetErrorMessage('IOError')
    
    # Exception catches an empty or corrupted OPENED_DB_FILES file
    except JSONDecodeError:
        return False, GetErrorMessage('JSONDecodeError')
    
    # Exception catches all other errors
    except:
        return False, GetErrorMessage('')



# RemoveFile() removes a given file from the listbox containing the given
#   user's previously opened files.
# Args:     filename = the file to remove from the list
#           user = the currently logged in user
# Returns:  none
def RemoveFile(filename, user):

    try:
        with open(OPENED_DB_FILES, 'r+') as file:
            existing_data = json.load(file)
            index = 0
            
            # Find the index for the appropriate file in the list
            for entry in existing_data[user]:
                if entry == filename:
                    file_index = index
                    break
                index += 1
            
            # Remove the file
            existing_data[user].pop(index)
            
            # Save the new data back to the file
            file.seek(0)
            json.dump(existing_data, file, indent = JSON_INDENT)
            file.truncate()
    
    # Exception catches a non-existent OPENED_DB_FILES file
    except IOError:
        return False, GetErrorMessage('IOError')
    
    # Exception catches an empty or corrupted OPENED_DB_FILES file
    except JSONDecodeError:
        return False, GetErrorMessage('JSONDecodeError')
    
    # Exception catches all other errors
    except:
        return False, GetErrorMessage('')