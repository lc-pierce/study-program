import os

import LogInWindow

if __name__ == '__main__':
    
    # Create the folder to store quiz files if not already present
    try:
        os.mkdir('database')
    except:
        pass
    
    app = LogInWindow.LogInWindow()
    app.mainloop()