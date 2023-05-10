import hashlib
import sqlite3 as sql

# Create cursor to navigate the database
with sql.connect("asis.db") as db:
    cursor = db.cursor()

# Using Prepared Statements (with Parameterized Queries) to prevent SQL Injection.


# Create master password and reset code SQL table.
def createMasterTable():
    cursor.execute("""

    CREATE TABLE IF NOT EXISTS master(
        id INTEGER PRIMARY KEY,
        password TEXT NOT NULL,
        resetCode TEXT NOT NULL
    );

    """)


# Create the account storage SQL table to store usage, usernames, and passwords.
def createAccountStorageTable():
    cursor.execute("""

    CREATE TABLE IF NOT EXISTS storage(
        id INTEGER PRIMARY KEY,
        usage TEXT NOT NULL,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    );

    """)


# Create the text storage SQL table to store raw text.
def createTextStorageTable():
    cursor.execute("""
    
    CREATE TABLE IF NOT EXISTS textStorage(
        id INTEGER PRIMARY KEY,
        uText TEXT NOT NULL
    );
    
    """)


# Method to delete the old master password in the event of a reset
def deleteOldMaster():
    command = "DELETE FROM master WHERE id = 1"
    cursor.execute(command)


# Create a new master password and reset code in the event of a reset
def createNewMaster(hPassword, resetCode):
    insertPassword = """

                INSERT INTO master(password, resetCode)
                VALUES(?, ?)

                """
    cursor.execute(insertPassword, (hPassword, resetCode))
    db.commit()


# Method to insert a new account into the database
def createNewAccountEntry(usage, username, password):
    insertData = """

            INSERT INTO storage (usage, username, password)
            VALUES (?, ?, ?)

            """
    cursor.execute(insertData, (usage, username, password))
    db.commit()


# Method to insert new raw text into the database
def createNewTextEntry(text):
    insertData = """

                INSERT INTO textStorage (uText)
                VALUES (?)

                """
    cursor.execute(insertData, (text,))
    db.commit()


# Remove a text entry from the database
def removeTextEntry(removeID):
    cursor.execute("DELETE FROM textStorage WHERE id = ?", (removeID,))
    db.commit()


# Remove an account from the database
def removeAccountEntry(removeID):
    cursor.execute("DELETE FROM storage WHERE id = ?", (removeID,))
    db.commit()


# Fetches the master password for login confirmation
def findMasterPassword(password):
    cursor.execute("SELECT * FROM master WHERE id = 1 AND password = ?", [password])
    return cursor.fetchall()


# Fetches the reset code for reset code confirmation
def findResetCode(resetCode):
    cursor.execute("SELECT * FROM master WHERE id = 1 AND resetCode = ?", [resetCode])
    return cursor.fetchall()


# Gets all entries in the account storage table and returns a list to display on the screen
def getAccountStorageTable():
    cursor.execute("SELECT * FROM storage")
    dbList = cursor.fetchall()
    return dbList


# Gets all entries in the text storage table and returns a list to display on the screen
def getTextStorageTable():
    cursor.execute("SELECT * FROM textStorage")
    dbList = cursor.fetchall()
    return dbList


# Check if the application has a master password, and return true or false to determine to show login or registration
def hasMaster():
    cursor.execute("SELECT * FROM master")
    return cursor.fetchall()
