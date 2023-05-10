from tkinter import *
from tkinter import filedialog
from functools import partial
from PIL import Image, ImageTk

import uuid
import encryption
import shutil
import os

import database as db
import pyperclip as pc
import customtkinter as ctk

import speechRec

# Tkinter initialization. These set up the main window, size, and title for the application
window = Tk()
window.update()
window.title("Assisted Secure Information Storage")
window.grid_rowconfigure(13, weight=1)
window.grid_columnconfigure(1, weight=1)
window.configure(bg='#242424')

# Initialize the data tables if they are not already initialized (Existence check is in each method)
db.createMasterTable()
db.createAccountStorageTable()
db.createTextStorageTable()


# Method to simplify the process to add images to the application
def addImage(imgStr):
    return ImageTk.PhotoImage(Image.open("Images/" + imgStr).resize((40, 40,)), Image.ANTIALIAS)


# Images utilizing the above method
######################################################
addAccountImage = addImage("addAccountIcon.png")
addFileImage = addImage("addFileIcon.png")
leftImage = addImage("leftIcon.png")
rightImage = addImage("rightIcon.png")
viewModeImage = addImage("viewModeIcon.png")
changeListImage = addImage("changeListIcon.png")
micImage = addImage("micIcon.png")
deleteImage = addImage("deleteIcon.png")
copyImage = addImage("copyIcon.png")
registerImage = addImage("registerIcon.png")
enterImage = addImage("enterIcon.png")
resetImage = addImage("resetIcon.png")
confirmImage = addImage("confirmIcon.png")


######################################################


# Method to create register window
def registerWindow():
    for widget in window.winfo_children():
        widget.destroy()

    window.geometry("420x220")
    window.unbind('<Return>')

    # Labels and entries to create the register components
    createPasswordLabel = ctk.CTkLabel(window, text="Create Password", font=("Impact", 28),
                                       fg_color="transparent", text_color="#f5f5f5", anchor=CENTER)
    createPasswordLabel.pack()

    passwordEntry = Entry(window, width=25, show="•", bg='#edf032', bd=0, font='Courier 20')
    passwordEntry.pack()
    passwordEntry.focus()

    confirmPasswordLabel = ctk.CTkLabel(window, text="Confirm Password", font=("Impact", 28),
                                        fg_color="transparent", text_color="#f5f5f5", anchor=CENTER)
    confirmPasswordLabel.pack()

    passwordConfirmEntry = Entry(window, width=25, show="•", bg='#edf032', bd=0, font='Courier 20')
    passwordConfirmEntry.pack()

    confirmMessageLabel = ctk.CTkLabel(window, font=("Impact", 18), text="",
                                       fg_color="transparent", text_color="#f5f5f5", anchor=CENTER)
    confirmMessageLabel.pack()

    # Method to save the password into the database
    def savePassword():
        if passwordEntry.get() == passwordConfirmEntry.get():
            db.deleteOldMaster()
            resetCode = str(uuid.uuid4().hex)

            db.createNewMaster(passwordEntry.get(), resetCode)
            resetCodeAcquisitionWindow(resetCode)
        else:
            confirmMessageLabel.config(text="Passwords do not match!")

    # Button to utilize the above method to save the password and continue to the reset code window
    enterButton = ctk.CTkButton(window, text="Register", command=savePassword, font=("Impact", 28),
                                fg_color='#f5f5f5', hover_color='#c2fcce', corner_radius=10, text_color='black',
                                anchor=CENTER, image=registerImage, compound="left")
    enterButton.pack(pady=10)


# Method to create the reset code acquisition window after registering
def resetCodeAcquisitionWindow(code):
    for widget in window.winfo_children():
        widget.destroy()

    window.geometry("800x300")
    window.unbind('<Return>')

    saveResetCodeLabel = ctk.CTkLabel(window,
                                      text="Save this code somewhere\n in case you need to recover your account!\n",
                                      font=("Impact", 20), text_color="#f5f5f5", anchor=CENTER)
    saveResetCodeLabel.pack()

    codeDisplayLabel = ctk.CTkLabel(window, text=code, font=("Helvetica", 26),
                                    text_color="#f5f5f5", anchor=CENTER)
    codeDisplayLabel.pack()

    # Method to copy the reset code to the user's clipboard for easier storage
    def copyCode():
        pc.copy(codeDisplayLabel.cget("text"))

    copyCodeButton = ctk.CTkButton(window, text="Copy Reset Code", command=copyCode, font=("Impact", 20),
                                   fg_color='#fdff00', hover_color='#feff4a', corner_radius=10,
                                   text_color='black',
                                   anchor=CENTER, image=copyImage, compound="left")
    copyCodeButton.pack(pady=10)

    # Method to return the user to the main application screen after clicking doneButton
    def returnToMain():
        accountMainWindow()

    doneButton = ctk.CTkButton(window, text="Done", command=returnToMain, font=("Impact", 20),
                               fg_color='#f5f5f5', hover_color='#c2fcce', corner_radius=10,
                               text_color='black',
                               anchor=CENTER, image=enterImage, compound="left")
    doneButton.pack(pady=10)


# The window in which the user inputs their saved reset code to reclaim their account in the event of a lost password
def resetWindow():
    for widget in window.winfo_children():
        widget.destroy()

    window.geometry("420x160")
    window.unbind('<Return>')

    enterCode = ctk.CTkLabel(window, text="Enter Reset Code", font=("Impact", 20), text_color="#f5f5f5", anchor=CENTER)
    enterCode.pack()

    resetCodeInput = ctk.CTkEntry(window, width=400, height=40, fg_color='#fdff00', border_width=0,
                                  font=("Helvetica", 20), corner_radius=10)
    resetCodeInput.pack()
    resetCodeInput.focus()

    resetCodeDisplay = ctk.CTkLabel(window, text="", font=("Courier", 24),
                                    fg_color="transparent", text_color="#f5f5f5", anchor=CENTER)
    resetCodeDisplay.pack()

    # This method checks whether the code from the database matches the user inputted code
    def checkCode():
        confirmed = db.findResetCode(resetCodeInput.get())
        if confirmed:
            registerWindow()
        else:
            resetCodeInput.delete(0, 'end')
            resetCodeDisplay.configure(text="Incorrect Code!")

    # Uses the checkCode() method upon the press of the button
    checkButton = ctk.CTkButton(window, text="Reset Password", command=checkCode, font=("Impact", 20),
                                fg_color='#fdff00', hover_color='#feff4a', corner_radius=10,
                                text_color='black',
                                anchor=CENTER, image=resetImage, compound="left")
    checkButton.pack(pady=15)


# The screen in which the user inputs their password to enter the main application window
def loginWindow():
    for widget in window.winfo_children():
        widget.destroy()

    window.geometry("400x200")
    window.configure(bg='#242424')
    enterPasswordLabel = ctk.CTkLabel(window, text="Enter Password", font=("Impact", 28),
                                      fg_color="transparent", text_color="#f5f5f5", anchor=CENTER)
    enterPasswordLabel.pack()

    passwordEntry = Entry(window, width=25, show="•", bg='#edf032', bd=0, font='Courier 18')
    passwordEntry.pack()
    passwordEntry.focus()

    passwordCheckerLabel = ctk.CTkLabel(window, text="", font=('Courier', 24),
                                        fg_color="transparent", text_color="#f5f5f5", anchor=CENTER)
    passwordCheckerLabel.pack()

    # Method to retrieve master password from the database
    def getMasterPassword():
        return db.findMasterPassword(passwordEntry.get())

    # Checks whether the retrieved password is the same as the user inputted one
    def checkPassword():
        matchingPassword = getMasterPassword()

        if matchingPassword:
            accountMainWindow()
        else:
            passwordCheckerLabel.configure(text="Incorrect Password")

    window.bind('<Return>', lambda event: checkPassword())

    # A method that is bound to resetButton to send the user to the reset screen
    def resetPassword():
        resetWindow()

    enterButton = ctk.CTkButton(window, text="Enter", command=checkPassword, font=("Impact", 20),
                                fg_color='#f5f5f5', hover_color='#e6e6e6', corner_radius=10,
                                text_color='black',
                                anchor=CENTER, image=enterImage, compound="left")
    enterButton.pack(pady=5)

    resetButton = ctk.CTkButton(window, text="Reset Password", height=25, command=resetPassword, font=("Impact", 22),
                                fg_color='#fdff00', hover_color='#feff4a', corner_radius=10,
                                text_color='black',
                                anchor=CENTER, image=resetImage, compound="left")
    resetButton.pack(pady=5)


begin = 0  # These variables are used when the main application displays a number of accounts on the screen.
end = 7  # The page only displays 7 accounts on the screen at a time, so these variables are manipulated.
i = begin  # in the nextPage() and previousPage() methods to change which set of 10 accounts are being viewed.
publicViewMode = True  # The boolean to toggle whether the view mode is public or private.
searchMode = False  # Boolean to toggle whether search mode is on or off.


# User accounts display
def accountWindowContent():
    global publicViewMode
    global searchMode

    # Method to remove an account from storage
    def removeAccountEntry(removeID):
        db.removeAccountEntry(removeID)
        global begin
        global end
        global i
        begin = 0
        end = 7
        i = begin
        accountMainWindow()

    # Method to flip to the next page of accounts if the user has more than 7 stored accounts
    def nextPage():
        global begin
        global end
        if (begin + 7) < len(db.getAccountStorageTable()):
            begin = begin + 7
            end = end + 7
            accountMainWindow()

    # Method to flip to the previous page of accounts
    def previousPage():
        global begin
        global end
        global i
        i = begin
        if (begin - 7) >= 0:
            begin = begin - 7
            i = begin
            end = end - 7
            accountMainWindow()

    # Method to navigate through the different types of data storage
    def toggleListView():
        textMainWindow()

    # Method to toggle public and private view mode
    def toggleViewMode():
        global publicViewMode
        if publicViewMode:
            publicViewMode = False
        else:
            publicViewMode = True
        accountMainWindow()

    def confirmDelete(tableEntry):
        deleteButton.configure(text="Confirm", fg_color="#ffeeed", hover_color="#fff8f7",
                               command=partial(removeAccountEntry, tableEntry))

    # Method to one-click-copy the password from the account section
    def copyPassword():
        pc.copy(passwordLabel.cget("text"))

    def viewSearchList():
        global searchMode
        searchMode = True
        accountMainWindow()

    window.geometry("1200x700")
    window.unbind('<Return>')

    # Button that calls the data list selection method
    listSelectButton = ctk.CTkButton(window, text="Now Viewing: Accounts", command=toggleListView, font=("Impact", 20),
                                     fg_color='#fdff00', hover_color='#feff4a', corner_radius=10, text_color='black',
                                     anchor=CENTER, image=changeListImage, compound="left")
    listSelectButton.grid(column=2)

    # Button that calls the view mode toggle method
    viewModeButton = ctk.CTkButton(window, text="Toggle View Mode", command=toggleViewMode, font=("Impact", 20),
                                   fg_color='#fdff00', hover_color='#feff4a', corner_radius=10, text_color='black',
                                   anchor=CENTER, image=viewModeImage, compound="left")
    viewModeButton.grid(column=0, row=0, pady=10)

    # Button that calls the voice assistance methods
    assistButton = ctk.CTkButton(window, text="Assistance", font=("Impact", 20),
                                 command=lambda: viewSearchList(),
                                 fg_color='#fdff00', hover_color='#feff4a', corner_radius=10, text_color='black',
                                 anchor=CENTER, image=micImage, compound="left")
    assistButton.grid(column=4, row=0, pady=10)

    # The right button calls the nextPage method, which changes to the next 7 entries if the user has more than 7
    rightButton = ctk.CTkButton(window, command=nextPage, image=rightImage, fg_color='#fdff00',
                                hover_color='#feff4a', text="", corner_radius=10, anchor=CENTER)
    rightButton.grid(column=4, pady=10, row=1)

    # The left button calls the previousPage method which decreases the number of entries by 7 and refreshes the page
    leftButton = ctk.CTkButton(window, command=previousPage, image=leftImage, fg_color='#fdff00', hover_color='#feff4a',
                               text="", corner_radius=10, anchor=CENTER)
    leftButton.grid(column=0, pady=10, row=1)

    # This button calls the addEntry method, prompting the user to add an account
    addButton = ctk.CTkButton(window, text="ADD", command=addAccountMainWindow, font=("Impact", 20),
                              fg_color='#fdff00', hover_color='#feff4a', corner_radius=10, text_color='black',
                              anchor=CENTER, image=addAccountImage, compound="left")
    addButton.grid(column=2, pady=10, row=1)
    usageLabel = ctk.CTkLabel(window, text="Site", font=("Impact", 20),
                              fg_color="transparent", text_color="#f5f5f5",
                              anchor=CENTER)
    usageLabel.grid(row=2, column=1, padx=21)

    usernameLabel = ctk.CTkLabel(window, text="Username", font=("Impact", 20),
                                 fg_color="transparent", text_color="#f5f5f5",
                                 anchor=CENTER)
    usernameLabel.grid(row=2, column=2, padx=23)

    passwordLabel = ctk.CTkLabel(window, text="Password", font=("Impact", 20),
                                 fg_color="transparent", text_color="#f5f5f5",
                                 anchor=CENTER)
    passwordLabel.grid(row=2, column=3, padx=103)

    if not searchMode:
        if db.getAccountStorageTable() is not None:  # Check if there are entries in the storage
            global i
            global begin
            global end
            i = begin

            while i < end:  # Iterates through 7 of the entries depending on which page

                tableList = db.getAccountStorageTable()
                if len(tableList) == 0:
                    break

                copyPasswordButton = ctk.CTkButton(window, text="Copy Password", command=copyPassword,
                                                   font=("Impact", 20),
                                                   fg_color='#fdff00', hover_color='#feff4a', corner_radius=10,
                                                   text_color='black',
                                                   anchor=CENTER, image=copyImage, compound="left")
                copyPasswordButton.grid(column=0, row=i + 3)

                # Labels to display the accounts on each page
                siteLabel = ctk.CTkLabel(window, text=encryption.decryptString(tableList[i][1]), width=220, height=45,
                                         font=("Helvetica", 20), fg_color="#1c1c1c", text_color="#f5f5f5",
                                         padx=10, pady=5, anchor=CENTER)
                siteLabel.grid(column=1, row=i + 3, ipadx=10)

                usernameLabel = ctk.CTkLabel(window, text=encryption.decryptString(tableList[i][2]), width=220,
                                             height=45,
                                             font=("Helvetica", 20), fg_color="#1c1c1c", text_color="#f5f5f5",
                                             padx=10, pady=5, anchor=CENTER)
                usernameLabel.grid(column=2, row=i + 3, ipadx=10)

                # Check if public view mode, and make private if it is not
                if publicViewMode:
                    passwordLabel = ctk.CTkLabel(window, text=encryption.decryptString(tableList[i][3]), width=220,
                                                 height=45,
                                                 font=("Helvetica", 20), fg_color="#1c1c1c", text_color="#f5f5f5",
                                                 padx=10, pady=5, anchor=CENTER)
                else:
                    passwordLabel = ctk.CTkButton(window, text=encryption.decryptString(tableList[i][3]), width=220,
                                                  height=45, hover_color="#f5f5f5", corner_radius=0,
                                                  font=("Helvetica", 20), fg_color="#1c1c1c", text_color="#1c1c1c",
                                                  anchor=CENTER)
                passwordLabel.grid(column=3, row=i + 3, ipadx=10)

                # Button that calls the removeEntry method to delete an account from storage
                deleteButton = ctk.CTkButton(window, text="Delete",
                                             command=partial(confirmDelete, tableList[i][0]), font=("Impact", 20),
                                             fg_color='#ff0a0a', hover_color='#cc0000', corner_radius=10,
                                             text_color='black', anchor=CENTER, image=deleteImage, compound="left")
                deleteButton.grid(column=4, row=i + 3, pady=5)

                i = i + 1

                if len(db.getAccountStorageTable()) <= i:
                    break
    else:
        begin = 0
        end = 7
        i = begin
        tableList = speechRec.findAccountMatches(db.getAccountStorageTable())

        while i < end:  # Iterates through 7 of the entries depending on which page

            if len(tableList) == 0:
                break

            copyPasswordButton = ctk.CTkButton(window, text="Copy Password", command=copyPassword,
                                               font=("Impact", 20),
                                               fg_color='#fdff00', hover_color='#feff4a', corner_radius=10,
                                               text_color='black',
                                               anchor=CENTER, image=copyImage, compound="left")
            copyPasswordButton.grid(column=0, row=i + 3)

            # Labels to display the accounts on each page
            siteLabel = ctk.CTkLabel(window, text=encryption.decryptString(tableList[i][1]), width=220, height=45,
                                     font=("Helvetica", 20), fg_color="#1c1c1c", text_color="#f5f5f5",
                                     padx=10, pady=5, anchor=CENTER)
            siteLabel.grid(column=1, row=i + 3, ipadx=10)

            usernameLabel = ctk.CTkLabel(window, text=encryption.decryptString(tableList[i][2]), width=220,
                                         height=45,
                                         font=("Helvetica", 20), fg_color="#1c1c1c", text_color="#f5f5f5",
                                         padx=10, pady=5, anchor=CENTER)
            usernameLabel.grid(column=2, row=i + 3, ipadx=10)

            # Check if public view mode, and make private if it is not
            if publicViewMode:
                passwordLabel = ctk.CTkLabel(window, text=encryption.decryptString(tableList[i][3]), width=220,
                                             height=45,
                                             font=("Helvetica", 20), fg_color="#1c1c1c", text_color="#f5f5f5",
                                             padx=10, pady=5, anchor=CENTER)
            else:
                passwordLabel = ctk.CTkButton(window, text=encryption.decryptString(tableList[i][3]), width=220,
                                              height=45, hover_color="#f5f5f5", corner_radius=0,
                                              font=("Helvetica", 20), fg_color="#1c1c1c", text_color="#1c1c1c",
                                              anchor=CENTER)
            passwordLabel.grid(column=3, row=i + 3, ipadx=10)

            # Button that calls the removeEntry method to delete an account from storage
            deleteButton = ctk.CTkButton(window, text="Delete",
                                         command=partial(confirmDelete, tableList[i][0]), font=("Impact", 20),
                                         fg_color='#ff0a0a', hover_color='#cc0000', corner_radius=10,
                                         text_color='black', anchor=CENTER, image=deleteImage, compound="left")
            deleteButton.grid(column=4, row=i + 3, pady=5)

            i = i + 1

            if len(db.getAccountStorageTable()) <= i:
                break


# User text display
def textWindowContent():
    global publicViewMode
    global searchMode

    def removeTextEntry(removeID):
        db.removeTextEntry(removeID)
        global begin
        global end
        global i
        begin = 0
        end = 7
        i = begin
        textMainWindow()

    # Method to flip to the next page of text
    def nextPage():
        global begin
        global end
        if (begin + 7) < len(db.getTextStorageTable()):
            begin = begin + 7
            end = end + 7
            textMainWindow()

    # Method to flip to the previous page of accounts
    def previousPage():
        global begin
        global end
        global i
        i = begin
        if (begin - 7) >= 0:
            begin = begin - 7
            i = begin
            end = end - 7
            textMainWindow()

    def toggleListView():
        fileManagementWindow()

    def toggleViewMode():
        global publicViewMode
        if publicViewMode:
            publicViewMode = False
        else:
            publicViewMode = True
        textMainWindow()

    def copyText():
        pc.copy(textDisplayLabel.cget("text"))

    def viewSearchList():
        global searchMode
        searchMode = True
        textMainWindow()

    window.geometry("1200x700")
    window.unbind('<Return>')

    listSelectButton = ctk.CTkButton(window, text="Now Viewing: Text", command=toggleListView, font=("Impact", 20),
                                     fg_color='#fdff00', hover_color='#feff4a', corner_radius=10, text_color='black',
                                     anchor=CENTER, image=changeListImage, compound="left")
    listSelectButton.grid(column=1)

    viewModeButton = ctk.CTkButton(window, text="Toggle View Mode", command=toggleViewMode, font=("Impact", 20),
                                   fg_color='#fdff00', hover_color='#feff4a', corner_radius=10, text_color='black',
                                   anchor=CENTER, image=viewModeImage, compound="left")
    viewModeButton.grid(column=0, row=0, pady=10)

    assistButton = ctk.CTkButton(window, text="Assistance", font=("Impact", 20),
                                 command=lambda: viewSearchList(),
                                 fg_color='#fdff00', hover_color='#feff4a', corner_radius=10, text_color='black',
                                 anchor=CENTER, image=micImage, compound="left")
    assistButton.grid(column=2, row=0, pady=10)

    # The right button calls the nextPage method, which changes to the next 15 entries if the user has more than 15
    rightButton = ctk.CTkButton(window, command=nextPage, image=rightImage, fg_color='#fdff00',
                                hover_color='#feff4a', text="", corner_radius=10, anchor=CENTER)
    rightButton.grid(column=2, pady=10, row=1)

    # The left button calls the previousPage method which decreases the number of entries by 15 and refreshes the page
    leftButton = ctk.CTkButton(window, command=previousPage, image=leftImage, fg_color='#fdff00', hover_color='#feff4a',
                               text="", corner_radius=10, anchor=CENTER)
    leftButton.grid(column=0, pady=10, row=1)

    # This button calls the addEntry method, prompting the user to add an account
    addButton = ctk.CTkButton(window, text="ADD", command=addTextMainWindow, font=("Impact", 20),
                              fg_color='#fdff00', hover_color='#feff4a', corner_radius=10, text_color='black',
                              anchor=CENTER, image=addAccountImage, compound="left")
    addButton.grid(column=1, pady=10, row=1)

    textLabel = ctk.CTkLabel(window, text="Text Content", font=("Impact", 20),
                             fg_color="transparent", text_color="#f5f5f5",
                             anchor=CENTER)
    textLabel.grid(row=2, column=1, padx=80)

    if not searchMode:
        if db.getTextStorageTable() is not None:  # If there are entries in the storage
            global i
            global begin
            global end
            i = begin

            while i < end:  # Iterates through 7 of the entries depending on which page

                textList = db.getTextStorageTable()
                if len(textList) == 0:
                    break

                # Labels to display the accounts on each page
                copyButton = ctk.CTkButton(window, text="Copy Text", command=copyText, font=("Impact", 20),
                                           fg_color='#fdff00', hover_color='#feff4a', corner_radius=10,
                                           text_color='black',
                                           anchor=CENTER, image=copyImage, compound="left")
                copyButton.grid(column=0, row=i + 3, ipadx=20)
                if publicViewMode:
                    textDisplayLabel = ctk.CTkLabel(window, text=encryption.decryptString(textList[i][1]), width=400,
                                                    height=45,
                                                    font=("Helvetica", 20), fg_color="#1c1c1c", text_color="#f5f5f5",
                                                    padx=10, pady=5, anchor=CENTER)
                else:
                    textDisplayLabel = ctk.CTkButton(window, text=encryption.decryptString(textList[i][1]), width=400,
                                                     height=45, hover_color="#f5f5f5", corner_radius=0,
                                                     font=("Helvetica", 20), fg_color="#1c1c1c", text_color="#1c1c1c",
                                                     anchor=CENTER)
                textDisplayLabel.grid(column=1, row=i + 3, ipadx=20)

                # Button that calls the removeEntry method to delete an account from storage
                deleteButton = ctk.CTkButton(window, text="Delete",
                                             command=partial(removeTextEntry, textList[i][0]), font=("Impact", 20),
                                             fg_color='#ff0a0a', hover_color='#cc0000', corner_radius=10,
                                             text_color='black', anchor=CENTER, image=deleteImage, compound="left")
                deleteButton.grid(column=2, row=i + 3, pady=5)

                i = i + 1

                if len(db.getTextStorageTable()) <= i:
                    break
    else:
        begin = 0
        end = 7
        i = begin
        textList = speechRec.findTextMatches(db.getTextStorageTable())
        while i < end:  # Iterates through 7 of the entries depending on which page

            if len(textList) == 0:
                break

            # Labels to display the accounts on each page
            copyButton = ctk.CTkButton(window, text="Copy Text", command=copyText, font=("Impact", 20),
                                       fg_color='#fdff00', hover_color='#feff4a', corner_radius=10,
                                       text_color='black',
                                       anchor=CENTER, image=copyImage, compound="left")
            copyButton.grid(column=0, row=i + 3, ipadx=20)
            if publicViewMode:
                textDisplayLabel = ctk.CTkLabel(window, text=encryption.decryptString(textList[i][1]), width=400,
                                                height=45,
                                                font=("Helvetica", 20), fg_color="#1c1c1c", text_color="#f5f5f5",
                                                padx=10, pady=5, anchor=CENTER)
            else:
                textDisplayLabel = ctk.CTkButton(window, text=encryption.decryptString(textList[i][1]), width=400,
                                                 height=45, hover_color="#f5f5f5", corner_radius=0,
                                                 font=("Helvetica", 20), fg_color="#1c1c1c", text_color="#1c1c1c",
                                                 anchor=CENTER)
            textDisplayLabel.grid(column=1, row=i + 3, ipadx=20)

            # Button that calls the removeEntry method to delete an account from storage
            deleteButton = ctk.CTkButton(window, text="Delete",
                                         command=partial(removeTextEntry, textList[i][0]), font=("Impact", 20),
                                         fg_color='#ff0a0a', hover_color='#cc0000', corner_radius=10,
                                         text_color='black', anchor=CENTER, image=deleteImage, compound="left")
            deleteButton.grid(column=2, row=i + 3, pady=5)

            i = i + 1

            if len(db.getTextStorageTable()) <= i:
                break


# Main application screen with all the viewable accounts
def accountMainWindow():
    for widget in window.winfo_children():
        widget.destroy()

    accountWindowContent()


# Main application screen with all the viewable text
def textMainWindow():
    for widget in window.winfo_children():
        widget.destroy()

    textWindowContent()


# Same as the account main window, but has entry text fields to input new accounts
def addAccountMainWindow():
    for widget in window.winfo_children():
        widget.destroy()

    def addEntry(usage, username, password):
        usageEntry = encryption.encryptString(usage)
        userEntry = encryption.encryptString(username)
        passwordEntry = encryption.encryptString(password)

        db.createNewAccountEntry(usageEntry, userEntry, passwordEntry)
        global begin
        global end
        global i
        begin = 0
        end = 7
        i = begin
        accountMainWindow()

    accountWindowContent()

    # Entries to input new accounts
    siteEntry = ctk.CTkEntry(window, width=225, fg_color="#fdff00", text_color="black",
                             placeholder_text="Website Title", placeholder_text_color="#757575", corner_radius=5,
                             font=("Impact", 20), border_width=0, height=40)
    siteEntry.grid(row=i + 4, column=1, padx=10)
    usernameEntry = ctk.CTkEntry(window, width=225, fg_color="#fdff00", text_color="black",
                                 placeholder_text="Username or Email", placeholder_text_color="#757575",
                                 corner_radius=5,
                                 font=("Impact", 20), border_width=0, height=40)
    usernameEntry.grid(row=i + 4, column=2, padx=10)
    passWordEntry = ctk.CTkEntry(window, width=225, fg_color="#fdff00", text_color="black",
                                 placeholder_text="Password", placeholder_text_color="#757575", corner_radius=5,
                                 font=("Impact", 20), border_width=0, height=40)
    passWordEntry.grid(row=i + 4, column=3, padx=10)

    # Button that calls the addEntry method which will add the account to the database
    confirmButton = ctk.CTkButton(window, text="Confirm Entry",
                                  command=lambda: addEntry(siteEntry.get(), usernameEntry.get(), passWordEntry.get()),
                                  font=("Impact", 20),
                                  fg_color='#f5f5f5', hover_color='#dedede', corner_radius=10,
                                  text_color='black', anchor=CENTER, image=confirmImage, compound="left")
    confirmButton.grid(column=2, row=i + 7, pady=5)


# # Same as the text main window, but has entry text fields to input new text
def addTextMainWindow():
    for widget in window.winfo_children():
        widget.destroy()

    def addEntry(text):
        textInput = encryption.encryptString(text)

        db.createNewTextEntry(textInput)
        global begin
        global end
        global i
        begin = 0
        end = 7
        i = begin
        textMainWindow()

    textWindowContent()

    # Entries to add new text
    textEntry = ctk.CTkEntry(window, width=225, fg_color="#fdff00", text_color="black", height=40,
                             placeholder_text="Text", placeholder_text_color="#757575", corner_radius=5,
                             font=("Impact", 20), border_width=0)
    textEntry.grid(row=i + 4, column=1, padx=80)
    confirmButton = ctk.CTkButton(window, text="Confirm Entry",
                                  command=lambda: addEntry(textEntry.get()),
                                  font=("Impact", 20),
                                  fg_color='#f5f5f5', hover_color='#dedede', corner_radius=10,
                                  text_color='black', anchor=CENTER, image=confirmImage, compound="left")
    confirmButton.grid(column=1, row=i + 6, pady=5)


# Main application screen with all the viewable files
def fileManagementWindow():
    for widget in window.winfo_children():
        widget.destroy()

    global publicViewMode

    def insertFile():
        # Get the path of the file
        filepath = filedialog.askopenfilename()

        # Move the file to the "Files" directory
        destinationDirectory = "Files"
        if not os.path.exists(destinationDirectory):
            os.makedirs(destinationDirectory)
        newPath = "Files/" + os.path.basename(filepath).split('/')[-1]
        print(newPath)
        shutil.move(filepath, destinationDirectory)
        encryption.encryptFile(newPath)
        os.remove(newPath)
        fileManagementWindow()

    # Method to delete the file
    def deleteFile(fileName):
        os.remove('Files/' + fileName)
        fileManagementWindow()

    # Method to flip to the next page of files
    def nextPage():
        global begin
        global end
        if (begin + 7) < len(db.getAccountStorageTable()):
            begin = begin + 7
            end = end + 7
            accountMainWindow()

    # Method to flip to the previous page of files
    def previousPage():
        global begin
        global end
        global i
        i = begin
        if (begin - 7) >= 0:
            begin = begin - 7
            i = begin
            end = end - 7
            accountMainWindow()

    def toggleListView():
        accountMainWindow()

    def toggleViewMode():
        global publicViewMode
        if publicViewMode:
            publicViewMode = False
        else:
            publicViewMode = True
        fileManagementWindow()

    # Method to retrieve a file from the application to the desktop
    def retrieveFile(fileName):
        filePath = 'Files/' + fileName
        encryption.decryptFile(filePath)
        decryptedFilePath = 'Files/' + str(fileName).replace('.enc', '')
        desktopPath = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        shutil.copy(decryptedFilePath, desktopPath)
        os.remove(decryptedFilePath)
        fileManagementWindow()

    window.geometry("1200x700")
    window.unbind('<Return>')

    listSelectButton = ctk.CTkButton(window, text="Now Viewing: Files", command=toggleListView, font=("Impact", 20),
                                     fg_color='#fdff00', hover_color='#feff4a', corner_radius=10, text_color='black',
                                     anchor=CENTER, image=changeListImage, compound="left")
    listSelectButton.grid(column=1)

    viewModeButton = ctk.CTkButton(window, text="Toggle View Mode", command=toggleViewMode, font=("Impact", 20),
                                   fg_color='#fdff00', hover_color='#feff4a', corner_radius=10, text_color='black',
                                   anchor=CENTER, image=viewModeImage, compound="left")
    viewModeButton.grid(column=0, row=0, pady=10)

    assistButton = ctk.CTkButton(window, text="Assistance", font=("Impact", 20),
                                 fg_color='#fdff00', hover_color='#feff4a', corner_radius=10, text_color='black',
                                 anchor=CENTER, image=micImage, compound="left")
    assistButton.grid(column=2, row=0, pady=10)

    rightButton = ctk.CTkButton(window, command=nextPage, image=rightImage, fg_color='#fdff00',
                                hover_color='#feff4a', text="", corner_radius=10, anchor=CENTER)
    rightButton.grid(column=2, pady=10, row=1)

    leftButton = ctk.CTkButton(window, command=previousPage, image=leftImage, fg_color='#fdff00', hover_color='#feff4a',
                               text="", corner_radius=10, anchor=CENTER)
    leftButton.grid(column=0, pady=10, row=1)

    # This button calls the insertFile method, prompting the user to add a file
    addButton = ctk.CTkButton(window, text="ADD", command=insertFile, font=("Impact", 20),
                              fg_color='#fdff00', hover_color='#feff4a', corner_radius=10, text_color='black',
                              anchor=CENTER, image=addFileImage, compound="left")
    addButton.grid(column=1, pady=10, row=1)

    textLabel = ctk.CTkLabel(window, text="File Name", font=("Impact", 20),
                             fg_color="transparent", text_color="#f5f5f5",
                             anchor=CENTER)
    textLabel.grid(row=2, column=1, padx=80)

    fileList = os.listdir("Files")

    if fileList is not None:  # If there are entries in the storage
        global i
        global begin
        global end
        i = begin
        while i < end:  # Iterates through 7 of the entries depending on which page

            print(fileList)
            if len(fileList) == 0:
                break

            # Button to call the retrieveFile() method
            retrieveButton = ctk.CTkButton(window, text="Retrieve File",
                                           command=lambda: retrieveFile(textDisplayLabel.cget("text")),
                                           font=("Impact", 20),
                                           fg_color='#fdff00', hover_color='#feff4a', corner_radius=10,
                                           text_color='black',
                                           anchor=CENTER, image=copyImage, compound="left")
            retrieveButton.grid(column=0, row=i + 3, ipadx=20)

            if publicViewMode:
                textDisplayLabel = ctk.CTkLabel(window, text=fileList[i], width=220, height=45,
                                                font=("Helvetica", 20), fg_color="#1c1c1c", text_color="#f5f5f5",
                                                padx=10, pady=5, anchor=CENTER)
                textDisplayLabel.grid(column=1, row=i + 3, ipadx=20)
            else:
                textDisplayLabel = ctk.CTkButton(window, text=fileList[i], width=220,
                                                 height=45, hover_color="#f5f5f5", corner_radius=0,
                                                 font=("Helvetica", 20), fg_color="#1c1c1c", text_color="#1c1c1c",
                                                 anchor=CENTER)
                textDisplayLabel.grid(column=1, row=i + 3, ipadx=20)

            # Button that calls the deleteFile() method to delete a file from storage
            deleteButton = ctk.CTkButton(window, text="Delete",
                                         command=lambda: deleteFile(fileList[i]), font=("Impact", 20),
                                         fg_color='#ff0a0a', hover_color='#cc0000', corner_radius=10,
                                         text_color='black', anchor=CENTER, image=deleteImage, compound="left")
            deleteButton.grid(column=2, row=i + 3, pady=5)

            i = i + 1

            if len(fileList) <= i:
                break
