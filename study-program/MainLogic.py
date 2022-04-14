#-----------------------------------------------------------------------------#
#   File:   MainLogic.py                                                      #
#   Author: Logan Pierceall                                                   #
#                                                                             #
#   This module contains the backend code utilized by MainWindow.py           #
#                                                                             #
#   This code makes extensive use of the file containing each user's          #
#       personal quiz database files, which is saved as the variable          #
#       OPENED_DB_FILES. The default filename is 'previousfiles.json'. Each   #
#       user is a separate key, and the associated value is a list of         #
#       of database files.                                                    #
#-----------------------------------------------------------------------------#


import json
from json.decoder import JSONDecodeError
import os
from tkinter import filedialog

# File contains a dictionary object where each key value is a user who has
#   opened at least one database file. The value attached to that key is a
#   list of all database files that user has opened.
OPENED_DB_FILES = 'previousfiles.json'

# Helps to format all JSON-serialized data
JSON_INDENT = 4



# AddNewUser() is called by LogInLogic.py when a new user is created. This
#   user is added as a new key to the OPENED_DB_FILES database
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
        return True, None
    
    except (IOError, JSONDecodeError):
        # OPENED_DB_FILES either doesn't exist or is corrupted/empty. Open
        #   in 'w+' to create a fresh file
        new_data = {username : []}
        
        try:
            with open(OPENED_DB_FILES, 'w+') as file:
                json.dump(new_data, file, indent = JSON_INDENT)
                file.truncate()
            return True, None
        
        except:
            return False, 'Unexpected error encountered'
    
    except:
        return False, 'Unexpected error encountered'



# AddQuizFile() allows the user to add a new database file to their listbox
#   widget. This file is also added to their list of previously opened files
#   in the OPENED_DB_FILES file.
# Args:     listbox      = the current user's listbox widget
#           current_user = the currently logged-in user
#           file         = a file to add to the listbox
# Returns:  True if the operation was successful
#           False and an error message otherwise
def AddQuizFile(listbox, current_user, file = None):

    # If a file wasn't passed as an argument, let the user select one
    if not file:
        types = (('JSON Files', '*.json'),('All files', '*.*'))
        new_file = filedialog.askopenfilename(title = 'Select file...',
                                              filetypes = types)
    else:
        new_file = file
    
    if not new_file:
        # No file seleted, cancel operation
        return True, None
    
    try:
        with open(OPENED_DB_FILES, 'r+') as file:
            existing_data = json.load(file)
                
            # Check if the file is already in the list to avoid duplicates
            for entry in existing_data[current_user]:
                if entry == new_file:
                    return False, 'File aleady present in the list'
                
            # Add the file to the user's list
            existing_data[current_user].append(new_file)
            file.seek(0)
            json.dump(existing_data, file, indent = JSON_INDENT)
            file.truncate()
        
    except (JSONDecodeError, IOError):
        # OPENED_DB_FILES either doesn't exist or is corrupted/empty. Open
        #   in 'w+' to create a fresh file
        new_data = {
            current_user: [new_file]
        }
        
        try:        
            with open(OPENED_DB_FILES, 'w+') as file:
                json.dump(new_data, file, indent = JSON_INDENT)
        
        except:
            return False, 'An unexpected error has ocurred'
        
    except:
        return False, 'An unexpected error has ocurred'
        
    # Add the filename to the listbox
    listbox.insert('end', os.path.basename(new_file))

    return True, None



# GetFilename() searches the list of previously opened files for the given user
#   and returns the filename at the given position
# Args:     file_selection = the list index of the filename to return
#           current_user   = the currently logged-in user
# Returns:  True and a filename if successful
#           False and an error message otherwise
def GetFilename(file_selection, current_user):

    try:
        with open(OPENED_DB_FILES, 'r') as infile:
            existing_data = json.load(infile)
            
            # Retrieve the current user's file list
            user_files = existing_data[current_user]
            
        return True, user_files[file_selection]
    
    except IOError:
        # OPENED_DB_FILES is non-existent or otherwise inaccessible
        return False, f'Unable to access {OPENED_DB_FILES}'
    
    except JSONDecodeError:
        # OPENED_DB_FILES is empty
        return False, f'No data found in {OPENED_DB_FILES}'

    except:
        return False, 'Unexpected error encountered'



# LoadQuiz() receives a list of user-selected database files and loads their
#   contents into a quiz list.
# Args:     files_index_list = list of indeces that indicate the files to
#                                  from the user's file list
#           current_user     = the currently logged-in user
# Returns:  True and a populated quiz if successful
#           False, an error message, and an empty quiz otherwise
def LoadQuiz(files_index_list, current_user):

    quiz = []       # Holds all quiz contents
    msg = ''        # Holds an error message (if needed)
    
    try:
        with open(OPENED_DB_FILES, 'r') as infile:
            existing_data = json.load(infile)
    
    except (JSONDecodeError, IOError):
        # OPENED_DB_FILES is non-existent or otherwise inaccessible
        return False, f'Unable to access {OPENED_DB_FILES}', None
    
    except:
        return False, 'Unexpected error encountered', None
            
    # Retrieve the user's personal file list
    user_files = existing_data[current_user]
    
    for index in files_index_list:
        try:
            with open(user_files[index], 'r+') as infile:
                quiz.extend(json.load(infile))
        
        except (JSONDecodeError, IOError):
            # Record the name of the file that couldn't be accessed
            filename = os.path.basename(user_files[index])
            msg += f'Error accessing {filename}\n'
            
    if not quiz:
        # No files could be loaded, operation failed
        return False, 'No selected files could be accessed', None
    else:
        return True, msg, quiz



# PopulateListbox() accesses the OPENED_DB_FILES database file, finds the
#   given user, and fills the listbox with the given user's previously
#   opened files
# Args:     user    = the currently logged-in user
#           listbox = the current user's listbox widget
# Returns:  none
def PopulateListbox(user, listbox):

    try:
        with open(OPENED_DB_FILES, 'r') as infile:
            existing_data = json.load(infile)
            for entry in existing_data[user]:
                listbox.insert('end', os.path.basename(entry))
        
        return True, None
    
    except IOError:
        # OPENED_DB_FILES is non-existent or otherwise inaccessible
        return False, f'Unable to access {OPENED_DB_FILES}'
    
    except JSONDecodeError:
        # OPENED_DB_FILES is empty
        return False, f'No data found in {OPENED_DB_FILES}'
    
    except:
        return False, 'Unexpected error encountered'



# RemoveFile() removes one or more files from the user's list within 
#   OPENED_DB_FILES
# Args:     file_list = the list of files to remove
#           user      = the currently logged in user
# Returns:  none
def RemoveFile(file_list, user):

    try:
        with open(OPENED_DB_FILES, 'r+') as file:
            existing_data = json.load(file)
            
            # Find the index for each file
            for selection in file_list:
                index = 0
                for entry in existing_data[user]:
                    if entry == selection:
                        break
                    index += 1
                
                # Remove the file
                existing_data[user].pop(index)
            
            # Save the data back to the file
            file.seek(0)
            json.dump(existing_data, file, indent = JSON_INDENT)
            file.truncate()
            
            return True, None
    
    except IOError:
        # OPENED_DB_FILES is non-existent or otherwise inaccessible
        return False, f'Unable to access {OPENED_DB_FILES}'
    
    except JSONDecodeError:
        # OPENED_DB_FILES is empty
        return False, f'No data found in {OPENED_DB_FILES}'
    
    except:
        return False, 'Unexpected error encountered'