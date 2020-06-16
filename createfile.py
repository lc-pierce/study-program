import os
import tkinter as tk
from tkinter import messagebox

class CreateFile:

    def __init__(self, filename, root_window, screen_width, screen_height):

        # Internalize the filename for use in the window title
        self.__filename = filename

        # Create the Create File window
        self.__create_window = tk.Toplevel(master = root_window)
        __create_win_height = 650
        __create_win_width = 650
        self.__screen_width = screen_width
        self.__screen_height = screen_height     
        __x_pos = int((self.__screen_width / 2) - (__create_win_width / 2))
        __y_pos = int((self.__screen_height / 2) - (__create_win_height / 2))
        self.__create_window.geometry(f'{__create_win_width}x{__create_win_height}+{__x_pos}+{__y_pos}')
        self.__create_window.title(f'Currently editing {os.path.basename(self.__filename)}')

        # Holds the current question being created for label creation usage
        self.__current_question = 1

        self.get_answer_info()



    # get_answer_info() is used to query the user about the number of possible answers for the next
    #   question being added to the file. It will be called before every new question added.
    def get_answer_info(self):

        # Create a pop-up window to hold info boxes
        self.__ans_info_window = tk.Toplevel(self.__create_window)
        __ans_info_win_height = 200
        __ans_info_win_width = 300
        __x_pos = int((self.__screen_width / 2) - (__ans_info_win_width / 2))
        __y_pos = int((self.__screen_height / 2) - (__ans_info_win_height / 2))
        self.__ans_info_window.geometry(f'{__ans_info_win_width}x{__ans_info_win_height}+{__x_pos}+{__y_pos}')
        self.__ans_info_window.title(f'Question {self.__current_question}')

        # Create the answer count label, entry box, and button
        self.__ans_count_label = tk.Label(self.__ans_info_window,
                                          text = f'How many posible answers for #{self.__current_question}?',
                                          font = ('times', 14))
        self.__ans_count_entry = tk.Entry(self.__ans_info_window,
                                          width = 10)
        self.__ans_count_button = tk.Button(self.__ans_info_window,
                                            text = 'Continue',
                                            command = self.process_answer_count,
                                            font = ('times', 14))

        # Create the radio buttons for single or multiple correct answers
        self.__radio_var = tk.IntVar(self.__ans_info_win)
        self.__rb1 = tk.Radiobutton(self.__ans_info_win,
                                    text = 'One correct answer',
                                    variable = self.__radio_var,
                                    value = 1,
                                    font = ('times', 12))
        self.__rb2 = tk.Radiobutton(self.__ans_info_win,
                                    text = 'Two+ correct answers',
                                    variable = self.__radio_var,
                                    value = 2,
                                    font = ('times', 12))

        self.__ans_count_label.grid(row = 0, column = 0)
        self.__ans_count_entry.grid(row = 0, column = 1)
        self.__rb1.grid(row = 1, column = 0)
        self.__rb2.grid(row = 1, column = 1)
        self.__ans_count_button.grid(columnspan = 2)



    # process_answer_count() retrieves the information from the answer info window to aid in creation
    #   of the objects for the main create file window
    def process_answer_count(self):

        # Retrieve the window info if present, or alert the user if something was left blank or
        #   entered incorrectly
        try:
            self.__answer_count = int(self.__ans_count_entry.get())
            self.__question_type = self.__radio_var.get()

            if (self.__question_type != 1) or (self.__question_type != 2):
                tk.messagebox.showerror('ERROR', 'Please select the number of answers.')
            elif (self.__answer_count < 1):
                tk.messagebox.showerror('ERROR', 'Number of answers can\'t be less than one.')
            else:
                # Destroy the answer info window, then load the widgets into the create file window
                self.__ans_info_win.destroy()
                self.create_widgets()
        except:
            tk.messagebox.showerror('ERROR',
                                    'Invalid entry detected. Ensure the answer count is a numerical value.')



    # create_widgets() populates the create file window with the appropriate number of entry boxes
    #   to complete the question and calls the function to write the data to the prior-specified file
    def create_windgets(self):

        __row_placement = 0

        # Create the question labels and entry box
        self.__current_question_label = tk.Label(self.__create_window,
                                                 text = f'Question #{self.__current_question}',
                                                 font = ('times', 15))
        self.__question_entry_label = tk.Label(self.__create_window,
                                               text = 'Enter the question in the box below:',
                                               font = ('times', 14))
        self.__question_entry_textbox = tk.Text(self.__create_window,
                                                width = 100,
                                                height = 5,
                                                wrap = 'word')
        self.__current_question_label.grid(row = __row_placement, columnspan = 3)
        __row_placement += 1
        self.__question_entry_label.grid(row = __row_placement, columnspan = 3)
        __row_placement += 1
        self.__question_entry_textbox.grid(row = __row_placement, columnspan = 3)
        __row_placement += 1

        # Dynamically create the answer entry objects and store them all in a list for processing later
        __answer_index = 1
        self.__answer_textbox_list = []
        self.__answer_label_list = []
        self.__answer_cb_list = []
        self.__cb_vars_list = []
        while __answer_index <= self.__answer_count:
            self.__cb_var = tk.IntVar(self.__create_window)
            self.__cb_var.set(0)
            self.__cb_vars_list.append(self.__cb_var)
            
            self.__cb = tk.Checkbutton(self.__create_window,
                                       text = 'Check if answers is a correct answer',
                                       variable = self.__cb_var,
                                       font = ('times', 14))
            self.__answer_cb_list.append(self.__cb)

            self.__answer_entry_label = tk.Label(self.__create_window,
                                                 text = f'Enter answer {__answer_index} below:',
                                                 font = ('times', 14))
            self.__answer_entry_textbox = tk.Text(self.__create_window,
                                                  width = 100,
                                                  height = 2,
                                                  wrap = 'word')
            self.__answer_label_list.append(self.__answer_entry_label)
            self.__answer_textbox_list.append(self.__answer_entry_textbox)

            self.__answer_entry_label.grid(row = __row_placement, column = 0, columnspan = 2)
            self.__cb.grid(row = __row_placement, column = 2)
            __row_placement += 1
            self.__answer_entry_textbox.grid(row = __row_placement, columnspan = 3)
            __row_placement += 1

            __answer_index += 1

        # Create the action buttons to process entered info
        self.__process_data_button = tk.Button(self.__create_window,
                                               text = 'Write To File',
                                               command = self.retrieve_data,
                                               font = ('times', 13))
        self.__next_question_button = tk.Button(self.__create_window,
                                                text = 'Add Another Question',
                                                command = self.next_question,
                                                font = ('times', 13))
        self.__next_question_button['state'] = 'disabled'
        self.__finish_button = tk.Button(self.__create_window,
                                         text = 'Finish & Exit',
                                         command = self.exit_creation,
                                         font = ('times', 13))
        self.__process_data_button.grid(pady = 15, row = __row_placement, column = 0)
        self.__next_question_button.grid(pady = 15, row = __row_placement, column = 1)
        self.__finish_button.grid(pady = 15, row = __row_placement, column = 2)



    # retrieve_data() gathers the data entered into the fields and writes it to the file in the specific
    #   format required to be read by the program in taking a quiz later
    def retrieve_data(self):

        with open(self.__filename, 'a+') as f:
            if self.__question_type == 1:
                f.write('TYP:single\n')
            else:
                f.write('TYP:multi\n')

            f.write('QST:' + self.__question_entry_textbox.get('1.0', 'end'))

            __correct_answer_text = ''
            __answer_list_index = 0
            for __entry in self.__answer_textbox_list:
                __text = __entry.get('1.0', 'end')
                f.write('ANS:' + __text)
                if self.__cb_vars_list[__answer_list_index].get() == 1:
                    __correct_answer_text += __text
                __answer_list_index += 1
            f.write('COR:' + __correct_answer_text)

        # Disable the process data button to prevent duplicate additions and enable the next question
        #   button to continue adding info
        self.__process_data_button['state'] = 'disabled'
        self.__next_question_button['state'] = 'active'


    # next_question() prepares the program to add an additional question to the file by increasing
    #   the question count, starting a new line in the file, destroying the current widgets, and
    #   calling the function to get the new answer info
    def next_question(self):

        self.__current_question += 1
        with open(self.__filename, 'a+') as f:
            f.write('\n')
            
        self.__current_question_label.grid_forget()
        self.__question_entry_label.grid_forget()
        self.__question_entry_textbox.grid_forget()
        for item in self.__answer_label_list:
            item.grid_forget()
        for item in self.__answer_textbox_list:
            item.grid_forget()
        for item in self.__answer_cb_list:
            item.grid_forget()
        self.__process_data_button.grid_forget()
        self.__next_question_button.grid_forget()
        self.__finish_button.grid_forget()
        
        self.get_answer_info()



    # exit_creation() is used to destroy the create file window and alert the user of successful
    #   file creation
    def exit_creation(self):

        tk.messagebox.showinfo('Success!',
                               f'{os.path.basename(self.__filename)} created successfully')
        self.__create_window.destroy()
