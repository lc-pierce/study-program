#-----------------------------------------------------------------------------#
#   Launch.py                                                                 #
#   Author: Logan Pierceall                                                   #
#                                                                             #
#   This module launches the program by calling the function to create the    #
#       initial log-in window found in LogInWindow.py                         #
#-----------------------------------------------------------------------------#

import LogInWindow

if __name__ == '__main__':

    app = LogInWindow.LogInWindow()
    app.mainloop()