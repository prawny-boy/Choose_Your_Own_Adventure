# import os
# os.startfile("C:\\Users\\seany\\Downloads\Personal\\Choose_Your_Own_Adventure\\CYOA2.py")
# os.startfile("C:\\Users\\seany\\Downloads\Personal\\Choose_Your_Own_Adventure\\CYOA2.py")
RESET = '\033[0m'
def get_color_escape(r, g, b, background=False):
    return '\033[{};2;{};{};{}m'.format(48 if background else 38, r, g, b)
print(get_color_escape(255, 128, 0)+'Fancy colors!' + RESET)