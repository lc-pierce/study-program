#-----------------------------------------------------------------------------#
#   File:   WidgetCreation.py                                                 #
#   Author: Logan Pierceall                                                   #
#   Date:   March 8, 2022                                                     #
#                                                                             #
#   This module contains constructors for all of the Tkinter widgets that are #
#       used by CreateDBWindow.py, LogInWindow.py, and MainWindow.py.         #
#-----------------------------------------------------------------------------#

import tkinter as tk

BG_COLOR = 'gainsboro'          # Default widget and window background color
BG_WHITE = 'ghost white'        # Default background color for entry widgets
FONT = ('georgia', 14)          # Default font for widgets
PAD = 5                         # Padding placed around certain widgets
TEXTBOX_SIZE = 1                # Default height/width for Text entry boxes
WRAPLENGTH = 500                # Default max length for lines of text


# CreateButton() creates and returns a tkinter Button widget
# Args:     parent = widget's parent object
#           text = text displayed on the button
#           command = function to be executed on button click
#           font = overloadable font selection
# Returns:  a tkinter Button object
def CreateButton(parent, text, command, font = FONT):

    return tk.Button(parent, text = text, command = command, font = font,
                     bg = BG_COLOR, width = 10)



# CreateCheckButton() creates and returns a tkinter Check Button widget
# Args:     parent = widget's parent object
#           text = text displayed as the button's label
#           var = the value retrieval variable associated with the button
#           font = overloadable font selection
# Returns:  a tkinter CheckButton object
def CreateCheckButton(parent, text, var, font = FONT):

    return tk.Checkbutton(parent, text = text, variable = var,
                          bg = BG_COLOR, activebackground = BG_COLOR,
                          font = font, wraplength = WRAPLENGTH,
                          justify = 'left', anchor = 'w')



# CreateEntry() creates and returns a tkinter Entry widget
# Args:     parent = widget's parent object
#           text_var = variable used to retrieve the widget's contents
#           font = overloadable font selection
# Returns:  a tkinter Entry object
def CreateEntry(parent, text_var, font = FONT):

    return tk.Entry(parent, textvariable = text_var, font = font)



# CreateFrame() creates and returns a tkinter Frame widget
# Args:     parent = widget's parent object
#           padx, pady = overloadable frame padding
# Returns:  a tkinter Frame object
def CreateFrame(parent, padx = PAD, pady = PAD):

    return tk.Frame(parent, padx = padx, pady = pady, bg = BG_COLOR)



# CreateLabel() creates and returns a tkinter Label widget
# Args:     parent = widget's parent object
#           text = text displayed on the label
#           font = overloadable font selection
# Returns:  a tkinter Label object
def CreateLabel(parent, text, font = FONT):

    return tk.Label(parent, text = text, anchor = 'nw',
                    font = font, bg = BG_COLOR)



# CreateLabelFrame() creates and returns a tkinter LabelFrame widget
# Args:     parent = widget's parent object
#           text = text displayed on the frame's label
#           font = overloadable font selection
# Returns:  a tkinter LabelFrame object
def CreateLabelFrame(parent, text, font = FONT):

    return tk.LabelFrame(parent, text = text, font = font, bg = BG_COLOR,
                         padx = PAD, pady = PAD, bd = 1, relief = 'sunken')



# CreateListbox() creates and returns a tkinter Listbox widget
# Args:     parent = widget's parent object
#           scrollbar = the scrollbar object attached to the listbox
#           font = overloadable font selection
# Returns:  a tkinter Listbox object
def CreateListbox(parent, scrollbar, font = FONT):

    return tk.Listbox(parent, font = font, bg = BG_WHITE,
                      yscrollcommand = scrollbar.set,
                      selectmode = 'extended', activestyle = 'dotbox')



# CreateRadioButton() creates and returns a tkinter Radio Button widget
# Args:     parent = widget's parent object
#           text = text displayed as the button's label
#           var = the value retrieval variable associated with the button
#           index = the numeric value for the button
#           font = overloadable font selection
# Returns:  a tkinter RadioButton object
def CreateRadioButton(parent, text, var, index, font = FONT):

    return tk.Radiobutton(parent, text = text, variable = var, value = index,
                          bg = BG_COLOR, activebackground = BG_COLOR,
                          font = font, wraplength = WRAPLENGTH,
                          justify = 'left', anchor = 'w')



# CreateText() creates and returns a tkinter Text widget
# Args:     parent = widget's parent object
#           font = overloadable font selection
#           height = overloadable widget height
#           width = overlaodable widget width
# Returns:  a tkinter Text object
def CreateText(parent, font = FONT, height = TEXTBOX_SIZE,
               width = TEXTBOX_SIZE):

    return tk.Text(parent, height = height, width = width, bg = BG_WHITE,
                   font = font, wrap = 'word')