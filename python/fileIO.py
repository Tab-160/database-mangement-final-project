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
    <a href=sign-in.html style="float:right;" id='user'>Sign-In</a>
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
    userID = str(userID)
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
    <a href=sign-in.html style="float:right;" id='user'>Sign-In</a>
    
"""
        f.write(head)

        # Get some basic info
        username = runSQL.runSQL("SELECT Username FROM Users WHERE userID = " + userID)[0][0]
        email = runSQL.runSQL("SELECT Email FROM Users WHERE userID = " + userID)[0][0]
        main_bank_name = runSQL.runSQL("SELECT l.name FROM Users u, Locations l WHERE u.MainBank = l.id AND u.userID = " + userID)[0][0]
        
        basic_info = "<p>Username: "
        basic_info += username
        basic_info += "</p>\n      <p>Email: "
        basic_info += email
        basic_info += "</p>\n      <p>Preferd Location: "
        basic_info += main_bank_name
        basic_info += "</p>\n"
        f.write(basic_info)
        
        transactions = runSQL.runSQL("SELECT p.Name, l.Name, t.Quantity, t.Trans_Date, t.Trans_Type FROM Transaction t, Locations l, Products p WHERE t.ProdID = p.ID AND t.LocID = l.ID AND t.UserID = " + userID)
        
        table = """    <h2>Search Results</h2>
    <table>
        <tr>
            <th>Product Name</th>
            <th>Location</th>
            <th>Amount</th>
            <th>Date</th>
            <th>Type of Transaction</th>
        </tr>"""
        
        # Loop though each of the elements in the list
        for i in transactions:
            # Opening tag for row
            row = "      <tr>\n"
            # Loop through each of the elements in the tuple
            for j in i:
                # Add the data as a td element
                row += "        <td>" + str(j) + "</td>\n"
            # Reached end of row, close row
            row += "      </tr>\n"
            # Write this row into file
            table += row
            
        # Once done, write to file
        f.write(table)

        # Finished with data, add footer
        foot = """    </table>
  </body>
</html>"""
        f.write(foot)
