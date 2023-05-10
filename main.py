import windows
import database as db

# If a master password exists, open the login window. Otherwise, open the register window.
if db.hasMaster():
    windows.loginWindow()
else:
    windows.registerWindow()

# Line of code to keep the application running.
windows.window.mainloop()
