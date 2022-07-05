import base64
from typing import final

def encrypt(message):
    message = str(message)
    message = base64.b64encode(message.encode('utf-8')).decode('utf-8')
    cipher = ''
    for letter in message:
        if letter == ' ':
            cipher += ' '
        elif letter == 'z':
            cipher += 'a'
        else:
            cipher += chr(ord(letter) + 1)
    return cipher

def decrypt(cipher):
    cipher = str(cipher)
    message = ''
    for letter in cipher:
        if letter == ' ':
            message += ' '
        elif letter == 'a':
            message += 'z'
        else:
            message += chr(ord(letter) - 1)
        
    final = base64.b64decode(message.encode('utf-8')).decode('utf-8')
    return final

