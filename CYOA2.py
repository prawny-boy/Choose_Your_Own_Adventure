from termcolor import cprint, colored
from sys import exit
from random import randint
from time import sleep
from achievements import achievements
from pygame import mixer
import sys
from keyboard import is_pressed
import os

# Inits
mixer.init()

# Program preset variables:
s = os.getcwd()+('\\Constants\\stats.txt' if "C:" in os.getcwd() else '/Constants/stats.txt')
e = 'Constants\\allendings.txt'
inventoryList = []
stories = {
    "tomb": 15,
    "amazon jungle": 20,
    "space story": 12,
    'time travel': 30,
    'school': 20,
    'mountain': 1,
} # name of story: amount of endings
storyList = ['quit'] + list(stories.keys())
for i in range(len(stories.keys())): storyList.append(str(i+1))
linesperuser = 4 # lines of stats per 1 user
initialstats = ['Endings: //', 'Achievements: //', 'Commands: //'] # preset of stats of a new user, / is normal int/str, while // is list
play = False
Reset = '\033[0m'
commandlist = ["help", "start", "stats", "save", "achievements", "credits", "updates", "inspiration"] # if add command also add in this unless it is an admin command, or quit, delete or reset
collections = {
    "sean": ["amazon jungle", "tomb", "time travel"],
    "oliver": ['school', "space story"],
    "levi": ['mountain'],
    "allplays": ["tomb", "amazon jungle", "space story", 'time travel', 'school', 'mountain']
}

# Stat Variables
user = ""
endings = []
userach = [] # user achievments
usercommands = [] # user commands
fails = 0
wins = 0

def slowprint(str:str, speed:float, attr:list, c='white', wait=3, skip=False) -> None:
    start = 0
    for char in str:
        cprint(char, end='', attrs=attr, color=c)
        sys.stdout.flush()
        sleep(speed)
        if is_pressed("shift") and start > wait and skip:
            cprint(str[start+1:], end="", color=c, attrs=attr)
            break
        start += 1
    sleep(speed)
    print()

def get_color_escape(r, g, b, background=False) -> str:
    return '\033[{};2;{};{};{}m'.format(48 if background else 38, r, g, b)

def user_system() -> str:
    done = False
    # where we ask for username and save, get stats etc.
    print("Enter your username (Not case sensitive), or enter 'new' to make a new account, empty to stay anonymous.")
    while True:
        username = input(" > ").lower()
        if username == "new":
            while True:
                print("Enter your new username, 'c' to cancel.")
                newuser = input(" > ")
                if newuser == "c":
                    print("Enter your username (Not case sensitive), or enter 'new' to make a new account, empty to stay anonymous.")
                    break
                elif newuser == "quit":
                    exit()
                invalid = False
                for char in newuser: # check if the username is valid
                    if char in ['!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '/', ':', ';', '<', '=', '>', '?', '[', '\\', '//', ']', '^', '`', '{', '|', '}', '~']:
                        invalid = True
                if len(newuser) < 3 or len(newuser) > 20 or newuser.lower() == "new":
                    invalid = True
                if not invalid:
                    done = checkusername(newuser)
                    if done:
                        username = newuser
                        break
                else:
                    print("Username must be 3 to 20 characters, with no special characters.\n")
                    if newuser.lower() == "new":
                        print("New is invalid because that is a function, but since you are smart...\nhttps://scratch.mit.edu/users/_ChoosUrAdventure_/\nFind the code for the special command...")
        elif username == "":
            print("Stayed anonymous.")
            break
        elif username == "quit":
            exit()
        else:
            with open(s, 'r') as file:
                content = file.readlines()
            if any(('User: /' + username.lower()) == i.strip("\n") for i in content):
                print(f"Successfully signed in as {username}.")
                break
            else:
                print("That username doesn't exist in our records. Please try again.")
        if done:
            break
    return username.lower()

def resetstats(user:str) -> None:
    # here we edit the stats file and reset everything
    with open(s, 'r') as file:
        lines = file.readlines()
    
    for i in range(len(lines)):
        lines[i] = lines[i].strip() # remove newline characters

    for i in range(len(lines)):
        if lines[i] == "User: /" + user:
            userline = i
            break

    for i in range(userline+1, userline+linesperuser):
        lines[i] = initialstats[i-(userline+1)]
    
    for i in range(len(lines)):
        lines[i] = lines[i] + "\n" # add newline characters

    with open(s, 'w') as file:
        file.writelines(lines)

def resetendingfile() -> None:
    resetlines = ""
    for story in stories.keys():
        resetlines += str(story) + ":" + (stories[story]-1) * "|" + "\n"
    with open(e, "w") as file:
        file.writelines(resetlines)

def deleteuser(user:str) -> None:
    # here we edit the stats file and reset everything
    with open(s, 'r') as file:
        lines = file.readlines()

    for i in range(len(lines)):
        if lines[i].strip() == "User: /" + user:
            userline = i
            break

    lines[userline:userline+linesperuser] = ""

    with open(s, 'w') as file:
        file.writelines(lines)
    
def addachievement(achname:str) -> None:
    done = False
    for achdict in achievements.keys():
        for ach in list(dict(achievements[achdict]).keys()):
            if str(ach).lower() == achname.lower():
                achname = ach
                achtype = achdict
                done = True
                break
        if done:
            break
    if not done:
        print("Error: Achievement not found. Key: " + achname)
    else:
        if not (achname + "/" + achtype) in userach:
            userach.append(achname + "/" + achtype)
            cprint(f"Completed {achtype.capitalize()} achievement: {achname}", "yellow")

def checkachievements() -> None:
    # here we check the check-nessessary achievements, such as the number of commands, times played, etc.
    for achdict in achievements.keys():
        for ach in achievements[achdict].keys():
            if len(achievements[achdict][ach]) == 2:
                done = False
                code = achievements[achdict][ach][1]
                atype = code.split(".")[0]
                key = code.split(".")[1].split("-")[0]
                if key == "allendings":
                    amount = stories[str(achdict).lower()]
                else:
                    amount = int(code.split(".")[1].split("-")[1])
                if atype in stories.keys():
                    endingscount = countendings(atype, key)
                    if endingscount >= amount:
                        done = True
                elif atype == "commands":
                    if key == "amount":
                        if len(usercommands) >= amount:
                            done = True
                    elif key == "allcommands":
                        alldone = True
                        for command in commandlist:
                            if any((str(command).lower()) == i for i in usercommands):
                                continue
                            else:
                                alldone = False
                                break
                        if alldone:
                            done = True
                elif atype == "stories":
                    if key == "totalplays":
                        playcount = countendings(None, key)
                        if playcount >= amount:
                            done = True
                    else:
                        if countendings(key, "collection") == 1:
                            done = True
                else:
                    print("Error. Type not valid:", atype)
                if done:
                    addachievement(ach)
            else:
                continue

def listachievements() -> None:
    # when the user wants to see other achievements
    cprint("\nACHIEVEMENTS", "yellow", attrs=["bold", "underline"])
    for achdict in achievements.keys():
        cprint(f"{achdict.capitalize()}:", attrs=["bold"])
        for ach in achievements[achdict].keys():
            cprint(f"    - {ach}: {achievements[achdict][ach][0]}", color=("white" if (ach+"/"+achdict in userach) else "dark_grey"))

def checkusername(user:str) -> bool:    
    x = ''
    file = open(s, 'r')
    content = file.readlines()
    if any(('User: /' + user.lower()) == i.strip("\n") for i in content):
        print('Username taken.')
        file.close()
    else:
        print('Username availible.')
        file.close()
        while x.lower() not in ['y', 'n']:
            x = input('Would you like this username? (y/n) ').lower()
            if x == "quit":
                exit()
        if x == 'y':
            file = open(s, 'a')
            file.write('User: /' + user.lower() + "\n")
            for i in range(linesperuser-1):
                file.write(initialstats[i]+"\n")
            print("Username registered. Don't forget this else you can't get your data!")
            return True
        elif x == 'n':
            return False

def grab_stats(user:str) -> tuple[list, list, list, int, int]:
    file = open(s, 'r')
    lines = file.readlines()

    for i in range(len(lines)):
        lines[i] = lines[i].strip() # remove newline characters

    for i in range(len(lines)):
        if lines[i] == "User: /" + user:
            userline = i
            break
    
    stats = []
    for i in range(userline + 1, userline + linesperuser):
        line = lines[i]
        n = 0
        while line[n] != "/":
            n += 1
        n += 1
        stats.append(line[n:len(line)].strip())
    
    for i in range(len(stats)): # This converts strings with more than one value to lists
        if stats[i][0] == "/":
            stats[i] = list(str(stats[i][1:]).split(","))

    # count endings for fails and wins
    stats.append(int(countendings(None, "fail", stats[0])))
    stats.append(int(countendings(None, "win", stats[0])))
    
    return tuple(stats)

def update_stats(user:str) -> None:
    global linesperuser, fails, wins
    # opens the file and saves the lines to a list
    with open(s, 'r') as file:
        lines = file.readlines()

    for i in range(len(lines)):
        lines[i] = lines[i].strip() # remove newlines
    
    # finds the user in the stats.txt file
    for i in range(len(lines)):
        if lines[i] == "User: /" + user:
            userline = i
            break

    # add stats, update
    for i in range(userline+1, linesperuser+userline):
        # variables reset each loop
        line = lines[i]
        statstart = None
        statislist = False
        statstring = ""
        stat = None

        # presets the stat to the current line's stat
        if "Endings" in line:
            stat = endings
        elif "Achievements" in line:
            stat = userach
        elif "Commands" in line:
            stat = usercommands

        # checks for / and // to see stats and if it is a string or a list - '//' is list, '/' is string
        for n in range(len(line)):
            if line[n] == "/":
                if line[n+1] == "/":
                    statstart = n+2
                    statislist = True
                    break
                else:
                    statstart = n+1
                    break
        
        # converts list to string that program can read later to change back to a list
        if statislist:
            if not stat == None:
                for item in stat:
                    if statstring == "":
                        statstring += str(item)
                    else:
                        statstring += ("," + str(item))
            else:
                statstring = ""
        else:
            statstring = stat
        
        # updates the line to new stats
        lines[i] = lines[i][:statstart] + str(statstring)
    
    for i in range(len(lines)):
        lines[i] = lines[i] + "\n" # add newline characters
                
    # writes the new list to the file
    with open(s, 'w') as file:
        file.writelines(lines)

def print_stats(user:str, endings:list, achievements:list, fails:int, wins:int) -> None:
    cprint(f"{str(user).capitalize()}'s Stats:", "green", attrs=["bold"])
    cprint("  Endings:", "red")
    # converts the list into a dictionary
    endingsdict = {}
    foundendings = []
    for item in endings:
        if not str(item).strip() == "":
            itemlist = str(item).split("/")
            itemlist[0] = getendingname(int(itemlist[0]), itemlist[1])
            if not itemlist[0] in foundendings:
                num = endings.count(item)
                endingsdict[itemlist[0]] = [itemlist[1], num]
                foundendings.append(itemlist[0])

    # prints the stats, sorted with how many times you have gotten it.
    # sorts stats
    endingsdict = dict(sorted(endingsdict.items(), key=lambda x:x[1]))

    # prints stats
    if endingsdict == {}:
        print("     No Endings for this User")
    else:
        initialstory = ""
        for item in endingsdict.keys():
            if initialstory == "" or initialstory != endingsdict[item][0]:
                print(f"    {str(endingsdict[item][0]).capitalize()}:")
                initialstory = endingsdict[item][0]
            print(f"      - '{str(item)}' {endingsdict[item][1]} times")

    # implement type and story sorting later
    cprint("  Achievements:", "yellow")
    # converts the list into a dictionary
    achdict = {}
    for item in achievements:
        if not str(item).strip() == "":
            itemlist = str(item).split("/")
            achdict[itemlist[0]] = itemlist[1]

    # prints the stats, sorted with how many times you have gotten it.
    # sorts stats
    achdict = dict(sorted(achdict.items(), key=lambda x:x[1]))

    # prints stats
    if achdict == {}:
        print("     No Achievements for this User")
    else:
        initialtype = ""
        for item in achdict.keys():
            if initialtype == "" or initialtype != achdict[item]:
                print(f"    {str(achdict[item]).capitalize()}:")
                initialtype = achdict[item]
            print(f"      - {str(item).capitalize()}")
    
    # print fails & wins
    cprint(f"  Fails: ", "red", end="")
    print(fails)
    cprint(f"  Wins: ", "green", end="")
    print(wins)

def choice(question:str, outcomes:list, options:list = ['y', 'n']) -> int:
    cprint('-----------------------------', attrs=['bold'])
    choice = ''
    numoptions = []
    numtype = False
    for i in range(1, len(options)+1):
        numoptions.append(str(i))
    print(question)
    option = str(options)
    option = option.replace('[', '')
    option = option.replace(']', '')
    option = option.replace("'", '')
    for a in range(0,len(options)):
        options[a] = str(options[a]).lower()
    print('Options: ' + option)
    while True:
        choice = str(input('Choice: ').lower()) 
        if choice == "quit":
            exit()
        elif choice in options:
            break
        elif choice in numoptions:
            numtype = True
            break
        else:
            print("\033[A"+(" "*(len(choice)+9))+"\033[A")
    if numtype:
        x = int(choice)-1
    else:
        for num in range(0,len(options)):
            if choice == str(options[num]):
                x = num
                break
    print("\n" + outcomes[x])
    return x

def inventory(addItem, amount=1, type="add", toggle:bool = True) -> None:
    stop = False
    if type == "add":
        startamount = amount
        while amount != 0:
            inventoryList.append(addItem)
            amount -= 1
        cprint("You recieved " + str(startamount) + " " + str(addItem) +"(s)", "green")
    else:
        startamount = amount
        while amount != 0:
            try:
                inventoryList.remove(addItem)
            except:
                stop = True
                break
            amount -= 1
        if not stop:
            cprint("You lost " + str(startamount) + " " + str(addItem) +"(s)", "red")

    if toggle:
        if not inventoryList == []:
            cprint("\nINVENTORY:", attrs=["bold"])
            found = []
            for item in inventoryList:
                if item in found:
                    pass
                else:
                    print(f"{inventoryList.count(item)} {item}")
                    found.append(item)
        else:
            cprint("\nYour inventory is empty.", attrs=["bold"])
        print()

def ending(name:str, number:int, story:str, type:str = "fail", alt:bool=False, altname:str="") -> None:
    global fails, wins
    # end and add it to the endings list
    colour = ""
    if type.lower().strip() == "win":
        colour = "green"
        wins += 1
    elif type.lower().strip() == "fail":
        colour = "red"
        fails += 1
    if not alt:
        cprint(f"(Ending {str(number)}/{str(stories[story.lower()])} '{str(name)}')", colour)
        endings.append(str(number)+"/"+story+"/"+type)
        addnewending(number, name, story.lower())
    else:
        cprint(f"(Ending {str(number)}/{str(stories[story.lower()])} Alternative '{str(name)}')", colour)
        cprint("This is an alternative ending. It will save as the normal ending.\n", "dark_grey")
        endings.append(str(number)+"/"+story+"/"+type)
        addnewending(number, altname, story.lower())

def addnewending(ending_num:int, ending_name:str, story:str) -> None:
    # if the name doesnt exist yet, add it.
    with open(e, 'r') as file:
        lines = file.readlines()

    i = 0
    for line in lines:
        if story in line:
            line = line.strip("\n").split(":")
            linelist = line[1].split("|")
            if linelist[ending_num-1] == ending_name:
                pass
            else:
                # add ending to file
                linelist[ending_num-1] = ending_name
                line = str(line[0]) + ":" + "|".join(linelist)
                lines[i] = line + "\n"
        i += 1
    
    with open(e, 'w') as file:
        file.writelines(lines)

def getendingname(ending_num:int, story:str) -> str:
    with open(e, "r") as file:
        lines = file.readlines()
    for line in lines:
        if story.lower() in line:
            line = line.strip()
            storyendings = line.split(":")[1].split("|")
            return storyendings[ending_num-1]
    return "Error, story invalid."

def countendings(story:str, mode:str, endinglist:list = None) -> int:
    # 6 modes, plays, all endings, fails, wins, totalplays, collection
    count = 0
    if mode == "play":
        for ending in endings:
            try:
                if str(ending).split("/")[1].lower() == story.lower():
                    count += 1
            except IndexError:
                continue
    elif mode == "allendings":
        foundendings = []
        for ending in endings:
            try:
                if str(ending).split("/")[1].lower() == story.lower():
                    if str(ending).split("/")[0] not in foundendings:
                        foundendings.append(str(ending).split("/")[0])
            except IndexError:
                continue
        count = len(foundendings)
    elif mode == "fail" or mode == "win":
        try:
            for ending in endinglist:
                if str(ending).split("/")[2] == mode:
                    count += 1
        except TypeError:
            print("Error. Needs endinglist input.")
        except IndexError:
            pass
    elif mode == "totalplays":
        for ending in endings:
            if ending != "":
                count += 1
    elif mode == "collection":
        rmlist = collections[story]
        for ending in endings:
            try:
                if str(ending).split("/")[1].lower() in rmlist:
                    rmlist.remove(str(ending).split("/")[1].lower())
            except IndexError:
                continue
        if len(rmlist) == 0:
            count += 1
    else:
        print("Error. Mode not valid:", mode)
    return count

def checkcommand(command:str) -> None:
    global user, running_commands, fails, wins, endings, userach, usercommands, inventoryList
    command = command.lower()
    real = True
    story = ''
    danger = colored('(Dangerous)', 'red')
    if command == "help":
        print(f"""List of commands:
  Help - brings up this list
  Start - starts the story selection
  Stats - prints the current user's stats
  Save - saves the user's current stats
  Reset - resets the current user's stats {danger}
  Delete - Deletes the current account, after goes back to sign in {danger}
  Achievements - Shows a list of all the achievements
  Switch - Signs out of the current account
  Inspiration - Shows our insipration story with music
  Quit - quits the story when in the story, if out of story quits program
  Credits - shows the credits & project info""")
    elif command == "start":
        print("""STORIES:
  1. Amazon Jungle
  2. Space Story
  3. Time Travel
  4. School
  5. Tomb Story
  6. Mountain""")
        while True:
            story = input('Please select a story: ')
            if story == 'quit':
                exit()
            elif story in storyList:
                break
            else:
                print("That is invalid, enter a story name or the corresponding number to a story.\n")
        inventoryList = []
        if story == "amazon jungle" or story == '1':
            cprint("\nAMAZON JUNGLE", "green", attrs=["bold"])
            story_amazon_adventure()
        elif story == "space story" or story == '2':
            cprint("\nSPACE STORY", "blue", attrs=["bold"])
            story_space()
        elif story == "time travel" or story == "3":
            cprint("\nTIME TRAVEL", "red", attrs=["bold"])
            story_timetravel()
        elif story == "school" or story == "4":
            cprint("\nSCHOOL - Made By Jayden Li", "yellow", attrs=["bold"])
            story_school(user)
        elif story == "tomb story" or story == "5":
            cprint(get_color_escape(255, 128, 0) + '\nTutankhamun\'s Tomb - Made By Ethan Wei' + Reset, attrs=["bold"])
            story_tomb()
        elif story == "mountain" or story == "6":
            cprint("\nMOUNT EVEREST", "light_grey", attrs=["bold"])
            story_mountain()
    elif command in ["save", "reset", "delete", "stats"]:
        if not user == "":
            if command == "save":
                print("Saving...")
                update_stats(user)
                print("Saved stats successfully.")
                addachievement("Saved")
            elif command == "reset":
                while True:
                    confirm = input(colored("Are you sure you want to continue? This will reset ALL of your stats. (y/n) ", "red")).upper()
                    if confirm == "Y":
                        resetstats(user)
                        endings, userach, usercommands, fails, wins = grab_stats(user)
                        print("Reset stats successfully.")
                        break
                    elif confirm == "quit":
                        exit()
                    elif confirm == "N":
                        print("Cancelled.")
                        break
                    else:
                        print("Invalid. Enter 'y' or 'n'")
            elif command == "delete":
                while True:
                    confirm = input(colored("Are you sure you want to continue? This will delete your account. (y/n) ", "red")).upper()
                    if confirm == "Y":
                        deleteuser(user)
                        user = ""
                        running_commands = False
                        print("Successfully deleted account. Please Sign In.")
                        break
                    elif confirm == "quit":
                        exit()
                    elif confirm == "N":
                        print("Cancelled.")
                        break
                    else:
                        print("Invalid. Enter 'y' or 'n'")
            elif command == "stats":
                print_stats(user, endings, userach, fails, wins)
        else:
            print("You need to be signed in into a account to use this function.")
    elif command == "achievements":
        listachievements()
    elif command == "switch":
        print(f"You are signed in as {user}")
        while True:
            confirm = input("Do you want to sign out? (y/n) ").upper()
            if confirm == "Y":
                update_stats(user)
                user = ""
                print("Signed out. Please Sign In.")
                running_commands = False
                break
            elif confirm == "quit":
                exit()
            elif confirm == "N":
                print("Cancelled.")
                break
            else:
                print("Invalid. Enter 'y' or 'n'")
    elif command == "inspiration":
        cprint("Inpirational Story", "yellow", attrs=["bold", "underline"])
        with open("Constants\\inspirational.txt", "r") as file:
            paralist = file.read().split("|")
        print("(shift to skip)")
        songlist = ["Songs\\Hope.mp3", "Songs\\Happy.mp3", "Songs\\Mystery.mp3"]
        for i in range(len(paralist)):
            mixer.music.load(songlist[i])
            mixer.music.play()
            slowprint(paralist[i], 0.05, ["bold"], skip=True)
        addachievement("Inspired")
        mixer.music.fadeout(1000)
    elif command == "quit":
        exit()
    elif command == 'updates':
        with open("Constants\\updates.txt", "r") as file:
            print(file.read())
        addachievement("Technician")
    elif command == 'credits':
        print("""
███████╗ ██████╗
██╔════╝██╔═══██╗
███████╗██║   ██║     \033[1mSean & Oliver Corporation Inc\033[0m
╚════██║██║   ██║
███████║╚██████╔╝
╚══════╝ ╚═════╝ 

------------------------------------------------
Version: 2.2 ("Updates" for latest changes)
Coded in VS Code, by Oliver Liu and Sean Chan
Logo: Aaron Zhang
Testers: Use 'testers' command
Story Writers: 
    Amazon Adventure - Sean Chan
    Space Story - Oliver Liu
    Time Travel - Sean Chan
    School - Jaden Li, imported by Oliver Liu
    Tutankhamun's Tomb - Ethan Wei, imported by Sean Chan
    Mountain - Levi Laij
    Underwater - Oliver Liu
------------------------------------------------""")
        addachievement("Supporter")
    elif command == "testers":
        cprint("TESTERS:", attrs=["bold", "underline"], color="blue")
        with open("Constants\\testers.txt", "r") as file:
            for line in file.readlines():
                print(line.strip("\n"))
    elif command == "198234":
        win = False
        answer = input("Question 1/5: How many times did you have to click in the second game to win? ").strip()
        if answer == "100":
            answer = input("Question 2/5: How many boats were in the minecraft course? ").strip()
            if answer == "5":
                answer = input("Question 3/5: What was the Youtube channel name you were directed to? ").lower().strip()
                if answer == "souloftheassassin":
                    answer = input("Question 4/5: Are you subscribed to said Youtube channel? ").lower().strip()
                    if answer == "yes":
                        answer = input("Question 5/5: What was the third scratch game titled? ").lower().strip()
                        if answer == 'special':
                            win = True
        if win:
            print("Success!")
            addachievement("The Long Egg")
        else:
            print("Wrong. Answer all questions correctly.")
    else:
        print("That is an invalid command. Try Again.")
        real = False
    if real == True and running_commands:
        usercommands.append(command)

# OLIVER - SPACE STORY
def story_space():
    print('\nYou are an astronaut stranded in space. Your fellow adventurers have all ran out of oxygen, but you still have 3 minutes of oxygen left.')
    inventory('Oxygen', 3)#3 oxygen
    c = choice("Your ship's wreckage is nearby. Would you like to explore it?", ["""You begin slowly drifting towards the hull.
    While drifting, you notice an oxygen tank.""", "You slowly spin around, and notice one of your friend's life support is still on."])
    
    if c == 0:
        inventory('Oxygen', 1, "lose")#2 oxygen
        c = choice("Will you take the tank, or continue exploring the ship?", ["You take the tank, but the ships slowly drifts away.", "You continue moving towards the ship, and see that there are three sections."], ['Tank', 'Ship'])
        
        if c == 0:
            inventory('Oxygen', 3, "add")#5 oxygen
            c = choice('Everything is out of reach.', ['A piece of space debris hurtles towards you, breaking your visor. Your suit begins to leak oxygen at a rapid pace. You die due to lack of oxygen.'], ['...'])
            
            if c == 0:
                inventory('Oxygen', 5, "lose")#0 oxygen
                ending("Bye Bye, Spacesuit", 1, "space story")
                
        elif c == 1:
            inventory('Oxygen', 1, "lose")#1 oxygen
            c = choice("Which part of the ship will you explore?", ["You explore the hull, which contains 5 tanks of oxygen.", "You explore the bridge, which has instructions on how to operate the ship.", "You explore the cargo bay, which contains a manual on how to fix the ship."], ["Hull", 'Bridge', 'Storage Bay'])
            
            if c == 0:
                inventory('Oxygen', 5, "add", False) # 5 oxygen
                c = choice('''You notice a few boxes, and a lever that may open the door. 
Will you go to the boxes, or open the door?''', ['You go towards the boxes, and find nothing.', 'You go towards the door, and pull the lever. The door creaks open slightly, but you force it open.'], ['Boxes', 'Door'])
                
                if c == 0:
                    inventory('Oxygen', 1, 'lose')
                    c = choice('What will you do now?', ['You slowly float towards the door, but something above sees and launches itself at you.', 'You slowly float towards the hatch, but something above sees and launches itself at you.'], ['Door', 'Hatch'])
                    print('You fiercely grapple with it, but to no avail. You die to [Bob the Alien]')
                    ending('Bob the Alien, It Can Kill You!', 4, "space story")
                    addachievement("Bob the Alien")
                    
                elif c == 1:
                    inventory('Oxygen', 1, 'lose')
                    c = choice('The door opens and you find a box of tools. What will you take from it?', ['You take the wrench, which you use to fix the wall panels. The chamber is now sealed.', 'You take the blowtorch, which sets your suit on fire, burning you alive.', 'You take the screwdriver, which allows you to fix the thrusters.'], ['Wrench', 'Blowtorch', 'Screwdriver'])
                    
                    if c == 0:
                        c == choice('Will you take off your helmet?', ['You take it off, but there is not air in the chamber, causing you to suffocate.', "You don't take it off, but now that you are in a sealed chamber the oxygen begins diffusing into the chamber, killing you."])
                        if c == 0:
                            print('You died due to lack of oxygen.')
                            ending("Oopsies", 6, "space story")
                        elif c == 1:
                            print('You died due to lack of oxygen.')
                            ending("Unlucky :(", 7, "space story")
                    elif c == 1:
                        print('You died due to fire.')
                        ending("Overheating", 5, "space story")
                        addachievement('Flamed')
                    elif c == 2:
                        print("""After fixing the thrusters, you jumpstart them using luck.
They roar to life, throwing you back and bringing you back to earth.
""")
                        ending("Back to Earth", 11, "space story", "win")
                        addachievement("How did we get back?")
            elif c == 1:
                inventory('Oxygen', 1, "lose", False)
                inventory('Operation Manual', 1, "add")
                print("You died due to lack of oxygen.")
                ending("Operation Ded", 2, "space story")
                
            elif c == 2: 
                print('You got lucky, and found a spare oxygen tank!')
                inventory('Repair Manual', 1, "add", False) # 1 oxygen
                c = choice('Will you fix the ship, or find more oxygen?', ['You try to fix the ship,', 'You go searching, and find 4 tanks inside on the wall.'], ['Fix', 'Search'])

                if c == 0:
                    print('But you die due to a lack of oxygen.')
                    ending("Dead Fix", 3, "space story")

                elif c == 1:
                    inventory('Oxygen', 3)#4 oxygen
                    c = choice('You see another ship in the distance. Will you go towards it?', ['You go to it, but the Hubble Space Telescope slams into you, killing both of you,', "You don't do anything, which wastes oxygen."])
                    if c == 0: 
                        print("You died to [Hubble Space Telescope].")
                        ending("Hubble Space Skill Issue", 9, "space story")
                    elif c == 1:
                        inventory('Oxygen', 2, 'lose')
                        c = choice('Because you wasted time, there is nothing you can do.', [''], ['...'])
                        if c == 0:
                            print('You died due to loss of oxygen.')
                            ending("Timewaster...", 10, "space story")
                
    elif c == 1:
        inventory('Oxygen', 1, "lose")#2 oxygen
        c = choice("Will you wake him up, or steal his oxygen?", ['He wakes up, startled. After you explain what is happening, he agrees to help you.', 'You take his oxygen, leaving him to die.'], ['Wake', 'Steal'])
        
        if c == 0:
            inventory('Oxygen', 1, "lose")#1 oxygen
            print('Your suit started malfunctioning! You now lose double oxygen.')
            c = choice('Will you explore the ship?', ['Sadly, while travelling to the ship, you run out of oxygen.'], ['Yes'])
            inventory("Oxygen", 2, 'lose')
            print('You died due to loss of oxygen.')
            ending("We're halfway there...", 12, "space story")
            
            
        elif c == 1:
            inventory('Oxygen', 2, "add")#4 oxygen
            c = choice('What to do...', ['You get hit by a meteorite, killing you.'], ['Nothing'])
            print('You died to [Meteorite].')
            ending("KARMA", 8, "space story")
            
    slowprint('THE END', 0.05, ["bold"])

# SEAN - AMAZON ADVENTURE

def story_amazon_adventure_pilot():
    x = choice("Do you want to go find a village, continue searching in the plane, or stay and build a shelter next to the plane crash?", ["You and John both leave the crashed plane and after hours of searching you find a village. As you approach the alarm sounds, and you are both captured by the native tribe. You are going to be hanged in 2 hours, unless you have something to give.", "'Do you know about anything else in the plane?' You ask John. 'Yes there is a wrench and a instruction manual in the glove box' John replies, taking the things out. He gives them to you. These could be helpful for fixing the plane...", "You stay at the plane crash site, making a shelter for you and John for the next month. After you run out of food, you face the option of adventuring into the dangerous forest for food, or staying at the shelter to starve."], ['village', 'search', 'stay'])
    if x == 0:
        if "Gem" in inventoryList:
            print("Luckily, you have that gem that you found in the river, so you offer them it. The tribe accepts you and the pilot as a member, letting you live with them forever.")
            inventory("Gem", 1, "lose")
            ending("Accepted into Tribe", 1, "amazon jungle")
        else:
            print("Well obviously you didn't have anything because you just crashed in a plane. After 2 hours of dread, you and John are hanged.")
            ending("Hanged", 2, "amazon jungle")
    elif x == 2:
        x = choice("Which do you choose?", ["You go into the forest and venture for food. You find mushrooms, but you don't know if they are poisonous. After bringing them back to the crash site, you face the decision: eating the mushroom, or not eating the mushroom and to continue looking for food.", "You stay at the plane crash without food, but don't last long."], ['forest', 'stay'])
        ending("Starved To Death", 3, "amazon jungle")
        if x == 0:
            x = choice("Which will you choose?", ["You decide to eat the mushroom but it ends up being poisonous. Oops!""", "You continue looking but it soon turns night. A flash of bright red fur and a scream from John. Before you can react, you fall victim to the night creature."""], ['eat', 'continue'])
            if x == 0:
                ending("Poisoned", 4, "amazon jungle")
            else:
                ending("The Creature of The Night", 5, "amazon jungle")
    else:
        story_amazon_adventure_search()

def story_amazon_adventure_search():
    global foundpilot
    if foundpilot:
        inventory("Toolbox", 1, "add", False)
        inventory("Instruction Manual")
        x = choice("Do you want to try fix the plane?", ["Luckily you have a toolbox, which helps you quickly fix the plane.", "You decide against trying to fix the plane. It would be too difficult anyway."])
    else:
        print("""You continue searching the plane and find a toolbox and a instruction manual for the plane in the glovebox. This may be helpful for fixing the plane...""")
        inventory("Toolbox", 1, "add", False)
        inventory("Instruction Manual")
        x = choice("Do you want to try fix the plane?", ["Luckily you have a toolbox, which helps you quickly fix the plane.", "You decide against trying to fix the plane. It would be too difficult anyway."])
    
    if x == 0:
        story_amazon_adventure_fix()
    else:
        if foundpilot:
            print("After awhile, You and John get hungry, and have run out of food, so decide to go out to look for some. You both stumble in the forest and fall down a cliff. Maybe look where you step?")
            ending("Clumsy Buddies", 17, "amazon jungle", alt=True, altname="Clumsy")
        else:
            print("After awhile, You get hungry, and have run out of food, so decide to go out to look for some. You stumble in the forest and fall down a cliff. Maybe look where you step?")
            ending("Clumsy", 17, "amazon jungle")

def story_amazon_adventure_fix():
    global end, foundpilot
    if "Toolbox" in inventoryList:
        if not foundpilot:
            print("""When you are finished, you jump into the pilot seat, getting ready to escape the forest. Looking at the forest gives you nightmares, so you hurridly start the engine. But right before you can go a dark animal jumps onto the front window, smashing the glass.""")
            x = choice("Do you want to defend yourself or go and hide?", ["You collect a pole standing not far off and hit the monster with it. 3 whacks and the monster is gone. Finally, you start the engine and go off in the plane, using the instruction manual as a guide.""", "You go and run to the back of the plane, but the creature follows you, breaking down the door and destroying all your hard work in fixing the plane. Before you can blink, you are devoured."""], ["defend", "hide"])
            if x == 0:
                ending("Defeated a Monster", 14, "amazon jungle", "win")
                addachievement("Escape of the Jungle")
            else:
                ending("So Close, But so Devoured", 15, "amazon jungle")
            end = True
        else:
            input("""Halfway through your engineering process, a high-pitched scream pierces the air. You run out to see that John has his instruction manual in his hands, but a feral animal is trying to grab it away. (Enter to continue)""")
            if (not "Gem" in inventoryList):
                print("""He stumbles and falls onto the ground, and the animal now procceds to jump on John and tear his flesh. He is long gone. You go and hide in the plane for several hours, but the dog doesn't do away. You are out of food supplies so you face an option.""")
                inventory("Instruction Manual", 1, "lose")
                foundpilot = False
                x = choice("Would you go and face the monster or stay and starve?", ["You go out to face the monster. You would die anyway, so beter die gloriously. Before you can even glimpse the monster, you are devoured. I don't think that was so glorious...", ""], ['face', 'stay'])
                if x == 0:
                    ending("Not A Glorious Death", 10, "amazon jungle")
                elif randint(1, 2) == 1:
                    print("You decide against fighting the monster, which stays there for a very long time, leading you into a slow and painful death. Starvation.")
                    ending("Starvation", 9, "amazon jungle")
                else:
                    print("You decide to not fight the monster, and after awhile it wonders away. You sit in the pilot's seat and admire your hard work in fixing the plane. You start the engine and take off successfully. But suddenly, your plane dips and when you realise you never knew how to drive a plane, you crash.")
                    ending("Crashed Again", 13, "amazon jungle")
                    addachievement("Again?!")
                end = True
            else:
                print("""You think fast. Getting the Gem that you found earlier, you wave it in the air, distracing the animal. This successfully distracts the animal,
making it run away, pulling the book away from John's hands and stealing it. At least you saved John...""")
                inventory("Instruction Manual", 1, "lose")
        if not end:
            print("""You sit in the passengers seat and admire your hard work in fixing the plane. John drives the plane away from the forest, flying back home.""")
            ending("Passenger Escape", 11, "amazon jungle", "win")
            addachievement("Pilot Buddy")
            addachievement("Escape of the Jungle")
    
def story_amazon_adventure():
    global foundpilot, end
    foundpilot = False
    end = False
    print("""\nYou are a passenger heading to Africa on a plane. You remember that you went bankrupt after losing while gambling. 
Your life is falling around you, so you decide to move to Africa to start a new life. While you are thinking about the latest happenings,
the plane suddenly dips and crashes into the trees. You go unconcious. 

When you wake up, you remember what happened and wish that you never went to Africa.""")
    x = choice("Do you want to walk to find the nearest village?", ["You go searching for a village, but instead find a very developed town. A nice citizen invites you to stay with him, and you accept. The citizen hands you a glass of green liquid.", "You stand there, aimlessly looking around for something to do. You see your plane a few feet away."])
    if x == 0:
        x = choice("Do you want to drink it?", ["When you drink the liquid, you pass out and wake up in a jail like cell. You are told that you will be used in an great experiment, if that is great or not.", "You put down the drink and hurridly leave the hut. There's something suspicious about the drink. You decide to start a new life, by yourself. The town leader sees your intelligence and offers you a job: a town advisor. On the other hand, a independent company offers you another path: a secret spy."])
        if x == 0:
            ending("Great Experiements", 6, "amazon jungle")
        elif x == 1:
            x = choice("Which will you take?", ["You become an advisor for the town, and earn a lot of money, soon becoming rich. You live a happy life in the town.", "You become a spy against the town, but you are not too good at it. After a week, you are caught and sent to jail."], ["advisor", "spy"])
            if x == 0:
                ending("Rich Boi", 7, "amazon jungle")
            else:
                ending("Jail Time", 8, "amazon jungle")
    else:
        x = choice("Do you want to see what is inside?", ["You walk towards the plane, opening the door to see the body of your pilot on the seats.", "I don't know why you would not want to see what has inside a plane, but ok. You can't survive with nothing so you died."""])
        if x == 0:
            x = choice("Do you want to check out his body or search the plane further?", ["You climb up to the pilot, over the rubble. You hear hoarse, shallow breaths! He is still alive! He opens his eyes and struggles up. 'Wat...er..' he mumbles.", "You keep searching, ignoring the pilots body. He's probably dead anyways. You find a locked storing shelf, but you don't have the key."], ["check", "search"])
            if x == 0:
                x = choice("Do you want to get him water?", ["You quickly dash out of the plane, looking for any water source. You see a water spring under a rock, and a fast flowing river in the distance.", "You decide that you can't be bothered to get water for him. It is his fault that you are in this place anyways. 'Please...' the pilot says before coughing harshly then going silent. Now you are alone."])
                if x == 0:
                    x = choice("Which one do you want to get water from?", ["You get water from the spring, rushing back to give it to your pilot. He drinks it and stands up. 'Thanks. By the way my name is John. Where are we?' he questions. 'We are in the amazons', you reply. John then goes into the plane's stores, unlocking them to get food. 'There is enough to last for about a month. We can stay here or go to find a village of some sort.' John tells you.", "You get water from the river, but right as you are about to go you find a cool looking gem in the water. You pick it up, before rushing back to give it to your pilot. He drinks it and stands up. 'Thanks. By the way my name is John. Where are we?' he questions. 'We are in the amazons', you reply. John then goes into the plane's stores, unlocking them to get food. 'There is enough to last for about a month. We can stay here or go to find a village of some sort.' John tells you."], ["spring", "river"])
                    if x == 0:
                        foundpilot = True
                        story_amazon_adventure_pilot()
                    else:
                        foundpilot = True
                        inventory("Gem")
                        story_amazon_adventure_pilot()
                else:
                    x = choice("Do you want to continue searching the plane, or try to find a village?", ["", "You go to a village, a big village with... FLOATING ISLANDS? What?! Apparantly this village is very technologically advanced, so you enter happily. At the gates, a laser (Non-fatal) scans your face and suddenly raises an alarm. The people shout angrily at you, but you don't know what they are saying. It's only when you are about to be killed by lasers (fatal) that they scold you for not saving an innocent life, the pilot's. You wish you had saved the pilot and wonder how the people knew as you are burned by the light, over and over again."], ["search", "village"])
                    if x == 0:
                        print("You search the plane and find a toolbox and instruction manual. This may be helpful in fixing the plane...")
                        story_amazon_adventure_search()
                    else:
                        ending("Sins Discovered", 18, "amazon jungle")
            else:
                x = choice("Do you want to search for the key?", ["You go and check in the pilot's pockets and find the key, unlocking the storage. Inside the storage is enough food for 2 months. You know that it won't last forever, but finding more food might be very good.", ""])
                if x == 0:
                    x = choice("What do you want to do?", ["You start looking for food but stumble upon a hidden mole-made hole. For some odd reason, you can't get out, so you starve to death.", "You stay at the plane crash site for a month, and start getting bored. Looking at the remains of the plane, you realise that it is easy to fix, by fitting the plane wing on."], ['food', 'stay'])
                    if x == 0:
                        ending("A Hole By A Mole", 12, "amazon jungle")
                    elif x == 1:
                        x = choice("Do you want to fix it?", ["You start to try to fix it but you need tools to do it. That's quite sad. I've never heard of someone who has died of boredom, so I think your're the first one. Good Night.", "You start getting hungry once your food supply is used up so go searching for food. While wondering you find some conveniently placed food. 'Someone must have left their lunch behind!' you think. Taking the food, you turn back and... SNAP!!! A bear trap catches you. You scream for help, But after awhile your shouts die down as you lose too much blood."])
                        if x == 0:
                            ending("Died of Boredom", 16, "amazon jungle")
                            addachievement("Die of Boredom")
                        else:
                            ending("Tomato Sauce Everywhere", 19, "amazon jungle")
                else:
                    print("You decide that it will be impossible to find the key. It probably fell off when the plane crashed.")
                    story_amazon_adventure_search()
        else:
            ending("Bad Choices", 20, "amazon jungle")
            addachievement("Bad Choices")

    if "Gem" in inventoryList:
        addachievement("Keep The Gem")
    slowprint("\nTHE END", 0.05, ["bold"])

# SEAN - TIME TRAVEL
def story_timetravel():
    print("""You have lived an ordinary life, so ordinary that nothing has happened to you that has been particularily interesting. At least not until this night. It is very dark, and the rain pours down, battering the windows hard.

You can't sleep. Waking up, you decide to walk up into the attic and see what is up there. It is cramped and dusty, but looking around you see a lone box, that reads 'enihcam emit'. You causiously walk towards the box. Suddenly, a blue glow flashes from the box, and before you can go, you are sucked in.

You pass out. After waking up you look around to meet an unfamiliar place. Instead of saying 'enihcam emit', the box now says '100 million years ago'. You wonder what it means and start walking. Around you is a leafy green jungle, and wierd noises see, to come from the trees. You find a clearing and a natural path.""")
    x = choice("Which will you explore?", ["You walk out to a clearing and in front of you lies a great t-rex, sleeping. You realise you have traveled to the time of the dinosaurs! Lucky that t-rex is sleeping. It seems that the t-rex is guarding something.", "You trudge down the path, but it seems like it has been made by a great big animal. After walking for awhile, you spot some red berries on a bush. You are extremly hungry."], ["Clearing", "Path"])
    if x == 0:
        x = choice("Do you want to see what it is guarding?", ["You slowly creep up and take a look at what the t-rex is protecting. Looking up to you, is a baby t-rex! It jumps out from under the great t-rex! (its mother) Baring its teeth at you, it stares at you with its green eyes.", "You run away, wanting to not go and disturb the dangerous t-rex. In the distance, you see your time machine box thing."])
        if x == 0:
            x = choice("Do you want to slowly back away, run and hide, or try to calm the small t-rex down?", ["You slowly back away, but eyeing you, the baby t-rex jumps on you and tears your flesh.", "You run, and hide behind a ditch. The baby t-rex cries out, and the big t-rex comes to hunt for you. Before you can go anywhere, the big t-rex accidentally squishes you. Oof.", 
                "You calm the baby down, and it starts to make cooing noises. Somehow you tamed a t-rex! Seeing your box time machine thing, you run with the t-rex and hop in. But the t-rex eats your box up in one bite. Oops. Now you are stuck in the time of the dinosaurs."], ["back away", "run", "calm"])
            if x == 0:
                ending("Destroyed by a Baby", 1, "time travel")
            elif x == 1:
                ending("Squished", 2, "time travel")
            elif x == 2:
                ending("Stuck with the dinosaurs", 3, "time travel")
        else:
            x = choice("Do you want to go to it?", ["You hop into your time machine box thing, looking at the last time you will see the dinosaurs.", "The machine get fried as a fire-breathing dinosaur blows on it. I guess you are stuck in the past..."])
            if x == 0:
                story_timetravel_2()
            else:
                ending("Burnt with the dinosaurs", 3, "time travel", alt=True, altname="Stuck with the dinosaurs")
    else:
        x = choice("Do you want to pick the berries then eat it, just pick the berries for later, or no berries?", ["You eat the berries and suddenly feel like you have great power. You start running to the box time travel thing and find that you are faster! You hop into the box and close the lid.", "You pick the berry to be eaten later. You run to the box and hop in, closing the lid.", "A dinosaur sees you from a distance and lumbers towards you. You run for ages, and the dinosaur leaves you. But you are lost."], ["eat", "pick", "no"])
        if x == 0:
            inventory("Power", 1)
            story_timetravel_2()
        elif x == 1:
            inventory("Berry", 1)
            story_timetravel_2()
        else:
            ending("Lost", 4, "time travel")
    
    slowprint("THE END", 0.05, ["bold"])

def story_timetravel_2():
    print("The box shakes and rattles loudly as it heads to who knows where. After awhile, you feel a jolt and look out of the box. Around you are small heaps of hay, and by judging the area, you seem to have come to a barn-like building.")
    print("You hop out of the box, and slowly creep to a small hay door. Peeking out, you see farmers working on the fields that seem to stretch on forever. Looking back, your box seems to have dissapeared.")
    x = choice("Do you want to go out to adventure?", ["You leave the barn quietly, and manage to sneak out without getting seen. Hiding behind a stack of hay, you peer at the farmers working in the distance. One of them is spying your haybale, but seems to not really care.", "You stay inside the barn, but hear footsteps approaching towards you form the outside."])
    if x == 0:
        x = choice("Do you want to show yourself to the farmers?", ["You quietly step out of your hiding place, and at once the farmer watching you gives a startled cry. You say you come it peace, but the farmers don't understand what you are saying.", "You keep hiding in your hiding spot, and spy a large farmhouse in the distance. Looking back, you realise that all the farmers seem to be working and not looking around."])
        if x == 0:
            if "Power" in inventoryList:
                print("\nThe farmers rush towards you, holding their tools to attack you. They are fast, but you are faster as you dash away from them, hiding in a clump of trees until they give up the chase. In running away, you lost your power, but at least you got away safely. You look around and see a dark forest looming ahead of you.")
                inventory("Power", 1, "lose")
                x = choice("Do you want to enter the forest?", ["You enter the forest hastily, to make sure that the farmers don't spot you again, as you know that you won't be sble to escape another time. As you wander amongst the trees, you hear a consistant thudding in the distance. You have a few options to decide from: Do you want to investegate the sound, continue walking in the forest, or try to head back just in case there are dangers lurking around?", "You don't want to risk getting attacked by a feral animal in the forest, so you stay at you hiding place for now. After waiting awhile, you get hungry, and wonder where you can get food from. In the distance, there is a farmhouse that might have some food!"])
                if x == 0:
                    x = choice("What do you choose?", ["You creep towards the sound of thudding and see a clearing up ahead. As you peek, you see that an lumberjack is cutting trees with wood. Before you can react, the lumberjack spots you and races towards you, misthinking that you are an enemy. He swings his axe and everything goes black.", "You continue walking and find a small campfire area in the forest. Your box thing sits in the middle.", "You start heading back but walk into a simple but smart trap: A extremly well hidden hole. Falling down, you land hard, and break your legs. You sit there for the whole day, getting hungrier and hungrier until you can't take it anymore, with the pain from your leg throbbing and giving you an headache."], ["Investagate", "Continue", "Go Back"])
                    if x == 0:
                        ending("Lumberjacked", 5, "time travel")
                        addachievement("Lumberjacked")
                    elif x == 1:
                        x = choice("Do you want to get into the box?", ["You get into the box, and close the lid.", "You decide against getting into the box, and before you can do anything, a feral animal comes and attacks you. A moment later, all that is left of you is... nothing."])
                        if x == 0:
                            story_timetravel_3()
                        else:
                            ending("Devoured", 7, "time travel")
                    else:
                        ending("That One Hole", 6, "time travel")
                else:
                    x = choice("Do you want to go to the farmhouse?", ["You head to the farmhouse, stopping to smell some green flowers that look suspiciously like leaves. Anyways, you make it to the farmhouse without getting seen, and find a whole butter cake just sitting on the wooden table. You take the whole cake and creep back out of the house, not getting seen. You see your box in the distance.", "You don't go to the farm-house, but see some red berries that look identical to the ones you ate before."])
                    if x == 0:
                        inventory("Cake", 1)
                        x = choice("Do you want to go to the box?", ["You run quickly to the box, and the farmers see you, but it's too late. You get in and close the lid.", "You don't go to the box, and while you are decide what to do next, you fail to realise that a farmer is standing right behind you..."])
                        if x == 0:
                            story_timetravel_3()
                        else:
                            ending("Karma", 8, "time travel")
                    else:
                        x = choice("Do you want to eat the berries?", ["You eat the berries and it turns out they were poisoned.", "You decide to not eat the berries, because they could be poisoned. Seeing your box in the distance you start heading to it, but find that you are quickly being chased by farmers. They catch up to you and the inevidable happens."])
                        if x == 0:
                            ending("Poisoned", 9, "time travel")
                        else:
                            ending("Teaming is not fair", 10, "time travel")

            elif "Berry" in inventoryList:
                print("The farmers rush towards you, and everything seems to fall apart. As a last ditch choice, you eat the berry and realise that you can jump higher than usual! Jumping over the farmers, they stop and stare as you quickly run away from the points of their glistening tools.")
                inventory("Berry", 1, "lose")
                print("\nSeeing your box in the distance, you run to it, and get in, closing the lid. Your feel that your power is slowly slipping away, but you have succesfully escaped the farmers.")
                story_timetravel_3()
            else:
                print("The farmers rush towards you with their tools pointed, and you don't stand a chance against them.")
                ending("Poked by Garden Tools", 11, "time travel")
        else:
            x = choice("Do you want to run to the farm house?", ["You take the risk, running silently to the farmhouse. Creeping past the door, you see a bag of gold sitting on the table! You grab it, but a few coins clatter onto the floor. A farmer comes and chases you out of the house.", "Not taking the risk, you stay in our hiding place for quite some time. Pleasantly, your box appears next to you. You hop in, closing the lid behind you as you get ready for the ride."])
            if x == 0:
                if "Power" in inventoryList:
                    print("\nYou have your power, so you outrun the farmer quickly, getting away with the gold. You see your box in the distance, so you sprint to it, getting in and closing the lid. Your power slips away, but you gained an extra bag of gold!")
                    inventory("Power", 1, "lose", False)
                    inventory("Gold", 1)
                    story_timetravel_3()
                elif "Berry" in inventoryList:
                    print("\nYou start running, but you can't outrun the farmer. As an last effort, you eat the berry and feel some kind of power emerging inside of you. But it is too late, and the farmer catches up to you and knocks you to the ground.")
                    inventory("Berry", 1, "lose")
                    ending("Don't Steal Next Time", 12, "time travel")
                else:
                    print("\nYou start running, but you can't outrun the farmer.")
                    ending("Slowpoke", 13, "time travel")
            else:
                story_timetravel_3()
    else:
        x = choice("Do you want to hide or show yourself to the farmer?", ["You decide that the farmers can't do much, so you show yourself to them. After seeing you, they grab hold of you and lock you in a cell.", "You decide to hide because it would be too risky to show yourself. But it doesn't make a difference are you are caught and locked in a cell."], ["show", "hide"])
        if x == 0:
            ending("Stuck with the Farmers", 14, "time travel")
        else:
            ending("You hid, but you're still stuck with the farmers...", 14, "time travel", alt=True, altname="Stuck with the Farmers")

def story_timetravel_3():
    print("You whirl around in the box, as it shakes and moves violently. Peeking out of the box, you see time passing before you eyes, the asteriod crashing into the earth, and the dinosaurs running away.")
    print("\nSuddenly, everything does dark, and all you see and hear is snow and howling winds for quite a long time. As you emerge into brightness again, you blink you eyes, as the box stops with a jolt.")
    print("\nLooking out, you see the dirt paths and road of a very old time. You step out of the box, and the box dissapears. You wonder down the streets and see soldiers patrolling everywhere. Looking at a nearby store, you spy a small bag of money that looks unattended.")
    x = choice("Do you want to make a grab for it?", ["You grab quickly at the bag, turning away to see a tall soldier right behind you.", "You decide against getting the bag, as there are too many soldiers around to try and catch you. Minding your own business, you stroll down the street. A nice person comes and gives you a tasting of cheese, saying something in a different language."])
    if x == 0:
        if "Power" in inventoryList:
            print("Luckily, you can outrun the soldier, as you gained some power from the berry before. You run away from the soldier, and he gives up the chase. After running for a while, your power slips away, but you are standing in front of a gigantic castle.")
            inventory("Power", 1, "lose", False)
            inventory("Gold", 1)
            x = choice("Do you want to enter the castle?", ["You enter the castle, and see two soldiers guarding the gate. They are sleeping on the job! You enter causiously, trying not to make any noise. Suddenly, you hear a crash from behind, and you realise you bumped the statue in your hurry to get away from the soldiers. The soldiers wake up and catch you, throwing you into jail.", "You decide to not go into the castle, because you are probably wanted for what you stole. Without looking, you walk into a tavern, and look up. The men in the bar stare at you angrily, and start running at you."])
            if x == 0:
                ending("Be careful, that's an antique!", 16, "time travel")
            else:
                x = choice("Do you want to run or give them your gold to get away?", ["You try to run away, but the men quickly catch up to you.", "Thinking fast, you hold out your bag of gold to the men. They stare at it greedily, and you throw it at them, letting you run away. You come to a beautiful meadow, one that looks amazing and capturing your attention"], ["run", "gold"])
                if x == 0:
                    ending("Beaten Up", 17, "time travel")
                else:
                    inventory("Gold", 1, "lose")
                    x = choice("Do you want to check out the meadow?", ["You decide to check out the meadow, and after awhile, you check the time and realise you have been looking for 3 years. Not being able to leave, you are trapped forever.", "You decide not to enter, and you realise that while you were checking out the meadow you completely missed your time machine sitting a few meters ahead. You enter happily, closing the lid to travel to a new time."])
                    if x == 0:
                        ending("The meadow of eternity", 18, "time travel")
                    else:
                        story_timetravel_4()
        else:
            print("You start running from the soldier, but you are caught quickly and taken into a jail cell.")
            ending("Stuck in Medieval", 15, "time travel")
    else:
        x = choice("Do you want to take it?", ["You decide that you want to eat the cheese as the person seems so nice. When you eat it, you feel something powerful, but don't know what it is. The person asks you if you want to buy the cheese.", "You decline the cheese gratefully, and the seller justs shruggs and goes away. Walking down the street, you come across an interesting store, Time selector."])
        if x == 0:
            if "Gold" in inventoryList:
                x = choice("Do you want to pay for the cheese?", ["You pay for the cheese, and take another bite of it. Suddenly, you feel like you have gained some power. Clicking your fingers, all the soldiers fall down dead. The shopkeeper looks at you, smiling, and you smile back. You hit double jump, and you fly upwards, so suspicously like minecraft. As you fly more and more upwards, and all the shops turn blocky. You try to turn back, but you are trapped forever, the shopkeeper's laugh echoing round and round your head.", "You decline to the shopkeeper, but the shopkeeper just smiles sadly at you and clicks his fingers. Everything goes dark."])
                if x == 0:
                    ending("Minecraft", 21, "time travel")
                else:
                    ending("Don't decline next time...", 19, "time travel")
            else:
                print("You would want to, but you don't have any money. You tell the shopkeeper this and he looks at you sadly. Clicking his fingers, all the soldiers rush to you, holding out their spears angrily.")
                ending("Broke", 20, "time travel")
        else:
            x = choice("Do you want to enter?", ["You enter the store, and a selection bar randomly pops up in front of you. On it are a list of different times. Which do you want to pick?", "You walk past, and see your time machine box ahead. Hopping in, you close the lid and prepare to travel to anotehr time."])
            if x == 0:
                x = choice("""Which do you want to pick?
1. Dinosaurs
2. Farmers
3. Medieval
4. WW2
5. Modern World
6. Space Civilisation""", ["", "", "", "", "", ""], ["1", "2", "3", "4", "5", "6"])
                print("Your box materialises in front of you, and you hop in. The only difference is that it now says the time you picked. Getting ready to leave, you close the lid.")
                if x == 0:
                    story_timetravel()
                elif x == 1:
                    story_timetravel_2()
                elif x == 2:
                    story_timetravel_3()
                elif x == 3:
                    story_timetravel_4()
                elif x == 4:
                    story_timetravel_5()
                elif x == 5:
                    story_timetravel_6()
            else:
                story_timetravel_4()

def story_timetravel_4():
    # WW2
    print("You are bumped and kicked around in the box as you travel to your next time. As you arrive, you hop out, hoping to see the present, but, sadly, you see a large open field. Looking around, you see nothing.")
    x = choice("Do you want to explore?", ["You start to look around and see a storm of troops coming towards you. They are holding up guns, so you duck and quickly get out of their way. On the other side is another group of soldiers. Lucky you didn't get caught in the crossfire! You hear gunshots as you leave the area, and come across a deserted city.", "You stay at your time machine, which after abit just dissapears. Suddenly, you hear gunshots, but it is too late, and you are caught in the crossfire."])
    if x == 0:
        x = choice("Do you want to enter?", ["You enter the abandoned city, and see destruction and collapsed buildings all around you. It looks like some kind of war was here. Out of all the buildings, there are three that still seem intact. One that looks like a great hall, another that looks like a bomb shelter, and one that is a temporary camp.", "You decide to keep walking, and soon find yourself in a massive desert."])
        if x == 0:
            x = choice("Which do you want to enter?", ["You enter the hall, and find it deserted. Suddenly, you hear a whistling sound and a large kaboom outside the hall. Before you can wonder what happened, you are incinerated in a blink of an eye.", "You open the heavy metal door to the bomb shelter and enter. Inside are a group of people, huddling, looking scared. They tell you that a bomb is coming, and that you are in WW2. Luckily you are in a bomb shelter, so you are not affected by the large explosion. Suddendly, your box appears in front of you.", "You enter the tent flap of the camp, and a soldier grabs you and holds a gun to your throat."], ["hall", "bomb shelter", "camp"])
            if x == 0:
                ending("Incinerated", 24, "time travel")
            elif x == 1:
                x = choice("Do you want to go into your box?", ["You enter your box and close the lid, saying bye to the other people in the shelter.", "You decide you won't go in, and after awhile the box dissapears. Suddenly, the door swings open and a gun is pointed straight at your forehead. Pew Pew."])
                if x == 0:
                    story_timetravel_6()
                elif x == 1:
                    ending("'Pew Pew' - That guy who plays too much Valorant", 25, "time travel")
            else:
                if "Gold" in inventoryList:
                    print("Thinking fast, you pull out your gold that you found earlier. The soldier decides to spare your life in return for the gold, and you hurridly leave the camp and the destructed city. You keep walking and find yourself in a desert. Starting to feel thirsty, you rummage around your bag to find water. Nothing.")
                    ending("Dehydration", 26, "time travel")
                else:
                    print("The soldier shoots his gun once, which is enough to make you go bye bye.")
                    ending("Sayonara", 27, "time travel")
        else:
            if "Cake" in inventoryList:
                print("You are extremely hungry, so look in your bag to find the cake that you stole earlier. Eating it happily, you continue until you see a small military camp.")
                inventory("Cake", 1, "lose")
                x = choice("Do you want to enter?", ["You enter the camp and find no-one inside. Taking a jug of water, you leave. Walking for a few days, you drink you your water, but also find a developed city that looks untouched by war.", "You continue, ignoring the camp. After an hour of hiking, the wind starts to pick up, and you realise you are caught in a sandstorm. You try to escape, but you trip and fall, sand covering your body like a blanket."])
                if x == 0:
                    inventory("Water", 1)
                    x = choice("Do you want to enter the city?", ["You arrive at the city, and see a sign saying 'Hiroshima'. Oops.", "I don't know why you don't want to enter a city when you have run out of water, but sure? You died of thirst."])
                    if x == 0:
                        ending("Bombed", 30, "time travel")
                    else:
                        ending("Bad Choices", 29, "time travel")
                        addachievement("Bad Choices")
                else:
                    ending("Buried Forever", 28, "time travel")
            else:
                print("You are extremely hungry, but there is no food at all. You then proceed to starve to death.")
                ending("Stranded in the Desert", 23, "time travel")
    else:
        ending("Caught in the crossfire", 22, "time travel")

def story_timetravel_5():
    # Present
    print("The box whirls around again, and when you jump out, you realise that you are back in your cellar. What an adventure!")
    ending("The Present", 22, "time travel", "win")
    addachievement("Back to reality")

def story_timetravel_6():
    # Future
    print("Once again, you are being travelled to a new time. Hoping to see your attic, you open the lid slowly and find yourself in an endless hallway.")
    print("\nYou hurry down the corridor quickly, and you realise that futuristic code is engraved onto the walls. You keep walking, but find nothing. It is not until you stumble upon a trapdoor that you get a break from the endless corridors.")
    x = choice("Do you want to go into the trapdoor?", ["You enter into the trapdoor to see a massive dark room, and a gigantic square floating object above you. For a minute, you stare at the large object, and see electrical orbs pulsing in and out of the square. Looking out from below the enormous cube structure, you see a thick red wire running from the cube to what looks like a super-computer. Looking around you see other coloured wires going into the computer. There is a ladder next to you that seems to lead to the top of the cube.", "You decide to not go into the trapdoor, and continue down the passageway. After a few intersections where you have to turn, you realise that you are lost in the bright, code etched corridors forever."])
    if x == 0:
        x = choice("Do you want to climb the ladder?", ["You start the long climb up the ladder and after what seems like a very long time, you reach the top. On the top is a massive printed text that reads: 'AI Supercomputer 3045'. Wondering what that means, you look up at the small supercomputer above you and see that it is pulsing red. There is a thin rope ladder leading to the top.", "You decide not to climb up the ladder, and continue wondering underneath the computer-feeding cubes. After awhile, you come across a large air compressed door. There is 2 buttons that both seem to open the door, but only one can be correct. One is red, and the other is blue."])
        if x == 0:
            x = choice("Do you want to climb up it?", ["You climb up to the top, and see the computer screen. On its pixelated display there is the history of what happened. Reading it, you realise that the year is 5002, and pollution has caused the whole world to be unliveable, and humans have gone extinct, except one who's whereabouts are unknown. This computer is the last memory of all the technology that the humans made, and the last memory that might ever exist. The computer auto-scrolls with your eyes, and the last line reads: 'If you are reading this, find the Earth restore gem before it is too late.' A countdown is right below it, reading 2 hours left.", "You decide not to go up to the computer, and suddenly, all the room lights up, and red alarms flash from everywhere. A ten second countdown flashes on the walls, and the structure collapses as a massive earthquake shakes violently. The air is toxic, and you can't breathe, so you don't last long."])
            if x == 0:
                pass #finish
            else:
                ending("Toxic Fumes", 32, "time travel")
        else:
            x = choice("Which button do you pick?", ["", ""], ["red", "blue"]) # finish
    else:
        ending("Lost in Code", 31, "time travel")


# JADEN - SCHOOL
def story_school(user:str):
    global name, o
    if user.lower() == 'pancake' or user.lower() == 'ethan':
        name = 'Ethan Wei'
        o = ' (still no girlfriend though)'
    else:
        name = 'Eefen Wedge'
        o = ''
    print(f"""You start the school year, fresh and ready. You got new shoes, new laptop and hopefully a new start.
As you get on the train, you notice that your best friend {name} isn't there, and he isn't responding to your messages, which is a bit weird but then again, {name} is weird, so you don't worry too much. 
When you get to Leederville station, you realise that there are no students around you. Feeling uneasy, you walk into school, hoping that this is all just a coincidence…
""")
    slowprint("\nYEAR 8 SURVIVOR SIMULATOR", 0.05, ['bold'], 'red')
    c = choice('Will you enter?', [f'You press the button, and are sucked into the game. Your friend {name} joins you too.', 'You continue on your way to school, and have a normal school year.'])
    if c == 0:
        print("As soon as you walk into the school, you hear a swish behind you, and then a man (whose face you can't see because that's plot armour) does an evil laugh. He explains to you that one by one, he is luring students back to school one by one so that they all fall victim to ligma. ")
        c = choice('''You have 3 options:
1. Ask him about ligma
2. Tell him about off and away policy
3. Chuck your phone and run
What will you do?''', ['You instantly fail, as the man clicks his fingers, and the world goes dark.', 'You instantly fail, as the man clicks his fingers, and the world goes dark.', """As you bolt away, across the oval, the man laughs again, says “excellent. A worthy subject.” Then vanishes into thin air, as darkness eats up the sky, and your vision goes blurry. You stumble into Mills and pass out. Let the trials begin."""], ['Ligma?', 'Off and Away', 'Phone'])
        if c == 0:
            slowprint('FAIL', 0.05, ['bold'], 'red')
            ending('LIGMA BALLS', 2, 'School')
            addachievement('LIGMA BALLS')
        elif c == 1:
            slowprint('FAIL', 0.05, ['bold'], 'red')
            ending('Turned off...', 3, 'School')
        elif c == 2:
            c = choice(f"""You wake up to find your best friend {name} standing over you. He explains that he faked his own death to escape from the man, who he calls “The Ligma Lord”.
The Ligma Lord has taken control of most of the students and planning to use them for world domination. 
{name} explains the school has become a hunting ground for the ligma-ed students to hunt down the remaining ones, and that no-one can leave school.
He says he thinks he has been here for 3 days, but he can't be sure. As soon as he says that Ligma-ed students start using Pythagoras to calculate where to attack them.
You and {name} start running for the door, when the air vent crashes open with Nelson Yan tumbling out, tackling {name} to the ground, 
causing {name} to scream loudly. You pause, considering what to do.""", [f"You run for the exit, as {name} uses his plot armour to shield you from the Ligma Zombies, sacrificing himself. Mills Building Entrance crumbles, allowing you to burst into the fresh air.", "You Blast “Never Gonna Give You Up” out of your speakers, vaporising the Ligma Zombies. But unfortunately, you didn't wear earplugs, and your eardrums explode, causing you to pass out, and fall victim to Ligma.", "The Foam in the Fire Extinguisher has the chemical properties to turn the ligma-ed students into healed Perth mod Students. Just as you think you have saved everyone, The Ligma Lord appears, and uses his Blooket Dark Energy, which traps you, as you are transported into the dark realm."], [f'Ditch {name}', 'Go back', 'Fire Extinguisher'])
            if c == 0:
                story_school_2()
            elif c == 1:
                slowprint('FAIL', 0.05, ['bold'], 'red')
                ending('Rick Astley let you down...', 4, 'School')
            elif c == 2:
                inventory('Fire Extinguisher', 1, 'add')
                print('''You Find Yourself on a Ghostly platform, on top of dark clouds, and directly in front of you is the Ligma Lord. 
He reveals his face, turning out to be no other than Mr McMahon He laughs, saying that he always appears as the person who you fear the most. 
He says that He is fear itself, and that fear will eventually conquer everything. His Voice darkens as he says that You have found his one weakness, 
and he has decided that you will be the first victim of the war.

BUT!!!

Because he was yapping for six billion years, that gave you the chance to reach into your bag and choose a weapon.''')
                addachievement('Godslayer')
                c = choice('Choose your weapon: ', ['You summon your inner Kendrick Lamar and start roasting him. It seems to be working, as he catches on fire until your laptops battery dies. Ligma Lord recovers, then blasts your body into ashes.', 'As You find the Formula to solving any immortal, Mr White randomly spawns and says to use the formula you must solve this quadratic equation. While You are figuring it out, Ligma Lord Burns your maths notebook, and then opens a black hole that destroys you immediately.', 'You pitch the mochi and it lands perfectly into his throat. As he is choking, you grab your empty fire extinguisher and slam it at him, causing him to fall. As you stand over his helpless body, he whispers some final words.', 'You make a mad dash into for the portal, and plunge through, but you hear Ligma Lord laugh as you burst into the fresh air.'], ['Laptop', 'Math Book', 'Mochi', "Portal"])

                if c == 0:
                    slowprint('FAIL', 0.05, ['bold'], 'red')
                    ending('Does anyone have a charger?', 5, 'School')
                elif c == 1:
                    slowprint('FAIL', 0.05, ['bold'], 'red')
                    ending('Mr White gave me a B for Maths...', 6, 'School')
                elif c == 2:
                    print('Ligma Lord: Well Done...')
                    sleep(1)
                    print('Ligma Lord: I have lost my power to fight... For you have conquered fear itself...')
                    sleep(1)
                    print('Ligma Lord: You are the one worthy of being a hero... Not just for students, but for the world...')
                    sleep(1)
                    print('Ligma Lord: Take that portal over there, it will send you back to Perth Modern...')
                    sleep(1)
                    print('Ligma Lord: I apologise for the Ligma, when you get back everything will be restored, except the ones who have died, not even I can deal with Death...')
                    sleep(1)
                    print("Ligma Lord: I'm sorry...")
                    sleep(1)
                    print('''As the Ligma Lord vanishes, you pick up your school bag, and bow your head in silence, 
then take a deep breath, and slowly walk towards the brightening portal. 
You take one last look behind you, to see the platform and clouds turn into a stream of light, 
then step through the portal, awaiting your first day of school.''')
                    ending('Master of Fear', 7, 'School', 'win')
                    addachievement('Ligma Master')
                elif c == 3:
                    story_school_2()

    elif c == 1:
        print(f'You live a normal life {o}.')
        ending('Still Here...', 1, 'School', 'win')

def story_school_2():
    print("""You decide to explore the hallways of Beasley, hoping to find anybody else that might still be alive. 
You break open the locked doors, to find a figure bent over in the shadows of the staircase. You call out to them,
but they give no response. You take a step forward, and turn on the lights, revealing your hass teacher, Mr McMahon. 
Is it just your imagination, or do they look a bit… funny? Then he/she turns towards you, revealing that they have been possessed with LIGMA!!!!! """)
    slowprint('BOSS BATTLE: Adam Smith and the Wealth of Ligma', 0.05, ['bold'])
    c = choice('''What will you do? 
Option 1: Say, "This isn't fair, I wasn't even late!
Option 2: Bring out your metal ruler and prepare to slap the ligma out of your teacher.
Option 3: Drink some Servo Slushie and turn into the smartest person on Earth (Not endorsed by Coca-Cola) ''', ["""Your Hass teacher turns red in the face and summons a grandfather clock, which shows that you were indeed 0.4 seconds late, 
and then proceeds to punch you in the face. Really Hard. """, """You pull out your ruler, and charge at the HASS teacher. They use the power of reports and cause you to lose motivation and concentration in your attack (and studies). 
They pull out a giant textbook and use the power of communism to summon a horde of Ligma-ed Students. You attempt to escape but they use guerilla warfare to cut you off and ending your rights. """, """The Chill of Ice runs through your veins, and you feel yourself becoming a Super Nerd. Your Hass Teacher smirks, then proceeds to summon a Horde of Ligma-ed Students. 
Luckily for you, you got an A in HASS and you make a social contract with them, cause them to revolt on the HASS Teacher, who screams, 
and then is consumed by a barrage of pointless questions from the students. The Ligma-ed students then dissolve into the shadows as they have no teacher, 
and so they are not students anymore. You feel sadness as you remember that you don't know how to un-ligma students, and that your friends can't be saved. 
With a heavy heart, you trudge past Beasley and into Andrews, hoping to find someone. """], ['1', '2', '3'])
    
    if c == 0:
        ending('My watch is 1 minute slow', 8, "school")
    elif c == 1:
        ending('Absolute !^*#@?” Nerds', 9, "school")
    elif c == 2:
        sleep(1)
        addachievement('With Great Power Comes Great Responsibility - Confucius (I think)')
        print(f"""You once again, bust open the locked doors and find the place a little creepy without the lights. You quietly walk past some lockers, 
finding Ligma-ed Students lying down left and right. You have hope that there might be someone who might be a student still here, but there seems to be no sign.  

UNTIL! 

You walk into a classroom with about twenty Year 8's in there, all equipped with survival tools. Seeing that you have not been ligma-ed, they invite you in, 
and explain that they have been hiding out at school, and researching on how to defeat the Ligma Lord, which would restore order to Perth Modern School. 
They say that their leader is Mr White, who used his legendary teacher keys to open this classroom for them, allowing for the students to have a safe base. 
However, Mr White caught an extremely contagious disease known as Karen, and the only cure lies in the maths office. 
The students are preparing to send a search party and ask you to come with them. You accept their invitation. The students are: 

PixilPrawn -> Coding Kid who looks like another kid called Jaden. He knows you the best and doesn't play games. 
Soul -> Guy who can't see without his glasses. {name}'s go to person to complain to. He uses a volleyball to beat up Ligma-ed People. 
Gorilla E. Duffy -> The weird kid who loves watching Anime, and somehow gained the power to summon infinite gum and blow big bubbles with the gum. 
Life Is Valorant -> The guy who plays too much Val, uses a VR Headset To simulate the background. 
Wingsley Kong ->  Super cool person who definitely didn't pay $50 to be in this. 
You have been taught how to use the powers of Counter-Ligma Jitsu as a way of self-defence. """)
        inventory('Counter-Ligma Jitsu', 1, 'add', False)
        print("""You and the search party decide to split up for efficiency. You are defeating enemies left and right with your Counter Ligma Jitsu. 
You are now at AU21, where you have planned to meet up with the rest of them. Suddenly, the lights go out, and you feel an ominous presence, 
almost as intense as Ligma Lord. Suddenly a flame comes in focus, sitting in the palm of someone's hand. As you walk closer, 
you see the body of Gorilla E. Duffy slumped over in front of them, blood trickling out of his ear. You immediately know that the mission has not gone to plan. 
""")
        c = choice('''What will you do?
Option 1: Run. This guy is too overpowered, regroup at base. 
Option 2: Run, but towards Duffy. You need to save him. 
Option 3: Crank Up the Wii Theme and Counter Ligma him. 
Option 4: Act all superhero-like and confront him. Stall until the rest of the group is here. 
''', ["""You activate your Nike Kicks and run towards the stairs. You are nearly at the exit when the man says: 

“English, or Spanish?” 

You feel your muscles tensing up as your heart sinks. You hear the music play and the Ligma-ed slowly close on you. 
He laughs and you get swallowed in the waves of Ligma. """, """You rush towards Duffy, but instantly get knocked back by the man. Realising you must stall for time, you turn towards him, 
readying up your Ultimate move. The man is no other than the new maths teacher Mr Black. He has a deranged look on his face and his veins bulge. 
He tells you that he is Mr White’s twin brother, and that he never got to be the favourite child. The Ligma Lord had promised him fame and glory 
if he managed to defeat all the remaining students. Mr Black suddenly has a giant grin as he summons two fireballs in his palms, and you have a 
sinking feeling that you might just be cooked""", """""", """You rush towards Duffy, but instantly get knocked back by the man. Realising you must stall for time, you turn towards him, 
readying up your Ultimate move. The man is no other than the new maths teacher Mr Black. He has a deranged look on his face and his veins bulge. 
He tells you that he is Mr White’s twin brother, and that he never got to be the favourite child. The Ligma Lord had promised him fame and glory 
if he managed to defeat all the remaining students. Mr Black suddenly has a giant grin as he summons two fireballs in his palms, and you have a 
sinking feeling that you might just be cooked"""], ['1', '2', '3', '4'])
        if c == 0:
            ending('First Person to Move is Ga-', 10, 'School')
        elif c == 2:
            m = randint(1,3)
            if m == 1:
                mixer.music.load('Songs\\Wii-Shop.mp3')
            elif m == 2:
                mixer.music.load('Songs\\Wii-Music.mp3')
            elif m == 3:
                mixer.music.load('Songs\\Wii-Sports.mp3')
            mixer.music.play()
            print("""You unleash First Form: Brainrot Banishment, which he easily deflects using advanced calculus. He decides to skip all the plot build-up 
and go straight for his almighty Seven Sinful Solutions, which creates a giant blackhole that turns the building 
into rubble, as your limbs get pulled apart by the intense gravity. """)
            ending('Bro needs to learn about plot development', 11, 'School')
        elif c == 3 or c == 1:
            slowprint("Hey, what's the formula for defeating old math teachers? ", 0.05, ['bold'])
            print("""The fireballs track your movements, so you attempt to deflect it. However, they explode before they make contact, 
causing your school shirt to burn away.""")
            c = choice("""What will you do?
Option 1: Use First Form: Brainrot Banishment
Use Tenth Form: Razor Sharp Grass""", ["""You use First Form: Brainrot Banishment and attempt to explode the fireballs before they reach you. They collide in a sparkle of light, 
as the floor begins to crack. You try to increase the speed of your attacks, but before you can, Mr Black used Pythagoras’ theorem to sneak up
behind you and stab you with a scientific calculator.""", """You realise that the surface area the fireball makes is larger if it doesn’t explode on impact. Knowing this, you decide that offence is the best defence, 
and use Tenth Form: Razor Sharp Grass to close the distance between you and Mr Black. Surprised by the speed, he tries to retreat, but you quickly switch to your 
secondary weapon and from point blank, deliver a devastating Three Dollar Tri Attack. You feel your arms drop from exhaustion, as Mr Black falls to his knees. 
Tired out, you walk over to Duffy, and nudge him, but he’s out cold. As your vision begins to fade, you lie down on the carpet when- 

BOOM. 

The floor underneath you starts disintegrating. You jump up, just as holes begin to form. You turn around to see Mr Black standing upright, as if possessed. As he lifts his head towards you, all you can see is pure red light coming from his eyes. 

This Battle isn’t over yet. """], ['1', '2'])
            if c == 1:
                ending('sKiBiDi BrAiNrOt is CrAzY', 12, 'School')
            elif c == 2:
                print("""The floor gives way entirely and rubble falls towards the ground. You feel a rush of adrenaline as you hold Duffy’s wrist and use Seventh Form: Slowed Down Phonk to slow down your fall to Lower Andrews. 
Realising you don’t have much energy left, you switch into an offensive stance, and prepare your one and only attack.""")
                c = choice("""Which move?
Option A: Use Second Form: Homework Hand-in
Option B: Use Sixth Form: Winds of Heavenly Transport
Option C: Use Eleventh Form: Last Resort""", ["""You use your homework answers to send a ripple of energy that disrupts Mr Black’s Aura Levels. He starts doing some weird dark portal opening that summons undead Ligma Zombies, which kind of means that they died three times, 
and are three times stronger. As they close on you and Duffy, you close your eyes, accepting your fate. """, """You teleport behind Mr Black and attempt to slice off his head using your Smart Rider, but he detects your presence and full-on thrusts you backwards, breaking your ribs. 
You fly back at least twenty metres as you slam into the wall, causing an impact mark on the white walls. """, """Because this move uses so much of your energy, you must hit this or else you’re cooked. You factor in wind speed, how tall Mr Black is, the number of tacos you’ve had, where the Blooket headquarters are, if the weather on Sunday will be rainy or sunny. You fire the beam of energy… 

And miss. 

Mr Black walks over slowly, and one-hit KOs you."""], ['A', 'B', 'C'])
                if c == 0:
                    print("""Suddenly, a volleyball comes smashing into the zombies, as it rebounds around. It’s your friends, finally here. PixilPrawn 
summons a lemonade stand that uses capitalism to cancel out Mr Black’s Ligma communism, making him unable to summon the zombies. 
Life is Valorant locks in and forces Mr Black into a corner, his shots shredding any possible manoeuvring from Mr Black. 
Wingsley Kong uses his cheering ability to boost the attack of Soul, who delivers the final blow, a powerful spike that blows off Mr Black’s head. 
You are in awe as they all stand looking really cool as Mr Black explodes into a shower of light. They tell you that because they were using google maps, 
they got led to the grand line, but they found the way back after finding the One Piece. They pick up Duffy and start heading back towards the 
classroom because plot twist, the One Piece was a cure to Karen. """)
                    addachievement('Luffy, that’s not the real One Piece… that’s Wingsley’s pocket money.')
                    
                    print("""You get back to the classroom, where the students are happy to see you alive. The smart girl in your year (that you can’t remember the name of) 
goes and injects the cure, which makes Mr White awake from his coma. He instantly starts calculating, and then spits out some prophetic lines 
about how the students need to work together to conquer the remaining buildings to defeat the evil forces of ligma, then proceeds to pass out. 
The students hold a brief meeting and decide that they should plan an assault on the remaining buildings that Ligma Lord has control over.
They tell you to get some sleep as you have been thoroughly exhausted by the day’s activities. You find yourself suddenly awaking in a dark void, falling. 
You try to yell for help, but your lips move soundlessly in the darkness. You hear the evil laughter of Ligma Lord as you feel a rush of wind awaken you 
from your nightmare. Wingsley Kong is shaking you awake as he explains that the attack groups had decided to strike early morning and left you here 
because they wanted you to rest. Hearing this news, you know that you must go help them because you have a feeling that they are going to mess up.  
Wingsley Kong agrees and wakes up Duffy because he is the only other person left in this room, even Mr White has gone.  """)
                elif c == 1:
                    ending('Cheats were enabled', 14, 'School')
                elif c == 2:
                    ending('The calculator was in radians...', 13, 'School')
                
# ETHAN - TUTANKHAMUN'S TOMB
def story_tomb():
    print("""You are a tomb explorer that explores ancient tombs. You recently decided to explore Tutankhamun's tomb. You took a plane over to Egypt, but while flying over Tutankhamun's tomb, the plane suddenly spluttered and crashed. You were flung out of the plane and landed near the tomb. You land without any food or water, but you have all the tools you need.""")
    x = choice("""Choices:
1. You can explore the tomb without any food or water
2. Leave exploring the tomb for later, and search for food and water in the plane's wreckage""", ["You pick up all of your tools, and slowly walk towards the tomb's entrance. You dust the sand away from the tomb entrance, and some of the sand gets blown into your face and up your nose, choking you. You have no water to clear your throat, so you suffocate.", "You walk towards the plane wreckage and discover that everyone inside the plane got burnt alive from the fire. You carefully walk into the plane's storage unit from a side door and haul out a box of food and water. After walking out the plane, you discover the captain of the plane is still alive, but badly injured. He asks for food and water."], ["1", "2"])
    if x == 0:
        ending("Bad Choices", 1, "tomb")
    else:
        inventory("Food", 2, "add", False)
        inventory("Water", 2, "add", True)
        x = choice("""Choices:
1. You give the captain some food and water.
2. You leave the captain to die, because you need all the food and water you have, to explore the tomb.								                  
3. You realize that even if you give the captain food and water he I still going to die, so you give up your mission of exploring the cave and take him to a hospital.""", ["You tear open your box of resources you got from the plane and give some food and water to the captain, but you realise that most of the food is burnt and inedible, meaning you now only have enough supplies to last a few days maximum.", "You leave for the tomb, not looking back even once at the pleading captain. You feel no guilt as to what you have just done, but on the bright side you have enough supplies for a whole week. You reach the tomb entrance.", "Throwing down your backpack full of your tools, you feed the captain then you give him a piggyback ride to the nearest town."], ["1", "2", "3"])
        if x == 0:
            inventory("Food", 1, "lose", False)
            inventory("Water", 1, "lose", False)
            x = choice("""Choices:
1. You decide that the captain is too much of a burden to bring along to the tomb, so you tell him the directions to the nearest town and set off to the tomb.
2. You decide to bring along the captain, thinking it would be useful to have another pair of hands to help you carry your stuff.""", ["After helping the captain, you pack up all your stuff and make your way to the tomb. When you reach the tomb you dust away the sand, and some of it gets in your nose, but some water washes it down. You descend the stairs, and you are officially in the tomb of Tutankhamun. As you walk down the corridor, you reach inside your bag to get a flashlight, but a mummy jumps out of a trapdoor and growls at you.", "Helping the captain up, you guys make for the tomb entrance, and reach it in no time, dusting away the sand, some of it gets into your nose, but some water helps wash it down. You descend the stairs, and you are now officially in the tomb of Tutankhamun. As you walk down the corridor, you reach inside your bag to get a flashlight, but a mummy jumps out of a trapdoor and growls at you."], ["1", "2"])
            if x == 1:
                x = choice("""Choices:
1. You grab onto the captain's hand and run from the mummy, but the captain slows you down.
2. You choose to save yourself, so you push the captain towards the mummy, and you run.""", ["As you run, you hear the mummy slowly gaining on you. The captain is slowing you down and there is no hope for you and the captain, you are both doomed.", "You push the captain towards the mummy and run. The captain screams at you, but that is suddenly cut short. You run quickly out of the tomb. You feel bad, and that you are going to be haunted about what happened for the rest of your life, but at least you stayed alive."], ["1", "2"])
                if x == 0:
                    ending("Infinitely Doomed", 3, "tomb")
                    addachievement('I Want My Mummy!')
                else:
                    ending("Sacrifices must be made", 4, "tomb")
            else:
                x = choice("""Choices:
1. Stay and fight the mummy with the metal rod at the bottom of your backpack.
2. Run.""", ["You reach inside your bag, and you fumble for the metal rod, but it is hooked on something. The mummy jumps on top of you, and the bag tumbles out of your reach. You close your eyes for the inevitable.", "You turn around and run, and you hear the mummy's footsteps slowly fading away. You make it out alive, but you are traumatized forever."], ["1", "2"])
                if x == 0:
                    ending("R.I.P", 5, "tomb")
                    addachievement('I Want My Mummy!')
                else:
                    ending("Mentally unstable... womp womp", 6, "tomb")
        elif x == 1:
            print("\nAfter entering the tomb, you slowly walk down the corridor, wary of any traps or ambushes from the undead. You reach inside your bag to get a flashlight, but you hear a footstep coming from ahead.")
            x = choice("""Choices:
1. You pull out your metal rod and wait for whatever it is ahead to show itself.
2. You pull out your metal rod and hide in a gap in the wall and wait for whatever it is to go away.
3. Run.""", ["You hold your weapon in one hand, and you prepare for whatever is coming towards you. The mummy appears much closer than you expected, but you still whack it on its head multiple times until it finally falls at your feet.", "You take out your metal rod and hide in the gap in the wall. The mummy walks right past you, and you let out the breath you were holding. You sneak behind the mummy and knock its head off.", "You turn around and run, and you hear the mummy's footsteps slowly fading away. You make it out alive, but you are traumatized forever."], ["1", "2", "3"])
            if x == 0:
                story_tomb_passageway()
            elif x == 1:
                story_tomb_passageway()
            else:
                ending("Mentally unstable... womp womp", 6, "tomb")
        else:
            ending("A Good Citizen", 2, "tomb", "win")

    slowprint("THE END", 0.05, ["bold"])

def story_tomb_passageway():
    x = choice("""Choices:
1. Continue down the passageway into the antechamber as fast as possible, before any other mummies appear.
2. Advance slowly, checking for any traps.""", ["You sprint down the passageway, but you catch your foot on a tripwire, and you fall flat on your face. You land on a mound of sand, and a mummy jumps right on top of you. It pushes you further into the sand, and you choke on the sand that gets in your mouth and down your throat.", "You get out your flashlight, and you slowly walk forward, scanning the wall and floor for any traps. You avoid a tripwire, and with some luck you step over the pressure plate. You make it to the door of the antechamber."], ["1", "2"])
    if x == 0:
        ending("5-Star Meal", 7, "tomb")
    else: 
        x = choice("""Choices:
1. Go into the antechamber and eat some of the food inside your bag, so you can restore some energy.
2. Walk through the antechamber without stopping, because there might be traps""", ["You open the door of the antechamber, and you sit on the closest spiritual animal couch. This angers the God of Tutankhamun, Anubis, but you are not aware of that, so you open a pack of beans, and you eat them. While you eat, a voice inside your head tells you to get off the couch...", "You walk swiftly through the antechamber, although you stop to admire one of the spiritual animal couches, the one which belonged to Anubis. This makes Anubis happy. Maybe he will help you later..."], ["1", "2"])
        if x == 0:
            inventory("Food", 1, "lose", True)
            x = choice("""Choices:
1. Ignore the voice and keep on eating, thinking it must be a random thought inside your head.
2. You get off the couch, realizing a God just spoke to you...""", ["You ignore the voice inside your head, and angers Anubis even more. He fires a beam of energy at your supplies, destroying all your tools and food, and he grants the beans that you just ate with powers. The beans burst out of your belly, causing many holes inside you.", "You get off the couch, but this doesn't make Anubis any happier. He decides to let you go for now, until you do something else to anger him."], ["1", "2"])
            if x == 0:
                ending("The turns have tabled", 8, "tomb")
                addachievement('Killed By [Anubis]')
            else:
                x = choice("""Choices:
1. You abandon your food, having lost your appetite, and you make for the burial chamber.							
2. You decide to go to the Annexe to find some utensils to finish your meal, as you are still hungry.""", ["When you enter the burial chamber, you notice that the coffin is sealed with magical markings, but you fail to notice the mummy behind the tomb staring at you, until it slashes your neck with an ancient weapon.", "You go into the annexe, and you spot some utensils with Anubis's marking on them. Without thinking, you scoop up some more of your beans and eat them. This angers Anubis even more, so he sends a blast of energy right at your face."], ["1", "2"])
                if x == 0:
                    ending("So close but so far...", 9, "tomb")
                    addachievement('I Want My Mummy!')
                else:
                    ending("Deep Fried", 10, "tomb")
                    addachievement('Killed By [Anubis]')
        else:
            x = choice("""Choices:
1. Continue into the annexe.
2. Go straight to the Burial Chamber, because anything inside the annexe won't be useful.""", ["You go to the annexe, and you spot utensils with Anubis's marking on them. You pick these up to admire.", "You go straight to the burial chamber of Tutankhamun and find the coffin tightly sealed with magical markings. You then spot another mummy standing behind the coffin, looking at you without its malicious eyes."], ["1", "2"])
            if x == 0:
                x = choice("""Choices:
1. Knowing these will be valuable, you pick them up and put them in your bag
2. You think that if you keep these, Anubis might get mad at you, so you put them safely on a stand.""", ["You put the utensils carefully into your bag, and you cross over to the burial chamber. The coffin is sealed with magical markings, so you ask Anubis how to open it. All this time you fail to notice the mummy behind you. It taps you on the shoulder, and you spin around with your metal rod in hand, but this time the mummy dodges your attack and slashes your neck.", "9d. You carefully set the utensils on the stand, making Anubis twice as happy with you! You cross over to the burial chamber, and you see the coffin sealed with magic. You also notice the mummy standing behind it."], ["1", "2"])
                if x == 0:
                    ending("Beheaded", 11, "tomb")
                    addachievement('I Want My Mummy!')
                else:
                    x = choice("""Choices:
1. You ask Anubis to open the coffin while you take care of the mummy.
2. You ask Anubis to take care of the mummy while you try to open the coffin.
3. ??? (mystery)""", ["Anubis slowly works undoing the magical binding on the coffin's lid, while you pull out your weapon and kill the mummy. But this time the mummy knows how to beat you. It dodges your first attack and slashes your neck.", "Anubis sends a beam of energy at the mummy, sending it flying, and it stops moving. You get to work on figuring out the magical binding, but you accidentally say the wrong hieroglyph and the coffin fires a magic bolt at your face.", "You remember that Anubis now owes you two favours, so you ask him to kill the mummy and unlock the coffin. Hearing your request, Anubis zaps the mummy and unlocks the coffin, revealing the mummified Tutankhamun and countless valuables."], ["1", "2", "3"]) # continue
                    if x == 0:
                        ending("At least you tried...", 12, "tomb")
                        addachievement('I Want My Mummy!')
                    elif x == 1:
                        ending("Should've Studied Harder", 13, "tomb")
                    else:
                        x = choice("""Choices:
1. You take all the valuables inside Tutankhamun's coffin and escape from the tomb.
2. Not satisfied, you want to explore the last room inside Tutankhamun's tomb, the treasury.""", ["You pick up all the gold bracelets, masks and other valuables inside Tutankhamun's coffin, admiring each and every carving on them. You quickly put them in your bag and retrace your steps out of the tomb. You reach daylight again, and you heave a sigh of relief, having completed your most dangerous heist yet.", "You turn to your right to face the treasury of Tutankhamun's tomb, which must contain a huge amount of treasure. Excited, you enter the treasury, imagining all the riches that should be inside. But when you open your eyes, instead of treasure, 4 mummies stood there staring at you..."], ["1", "2"])
                        if x == 0:
                            ending("The rich", 14, "tomb", "win")
                            addachievement("The Rich")
                        else:
                            ending("Got too Greedy", 15, "tomb")
                            addachievement('I Want My Mummy!')
            else:
                x = choice("""Choices:
1. Ask Anubis to tell you how to open Tutankhamun's coffin, and deal with the mummy yourself.
2. Ask Anubis to kill the mummy, while you try to open Tutankhamun's coffin.""", ["Anubis slowly works undoing the magical binding on the coffin's lid, while you pull out your weapon and kill the mummy. But this time the mummy knows how to beat you. It dodges your first attack and slashes your neck.", "Anubis sends a beam of energy at the mummy, sending it flying, and it stops moving. You get to work on figuring out the magical binding, but you accidentally say the wrong hieroglyph and the coffin fires a magic bolt at your face."], ["1", "2"])
                if x == 0:
                    ending("At least you tried...", 12, "tomb")
                    addachievement('I Want My Mummy!')
                else:
                    ending("Should've Studied Harder", 13, "tomb")

# LEVI - MOUNTAIN
def story_mountain():
    print('You are an experienced mountain climber. You are about to go on your greatest adventure yet, climbing Mt Everest.')
    c = choice("""Who will you go with? 
Derek: Your best friend since 5th grade. You know him best, but it is his first time.
William: A professional climber that has been climbing since 1994. He is experienced and has all the gear. 
Pat: Your friendly neighborhood postman. A chill dude who is built like a bodybuilder on steroids.""", ['You choose Derek, and he is excited to go with you. You begin your journey up the mountain.', 'You choose William, he firmly shakes your hand and tells you that you are in good hands.', 'You choose Pat, who almost rips off your arm as he greets you. '], ['Derek', 'William', 'Pat'])
    if c == 0:
        pass
    elif c == 1:
        pass
    elif c == 2:
        pass

# OLIVER - UNDERWATER
def story_underwater():
    pass

# GAME LOOP
while True:
    user = user_system()
    if user != "":
        endings, userach, usercommands, fails, wins = grab_stats(user)
    running_commands = True
    while running_commands:
        print("")
        checkcommand(input("Enter a command ('Help' for options) > "))
        if not user == "":
            update_stats(user)
            checkachievements()
            update_stats(user)