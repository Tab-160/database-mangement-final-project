""" Basic socket programming example of server application

    Runs an HTTP/1.1 server. 

"""
import socket
import multiprocessing
import time

import runSQL
import fileIO
import passwordManagement
import HTTPResponse

HOST = "10.200.100.92"  # localhost
PORT = 50001        # Port to listen on
DOMAIN = HOST + ":" + str(PORT)

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
                    #print ("Data:", data)

                    if not data:   # If there is no data, skip till there is
                        continue

                    # Check if there is a userID cookie
                    cookie_loc = data.find(b'Cookie: userID=')
                    cookie = b''
                    # If there is, grab the value
                    if cookie_loc > -1:
                        cookie = data[cookie_loc + 15:data.find(b'/r/n')]

                    # Checks HTTP version
                    version_index = data.find(b'HTTP')
                    # If version is not 1.1, send error and get next data                    
                    if data[version_index:version_index+7] != b'HTTP/1.':
                        # Build error message and send
                        conn.sendall(HTTPResponse.error505())
                        
                        continue # Skip to next data sent by client
                    
                    # Check what type of request it is
                    requestType = data[0:data.find(b' ')]
                    # If the request is a get request, send the associated file
                    if requestType == b'GET':
                        # Get the location of the file
                        file_loc = fileIO.getFileLoc(data).decode('utf-8')

                        # If the user wants to see profile, then create it
                        if file_loc == "profile.html":
                            fileIO.createUserFile(cookie, "profile.html")
                        
                        # All files are in the assets folder
                        file_loc = fileIO.PROJECT_LOCATION + "assets" + file_loc
                      
                        #Send file
                        conn.sendall(HTTPResponse.sendFile(file_loc))

                    # If there is a post request, then it is search
                    elif requestType == b'POST':
                        print("Post")
                        
                        file_loc = fileIO.getFileLoc(data).decode('utf-8')
                        print(file_loc)
                        
                        # Find the body of the data
                        data = data[data.find(b'\r\n\r\n')+4:]

                        # If the post request was for search_results, then run search
                        if file_loc == "/search_results":
                            # Run SQL
                            sql_result = runSQL.runSQL(data.decode('utf-8'))
                            # Create search_result.html
                            fileIO.createSearchFile(sql_result, fileIO.PROJECT_LOCATION + "assets\\search_results.html")

                            # Build and send response
                            conn.sendall(HTTPResponse.postResponse(file_loc.encode('utf-8')))

                        # Sign in user
                        elif file_loc == "/page":
                            print("Page")
                            # Get from start to bar, store as string
                            username = data[0:data.find(b'|')].decode('utf-8')

                            # Get from bar (don't include) to end, this is password
                            password = data[data.find(b'|')+1:].decode('utf-8')

                            # Get userid of user associated with username, password
                            userID = passwordManagement.verifyPassword(username, password)

                            if userID: # if not false
                                print("userID")
                                # Create profile page
                                fileIO.createUserFile(userID, fileIO.PROJECT_LOCATION + "assets\\profile.html")

                                # Create a generic post response
                                response = HTTPResponse.postResponse(b'profile.html')

                                # Remove last two characters
                                response = response[0:len(response)-2]
                                # Add cookie
                                response += b"Set-Cookie: userID=" + userID.encode('utf-8') + b"/r/n/r/n"

                                print(response, len(response))
                                # Make sure that all is sent
                                amountSent = 0
                                while amountSent < len(response):
                                    amountSent = conn.send(response)
                                    print(amountSent)

                            
               
                    else:   # Not a GET or POST request, therefor not supported
                        #Build the error message and send
                        conn.sendall(HTTPResponse.error501())

if __name__ == '__main__':
    # Start the server, and every 5 seconds restart it
    """while(True):
        server = multiprocessing.Process(target=runHTTPServer)
        server.start()
        print("Starting server!")
        time.sleep(15)
        print("Closing Server!")
        server.terminate()"""
    runHTTPServer()

