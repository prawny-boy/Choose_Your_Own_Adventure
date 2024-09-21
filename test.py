from inputimeout import inputimeout
import sys
while True:
    e=''
    print('a')
    print('a')
    try:
        e = inputimeout('Chiner', 5)
    except:
        
        print()
        LINE_UP = '\033[1A'
        LINE_CLEAR = '\x1b[2K'
        print(LINE_UP, end='')
        sys.stdout.flush()
        print('You died')
    if e == '':
        break