import tkinter as tk

BLUE = '#b0c4de'
FONT = ('georgia', 12)
YELLOW = '#ffefd5'
WHITE = '#f8f8ff'


def CreateButton(parent, _text, _cmd, _height, _width=15):
    """Initialize and return a tkinter Button widget.
    
    Arguments:
        parent: the Button's parent object
        _text: the text displayed on the Button
        _cmd: the function called by the Button
        _height: the height of the Button
        _width: the width of the Button (default: 15)
    
    Returns:
        A tkinter Button widget
    """
    
    return tk.Button(parent, text=_text, command=_cmd, height=_height,
                     width=_width, bg=YELLOW, activebackground=YELLOW,
                     font=FONT, takefocus=0)


def CreateCanvas(parent, _bg=BLUE):
    """Initialize and return a tkinter Canvas widget.
    
    Arguments:
        parent: the Canvas' parent object
        _bg: the background color for the Canvas (default: BLUE)
    
    Returns:
        A tkinter Canvas widget
    """
    
    return tk.Canvas(parent, bg=_bg, highlightthickness=0)


def CreateCheckButton(parent, _text, _var):
    """Initialize and return a tkinter Checkbutton widget.
    
    Arguments:
        parent: the Checkbutton's parent object
        _text: the text displayed on the Checkbutton's label
        _var: the variable used to determine the Checkbutton's checked status
    
    Returns:
        A tkinter Checkbutton widget
    """

    return tk.Checkbutton(parent, text=_text, variable=_var, font=FONT,
                          bg=WHITE, activebackground=WHITE, wraplength=600,
                          justify='left', anchor='w', takefocus=0)


def CreateEntry(parent, _var, _show=''):
    """Initialize and return a tkinter Entry widget.
    
    Arguments:
        parent: the Entry's parent object
        _var: the variable used to retrieve the Entry's contents
        _show: sets visibility status for Entry's contents (default: visible)
    
    Returns:
        A tkinter Entry widget
    """
    
    return tk.Entry(parent, textvariable=_var, show=_show, font=FONT,
                    width=30, bd=5)


def CreateFrame(parent, _padx=5, _pady=5):
    """Initialize and return a tkinter Frame widget.
    
    Arguments:
        parent: the Frame's parent object
        _padx: the Frame's horizontal padding (default: 5)
        _pady: the Frame's vertical padding (default: 5))
    
    Returns:
        A tkinter Frame widget
    """
    
    return tk.Frame(parent, padx = _padx, pady = _pady, bg = WHITE)


def CreateLabel(parent, _text, _font=FONT, _anchor='nw'):
    """Initialize and return a Tkinter Label widget.
    
    Arguments:
        parent: the Label's parent object
        _text: the text displayed on the Label
        _font: the font style used by the Label's text (default: FONT)
        _anchor: the alignment of the text within the Label (default: nw)
    
    Returns:
        A tkinter Label widget
    """
    
    return tk.Label(parent, text=_text, font=_font, anchor=_anchor, bg=WHITE,
                    justify='left', wraplength=615, width=30)


def CreateLabelFrame(parent, _text):
    """Initialize and return a tkinter LabelFrame widget.
    
    Arguments:
        parent: the LabelFrame's parent object
        _text: the text displayed on the LabelFrame's label
    
    Returns:
        A tkinter LabelFrame widget
    """

    return tk.LabelFrame(parent, text=_text, font=FONT, bg=WHITE, bd=1,
                         padx=2, pady=2, relief='sunken')


def CreateListbox(parent, _scrollbar):
    """Initialize and return a tkinter Listbox widget.
    
    Arguments:
        parent: the Listbox's parent object
        _scrollbar: the Scrollbar widget attached to the Listbox
    
    Returns:
        A tkinter Listbox widget
    """

    return tk.Listbox(parent, yscrollcommand=_scrollbar.set, font=FONT,
                      bg=WHITE, selectmode='multiple', activestyle='dotbox')


def CreateRadioButton(parent, _text, _var, _index):
    """Initialize and return a tkinter Radiobutton widget.
    
    Arguments:
        parent: the Radiobutton's parent object
        _text: the text displayed on the Radiobutton's label
        _var: the variable used to determine the Radiobutton's checked status
        _index: the int used to set the value for a checked Radiobuton
    
    Returns:
        A tkinter Radiobutton widget
    """

    return tk.Radiobutton(parent, text=_text, variable=_var, value=_index,
                          font=FONT, wraplength=600, anchor='w', bg=WHITE,
                          activebackground=WHITE, justify='left')


def CreateScrollbar(parent):
    """Initialize and return a tkinter Scrollbar widget.
    
    Arguments:
        parent: the Scrollbar's parent object
    
    Returns:
        A tkinter Scrollbar widget
    """

    return tk.Scrollbar(parent, orient='vertical')


def CreateText(parent):
    """Initialize and return a tkinter Text widget.
    
    Arguments:
        parent: the Text's parent object
    
    Returns:
        A tkinter Text widget
    """

    return tk.Text(parent, font=FONT, bg=WHITE, wrap='word', height=2,
                   width=58)