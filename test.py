# import os
# os.startfile("C:\\Users\\seany\\Downloads\Personal\\Choose_Your_Own_Adventure\\CYOA2.py")
# os.startfile("C:\\Users\\seany\\Downloads\Personal\\Choose_Your_Own_Adventure\\CYOA2.py")
# assign list
l = ['hello', 'geek', 'have', 'a', 'geeky', 'day']
 
# assign string
s = 'geek'
 
# check if string is present in list
if any(s == i for i in l):
    print(f'{s} is present in the list')
else:
    print(f'{s} is not present in the list')