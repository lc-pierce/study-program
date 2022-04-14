#-----------------------------------------------------------------------------#
#   File:   Widgets.py                                                        #
#   Author: Logan Pierceall                                                   #
#                                                                             #
#   This module contains constructor functions for all of the tkinter widgets #
#       used by LogInWindow.py, MainWindow.py, QuizWindow.py, and             #
#       CreateDBWindow.py                                                     #
#-----------------------------------------------------------------------------#

import tkinter as tk

# Widget constant options
BLUE   = '#b0c4de'
FONT   = ('georgia', 12)
YELLOW = '#ffefd5'
WHITE  = '#f8f8ff'

# CreateButton() initializes and returns a tkinter button object
# Args:     parent  = button's parent object
#           _text   = text displayed on the button
#           _cmd    = function executed by the button
#           _height = height of the button
#           _width  = width of the button
# Returns:  a tkinter button
def CreateButton(parent, _text, _cmd, _height, _width = None):

    # Default button width if not explicitly provided
    if not _width:
        _width = 15
    
    return tk.Button(parent, text = _text, command = _cmd, height = _height,
                     width = _width, bg = YELLOW, activebackground = YELLOW,
                     font = FONT, takefocus = 0)



# CreateCanvas() initializes and returns a tkinter canvas object
# Args:     parent = canvas' parent object
#           _bg    = background color of the canvas 
# Returns:  a tkinter canvas
def CreateCanvas(parent, _bg = None):

    # Default background color if not explicitly provided
    if not _bg:
        _bg = BLUE
    
    return tk.Canvas(parent, bg = _bg, highlightthickness = 0)



# CreateCheckButton() initializes and returns a tkinter checkbutton object
# Args:     parent = checkbutton's parent object
#           _text  = text displayed on the checkbutton's label
#           _var   = retrieval variable associated with the checkbutton
# Returns: a tkinter chuckbutton
def CreateCheckButton(parent, _text, _var):

    return tk.Checkbutton(parent, text = _text, variable = _var,
                          bg = WHITE, activebackground = WHITE, font = FONT,
                          wraplength = 600, justify = 'left', anchor = 'w',
                          takefocus = 0)



# CreateEntry() initializes and returns a tkinter entry object
# Args:     parent = entry box's parent object
#           _var   = retrieval variable associated with the entry box
#           _show  = determines if entered characters are visible or not
# Returns:  a tkinter entry box
def CreateEntry(parent, _var, _show = None):

    # Show the widget's contents unless explicity told not to
    if not _show:
        _show = ''
    
    return tk.Entry(parent, textvariable = _var, show = _show, font = FONT,
                    width = 30, bd = 5)



# CreateFrame() initializes and returns a tkinter frame object
# Args:     parent = frame's parent object
#           _padx  = horizontal padding around the frame
#           _pady  = vertical padding around the frame
# Returns: a tkinter frame
def CreateFrame(parent, _padx = None, _pady = None):

    # Default padding if not explicity provided
    if not _padx:
        _padx = 5
    if not _pady:
        _pady = 5
    
    return tk.Frame(parent, padx = _padx, pady = _pady, bg = WHITE)



# CreateLabel() initializes and returns a tkinter label object
# Args:     parent  = label's parent object
#           _text   = text displayed on the label
#           _font   = font used by the label's text
#           _anchor = positioning of text within the label
# Returns:  a tkinter label
def CreateLabel(parent, _text, _font = None, _anchor = None):

    # Default text font if not explicity provided
    if not _font:
        _font = FONT
    
    # Default positioning of text if not explicity provided
    if not _anchor:
        _anchor = 'nw'
    
    return tk.Label(parent, text = _text, font = _font, anchor = _anchor,
                    bg = WHITE, justify = 'left', wraplength = 615, width = 30)



# CreateLabelFrame() initializes and returns a tkinter labelframe object
# Args:     parent = labelframe's parent object
#           _text  = text displayed on the labelframe
# Returns: a tkinter labelframe
def CreateLabelFrame(parent, _text):

    return tk.LabelFrame(parent, text = _text, font = FONT, bg = WHITE,
                         padx = 2, pady = 2, bd = 1, relief = 'sunken')



# CreateListbox() initializes and returns a tkinter listbox object
# Args:     parent    = listbox's parent object
#           scrollbar = scrollbar object associated with the listbox
# Returns:  a tkinter listbox
def CreateListbox(parent, scrollbar):

    return tk.Listbox(parent, yscrollcommand = scrollbar.set, font = FONT,
                      bg = WHITE, selectmode = 'multiple',
                      activestyle = 'dotbox')



# CreateRadioButton() initializes and returns a tkinter radiobutton object
# Args:     parent = radiobutton's parent object
#           _text  = text displayed on the radiobutton's label
#           _var   = retrieval variable associated with the radiobutton
#           _index = value returned by radiobutton when retrieved
# Returns:  a tkinter radiobutton
def CreateRadioButton(parent, _text, _var, _index):

    return tk.Radiobutton(parent, text = _text, variable = _var,
                          value = _index, font = FONT, wraplength = 600,
                          bg = WHITE, activebackground = WHITE,
                          anchor = 'w', justify = 'left')



# CreateScrollbar() initializes and returns a tkinter scrollbar object
# Args:     parent = scrollbar's parent object
# Returns:  a tkinter scrollbar
def CreateScrollbar(parent):

    return tk.Scrollbar(parent, orient = 'vertical')



# CreateText() initializes and returns a tkinter text box
# Args:     parent = text box's parent object
# Returns:  a tkinter text box
def CreateText(parent):

    return tk.Text(parent, font = FONT, bg = WHITE, wrap = 'word',
                   height = 2, width = 58)