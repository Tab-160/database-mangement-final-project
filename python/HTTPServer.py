# Basic socket programming example of server application

import socket
import multiprocessing
import time
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

            s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

            # Blocks and waits for an incoming request.
            # When connection is made, store in conn
            conn, addr = s.accept()

            with conn:
                print(addr)
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
                        domain = HOST + ":" + str(PORT)
                        # Get the location of the file
                        file_loc = fileIO.getFileLoc(data, domain)
                        
                        # All files are in the assets folder
                        file_loc = fileIO.PROJECT_LOCATION + "assets\\" + file_loc

                        
                        #Send file
                        fileIO.sendFile(conn, file_loc)

                        continue    # Skip to next data sent by client

                    # If there is a post request, then it is search or sign-in
                    elif(data[0:data.find(" ")] == "POST"):
                        # Find the body of the data
                        data = data[data.find("\r\n\r\n")+4:]
                        # Currently, only search implemented. So, run search
                        fileIO.createFile(runSQL.runSQL(data), fileIO.PROJECT_LOCATION + "assets\\search_results.html")

                        # Build and send response, assuming search
                        msg = b"HTTP/1.1 303 See Other\r\n"
                        msg += b"Content-Length: 205\r\n"
                        msg += b"Connection: keep-alive\r\n"
                        msg += b"Location: search_results.html\r\n\r\n"

                        # Open response
                        with open(fileIO.PROJECT_LOCATION + "assets\\redirect.html", 'rb') as f:  # Opens and reads file
                            file_contents = f.read()

                        msg += file_contents

                        conn.sendall(msg)
               
                    else:   # Not a GET or POST request, therefor not supported
                        #Build the error message
                        msg = "HTTP/1.1 501 Not Implemented\r\n"
                        msg += "Content-Length: 63\r\n\r\n" # Final header
                        msg += "As of 2021-12-09, server does not yet support non-GET or POST requests."

                        conn.sendall(msg.encode('utf-8'))   # Send error to client

if __name__ == '__main__':
    #while(True):
    #    server = multiprocessing.Process(target=runHTTPServer)
    #    server.start()
    #    print("Starting server!")
    #    time.sleep(5)
    #    print("Closing Server!")
    #    server.terminate()
    runHTTPServer()







        
