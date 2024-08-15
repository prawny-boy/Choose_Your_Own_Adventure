from keyboard import is_pressed
from time import sleep
from termcolor import cprint
import sys
def slowprint(str:str, speed:float, attr:list, c='white', wait=3, skip=False) -> None:
    start = 0
    for char in str:
        cprint(char, end='', attrs=attr, color=c)
        sys.stdout.flush()
        sleep(speed)
        if is_pressed("enter") and start > wait and skip:
            print(str[start:-1])
            break
        start += 1
    sleep(speed)
    print()
slowprint("Fattydfghjhgfdsdfghjhgfdsdfgh", 0.01, ["bold"], skip=True)