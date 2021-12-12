""" Basic socket programming example of server application

    Runs an HTTP/1.1 server. 

"""
import socket
import multiprocessing
import time

import runSQL
import fileIO

HOST = "127.0.0.1"  # localhost
PORT = 50001        # Port to listen on
DOMAIN = "127.0.0.1:50001"

def runHTTPServer():
    """Starts and continues operation of HTTP server"""
    while True:
        # Sets code up to use IPv4 and TCP.
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))    # Binds HOST ip to PORT socket
            s.listen()  # Prepares server to hear a connection

            s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

            # Blocks and waits for an incoming request.
            # When connection is made, store in conn
            conn, addr = s.accept()

            with conn:
                while True:
                    print("waiting for data...")
                    # Recives and prints data from client
                    data = conn.recv(4096)
                    print ("Data:", data)

                    if not data:   # If there is no data, skip till there is
                        continue

                    # Checks HTTP version
                    version_index = data.find(b'HTTP')
                    # If version is not 1.1, send error and get next data                    
                    if data[version_index:version_index+7] != b'HTTP/1.':
                        # Build error message
                        msg = b'HTTP/1.1 505 Version Not Supported\r\n'
                        msg += b'Content-Length: 62\r\n\r\n' # Final header
                        msg += b'As of 2021-11-29, this server only works with HTTP version 1.x'

                        conn.sendall(msg)   # Send error to client
                    
                        continue # Skip to next data sent by client
                    
                    # If the request is a get request, send the associated file
                    if data[0:data.find(b' ')] == b'GET':
                        # Get the location of the file
                        file_loc = fileIO.getFileLoc(data)
                        # All files are in the assets folder
                        file_loc = fileIO.PROJECT_LOCATION + "assets\\" + file_loc
                        
                        #Send file
                        fileIO.sendFile(conn, file_loc)

                        continue    # Skip to next data sent by client

                    # If there is a post request, then it is search
                    elif data[0:data.find(b' ')] == b'POST':
                        # Find the body of the data
                        data = data[data.find(b'\r\n\r\n')+4:]
                        # Run SQL
                        sql_result = runSQL.runSQL(data)
                        # Create search_result.html
                        fileIO.createFile(sql_result, fileIO.PROJECT_LOCATION + "assets\\search_results.html")

                        # Build and send response
                        msg = b"HTTP/1.1 303 See Other\r\n"
                        msg += b"Connection: keep-alive\r\n"
                        msg += b"Location: search_results.html\r\n\r\n"

                        conn.sendall(msg)

                    #elif data[0:data.find(b' ')] == b'PUT':
                        # Sign user in here
               
                    else:   # Not a GET or POST request, therefor not supported
                        #Build the error message
                        msg = "HTTP/1.1 501 Not Implemented\r\n"
                        msg += "Content-Length: 63\r\n\r\n" # Final header
                        msg += "As of 2021-12-09, server does not yet support non-GET or POST requests."

                        conn.sendall(msg.encode('utf-8'))   # Send error

if __name__ == '__main__':
    # Start the server, and every 5 seconds restart it
    #while(True):
    #    server = multiprocessing.Process(target=runHTTPServer)
    #    server.start()
    #    print("Starting server!")
    #    time.sleep(5)
    #    print("Closing Server!")
    #    server.terminate()
    runHTTPServer()







        
