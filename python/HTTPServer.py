# Basic socket programming example of server application

import socket
import threading
import runSQL
import WebSocket

def runHTTPServer():
    """Starts and continues operation of HTTP server"""
        
    HOST = '127.0.0.1'  # localhost
    PORT = 50001        # Port to listen on

    while(True):
        # Sets code up to use IPv4 and TCP.
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))    # Binds HOST ip to PORT socket
            s.listen()  # Prepares server to hear a connection

            # Blocks and waits for an incoming request.
            # When connection is made, store in conn
            conn, addr = s.accept()

            with conn:
                while(True):
                    print("waiting for data...")
                    # Recives and prints data from client
                    data = conn.recv(4096)

                    # Turn into regular text
                    data = data.decode('utf-8')
                
                    print ("Data:", data)

                    if(not data):
                        break

                    # Checks HTTP version
                    version_index = data.find("HTTP")
                        # If version is not 1.1, send error and get next data                    
                    if(data[version_index:version_index+7] != "HTTP/1."):
                        # Build error message
                        msg = "HTTP/1.1 505 Version Not Supported\r\n"
                        msg += "Content-Length: 62\r\n\r\n" # Final header
                        msg += "As of 2021-11-29, this server only works with HTTP version 1.x"

                        conn.sendall(msg.encode('utf-8'))   # Send error to client
                    
                        continue # Skip to next data sent by client
                    
                    # If the request is not a get request
                    if(data[0:3] != "GET"):
                        #Build the error message
                        msg = "HTTP/1.1 501 Not Implemented\r\n"
                        msg += "Content-Length: 63\r\n\r\n" # Final header
                        msg += "As of 2021-11-29, server does not yet support non-GET requests."

                        conn.sendall(msg.encode('utf-8'))   # Send error to client
                    
                        continue    # Skip to next data sent by client
                    

                
                    file_loc = data[4:version_index-1]  # Grab the file location

                    if(file_loc == "/"):    # If /, then index is wanted
                        file_loc += "index.html"

                    file_loc = "C:\\Users\\rgreenup24\\Desktop\\finalProjectDatabase\\assets" + file_loc  # All files are in the assets folder

                    # If there is an illegal char, ignore everything after
                    if(file_loc.find("?") > 0):
                        file_loc = file_loc[0:file_loc.find("?")]

                    #Send file
                    sendFile(conn, file_loc)

        
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
        print ("404")
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


if __name__ == '__main__':
    #HTTPServer = threading.Thread(target=runHTTPServer)
    #SocketServer = threading.Thread(target=runSocketServer)
    #HTTPServer.start()
    #SocketServer.start()
    runHTTPServer()
