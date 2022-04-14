#-----------------------------------------------------------------------------#
#   File:   CreateDBLogic.py                                                  #
#   Author: Logan Pierceall                                                   #
#                                                                             #
#   This module contains the backend code utilized by CreateDBWindow.py       #
#-----------------------------------------------------------------------------#

import os
import json
from json.decoder import JSONDecodeError

import MainWindow

# Holds all of the dictionary objects containing question info after they've
#   been serialized by the JSONidy() function
dict_objects = []

# Helps to format all JSON-serialized data
JSON_INDENT = 4



# CheckFields() validates the info provided by the user in the Database
#   Creation window. If all of the info is valid, it will be passed to
#   the JSONify() function to prepare it for eventual serialization
# Args:     question         = the question text
#           initial_q_text   = 'Question' box default placeholder text
#           answers          = list of answer texts
#           initial_ans_text = 'Answer' box default placeholder text
#           cb_vals          = list of 'Correct Answer' check button values
# Returns:  True if all checks are passed
#           False and an error message if one of the checks fails
def CheckFields(question, initial_q_text, answers, initial_ans_text, cb_vals):
    
    # Ensure the question box was populated
    if not question or question == initial_q_text:
        return False, 'No question entered'
    
    # Ensure at least one answer was marked correct
    no_corrects = True
    for cb in cb_vals:
        if cb == 1:
            no_corrects = False
            break
    if no_corrects:
        return False, 'No answers were marked as correct'
    
    # Ensure no answer boxes were left unpopulated while also being marked as
    #   a correct answer
    index = 0
    for answer in answers:
        if not answer or answer == initial_ans_text:
            if cb_vals[index] == 1:
                msg = f'Answer {index + 1} wasn\'t populated but ' \
                      'was marked as a correct answer'
                return False, msg
        index += 1
    
    # If all checks pass, prepare the information in JOSN format
    JSONify(question, answers, cb_vals, initial_ans_text)
    return True, None



# FinalCheck() is called before finalizing the file creation. If all of the
#   fields were left empty, proceed to serializing the data. Otherwise,
#   the data should be recorded and it is passed to CheckFields()
# Args:     question         = the question text
#           initial_q_text   = 'Question' box default placeholder text
#           answers          = list of answer texts
#           initial_ans_text = 'Answer' box default placeholder text
#           cb_vals          = list of 'Correct Answer' check button values
# Returns:  
def FinalCheck(question, initial_q_text, answers, initial_ans_text, cb_vals):

    # Flags to mark failed checks
    question_flag       = False
    answer_entries_flag = False
    correct_answer_flag = False

    # Check for an empty question entry
    if not question or question == initial_q_text:
        question_flag = True
    
    # Check if all answer entries were left empty
    empty_answers = 0
    for answer in answers:
        if not answer or answer == initial_ans_text:
            empty_answers += 1
    if empty_answers == len(answers):
        answer_entries_flag = True
    
    # Check if any 'correct answer' check buttons were marked
    empty_checks = 0
    for value in cb_vals:
        if value == 0:
            empty_checks += 1
    if empty_checks == len(cb_vals):
        correct_answer_flag = True
    
    # If all checks failed, return True to continue to finalizing the data.
    #   Otherwise, return False and record the entered data before finalizing
    #   the data
    if question_flag and answer_entries_flag and correct_answer_flag:
        return True
    else:
        return False



# JSONify() inserts the user-provided info into a dictionary structure that
#   then gets added to a list. Once the file creation is finished, the
#   list will be written to a file.
# Args:     question        = the question string
#           answers         = the list of answer strings
#           cb_vals         = the list of check button values
#           intial_ans_text = the string initially inserted into answer boxes
# Returns:  none
def JSONify(question, answers, cb_vals, initial_ans_text):

    # Tally the entries marked as correct
    num_correct = 0
    for val in cb_vals:
        if val == 1:
            num_correct += 1
    
    # Determine if the question has a single answer or multiple
    if num_correct == 1:
        q_type = 'single'
    else:
        q_type = 'multi'

    # Initialize the new dict object
    new_entry = {
        "Type": q_type,
        "Question": question
    }
    
    # Holds the number of total characters in all of the answer entries
    ans_char_count = 0
    
    # Insert the answer entries, omitting any left unpopulated. Also tally
    #   the number of answer options
    index = 1
    ans_count = 0
    for entry in answers:
        if not entry or entry == initial_ans_text:
            continue
        ans_count += 1
        ans_char_count += len(entry)
        key_str = 'Answer' + str(index)
        new_entry.update({key_str: entry})
        index += 1
    
    # Insert the number of answer options
    new_entry.update({"NumOfAnswers": ans_count})
    
    # Insert the total number of characters in the answer strings
    new_entry.update({'CharCount': ans_char_count})
    
    # A single correct answer is entered directly into the dictionary, while
    #   multiple correct answers are first placed into a list
    ans_list = []
    index = 0
    for val in cb_vals:
        if val == 1:
            if num_correct == 1:
                new_entry.update({'Correct': answers[index]})
                break
            else:
                ans_list.append(answers[index])
        index += 1
    if ans_list:
        new_entry.update({'Correct': ans_list})
        
    # Add the new dictionary object to the list
    dict_objects.append(new_entry)



# SerializeDB() saves the contents of 'dict_objects' as a JSON file
# Args:     file = the filename chosen by the user
# Returns:  True and a success message if successful
#           False and an error message otherwise
def SerializeDB(file):

    try:
        with open(file, 'w') as outfile:
            json.dump(dict_objects, outfile, indent = JSON_INDENT)
        
        return True, f'{os.path.basename(file)} successfully saved!'
    
    except (IOError, JSONDecodeError):
        # Some system feature is preventing the file from being created
        return False, f'{os.path.basename(file)} could not be created'
    
    except:
        return False, 'Unexpected error encountered'