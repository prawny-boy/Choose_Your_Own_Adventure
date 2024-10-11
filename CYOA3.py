from moduleInstall import installIfNeeded
from datetime import datetime
def log(message):
    print(datetime.now().strftime("%a %b %d %H:%M:%S") + " - " + str(message))
installIfNeeded("termcolor", "termcolor", log = log)
installIfNeeded("keyboard", "keyboard", log = log)
installIfNeeded("pygame", "pygame", log = log)
import sys
sys.dont_write_bytecode = True # makes sure _pycache_ is not created
from termcolor import cprint, colored
from keyboard import is_pressed
import pygame
import base64

def b64_encode(s:str) -> str:
    sample_string_bytes = s.encode("ascii")
    base64_bytes = base64.b64encode(sample_string_bytes)
    base64_string = base64_bytes.decode("ascii")
    return base64_string

def b64_decode(s:str) -> str:
    base64_bytes = s.encode("ascii")
    sample_string_bytes = base64.b64decode(base64_bytes)
    sample_string = sample_string_bytes.decode("ascii")
    return sample_string
    
print(b64_encode(input('Encode: ')))
print(b64_decode(input('Decode: ')))