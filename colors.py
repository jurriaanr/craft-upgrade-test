import os
import sys
from sty import fg, bg, ef, rs
if sys.platform.lower() == "win32":
    os.system('color')

def black(text):
    print('\033[30m', text, '\033[0m', sep='')

def red(text):
    print(fg.red, text, fg.rs, sep='')

def green(text):
    print(fg(116, 226, 0), text, fg.rs, sep='')

def yellow(text):
    print('\033[33m', text, '\033[0m', sep='')

def blue(text):
    print('\033[34m', text, '\033[0m', sep='')

def magenta(text):
    print('\033[35m', text, '\033[0m', sep='')

def cyan(text):
    print('\033[36m', text, '\033[0m', sep='')

def gray(text):
    print('\033[90m', text, '\033[0m', sep='')
