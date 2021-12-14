""" deals with password management

    Methods:
        verifyPassword()
        
"""

import hashlib

import runSQL


def verifyPassword(username, password):
    """ Given username, checks that password  is the correct password

        Returns: the UserID of the user, or null if username not found or password
            incorrect
    """
    # Get the password for the given username
    correctPass = runSQL.runSQL("SELECT Password FROM Users WHERE Username = '" + username + "'")
    # Because runSQL returns list to tuples, and we just want data, get data
    try:
        correctPass = correctPass[0][0]
    except: # If out of bounds error, then username doesn't exist
        return False

    # Retrieve salt
    salt = runSQL.runSQL("SELECT Salt FROM Users WHERE Username = '" + username + "'")
    salt = salt[0][0]

    # Append the salt to the end of password
    combinedPassword = password + salt

    # Hash the combined password with sha512
    hashed = hashlib.sha512(combinedPassword.encode('utf-8')).hexdigest()

    # If the values are the same
    if correctPass == hashed:
        return runSQL.runSQL("SELECT UserID FROM Users WHERE Username = '" + username + "'")[0][0]

    # If we get to this point, username and password do not match
    return False

