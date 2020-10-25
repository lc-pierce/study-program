import os
import tkinter as tk
from tkinter import messagebox

class CreateFile:

    def __init__ (self, filename, root_window, screen_width, screen_height):
    
        self.__filename = filename
        self.__current_question = 1
        
        self.__bg_color = 'PaleTurquoise2'
        self.__font_color = 'grey1'
        self.__font = 'georgia'
        self.__button_color = 'ghost white'
        
        # Create the new form window
        self.__create_window = tk.Toplevel(master = root_window)
        self.__create_window.title(f'Currently editing {os.path.basename(filename)}')
        self.__create_window.config(bg = self.__bg_color)
        self.__screen_width = screen_width
        self.__screen_height = screen_height
        self.__create_win_width = 1100
        self.__create_win_height = 750
        
        self.set_window_dimensions(self.__create_win_width, self.__create_win_height)
        self.create_window_layout()
    
    
    
    # Sets the position of the screen on the window. Helps resizing and placing the window if
    #   additional answer boxes are added on later
    def set_window_dimensions (self, width, height):
    
        __x_pos = int((self.__screen_width / 2) - (width / 2))
        __y_pos = int((self.__screen_height / 2) - (height / 2) - 30)
        self.__create_window.geometry(f'{width}x{height}+{__x_pos}+{__y_pos}')
    
    
    
    # Creates the frames for the window objects and calls the functions to create those objects
    def create_window_layout (self):
    
        self.__title_frame = tk.Frame(self.__create_window,
                                      padx = 5,
                                      pady = 5,
                                      height = 1,
                                      bg = self.__bg_color)
        self.__widgets_frame = tk.Frame(self.__create_window,
                                        padx = 5,
                                        pady = 5,
                                        bg = self.__bg_color)
        self.__title_frame.pack(side = 'top', fill = 'x')
        self.__widgets_frame.pack(side = 'bottom', fill = 'both', expand = 'true')
        
        self.__question_button_widgets_frame = tk.Frame(self.__widgets_frame,
                                                        padx = 5,
                                                        bg = self.__bg_color)
        self.__answer_widgets_frame = tk.Frame(self.__widgets_frame,
                                               padx = 5,
                                               pady = 5,
                                               bg = self.__bg_color)
        self.__additional_answers_frame = tk.Frame(self.__widgets_frame,
                                                   padx = 5,
                                                   pady = 5,
                                                   bg = self.__bg_color)
        self.__question_button_widgets_frame.pack(side = 'left', fill = 'both', expand = 'true')
        self.__answer_widgets_frame.pack(side = 'left', fill = 'both', expand = 'true')
        
        self.__title_label = tk.Label(self.__title_frame,
                                      text = f'QUESTION {self.__current_question}',
                                      font = (self.__font, 18, 'bold'),
                                      bg = self.__bg_color,
                                      fg = self.__font_color)
        self.__title_label.pack(fill = 'both', expand = 'true')
        
        # Lists hold all of the created objects so their contents can easily be pulled and added to
        #   the file later
        self.__answer_frames_list = []
        self.__answer_textbox_list = []
        self.__cb_vars_list = []
        self.__answer_index = 0
        
        # Flag for if additionally created answer boxes have been added to the window
        self.__additional_page = False
        
        # Creates the question box, answer boxes, and action buttons
        self.create_question_widgets()
        self.create_button_widgets()
        self.create_additional_answer_widget()
        for __looper in range(4):
            self.create_answer_widget(False)
    
    
    
    # Creates the widgets for the question entry portion of the window
    def create_question_widgets (self):
    
        self.__question_frame = tk.Frame(self.__question_button_widgets_frame,
                                         bg = self.__bg_color)
        self.__question_frame.pack(side = 'top', fill = 'both', expand = 'true')
        
        self.__current_question_label = tk.Label(self.__question_frame,
                                                 text = 'Enter the question below:',
                                                 font = (self.__font, 14, 'bold'),
                                                 anchor = 'w',
                                                 bg = self.__bg_color,
                                                 fg = self.__font_color)
        self.__current_question_label.pack(side = 'top', fill = 'x')
        
        self.__question_entry_textbox = tk.Text(self.__question_frame,
                                                height = 25, width = 40,
                                                wrap = 'word',
                                                font = self.__font,
                                                bg = 'ghost white')
        self.__question_entry_textbox.pack(side = 'top', fill = 'x')
        
        # Bind the "Tab" button so it can be used to quickly move between entry boxes
        self.__question_entry_textbox.bind_class("Text", "<Tab>", self.focus_next_widget)
    
    
    
    def create_question_widgets (self):
    
        self.__question_frame = tk.Frame(self.__question_button_widgets_frame,
                                         bg = self.__bg_color)
        self.__question_frame.pack(side = 'top', fill = 'both', expand = 'true')
        
        self.__current_question_label = tk.Label(self.__question_frame,
                                                 text = 'Enter the question below:',
                                                 font = (self.__font, 14, 'bold'),
                                                 anchor = 'w',
                                                 bg = self.__bg_color,
                                                 fg = self.__font_color)
        self.__current_question_label.pack(side = 'top', fill = 'x')
        
        self.__question_entry_textbox = tk.Text(self.__question_frame,
                                                height = 25, width = 40,
                                                wrap = 'word',
                                                font = self.__font,
                                                bg = 'ghost white')
        self.__question_entry_textbox.pack(side = 'top', fill = 'x')
        self.__question_entry_textbox.bind_class("Text", "<Tab>", self.focus_next_widget)


    
    # Creates the buttons that will add text entry fields to the file, empty the fields for a new
    #   question, and save the file and exit creation
    def create_button_widgets (self):
    
        self.__buttons_frame = tk.Frame(self.__question_button_widgets_frame,
                                        padx = 5,
                                        pady = 5,
                                        bg = self.__bg_color)
        self.__process_next_frame = tk.Frame(self.__buttons_frame,
                                             bg = self.__bg_color)
        self.__finish_frame = tk.Frame(self.__buttons_frame,
                                       bg = self.__bg_color)
        self.__buttons_frame.pack(side = 'bottom', fill = 'both', expand = 'true')
        self.__process_next_frame.pack(side = 'top', fill = 'both', expand = 'true')
        self.__finish_frame.pack(side = 'bottom', fill = 'both', expand = 'true')
        
        self.__process_data_button = tk.Button(self.__process_next_frame,
                                               text = 'WRITE TO FILE',
                                               command = self.check_data,
                                               font = (self.__font, 13, 'bold'),
                                               bd = 3,
                                               bg = self.__button_color,
                                               fg = self.__font_color,
                                               activebackground = self.__button_color,
                                               takefocus = 0)
        self.__next_question_button = tk.Button(self.__process_next_frame,
                                                text = 'NEXT QUESTION',
                                                command = self.next_question,
                                                font = (self.__font, 13, 'bold'),
                                                bd = 3,
                                                bg = self.__button_color,
                                                fg = self.__font_color,
                                                activebackground = self.__button_color,
                                                takefocus = 0)
        self.__finish_button = tk.Button(self.__finish_frame,
                                         text = 'FINISH & EXIT',
                                         command = self.exit_creation,
                                         font = (self.__font, 13, 'bold'),
                                         bd = 3,
                                         bg = self.__button_color,
                                         fg = self.__font_color,
                                         activebackground = self.__button_color,
                                         takefocus = 0)
        self.__process_data_button.pack(side = 'left', fill = 'both', expand = 'true')
        self.__next_question_button.pack(side = 'right', fill = 'both', expand = 'true')
        self.__finish_button.pack(fill = 'both', expand = 'true')
        
        # Disables the next question button until the current fields have been added to the file
        self.__next_question_button['state'] = 'disabled'
    
    
    
    # Creates the buttons used to add or remove answer entry boxes from the window
    def create_additional_answer_widget (self):
    
        self.__add_rmv_answers_frame = tk.Frame(self.__answer_widgets_frame,
                                                bg = self.__bg_color)
        self.__add_rmv_answers_frame.pack(side = 'top', fill = 'x')
        
        self.__additional_answers_button = tk.Button(self.__add_rmv_answers_frame,
                                                     text = '+1 ANSWER BOX',
                                                     command = self.add_answer,
                                                     font = (self.__font, 13, 'bold'),
                                                     bd = 3,
                                                     height = 1,
                                                     pady = 5,
                                                     bg = self.__button_color,
                                                     fg = self.__font_color,
                                                     activebackground = self.__button_color,
                                                     takefocus = 0)
        self.__remove_answer_button = tk.Button(self.__add_rmv_answers_frame,
                                                text = '-1 ANSWER BOX',
                                                command = self.remove_answer,
                                                font = (self.__font, 13, 'bold'),
                                                bd = 3,
                                                height = 1,
                                                pady = 5,
                                                bg = self.__button_color,
                                                fg = self.__font_color,
                                                activebackground = self.__button_color,
                                                takefocus = 0)
        self.__additional_answers_button.pack(side = 'left', fill = 'both')
        self.__remove_answer_button.pack(side = 'right', fill = 'both')
    
    
    
    # Creates an answer box widget and a checkbox to mark whether the box is a correct answer
    def create_answer_widget (self, page_flag):
    
        self.__answer_index += 1
    
        # If the extra window size for additional widgets has been created then put those widgets
        #   there. Otherwise, add them to the original window space
        if not page_flag:
            __master_frame = self.__answer_widgets_frame
        else:
            __master_frame = self.__additional_answers_frame
        
        # Create the frames
        self.__answer_frame = tk.Frame(__master_frame,
                                       bg = self.__bg_color)
        self.__answer_label_cb_frame = tk.Frame(self.__answer_frame,
                                                bg = self.__bg_color)
        self.__answer_entry_frame = tk.Frame(self.__answer_frame,
                                             bg = self.__bg_color)
        self.__answer_frame.pack(side = 'top', fill = 'x')
        self.__answer_label_cb_frame.pack(side = 'top', fill = 'x')
        self.__answer_entry_frame.pack(side = 'bottom', fill = 'x')
        
        # Create the check button for indicating whether the answer is a correct answer
        self.__cb_var = tk.IntVar(self.__create_window)
        self.__cb_var.set(0)
        self.__cb = tk.Checkbutton(self.__answer_label_cb_frame,
                                   text = 'Check for a correct answer',
                                   variable = self.__cb_var,
                                   font = (self.__font, 10),
                                   bg = self.__bg_color,
                                   fg = self.__font_color,
                                   activebackground = self.__bg_color,
                                   selectcolor = 'ghost white',
                                   takefocus = 0)
        self.__cb.pack(side = 'right')
        
        # Create the answer entry objects
        self.__answer_entry_label = tk.Label(self.__answer_label_cb_frame,
                                             text = f'Enter answer {self.__answer_index}:',
                                             font = (self.__font, 12),
                                             bg = self.__bg_color,
                                             fg = self.__font_color)
        self.__answer_entry_textbox = tk.Text(self.__answer_entry_frame,
                                              height = 4, width = 40,
                                              wrap = 'word',
                                              font = self.__font,
                                              bg = 'ghost white')
        self.__answer_entry_label.pack(side = 'left')
        self.__answer_entry_textbox.pack(fill = 'x')
        
        # Add the objects to their lists
        self.__answer_frames_list.append(self.__answer_frame)
        self.__cb_vars_list.append(self.__cb_var)
        self.__answer_textbox_list.append(self.__answer_entry_textbox)
    
    
    
    # Adds a new answer entry box to the window
    def add_answer (self):
    
        # Only allows a max of 10 possible answer entry boxes
        if self.__answer_index > 9:
            self.show_error_message('Answer limit reached.')
        
        # Only 6 boxes fit into the original window. If more are created, resize the window to
        #   add additional space
        elif self.__answer_index > 5:
            if not self.__additional_page:
                self.__additional_page = True
                self.create_additional_answer_page()
            self.create_answer_widget(True)
        else:
            self.create_answer_widget(False)
    
    
    
    # Removes an answer entry box from the screen so that an unneeded one won't interrupt
    #   processing
    def remove_answer (self):
    
        # At least 2 answer possiblities are required, otherwise it's not much of a question
        if self.__answer_index > 2:
            self.__answer_index -= 1
        
            # If the remaining answer boxes will fit in the original window then resize it
            if self.__additional_page:
                if self.__answer_index < 7:
                    self.set_window_dimensions(self.__create_win_width, self.__create_win_height)
                    self.__additional_page = False
            
            # Remove the associated objects from their lists
            __current_frame = self.__answer_frames_list.pop(self.__answer_index)
            __current_frame.forget()
            self.__cb_vars_list.pop(self.__answer_index)
            self.__answer_textbox_list.pop(self.__answer_index)
        
        else:
            self.show_error_message('At least 2 answer boxes required.')
    
    
    
    # Resizes the window in order to add more widgets
    def create_additional_answer_page (self):
    
        self.set_window_dimensions(self.__create_win_width + 400, self.__create_win_height)
        self.__additional_answers_frame.pack(side = 'right', fill = 'both', expand = 'true')
    
    
    
    # Verifies that the question and answer boxes are all populated and that at least one answer
    #   has been marked as correct before processing
    def check_data (self):
        
        __answer_list_index = 0
        __answer_count = 0
        __answers_list = []
        
        # Used to indicate a validation check failed
        __good_question = True
        __good_answers_text = True
        __good_answers_checkbox = True
        
        # First verify the question box isn't empty
        __question_str = self.__question_entry_textbox.get('1.0', 'end')
        if __question_str == '\n':
            __good_question = False
            self.show_error_message('No question entered!')
        else:
            
            # Next verify that all of the answer boxes present were populated
            for __entry in self.__answer_textbox_list:
                __text = __entry.get('1.0', 'end')
                if __text == '\n':
                    __good_answers_text = False
                    self.show_error_message(f'Answer entry box {__answer_list_index + 1} left empty')
                    break
                else:
                    __answers_list.append(__text)
                
                    # Check whether or not the answer was marked as a correct one and append a
                    #   special character if so
                    if self.__cb_vars_list[__answer_list_index].get() == 1:
                        __answers_list[__answer_list_index] = __answers_list[__answer_list_index].rstrip()
                        __answers_list[__answer_list_index] += '@\n'
                        __answer_count += 1
                
                __answer_list_index += 1
            
            # Finally, ensure that at least one answer was marked as correct
            if __good_answers_text and __answer_count == 0:
                __good_answers_checkbox = False
                self.show_error_message('No answers were marked as correct')
        
        # If all validation checks passed, allow the data to be written
        if __good_question and __good_answers_text and __good_answers_checkbox:
            self.write_data(__answer_count, __question_str, __answers_list)
    
    
    
    # Writes the data gathered to the file
    def write_data (self, num_answers, question, answers):
    
        with open(self.__filename, 'a+') as __f:
        
            if num_answers > 1:
                __f.write('TYP:multi\n')
            else:
                __f.write('TYP:single\n')
            __f.write('QST:' + question)
            
            for __entry in answers:
                __f.write('ANS:' + __entry)
        
        # Disable the process button so the info isn't accidentally added twice and enable the
        #   button to empty fields for a new question
        self.__process_data_button['state'] = 'disabled'
        self.__next_question_button['state'] = 'active'
    
    
    
    # Resets the window in order to create a new question
    def next_question (self):
    
        self.__current_question += 1
        self.__title_frame.forget()
        self.__widgets_frame.forget()
        if self.__additional_page:
            self.__additional_answers_frame.forget()
            self.set_window_dimensions(self.__create_win_width, self.__create_win_height)
        self.create_window_layout()
    
    
    
    # Close the window and alert the user the file was created
    def exit_creation (self):
    
        tk.messagebox.showinfo('SUCCESS!',
                               f'{os.path.basename(self.__filename)} created successfully.')
        self.__create_window.destroy()
    
    
    
    # Displays an error message to the user
    def show_error_message (self, message):
    
        tk.messagebox.showerror('ERROR', message)
    
    
    
    # Binds the Tab key to switch between object fields rather than insert spaces
    def focus_next_widget(self, event):
        event.widget.tk_focusNext().focus()
        return("break")