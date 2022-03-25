#-----------------------------------------------------------------------------#
# CreateDBLogic.py                                                            #
# Author: Logan Pierceall                                                     #
# Date: March 14, 2022                                                        #
#-----------------------------------------------------------------------------#

import os
import json
from json.decoder import JSONDecodeError

# Holds all of the dictionary objects containing question info after they've
#   been serialized by the JSONidy() function
dict_objects = []
JSON_INDENT = 4         # Helps to format all JSON-serialized data



# CheckFields() validates the info provided by the user in the Database
#   Creation window. If all of the info is valid, it will be passed to
#   the JSONify() function to prepare it for eventual serialization
# Args:     question = text entered into the 'Question' box
#           initial_q_text = the text initally placed into the 'Question'
#                            box when the widget is created
#           answers = a list containing all of the text entered into each
#                     individual 'Answer' box
#           initial_ans_text = the text initially placed into the 'Answer'
#                              boxes when the widgets are created
#           cb_vals = a list containing the value of all the 'Correct Answer'
#                     check boxes. "1" indicates the box was checked
#           finish_flag = a boolean indicating if this function is being called
#                         by the 'Save & Finish' button
# Returns:  True and an empty string if all checks are passed
#           False and an error message if one of the checks fails
def CheckFields(question, initial_q_text, answers, initial_ans_text, cb_vals,
                finish_flag):
    
    # Check that the question field wasn't left empty and doesn't contain the
    #   initial string contents
    q_flag = False
    if question == '' or question == initial_q_text:
        q_flag = True
    
    # Check the answer fields and record the index of every field left empty
    #   so that they can be compared to the checkbutton values. An answer
    #   marked 'correct' that was also left empty will throw an error
    ans_flag = True
    ans_empties = []
    index = 0
    for entry in answers:
        if entry != '' and entry != initial_ans_text:
            ans_flag = False
        else:
            ans_empties.append(index)
        index += 1
    
    # Check the checkbutton values to ensure at least one answer was marked as
    #   'correct' and record the index of all entries marked 'correct' to
    #   compare them to the empty answers list
    cb_flag = True
    cb_corrects = []
    index = 0
    for val in cb_vals:
        if val == 1:
            cb_flag = False
            cb_corrects.append(index)
        index += 1
        
    # First check 'finish_flag'. If it's true, and if all fields were left
    #   empty, assume this was done intentionally and return without any
    #   further processing
    if (finish_flag and q_flag and ans_flag and cb_flag):
        return True, ''
    
    # If the question field was left upopulated, throw an error
    if q_flag:
        return False, 'No question entered!'
    
    # If all answer fields were left unpopulated, throw an error
    if ans_flag:
        return False, 'At least one answer option must be populated.'
    
    # If no checkbuttons were marked, throw an error
    if cb_flag:
        return False, 'At least one answer must be marked correct.'
    
    # If an answer was marked correct but no information was entered into the
    #   field by the user, throw an error
    for val in cb_corrects:
        for entry in ans_empties:
            if val == entry:
                return False, 'An empty answer was marked as correct'
    
    # If all checks pass, pass the info to JSONify() to prepare for
    #   serialization
    JSONify(question, answers, cb_vals, initial_ans_text)
    return True, ''



# JSONify() inserts the user-provided info into a dictionary structure that
#   then gets added to a list. Once the file creation is finished, the
#   list will be written to a file.
# Args:     question = the question string
#           answers = the list of answer strings
#           cb_vals = the list of check button values
#           intial_ans_text = the string initially inserted into answer boxes
# Returns:  none
def JSONify(question, answers, cb_vals, initial_ans_text):

    # Check how many entries were marked correct
    num_correct = 0
    for val in cb_vals:
        if val == 1:
            num_correct += 1
    
    # If only one correct answer, the question type is single answer. More than
    #   one correct is a multiple choice
    if num_correct == 1:
        q_type = 'single'
    else:
        q_type = 'multi'

    # Initialize the new dict object
    new_entry = {
        "Type": q_type,
        "Question": question
    }
    
    # Insert the number of answer options, omitting any entries left empty or
    #   as the initial string inserted into the text box object
    count = 0
    for entry in answers:
        if entry == '' or entry == initial_ans_text:
            continue
        count += 1
    new_entry.update({"NumOfAnswers": count})
    
    # Insert the individual answer entries, omitting any entries left empty or
    #   as the initial string inserted into the text box object
    index = 1
    for entry in answers:
        # If the answer entry box was left blank, omit it
        if entry == '' or entry == initial_ans_text:
            continue
        
        key_str = 'Answer' + str(index)
        new_entry.update({key_str: entry})
        index += 1
    
    # A single correct answer is entered directly into the dictionary, while
    #   multiple correct answers are first placed into a list
    ans_list = []
    index = 0
    for val in cb_vals:
        if val == 1:
            if num_correct == 1:
                new_entry.update({'Correct': answers[index]})
            else:
                ans_list.append(answers[index])
        index += 1
    if len(ans_list) > 0:
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
    
    except IOError:
        return False, f'{os.path.basename(file)} could not be created'
    
    except JSONDecodeError:
        return False, f'Unable to write to {os.path.basename(file)}'
    
    except:
        return False, 'Unexpected error encountered'