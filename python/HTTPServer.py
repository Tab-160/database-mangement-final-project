# Basic socket programming example of server application

import socket
import threading
import runSQL
import fileIO

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
                    
                    # If the request is a get request
                    if(data[0:data.find(" ")] == "GET"):
                        file_loc = data[4:version_index-1]  # Grab the file location

                        if(file_loc == "/"):    # If /, then index is wanted
                            file_loc += "index.html"

                        # All files are in the assets folder
                        file_loc = "C:\\Users\\rgreenup24\\Desktop\\finalProjectDatabase\\assets" + file_loc

                        # If there is an illegal char, ignore everything after
                        if(file_loc.find("?") > 0):
                            file_loc = file_loc[0:file_loc.find("?")]

                        #Send file
                        fileIO.sendFile(conn, file_loc)

                        continue    # Skip to next data sent by client

                    # If there is a post request, then it is search or sign-in
                    elif(data[0:data.find(" ")] == "POST"):
                        data = data[data.find("\r\n\r\n")+4:]
                        print(data)
                        print(runSQL.runSQL(data))

                
                    else:   # Not a GET or POST request, therefor not supported
                        #Build the error message
                        msg = "HTTP/1.1 501 Not Implemented\r\n"
                        msg += "Content-Length: 63\r\n\r\n" # Final header
                        msg += "As of 2021-12-09, server does not yet support non-GET or POST requests."

                        conn.sendall(msg.encode('utf-8'))   # Send error to client

if __name__ == '__main__':
    runHTTPServer()
