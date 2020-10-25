import random

class QuizBank:

    def __init__ (self, filename):
    
        self.__filename = filename
        self.__answers_list = []
        self.__answer_count = 0
        self.__question_type = ''
        self.__question_str = ''
    
    
    
    def get_answer (self):
    
        return self.__answers_list.pop(random.randint(0, len(self.__answers_list) - 1))
    
    
    
    def get_answer_count (self):
    
        return self.__answer_count
    
    
    
    def get_filename (self):
    
        return self.__filename
    
    
    
    def get_question (self):
    
        return self.__question_str
    
    
    
    def get_question_type (self):
    
        return self.__question_type
    
    
    
    def append_answers_list (self, ans_str):
    
        self.__answers_list.append(ans_str)
    
    
    
    def increase_answer_count (self):
    
        self.__answer_count += 1
    
    
    
    def set_question_str (self, str):
        
        self.__question_str += str



class SingleChoiceQB(QuizBank):

    def __init__ (self, filename):
        QuizBank.__init__(self, filename)
        self.__correct_answer = -1
        self.__question_type = 's'
    
    
    
    def get_correct_answer (self):
    
        return self.__correct_answer
    
    
    
    def get_question_type (self):
    
        return self.__question_type
    
    
    
    def set_correct_answer (self, correct_ans_index):
    
        self.__correct_answer = correct_ans_index



class MultiChoiceQB(QuizBank):

    def __init__ (self, filename):
    
        QuizBank.__init__(self, filename)
        self.__correct_answer = ''
        self.__question_type = 'm'
    
    
    
    def get_correct_answer (self):
    
        return self.__correct_answer
    
    
    
    def get_question_type (self):
    
        return self.__question_type
    
    
    
    def set_correct_answer (self, correct_ans_index):
    
        self.__correct_answer += str(correct_ans_index)