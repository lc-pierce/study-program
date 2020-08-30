import os
import tkinter as tk
from tkinter import messagebox

class CreateFile:

    def __init__ (self, filename, root_window, screen_width, screen_height):
    
        self.__filename = filename
        with open(self.__filename, 'a+') as __f:
            __f.write(f'FIL:{os.path.basename(self.__filename)}\n')
            
        self.__current_question = 1
        
        self.__create_window = tk.Toplevel(master = root_window)
        self.__create_window.title(f'Current editing {os.path.basename(filename)}')
        self.__create_window.config(bg = 'dodger blue')
        self.__screen_width = screen_width
        self.__screen_height = screen_height
        self.__create_win_width = 1100
        self.__create_win_height = 700
        
        self.set_window_dimensions(self.__create_win_width, self.__create_win_height)
        self.create_window_layout()



    def set_window_dimensions (self, width, height):
    
        __x_pos = int((self.__screen_width / 2) - (width / 2))
        __y_pos = int((self.__screen_height / 2) - (height / 2))
        self.__create_window.geometry(f'{width}x{height}+{__x_pos}+{__y_pos}')



    def create_window_layout (self):
    
        self.__title_frame = tk.Frame(self.__create_window,
                                      padx = 5, pady = 5,
                                      height = 1,
                                      bg = 'dodger blue')
        self.__widgets_frame = tk.Frame(self.__create_window,
                                        padx = 5, pady = 5,
                                        bg = 'dodger blue')
        self.__title_frame.pack(side = 'top', fill = 'x')
        self.__widgets_frame.pack(side = 'bottom', fill = 'both', expand = 'true')
        
        self.__question_button_widgets_frame = tk.Frame(self.__widgets_frame,
                                                        padx = 5,
                                                        bg = 'dodger blue')
        self.__answer_widgets_frame = tk.Frame(self.__widgets_frame,
                                               padx = 5, pady = 5,
                                               bg = 'dodger blue')
        self.__additional_answers_frame = tk.Frame(self.__widgets_frame,
                                                   padx = 5, pady = 5,
                                                   bg = 'dodger blue')
        self.__question_button_widgets_frame.pack(side = 'left', fill = 'both', expand = 'true')
        self.__answer_widgets_frame.pack(side = 'left', fill = 'both', expand = 'true')
        
        self.__title_label = tk.Label(self.__title_frame,
                                      text = f'QUESTION {self.__current_question}',
                                      font = 'times 18 bold',
                                      bg = 'dodger blue', fg = 'mint cream')
        self.__title_label.pack(fill = 'both', expand = 'true')

        self.__answer_frames_list = []
        self.__answer_textbox_list = []
        self.__cb_vars_list = []
        self.__answer_index = 0
        
        self.create_question_widgets()
        self.create_button_widgets()
        self.create_answer_widget(False)
        self.create_answer_widget(False)
        self.create_additional_answer_widget(False)



    def create_question_widgets (self):
    
        self.__question_frame = tk.Frame(self.__question_button_widgets_frame,
                                         bg = 'dodger blue')
        self.__question_frame.pack(side = 'top', fill = 'both', expand = 'true')
        
        self.__current_question_label = tk.Label(self.__question_frame,
                                                 text = 'Enter the question below:',
                                                 font = 'times 14 bold',
                                                 anchor = 'w',
                                                 bg = 'dodger blue', fg = 'mint cream')
        self.__current_question_label.pack(side = 'top', fill = 'x')
        
        self.__question_entry_textbox = tk.Text(self.__question_frame,
                                                height = 30, width = 40,
                                                wrap = 'word',
                                                bg = 'mint cream')
        self.__question_entry_textbox.pack(side = 'top', fill = 'x')
        self.__question_entry_textbox.bind_class('Text', '<Tab>', self.focus_next_widget)



    def create_button_widgets (self):
    
        self.__buttons_frame = tk.Frame(self.__question_button_widgets_frame,
                                        padx = 5, pady = 5,
                                        bg = 'dodger blue')
        self.__process_next_frame = tk.Frame(self.__buttons_frame,
                                             bg = 'dodger blue')
        self.__finish_frame = tk.Frame(self.__buttons_frame,
                                       bg = 'dodger blue')
        self.__buttons_frame.pack(side = 'bottom', fill = 'both', expand = 'true')
        self.__process_next_frame.pack(side = 'top', fill = 'both', expand = 'true')
        self.__finish_frame.pack(side = 'bottom', fill = 'both', expand = 'true')
        
        self.__process_data_button = tk.Button(self.__process_next_frame,
                                               text = 'WRITE TO FILE',
                                               command = self.retrieve_data,
                                               font = 'times 13 bold',
                                               bd = 3,
                                               bg = 'dodger blue', fg = 'mint cream',
                                               activebackground = 'dodger blue')
        self.__next_question_button = tk.Button(self.__process_next_frame,
                                                text = 'NEXT QUESTION',
                                                command = self.next_question,
                                                font = 'times 13 bold',
                                                bd = 3,
                                                bg = 'dodger blue', fg = 'mint cream',
                                                activebackground = 'dodger blue')
        self.__finish_button = tk.Button(self.__finish_frame,
                                         text = 'FINISH & EXIT',
                                         command = self.exit_creation,
                                         font = 'times 13 bold',
                                         bd = 3,
                                         bg = 'dodger blue', fg = 'mint cream',
                                         activebackground = 'dodger blue')
        self.__next_question_button['state'] = 'disabled'
        self.__process_data_button.pack(side = 'left', fill = 'both', expand = 'true')
        self.__next_question_button.pack(side = 'right', fill = 'both', expand = 'true')
        self.__finish_button.pack(fill = 'both', expand = 'true')



    def create_answer_widget (self, page_flag):
    
        if not page_flag:
            __master_frame = self.__answer_widgets_frame
        else:
            __master_frame = self.__additional_answers_frame
        
        self.__answer_index += 1
        
        self.__answer_frame = tk.Frame(__master_frame,
                                       bg = 'dodger blue')
        self.__answer_label_cb_frame = tk.Frame(self.__answer_frame,
                                                bg = 'dodger blue')
        self.__answer_entry_frame = tk.Frame(self.__answer_frame,
                                             bg = 'dodger blue')
        self.__answer_frame.pack(fill = 'x')
        self.__answer_label_cb_frame.pack(side = 'top', fill = 'x')
        self.__answer_entry_frame.pack(side = 'bottom', fill = 'x')
        
        self.__cb_var = tk.IntVar(self.__create_window)
        self.__cb_var.set(0)
        self.__cb = tk.Checkbutton(self.__answer_label_cb_frame,
                                   text = 'Check for a correct answer',
                                   variable = self.__cb_var,
                                   font = 'times 11',
                                   bg = 'dodger blue', fg = 'mint cream',
                                   activebackground = 'dodger blue',
                                   selectcolor = 'black')
        self.__cb.pack(side = 'right')
        self.__cb_vars_list.append(self.__cb_var)
        
        self.__answer_entry_label = tk.Label(self.__answer_label_cb_frame,
                                             text = f'Enter answer {self.__answer_index}:',
                                             font = 'times 15',
                                             bg = 'dodger blue', fg = 'mint cream')
        self.__answer_entry_textbox = tk.Text(self.__answer_entry_frame,
                                              height = 4, width = 40,
                                              wrap = 'word',
                                              bg = 'mint cream')
        self.__answer_entry_label.pack(side = 'left')
        self.__answer_entry_textbox.pack(fill = 'x')
        self.__answer_textbox_list.append(self.__answer_entry_textbox)



    def create_additional_answer_widget (self, page_flag):
    
        if not page_flag:
            __master_frame = self.__answer_widgets_frame
        else:
            __master_frame = self.__additional_answers_frame
            
        self.__additional_answers_button = tk.Button(__master_frame,
                                                     text = 'ADD ADDITIONAL ANSWER',
                                                     command = self.add_answer,
                                                     font = 'times 13 bold',
                                                     bd = 3, height = 1, pady = 5,
                                                     bg = 'dodger blue', fg = 'mint cream',
                                                     activebackground = 'dodger blue')
        self.__additional_answers_button.pack(side = 'bottom', fill = 'x')



    def add_answer (self):
    
        self.__additional_page = False
    
        if self.__answer_index > 9:
            tk.messagebox.showerror('ERROR', 'Answer limit reached.')
        elif self.__answer_index > 4:
            if not self.__additional_page:
                self.__additional_page = True
                self.create_additional_answer_page()
                self.__additional_answers_button.forget()
                self.create_additional_answer_widget(True)
            self.create_answer_widget(True)
        else:
            self.create_answer_widget(False)



    def create_additional_answer_page (self):
    
        self.set_window_dimensions(self.__create_win_width+400, self.__create_win_height)
        self.__additional_answers_frame.pack(side = 'right', fill = 'both', expand = 'true')



    def retrieve_data (self):
        
        __answer_list_index = 0
        __answer_count = 0
        __answers_list = []
        __correct_str = 'COR:'
        for __entry in self.__answer_textbox_list:
            __text = __entry.get('1.0', 'end')
            __answers_list.append(__text)
            
            if self.__cb_vars_list[__answer_list_index].get() == 1:
                __correct_str += str(__answer_list_index)
                __answer_count += 1
                
            __answer_list_index += 1
            
        with open(self.__filename, 'a+') as __f:
            if __answer_count > 1:
                __f.write('TYP:multi\n')
            else:
                __f.write('TYP:single\n')
            __f.write('QST:' + self.__question_entry_textbox.get('1.0', 'end'))
            for __entry in __answers_list:
                __f.write('ANS:' + __entry)
            __f.write(__correct_str + '\n')
            
        self.__process_data_button['state'] = 'disabled'
        self.__next_question_button['state'] = 'active'



    def next_question (self):
    
        self.__current_question += 1
        self.__title_frame.forget()
        self.__widgets_frame.forget()
        if self.__additional_page:
            self.__additional_answers_frame.forget()
            self.set_window_dimensions(self.__create_win_width, self.__create_win_height)
        self.create_window_layout()



    def exit_creation (self):
    
        tk.messagebox.showinfo('SUCCESS!',
                               f'{os.path.basename(self.__filename)} created successfully.')
        self.__create_window.destroy()



    def focus_next_widget (self, event):
    
        event.widget.tk_focusNext().focus()
        return('break')