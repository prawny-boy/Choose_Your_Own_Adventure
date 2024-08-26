#choice = input('Chiner')
#print("\033[A"+(" "*(len(choice)+9))+"\033[A")
#print('hi')
import time
CURSOR_UP = "\033[1A"
hi = "\033[1A"
CLEAR = "\x1b[2K" + CURSOR_UP
print(CURSOR_UP)
print(CURSOR_UP + CLEAR, end="hi")   # clears ONE line
print("pineapple")