""" Builds appropriete HTTP response messages

"""

def error505():
    """ Builds and returns an HTTP/1.1 505 Version Not Supported"""
    msg = b'HTTP/1.1 505 Version Not Supported\r\n'
    msg += b'Content-Length: 62\r\n\r\n' # Final header
    msg += b'As of 2021-11-29, this server only works with HTTP version 1.x'

    return msg

def error501():
    """ Builds and returns an HTTP/1.1 501 Not Implemented"""
    msg = b'HTTP/1.1 501 Not Implemented\r\n'
    msg += b'Content-Length: 63\r\n\r\n' # Final header
    msg += b'As of 2021-12-09, server does not yet support non-GET or POST requests.'

    return msg

def sendFile(file_loc):
    """ Builds a HTTP/1.1 response with file file_loc as the content

    Args:
        file_loc: string with the location of the file to be included

    Return:
        HTTP/1.1 response as a binary string
    """   
    file_contents = b''

    # Read in file
    try:
        with open(file_loc, 'rb') as f: 
            file_contents = f.read()
    except: # If file cannot be opened, then assume that it cannot be found
        return b'HTTP/1.1 404 File Not Found\r\n\r\n'

    status_code = b'HTTP/1.1 200 OK\r\n'   # Proper HTTP status code

    # Set up headers as binary
    headers = b'Connection: keep-alive\r\n'
    headers += b'Content-Length: ' + str(len(file_contents)).encode('utf-8')
    headers += b'\r\n\r\n'  # This is the last header, so a blank line is added

    # message to be sent
    msg = status_code
    msg += headers
    msg += file_contents

    return msg

def postReponse():
    msg = b"HTTP/1.1 303 See Other\r\n"
    msg += b"Connection: keep-alive\r\n"
    msg += b"Location: search_results.html\r\n\r\n"

    return msg
