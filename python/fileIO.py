"""File IO stuff. 

    Handles all file input/output operations that are not SQL-query related
    Methods:
        getFileLoc(request)
        createFile(sql_response, file_loc)

"""

# Used to send file
import socket

import HTTPServer
import runSQL

# Location of this project
# Example: "C:\\Users\\rgreenup24\\Desktop\\finalProjectDatabase\\"
PROJECT_LOCATION = "D:\\database-mangement-final-project\\"


def getFileLoc(request):
    """ Finds the file location from an HTTP request
        Uses the domain specified in HTTPServer

    Args:
        request: An HTTP GET request
    """
    # Find the end of the first line, ending point of file location
    version_index = request.find(b'HTTP')

    # Because this is a GET request
    # We know the file location begins at index 4
    # Goes until the space before "HTTP"
    file_loc = request[request.find(b' ') + 1:version_index-1]

    # If the server included the domain, ignore it
    while(file_loc.find(HTTPServer.DOMAIN.encode('utf-8')) > 0):
        file_loc = file_loc[len(HTTPServer.DOMAIN)+2:]
    
    if(file_loc == b'/'):    # If /, then index is wanted
        file_loc += b"index.html"
    
    # If there is an illegal char, ignore everything after
    if(file_loc.find(b'?') > 0):
        file_loc = file_loc[0:file_loc.find(b'?')]

    return(file_loc)
    

def createSearchFile(sql_response, file_loc):
    """ Creates a HTML file at file_loc that
        displays the data in sql_response nicely

    Args:
        sql_response: A list of tuples with the data from a pyodbc execution
        file_loc: Location for the file to be created
            If it already exists, file will be overwritten
    """
    
    with open(file_loc, 'w') as f:  # creates file
        # Writes the top of the file
        head = """<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8"/>
  </head>
  <body>
    <a href="index.html">Home</a>
    <a href="search.html">Search for a product</a>
    <a href=sign-in.html align=right id='user'>Sign-In</a>
    <h2>Search Results</h2>
    <table>
        <tr>
            <th>Name</th>
            <th>Category</th>
            <th>Unit Volume</th>
        </tr>
"""
        f.write(head)

        # Loop though each of the elements in the list
        for i in sql_response:
            # Opening tag for row
            row = "      <tr>\n"
            # Loop through each of the elements in the tuple
            for j in i:
                # Add the data as a td element
                row += "        <td>" + str(j) + "</td>\n"
            # Reached end of row, close row
            row += "      </tr>\n"
            # Write this row into file
            f.write(row)

        # Finished with data, add footer
        foot = """    </table>
  </body>
</html>"""
        f.write(foot)

        #done

def createUserFile(userID, file_loc):
    """ Creates a HTML file at file_loc that
        displays user info

    Args:
        sql_response: A list of tuples with the data from a pyodbc execution
        file_loc: Location for the file to be created
            If it already exists, file will be overwritten
    """
    
    with open(file_loc, 'w') as f:  # creates file
        # Writes the top of the file
        head = """<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8"/>
  </head>
  <body>
    <a href="index.html">Home</a>
    <a href="search.html">Search for a product</a>
    <a href=sign-in.html align=right id='user'>Sign-In</a>
    
"""
        f.write(head)

        username = runSQL.runSQL("SELECT Username FROM Users WHERE userID = '" + userID + "'")[0][0]

        f.write("<p>Your username is: " + username + "</p>")

        # Finished with data, add footer
        foot = """    </table>
  </body>
</html>"""
        f.write(foot)
