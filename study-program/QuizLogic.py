#-----------------------------------------------------------------------------#
#   QuizLogic.py                                                              #
#   Author: Logan Pierceall                                                   #
#-----------------------------------------------------------------------------#

import random


# CheckCB() determines if the user-chosen answers to a multiple answer question
#   were the correct answers
# Args:     user_choices = the index list of answer options chosen
#           entry        = the current quiz question
# Returns:  True if the user chose all of the correct answers
#           False and the list of user-chosen answers otherwise
def CheckCB(user_choices, entry):
    
    # Convert the user's button choices into text answers
    user_answers = []
    for index in user_choices:
        user_answers.append(entry['Answer' + str(index)])
    
    # If the user provided too few or too many answers, return without checking
    if (len(user_answers) < len(entry['Correct']) or
        len(user_answers) > len(entry['Correct'])):
        return False, user_answers
    
    # Copy the 'correct' list to avoid altering the 'entry' object
    correct_answers = entry['Correct'].copy()
    
    # Check the user's answers against the correct list
    for answer in user_answers:
        index = 0
        found = False
        for correct in correct_answers:
            if answer == correct:
                found = True
                break
            index += 1
        
        # If a match was found, remove that answer from the correct list
        if found:
            correct_answers.pop(index)
    
    # If no correct answers remain in the list, the user chose them all
    if correct_answers:
        return False, user_answers
    else:
        return True, None



# CheckRadio() determines if the user-chosen answer to a single answer question
#   is correct
# Args:     answer_index = the number of the answer string chosen
#           entry        = the current quiz question
# Returns:  True if the answer is correct
#           False otherwise
def CheckRadio(answer_index, entry):

    user_answer = entry['Answer' + str(answer_index)]
    correct_answer = entry['Correct']

    if user_answer == correct_answer:
        return True
    else:
        return False



# GetAnswer() retrieves a single answer string
# Args:     index = the numbered answer to retrieve
#           entry = the current quiz question
# Returns:  the answer string
def GetAnswer(index, entry):

    return entry['Answer' + str(index)]



# GetAnswerCount() retrieves the number of answer options for a given quiz
#   entry
# Args:     entry = the current quiz question dictionary
# Returns:  the integer number of possible answers
def GetAnswerCount(entry):
    
    return entry['NumOfAnswers']



# GetCBVars() iterates through the list of answer option checkbutton variables
#   and collects the indeces of the options chosen by the user
# Args:     cb_list      = the list of checkbutton variables
#           answers_list = the list of answer options
# Returns:  a list of integers representing the answer strings chosen
def GetCBVars(cb_list, answers_list):

    index = 0
    chosen_answers = []
    for cb in cb_list:
        if cb.get() == 1:
            chosen_answers.append(answers_list[index])
        index += 1
    
    return chosen_answers



# GetCharCount() retrieves the total number of characters in all of the answer
#   options
# Args:     entry = the current quiz question
# Returns:  the integer amount of characters
def GetCharCount(entry):

    return entry['CharCount']



# GetEntry() retrieves a quiz question object from the list, if one exists
# Args:     quiz = the list containing all quiz question objects
# Returns:  a single quiz question object if one exists
#           'None' otherwise
def GetEntry(quiz):

    try:
        return quiz.pop()
    except:
        return None



# GetQuestion() returns the question text for the current quiz question
# Args:     entry = the current quiz question
# Returns:  the question string
def GetQuestion(entry):

    return entry['Question']



# ShuffleAnswers() creates a list of integers as long as the number of answer
#   options for the current question and shuffles that order to help create a
#   randomized presentation of answers
# Args:     entry = the current quiz question
# Returns:  a randomly shuffled list of integers
def ShuffleAnswers(entry):

    ans_list = []
    for i in range(1, entry['NumOfAnswers'] + 1):
        ans_list.append(i)
    random.shuffle(ans_list)
    return ans_list