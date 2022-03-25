#-----------------------------------------------------------------------------#
#   QuizLogic.py                                                              #
#   Author: Logan Pierceall                                                   #
#   Date: March 12, 2022                                                      #
#-----------------------------------------------------------------------------#

import random

import QuizList

def CheckCB(user_choices, quiz, entry):

    # Retrieve the list of correct answers and count them
    correct_answers = quiz.GetCorrectAnswer(entry)
    total_corrects = len(correct_answers)
    
    # Convert the user's button choices into text answers
    user_answers = []
    for index in user_choices:
        user_answers.append(quiz.GetAnswer(index, entry))
    
    # Check the user's answers against the correct list and increment the
    #   number found to be correct
    num_of_corrects = 0
    for answer in user_answers:
        for correct_answer in correct_answers:
            if answer == correct_answer:
                num_of_corrects += 1
                break
    
    if num_of_corrects == total_corrects:
        return True
    else:
        return False



def CheckRadio(user_answer, quiz, entry):

    if quiz.GetAnswer(user_answer, entry) == quiz.GetCorrectAnswer(entry):
        return True
    else:
        return False



def GetAnswer(index, quiz, entry):

    return quiz.GetAnswer(index, entry)



def GetCBVars(cb_list, answers_list):

    index = 0
    chosen_list = []
    for cb in cb_list:
        if cb.get() == 1:
            chosen_list.append(answers_list[index])
        index += 1
    
    return chosen_list



def GetEntry(quiz):

    result, entry = quiz.GetEntry()
    if result:
        return True, entry
    else:
        return False, 0



def GetEntryType(quiz, entry):

    return quiz.GetEntryType(entry)



def GetQuestion(quiz, entry):

    return quiz.GetQuestion(entry)



def GetQuestionNumber(number, quiz):

    return f'Question {number} of {quiz.GetTotalQuestions()}'



def GradeQuiz(questions_answered, quiz):

    if questions_answered == 0:
        return False, 'Answer a question first!'
    
    correct = quiz.GetNumberOfCorrects()
    score = correct / questions_answered
    msg = f'You answered {correct} out of {questions_answered} for {score:.2%}'
    return True, msg



def IncrementCorrectAns(quiz):

    quiz.IncrementCorrectAns()



def ShuffleAnswers(quiz, entry):

    ans_list = []
    for i in range(1, quiz.GetAnswerCount(entry) + 1):
        ans_list.append(i)
    random.shuffle(ans_list)
    return ans_list