""" Functions related to WebSocket"""

import base64
import struct

from hashlib import sha1


def buildResponse(key):
    """Creates proper response for a server to send to a Websocket
        from key key
        Does not send!!!!
    """
    magic_string = b'258EAFA5-E914-47DA-95CA-C5AB0DC85B11'

    # Concatenate key with magic_string
    key += magic_string

    # Hash key
    accept = sha1(key).digest()

    # Turn to base-64
    accept = base64.b64encode(accept)
    print("\n", accept, "\n")

    # Add to rest of message
    val = b'HTTP/1.1 101 Switching Protocols\r\n'
    val += b'Upgrade: websocket\r\n'
    val += b'Connection: Upgrade\r\n'
    val += b'Sec-WebSocket-Accept: ' + accept + b'\r\n\r\n'    

    return val

def findKey(data):
    """ Returns the value of the Sec-WebSocket-Key header in data
        Takes in a string
"""
    # Where the header title ends and value begins
    key_index = data.find(b'Sec-WebSocket-Key: ')
    key_index += 19

    key_value = data[key_index:data.find(b'==')+2]
    return key_value
    
