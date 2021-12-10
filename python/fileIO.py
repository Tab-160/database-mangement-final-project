# File IO stuff
# has:
# sendFile()
# buildHTML()

import socket

# For testing:
import runSQL
 
def sendFile(conn, file_loc):
    """ Sends file over TCP connection using HTTP/1.1

    Args:
        conn: An accepted TCP connection
        file_loc: string with the location of the file to be sent
    """   
    file_contents = -1

    try:
        with open(file_loc, 'rb') as f:  # Opens and reads file
            file_contents = f.read()
    except: # If file cannot be opened, then assume that it cannot be found
        conn.sendall("HTTP/1.1 404 File Not Found\r\n".encode('utf-8'))
        print ("fileIO404")
        return

    status_code = "HTTP/1.1 200 OK\r\n"   # Proper HTTP status code

    headers = "Connection: keep-alive\r\n"
    headers += "Content-Length: " + str(len(file_contents)) + "\r\n\r\n"
    # This is the last header, so a blank line is added

    # message to be sent
    msg = status_code.encode('utf-8')
    msg += headers.encode('utf-8')
    msg += file_contents

    print("Sending", file_loc)
    conn.sendall(msg)   # Send message
    print("Sent!\n\n")

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
  <head>
  </head>
  <body>
    <a href="index.html">Home</a>
    <a href=sign-in.html>Sign-In</a>
    <a href="search.html">Search for a product</a>
    <p>Search Results</p>
    <table>
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


if __name__ == '__main__':
    createFile(runSQL.runSQL("SELECT * FROM products"), "C:\\Users\\rgreenup24\\Desktop\\finalProjectDatabase\\assets\\file.html")
