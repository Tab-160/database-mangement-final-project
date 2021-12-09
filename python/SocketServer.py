# Basic socket programming example of server application

import socket
import threading
import runSQL
import WebSocket
import struct
import base64

def runSocketServer():        
    HOST = '127.0.0.1'  # localhost
    PORT = 50002        # Port to listen on

    while(True):
        # Sets code up to use IPv4 and TCP.
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))    # Binds HOST ip to PORT socket
            s.listen()  # Prepares server to hear a connection

            # Blocks and waits for an incoming request.
            # When connection is made, store in conn
            conn, addr = s.accept()

            with conn:
                # Recives and prints data from client
                data = conn.recv(4096)

                # Turn into regular text
                #data = data.decode('utf-8')
                print ("SocketServer Data:", data)

                # Get key
                key = WebSocket.findKey(data)
                print(len(base64.b64decode(key)))
                print(key)
                
                # Send proper response
                handshake = WebSocket.buildResponse(key)
                print("Handshake:", handshake)

                # Change the EnDian format
                little = struct.pack('<s', handshake)
                big = struct.pack('>s', handshake)
                print("Big:", big)
                print("Little:", little)
                
                conn.send(handshake)


                # Recive sql request
                data = conn.recv(4096)

                print("SocketServer Data before decoding:", data)

                # Turn into regular text
                data = data.decode('utf-8')
                print ("SocketServer Data:", data)
                

                # Run SQL
                sql_result = runSQL.runSQL(data)

                print(sql_result)


        
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
    runSocketServer()
