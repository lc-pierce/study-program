Study Program
Author: Logan Pierceall
Date: June 16, 2020

Study Program is a Python-based program designed to quiz the user in a similar fashion to using
flashcards. The main interface, launched by running studyprogram.py, contains a list box holding
all of the data files previously seen by the program (initially this will be blank), four operational
buttons, and a small help window offering some explanation to the buttons' funcionality.


The buttons offered have the following functionality:
Add new file to list: Opens a window to select a data file that will load question & answer info into
                      the program. The data file will also be added to the list box for faster access
                      in the future.
                      
Load selected files: After selecting one or more files to load from the list, the files will be read
                     into the program to be used in taking a quiz over their contents.
                     
Take quiz: After loading the data files into the program, use this button to take a quiz

Create new database file: Opens a separate window containing form fields to be used in populating a
                          new file in the appropriate format that can be used by the program later to
                          take a quiz


The database files created and read by the program are required to be .txt files and must utilize the 
following format. For convenience, some data files have been included with the program's files.
FIL:...
TYP:...
QST:...
ANS:...
ANS:...
ANS:...
ANS:...
COR:...

FIL contains the filename, which will be used by the program to show in which database file a particular
question can be found. It only appears once, at the beginning of the file. The rest of the lines represent
information for one question and will be repeated as needed for the total number of questions.
TYP contains the type of the question following, which will either be a single answer (single) or
a multiple choice answer (multi) question. This will affect how many answer options are simultaneously
selectable when taking a quiz.
QST contains the question itself.
ANS contains a single answer option. The amount of times this line will appear per question is dependent
on the number of answer options a question has.
COR contains the correct answer for the question. If the question is multiple choice, the line will be a 
composite made of all of the correct answers listed one after another, without spaces between, in the same 
order as they appear in the list of ANS lines.


The "Create new database file" button will open a separate form to create a formatted data file. A third window will 
pop up before every question to ask the user to enter the number of possible answers for the next question to be 
created and whether the question is a single or multiple choice type question. The create a file form contains an entry
box for the question text and another for each of the possible answers. Check boxes appear above the answer form fields 
to indicate the answer is the correct answer.