"""File IO stuff. 

    Handles all file input/output operations that are not SQL-query related
    Methods:
        getFileLoc(request)
        sendFile(conn, file_loc)
        createFile(sql_response, file_loc)

"""

# Used to send file
import socket

import HTTPServer

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
    version_index = request.find("HTTP")

    # Because this is a GET request
    # We know the file location begins at index 4
    # Goes until the space before "HTTP"
    file_loc = request[4:version_index-1]

    # If the server included the domain, ignore it
    while(file_loc.find(HTTPServer.DOMAIN) > 0):
        file_loc = file_loc[len(HTTPServer.DOMAIN)+1:]
    
    if(file_loc == "/"):    # If /, then index is wanted
        file_loc += "index.html"
    
    # If there is an illegal char, ignore everything after
    if(file_loc.find("?") > 0):
        file_loc = file_loc[0:file_loc.find("?")]

    return(file_loc)
    
 
def sendFile(conn, file_loc):
    """ Sends file over TCP connection using HTTP/1.1

    Args:
        conn: An accepted TCP connection
        file_loc: string with the location of the file to be sent
    """   
    file_contents = b''

    # Read in file
    try:
        with open(file_loc, 'rb') as f: 
            file_contents = f.read()
    except: # If file cannot be opened, then assume that it cannot be found
        conn.sendall(b'HTTP/1.1 404 File Not Found\r\n\r\n')
        return

    status_code = b'HTTP/1.1 200 OK\r\n'   # Proper HTTP status code

    # Set up headers as binary
    headers = b'Connection: keep-alive\r\n'
    headers += b'Content-Length: ' + bin(len(file_contents)) + b'\r\n\r\n'
    # This is the last header, so a blank line is added

    # message to be sent
    msg = status_code
    msg += headers
    msg += file_contents

    conn.sendall(msg)   # Send message

def createFile(sql_response, file_loc):
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
  <head></head>
  <body>
    <a href="index.html">Home</a>
    <a href=sign-in.html>Sign-In</a>
    <a href="search.html">Search for a product</a>
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
