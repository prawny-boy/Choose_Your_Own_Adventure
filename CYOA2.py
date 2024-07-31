from termcolor import cprint, colored
from sys import exit
from updates import updates
from random import randint
from time import sleep

# Program preset variables:
yn = ['Y', 'N'] # just for shortcutting
s = 'stats.txt'
inventoryList = []
storyList = ["amazon adventure", '1', "space story", '2', '3', 'time travel', 'school', '4', "tomb story", "5", 'quit']
achievements = { #name: [description, code, class]
    # Special
    # Easter Eggs
    "The Long Egg": ["The Long Egg", "Find the longest Easter Egg in the game.", "egg.long-1", "special"]
}
linesperuser = 5 # lines of stats per 1 user
initialstats = ['Endings: //', 'Achievements: //', 'Fails: /0', 'Wins: /0'] # preset of stats of a new user, / is normal int/str, while // is list

# Stat Variables
user = ""
endings = []
userach = [] # user achievments
fails = 0
wins = 0
eastereggs = []
play = False

def user_system():
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
                for char in newuser:
                    if char in ['!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~']:
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
            file = open(s, 'r')
            content = file.read()
            if ('User: /' + username.lower()) in content:
                file.close()
                print(f"Successfully signed in as {username}.")
                break
            else:
                print("That username doesn't exist in our records. Please try again.")
        if done:
            break
    return username.lower()

def resetstats(user:str):
    # here we edit the stats file and reset everything
    with open(s, 'r') as file:
        lines = file.readlines()
    
    for i in range(len(lines)):
        lines[i] = lines[i].strip() # remove newline characters

    for i in range(len(lines)):
        if lines[i] == "User: /" + user:
            userline = i
            break

    for i in range(userline + 1, userline + linesperuser):
        lines[i] = initialstats[i-(userline+1)]
    
    for i in range(len(lines)):
        lines[i] = lines[i] + "\n" # add newline characters

    with open(s, 'w') as file:
        file.writelines(lines)

def deleteuser(user:str):
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
    
def updateachievements(currentach:list, allach:list):
    # here we check which advancements have been completed using variables
    completedach = []
    keys = list(allach.keys())
    for i in range(len(keys)):
        if checkachievement(allach[keys[i]][2]):
            if not allach[keys[i]][0] in currentach:
                cprint(f"Completed {allach[keys[i]][3]} achievement: {allach[keys[i]][0]}", "yellow")
                completedach.append(allach[keys[i]][0])

    return completedach

def checkachievement(code:str):
    # here we read the endcoding on our achievements
    completed = False
    c = code.split('-')
    n = c[0].split('.')
    name1 = n[0]
    if len(n) > 1:
        name2 = n[1]
    amount = c[1]
    if name1 == "egg":
        if name2 in eastereggs:
            completed = True
    
    return completed

def checkusername(user:str):
    x = ''
    file = open(s, 'r')
    content = file.read()
    if ('User: /' + user.lower()) in content:
        print('Username taken.')
        file.close()
    else:
        print('Username availible.')
        file.close()
        while x.upper() not in yn:
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

def grab_stats(user:str):
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
    return tuple(stats)

def update_stats(user:str):
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
    for i in range(userline+1, linesperuser):
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
        elif "Fails" in line:
            stat = fails
        elif "Wins" in line:
            stat = wins
        
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

def print_stats(user:str, endings:list, achievements:list, fails:int, wins:int):
    cprint(f"{user}'s Stats:", "green", attrs=["bold"])
    cprint("  Endings:", "red")
    # converts the list into a dictionary
    endingsdict = {}
    foundendings = []
    for item in endings:
        itemlist = str(item).split("/")
        if not itemlist[0] in foundendings:
            num = endings.count(item)
            endingsdict[itemlist[0]] = [itemlist[1], num]
            foundendings.append(itemlist[0])

    # prints the stats, sorted with how many times you have gotten it.
    # sorts stats
    endingsdict = dict(sorted(endingsdict.items(), key=lambda x:x[1]))

    # prints stats
    initialstory = ""
    for item in endingsdict.keys():
        if initialstory == "" or initialstory != endingsdict[item][0]:
            print(f"    {endingsdict[item][0]}:")
            initialstory = endingsdict[item][0]
        print(f"      - '{item}' {endingsdict[item][1]} times")

    # try implement type sorting later
    cprint("  Achievements:", "yellow")
    for item in achievements:
        print("    - " + str(item))
    
    # print fails & wins
    cprint(f"  Fails: ", "red", end="")
    print(fails)
    cprint(f"  Wins: ", "green", end="")
    print(wins)

def choice(question:str, outcomes:list, options:list = yn, end:list = []):
    choice = ''
    print(question)
    option = str(options)
    option = option.replace('[', '')
    option = option.replace(']', '')
    option = option.replace("'", '')
    for a in range(0,len(options)):
        options[a] = str(options[a]).lower()
    print('Options: ' + option)
    while True:
        choice = input('Choice: ').lower()
        if choice == "quit":
            exit()
        elif choice in options:
            break
        else:
            print("\033[A"+(" "*(len(choice)+9))+"\033[A")
    for num in range(0,len(options)):
        if choice == str(options[num]):
            x = num
            break
    print("\n" + outcomes[x])
    return x

def inventory(addItem, amount=1, type="add", toggle:bool = True):
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

def ending(name:str, number:int, totalendings:int, story:str, type:str = "fail"):
    global endings
    # end and add it to the endings list
    colour = ""
    if type.lower().strip() == "win":
        colour = "green"
    elif type.lower().strip() == "fail":
        colour = "red"
    cprint(f"(Ending {str(number)}/{str(totalendings)} '{str(name)}')", colour)

    endings.append(name+"/"+story+"/"+type)

def checkcommand(command:str):
    global user, inventoryList, running_commands
    command = command.lower()
    story = ''
    if command == "help":
        print("""List of commands:
  Help - brings up this list
  Start - starts the story selection
  Stats - prints the current user's stats
  Save - saves the user's current stats
  Reset - resets the current user's stats (Dangerous)
  Delete - Deletes the current account, after goes back to sign in (Dangerous)
  Quit - quits the story when in the story, if out of story quits program
  Credits - shows the credits & project info""")
    elif command == "start":
        print("""STORIES:
  1. Amazon Adventure
  2. Space Story
  3. Time Travel
  4. School
  5. Tomb Story""")
        while True:
            story = input('Please select a story: ')
            if story == 'quit':
                exit()
            elif story in storyList:
                break
            else:
                print("That is invalid, enter a story name or the corresponding number to a story.\n")
        inventoryList = []
        if story == "amazon adventure" or story == '1':
            cprint("\nAMAZON ADVENTURE", "green", attrs=["bold"])
            story_african_adventure()
        elif story == "space story" or story == '2':
            cprint("\nSPACE STORY", "purple", attrs=["bold"])
            story_space()
        elif story == "time travel" or story == "3":
            cprint("\nTIME TRAVEL", "yellow", attrs=["bold"])
            story_timetravel()
        elif story == "school" or story == "4":
            cprint("\nSCHOOL - Made By Jayden Li", "yellow", attrs=["bold"])
            story_school(user)
        elif story == "tomb story" or story == "5":
            cprint("\nTutankhamun's Tomb - Made By Ethan Wei", "magenta", attrs=["bold"])
            story_tomb()
    elif command in ["save", "reset", "delete", "stats"]:
        if not user == "":
            if command == "save":
                print("Saving...")
                update_stats(user)
                print("Saved stats successfully.")
            elif command == "reset":
                while True:
                    confirm = input(colored("Are you sure you want to continue? This will reset ALL of your stats. (y/n) ", "red")).upper()
                    if confirm == "Y":
                        resetstats(user)
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
    elif command == "quit":
        exit()
    elif command == 'updates':
        print(updates)
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
Testers: Aaron Zhang, Nelson Yan, Ethan Wei
Story Writers: 
    Amazon Adventure - Sean Chan
    Space Story - Oliver Liu
    Time Travel - Sean Chan
    School - Jayden Li, imported by Oliver Liu
    Tutankhamun's Tomb - Ethan Wei, imported by Sean Chan
------------------------------------------------""")
    elif command == "198234":
        win = False
        answer = input("Question 1/4: How many times did you have to click the flag to win? ").strip()
        if answer == "100":
            answer = input("Question 2/4: How many checkpoints were in the minecraft hunt? ").strip()
            if answer == "10":
                answer = input("Question 3/4: What was the Youtube channel name you were directed to? ").lower().strip()
                if answer == "thebestcoolnelsonyan":
                    answer = input("Question 4/4: What was the third scratch game titled? ").lower().strip()
                    if answer == "special":
                        win = True
        if win:
            print("Success!")
            eastereggs.append("long")
        else:
            print("Wrong. Answer all questions correctly.")

    else: 
        print("That is an invalid command. Try Again.")

# SPACE STORY
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
            c = choice('Everything is out of reach.', ['A piece of space debris hurtles towards you, breaking your visor. Your suit begins to leak oxygen at a rapid pace.'], ['...'])
            
            if c == 0:
                inventory('Oxygen', 5, "lose")#0 oxygen
                print("You died due to lack of oxygen. " + colored("\n(Ending 1/11 'Bye Bye, Spacesuit')", "red"))
                
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
                    print('You fiercely grapple with it, but to no avail. You perish.')
                    print("You died to [Bob the Alien] " + colored(f"\n(Ending 4/11 'Bob the Alien, It Can Kill You!')", "red"))
                    
                elif c == 1:
                    inventory('Oxygen', 1, 'lose')
                    c = choice('The door opens and you find a box of tools. What will you take from it?', ['You take the wrench, which you use to fix the wall panels. The chamber is now sealed.', 'You take the blowtorch, which sets your suit on fire, burning you alive.', 'You take the screwdriver, which allows you to fix the thrusters.'], ['Wrench', 'Blowtorch', 'Screwdriver'])
                    
                    if c == 0:
                        c == choice('Will you take off your helmet?', ['You take it off, but there is not air in the chamber, causing you to suffocate.', "You don't take it off, but now that you are in a sealed chamber the oxygen begins diffusing into the chamber, killing you."])
                        if c == 0:
                            print('You died due to lack of oxygen. ' + colored("(Ending 6/11 'Oopsies')"), 'red')
                        elif c == 1:
                            print('You died due to lack of oxygen. ' + colored("Ending 7/11 'Unlucky :('", 'red'))
                    elif c == 1:
                        print('You died due to fire. ' + colored("(Ending 5/11 'Overheating')", 'red'))
                    elif c == 2:
                        print("""After fixing the thrusters, you jumpstart them using luck.
They roar to life, throwing you back and bringing you back to earth.
""" + colored("(Ending 20/20 'Back to Earth')", 'green'))
                
            elif c == 1:
                inventory('Oxygen', 1, "lose", False) # 0 oxygen
                inventory('Operation Manual', 1, "add")
                print("You died due to lack of oxygen. " + colored("\n(Ending 2/11 'I can operate! But I'm dead...')", "red"))
                
            elif c == 2: 
                print('You got lucky, and found a spare oxygen tank!')
                inventory('Repair Manual', 1, "add", False) # 1 oxygen
                c = choice('Will you fix the ship, or find more oxygen?', ['You try to fix the ship,', 'You go searching, and find 4 tanks inside on the wall.'], ['Fix', 'Search'])

                if c == 0:
                    print('but die due to a lack of oxygen. ' + colored("\n(Ending 3/11 'Fix My Death...')", 'red'))

                elif c == 1:
                    inventory('Oxygen', 3)#4 oxygen
                    c = choice('You see another ship in the distance. Will you go towards it?', ['You go to it, but the Hubble Space Telescope slams into you, killing both of you,', "You don't do anything, which wastes oxygen."])
                    if c == 0: 
                        print("You died to [Hubble Space Telescope]. " + colored("(Ending 9/11 'Hubble Space Skill Issue')", 'red'))
                    elif c == 1:
                        inventory('Oxygen', 2, 'lose')
                        c = choice('Because you wasted time, there is nothing you can do.', [''], ['...'])
                        if c == 0:
                            print('You died due to loss of oxygen. ' + colored("(Ending 10/11 'Timewaster...')", 'red'))
                
    elif c == 1:
        inventory('Oxygen', 1, "lose")#2 oxygen
        c = choice("Will you wake him up, or steal his oxygen?", ['He wakes up, startled. After you explain what is happening, he agrees to help you.', 'You take his oxygen, leaving him to die.'], ['Wake', 'Steal'])
        
        if c == 0:
            inventory('Oxygen', 1, "lose")#1 oxygen
            print('You now lose double oxygen.')
            c = choice('Will you explore the ship?', ['Sadly, while travelling to the ship, you run out of oxygen.'], ['Yes'])
            inventory("Oxygen", 2, 'lose')
            print('You died due to loss of oxygen.' + colored("(Ending 11/11 'We're halfway there...')", 'red'))
            
            
        elif c == 1:
            inventory('Oxygen', 2, "add")#4 oxygen
            c = choice('What to do...', ['You get hit by a meteorite, killing you.'], ['Nothing'])
            print('You died to [Meteorite]. ' + colored("(Ending 8/11 'KARMA')"))
            
    cprint('THE END', attrs=["bold"])

# AFRICAN FOREST
foundpilot = False
end = False

def story_african_adventure_pilot():
    x = choice("Do you want to go find a village, continue searching in the plane, or stay and build a shelter next to the plane crash?", ["You and John both leave the crashed plane and after hours of searching you find a village. As you approach the alarm sounds, and you are both captured by the native tribe. You are going to be hanged in 2 hours, unless you have something to give.", "'Do you know about anything else in the plane?' You ask John. 'Yes there is a wrench and a instruction manual in the glove box' John replies, taking the things out. He gives them to you. These could be helpful for fixing the plane...", "You stay at the plane crash site, making a shelter for you and John for the next month. After you run out of food, you face the option of adventuring into the dangerous forest for food, or staying at the shelter to starve."], ['village', 'search', 'stay'])
    if x == 0:
        if "Gem" in inventoryList:
            print("Luckily, you have that gem that you found in the river, so you offer them it. The tribe accepts you and the pilot as a member, letting you live with them forever." + colored("\n(Ending 1/20 'Accepted into tribe')", "red"))
            inventory("Gem", 1, "lose")
        else:
            print("Well obviously you didn't have anything because you just crashed in a plane. After 2 hours of dread, you and John are hanged. " + colored("\n(Ending 2/20 'Hanged')", "red"))
    elif x == 2:
        x = choice("Which do you choose?", ["You go into the forest and venture for food. You find mushrooms, but you don't know if they are poisonous. After bringing them back to the crash site, you face the decision: eating the mushroom, or not eating the mushroom and to continue looking for food.", "You stay at the plane crash without food, but don't last long. " + colored("\n(Ending 3/20 'Starved to death')", "red")], ['forest', 'stay'])
        if x == 0:
            x = choice("Which will you choose?", ["You decide to eat the mushroom but it ends up being poisonous. Oops! """ + colored("\n(Ending 4/20 'Poisoned')", "red"), "You continue looking but it soon turns night. A flash of bright red fur and a scream from John. Before you can react, you fall victim to the night creature.""" + colored("\n(Ending 5/20 'The creature of the night')", "red")], ['eat', 'continue'])
    else:
        story_african_adventure_search()

def story_african_adventure_search():
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
        story_african_adventure_fix()
    else:
        if foundpilot:
            print("After awhile, You and John get hungry, and have run out of food, so decide to go out to look for some. You both stumble in the forest and fall down a cliff. Maybe look where you step?" + colored("\n(Ending 17/20 Alternative 'Clumsy Buddies')", "red"))
        else:
            print("After awhile, You get hungry, and have run out of food, so decide to go out to look for some. You stumble in the forest and fall down a cliff. Maybe look where you step?" + colored("\n(Ending 17/20 'Clumsy')", "red"))

def story_african_adventure_fix():
    global end, foundpilot
    if "Toolbox" in inventoryList:
        if not foundpilot:
            print("""When you are finished, you jump into the pilot seat, getting ready to escape the forest. Looking at the forest gives you nightmares, so you hurridly start the engine. But right before you can go a dark animal jumps onto the front window, smashing the glass.""")
            choice("Do you want to defend yourself or go and hide?", ["You collect a pole standing not far off and hit the monster with it. 3 whacks and the monster is gone. Finally, you start the engine and go off in the plane, using the instruction manual as a guide. """ + colored("\n(Ending 14/20 'Defeated a Monster')", "red"), "Go run to the back of the plane, but the creature follows you, breaking down the door and destroying all your hard work in fixing the plane. Before you can blink, you are devoured. """ + colored("\n(Ending 15/20 'So Close, But so devoured')", "red")], ["defend", "hide"])
            end = True
        else:
            input("""Halfway through your engineering process, a high-pitched scream pierces the air. You run out to see that John has his instruction manual in his hands, but a feral animal is trying to grab it away. (Enter to continue)""")
            if (not "Gem" in inventoryList):
                print("""He stumbles and falls onto the ground, and the animal now procceds to jump on John and tear his flesh. He is long gone. You go and hide in the plane for several hours, but the dog doesn't do away. You are out of food supplies so you face an option.""")
                inventory("Instruction Manual", 1, "lose")
                foundpilot = False
                choice("Would you go and face the monster or stay and starve?", ["You go out to face the monster. You would die anyway, so beter die gloriously. Before you can even glimpse the monster, you are devoured. I don't think that was so glorious... " + colored("\n(Ending 10/20 'Not A Glorious Death')", "red"), ("You decide against fighting the monster, which stays there for a very long time, leading you into a slow and painful death. Starvation." + colored("\n(Ending 9/20 'Starvation')", "red")) if randint(0, 1) == 0 else ("You decide to not fight the monster, and after awhile it wonders away. You sit in the pilot's seat and admire your hard work in fixing the plane. You start the engine and take off successfully. But suddenly, your plane dips and when you realise you never knew how to drive a plane, you crash." + colored("\n(Ending 13/20 'Crashed Again')", "red"))], ['face', 'stay'])
                end = True
            else:
                print("""You think fast. Getting the Gem that you found earlier, you wave it in the air, distracing the animal. This successfully distracts the animal,
making it run away, pulling the book away from John's hands and stealing it. At least you saved John...""")
                inventory("Instruction Manual", 1, "lose")
        if not end:
            print("""You sit in the passengers seat and admire your hard work in fixing the plane. John drives the plane away from the forest,
flying back home. """ + colored("(Ending 11/20 'Passenger Escape')", "red"))
    
def story_african_adventure():
    global foundpilot
    print("""\nYou are a passenger heading to Africa on a plane. You remember that you went bankrupt after losing while gambling. 
Your life is falling around you, so you decide to move to Africa to start a new life. While you are thinking about the latest happenings,
the plane suddenly dips and crashes into the trees. You go unconcious. 

When you wake up, you remember what happened and wish that you never went to Africa.""")
    x = choice("Do you want to walk to find the nearest village?", ["You go searching for a village, but instead find a very developed town. A nice citizen invites you to stay with him, and you accept. The citizen hands you a glass of green liquid.", "You stand there, aimlessly looking around for something to do. You see your plane a few feet away."])
    if x == 0:
        x = choice("Do you want to drink it?", ["When you drink the liquid, you pass out and wake up in a jail like cell. You are told that you will be used in an great experiment, if that is great or not. " + colored("\n(Ending 6/20 'Great Experiments')", "red"), "You put down the drink and hurridly leave the hut. There's something suspicious about the drink. You decide to start a new life, by yourself. The town leader sees your intelligence and offers you a job: a town advisor. On the other hand, a independent company offers you another path: a secret spy."])
        if x == 1:
            x = choice("Which will you take?", ["You become an advisor for the town, and earn a lot of money, soon becoming rich. You live a happy life in the town." + colored("\n(Ending 7/20 'Rich boi')", "red"), "You become a spy against the town, but you are not too good at it. After a week, you are caught and sent to jail." + colored("\n(Ending 8/20 'Jail Time')", "red")], ["advisor", "spy"])
    else:
        x = choice("Do you want to see what is inside?", ["You walk towards the plane, opening the door to see the body of your pilot on the seats.", "I don't know why you would not want to see what has inside a plane, but ok. You can't survive with nothing so you died. """ + colored("\n(Ending 20/20 'Bad Choices')", "red")])
        if x == 0:
            x = choice("Do you want to check out his body or search the plane further?", ["You climb up to the pilot, over the rubble. You hear hoarse, shallow breaths! He is still alive! He opens his eyes and struggles up. 'Wat...er..' he mumbles.", "You keep searching, ignoring the pilots body. He's probably dead anyways. You find a locked storing shelf, but you don't have the key."], ["check", "search"])
            if x == 0:
                x = choice("Do you want to get him water?", ["You quickly dash out of the plane, looking for any water source. You see a water spring under a rock, and a fast flowing river in the distance.", "You decide that you can't be bothered to get water for him. It is his fault that you are in this place anyways. 'Please...' the pilot says before coughing harshly then going silent. Now you are alone."])
                if x == 0:
                    x = choice("Which one do you want to get water from?", ["You get water from the spring, rushing back to give it to your pilot. He drinks it and stands up. 'Thanks. By the way my name is John. Where are we?' he questions. 'We are in the amazons', you reply. John then goes into the plane's stores, unlocking them to get food. 'There is enough to last for about a month. We can stay here or go to find a village of some sort.' John tells you.", "You get water from the river, but right as you are about to go you find a cool looking gem in the water. You pick it up, before rushing back to give it to your pilot. He drinks it and stands up. 'Thanks. By the way my name is John. Where are we?' he questions. 'We are in the amazons', you reply. John then goes into the plane's stores, unlocking them to get food. 'There is enough to last for about a month. We can stay here or go to find a village of some sort.' John tells you."], ["spring", "river"])
                    if x == 0:
                        foundpilot = True
                        story_african_adventure_pilot()
                    else:
                        foundpilot = True
                        inventory("Gem")
                        story_african_adventure_pilot()
                else:
                    x = choice("Do you want to continue searching the plane, or try to find a village?", ["", "You go to a village, a big village with... FLOATING ISLANDS? What?! Apparantly this village is very technologically advanced, so you enter happily. At the gates, a laser (Non-fatal) scans your face and suddenly raises an alarm. The people shout angrily at you, but you don't know what they are saying. It's only when you are about to be killed by lasers (fatal) that they scold you for not saving an innocent life, the pilot's. You wish you had saved the pilot and wonder how the people knew as you are burned by the light, over and over again." + colored("\n(Ending 18/20 'Sins Discovered')", "red")], ["search", "village"])
                    if x == 0:
                        print("You search the plane and find a toolbox and instruction manual. This may be helpful in fixing the plane...")
                        story_african_adventure_search()
            else:
                x = choice("Do you want to search for the key?", ["You go and check in the pilot's pockets and find the key, unlocking the storage. Inside the storage is enough food for 2 months. You know that it won't last forever, but finding more food might be very good.", ""])
                if x == 0:
                    x = choice("What do you want to do?", ["You start looking for food but stumble upon a hidden mole-made hole. For some odd reason, you can't get out, so you starve to death." + colored("\n(Ending 12/20 'A Hole By A Mole')", "red"), "You stay at the plane crash site for a month, and start getting bored. Looking at the remains of the plane, you realise that it is easy to fix, by fitting the plane wing on."], ['food', 'stay'])
                    if x == 1:
                        x = choice("Do you want to fix it?", ["You start to try to fix it but you need tools to do it. That's quite sad. I've never heard of someone who has died of boredom, so I think your're the first one. Good Night." + colored("\n(Ending 16/20 'Died of Boredom')", "red"), "You start getting hungry once your food supply is used up so go searching for food. While wondering you find some conveniently placed food. 'Someone must have left their lunch behind!' you think. Taking the food, you turn back and... SNAP!!! A bear trap catches you. You scream for help, But after awhile your shouts die down as you lose too much blood." + colored("\n(Ending 19/20 'Tomato Sauce Everywhere')", "red")])
                else:
                    print("You decide that it will be impossible to find the key. It probably fell off when the plane crashed.")
                    story_african_adventure_search()

    cprint("\nTHE END", attrs=["bold"])

# TIME TRAVEL
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
                ending("Destroyed by a Baby", 1, 20, "time travel")
            elif x == 1:
                ending("Squished", 2, 20, "time travel")
            elif x == 2:
                ending("Stuck with the dinosaurs", 3, 20, "time travel")
        else:
            x = choice("Do you want to go to it?", ["You hop into your time machine box thing, looking at the last time you will see the dinosaurs.", "The machine get fried as a fire-breathing dinosaur blows on it. I guess you are stuck in the past..."])
            if x == 0:
                pass
                # some new time
            else:
                ending("Burnt with the dinosaurs", 3, 20, "time travel") # add alternative option
    else:
        x = choice("Do you want to pick the berries then eat it, just pick the berries for later, or no berries?", ["", "", ""], ["eat", "pick", "no"])
        # finish
    
    cprint("\nTHE END", attrs=['bold'])

# JAYDEN - SCHOOL STORY
def story_school(user:str):
    global name, o, hass, math, eng
    if user.lower() == 'pancake' or user.lower() == 'ethan':
        name = 'Ethan Wei'
        o = ' (still no girlfriend though)'
    else:
        name = 'Eefen Wedge'
        o = ''
    while True:
        hass = input('HASS Teacher: ')
        if 'mr' in hass.lower() or 'mrs' in hass.lower():
            break
    while True:
        math = input('Math Teacher: ')
        if 'mr' in math.lower() or 'mrs' in math.lower() or 'dr' in math.lower():
            break
    while True:
        eng = input('English Teacher: ')
        if 'mr' in eng.lower() or 'mrs' in eng.lower() or 'ms' in eng.lower():
            break
    print(f"""You start the school year, fresh and ready. You got new shoes, new laptop and hopefully a new start.
As you get on the train, you notice that your best friend {name} isn’t there, and he isn’t responding to your messages, which is a bit weird but then again, {name} is weird, so you don’t worry too much. 
When you get to Leederville station, you realise that there are no students around you. Feeling uneasy, you walk into school, hoping that this is all just a coincidence…
""")
    cprint("\nYEAR 8 SURVIVOR SIMULATOR", color='red', attrs=['bold'])
    c = choice('Will you enter?', [f'You press the button, and are sucked into the game. Your friend {name} joins you too.', 'You continue on your way to school, and have a normal school year.'])
    if c == 0:
        print("As soon as you walk into the school, you hear a swish behind you, and then a man (whose face you can’t see because that’s plot armour) does an evil laugh. He explains to you that one by one, he is luring students back to school one by one so that they all fall victim to ligma. ")
        c = choice('''You have 3 options:
1. Ask him about ligma
2. Tell him about off and away policy
3. Chuck your phone and run
What will you do?''', ['You instantly fail, as the man clicks his fingers, and the world goes dark.', 'You instantly fail, as the man clicks his fingers, and the world goes dark.', """As you bolt away, across the oval, the man laughs again, says “excellent. A worthy subject.” Then vanishes into thin air, as darkness eats up the sky, and your vision goes blurry. You stumble into Mills and pass out. Let the trials begin."""], ['Ligma?', 'Off and Away', 'Phone'])
        if c == 0:
            cprint('FAIL', attrs=['bold'], color='red')
            ending('LIGMA BALLS', 2, 20, 'School')
        elif c == 1:
            cprint('FAIL', attrs=['bold'], color='red')
            ending('Turned off...', 3, 20, 'School')
        elif c == 2:
            c = choice(f"""You wake up to find your best friend {name} standing over you. He explains that he faked his own death to escape from the man, who he calls “The Ligma Lord”.
The Ligma Lord has taken control of most of the students and planning to use them for world domination. 
{name} explains the school has become a hunting ground for the ligma-ed students to hunt down the remaining ones, and that no-one can leave school.
He says he thinks he has been here for 3 days, but he can’t be sure. As soon as he says that Ligma-ed students start using Pythagoras to calculate where to attack them.
You and {name} start running for the door, when the air vent crashes open with Nelson Yan tumbling out, tackling {name} to the ground, 
causing {name} to scream loudly. You pause, considering what to do.""", [f"You run for the exit, as {name} uses his plot armour to shield you from the Ligma Zombies, sacrificing himself. Mills Building Entrance crumbles, allowing you to burst into the fresh air.", "You Blast “Never Gonna Give You Up” out of your speakers, vaporising the Ligma Zombies. But unfortunately, you didn’t wear earplugs, and your eardrums explode, causing you to pass out, and fall victim to Ligma.", "The Foam in the Fire Extinguisher has the chemical properties to turn the ligma-ed students into healed Perth mod Students. Just as you think you have saved everyone, The Ligma Lord appears, and uses his Blooket Dark Energy, which traps you, as you are transported into the dark realm."], [f'Ditch {name}', 'Go back', 'Fire Extinguisher'])
            if c == 0:
                pass #unfinished
            elif c == 1:
                cprint('FAIL', attrs=['bold'], color='red')
                ending('Rick Astley let you down...', 4, 20, 'School')
            elif c == 2:
                inventory('Fire Extinguisher', 1, 'add')
                print('''You Find Yourself on a Ghostly platform, on top of dark clouds, and directly in front of you is the Ligma Lord. 
He reveals his face, turning out to be no other than Mr McMahon He laughs, saying that he always appears as the person who you fear the most. 
He says that He is fear itself, and that fear will eventually conquer everything. His Voice darkens as he says that You have found his one weakness, 
and he has decided that you will be the first victim of the war.

BUT!!!

Because he was yapping for six billion years, that gave you the chance to reach into your bag and choose a weapon.''')
                #add achievement (fight a god with your school bag.)
                c = choice('Choose your weapon: ', ['You summon your inner Kendrick Lamar and start roasting him. It seems to be working, as he catches on fire until your laptops battery dies. Ligma Lord recovers, then blasts your body into ashes.', 'As You find the Formula to solving any immortal, Mr White randomly spawns and says to use the formula you must solve this quadratic equation. While You are figuring it out, Ligma Lord Burns your maths notebook, and then opens a black hole that destroys you immediately.', 'You pitch the mochi and it lands perfectly into his throat. As he is choking, you grab your empty fire extinguisher and slam it at him, causing him to fall. As you stand over his helpless body, he whispers some final words.', 'You make a mad dash into for the portal, and plunge through, but you hear Ligma Lord laugh as you burst into the fresh air.'], ['Laptop', 'Math Book', 'Mochi', "Portal"])

                if c == 0:
                    cprint('FAIL', attrs=['bold'], color='red')
                    ending('Does anyone have a charger?', 5, 20, 'School')
                elif c == 1:
                    cprint('FAIL', attrs=['bold'], color='red')
                    ending('Mr White gave me a B for Maths...', 6, 20, 'School')
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
                    print('Ligma Lord: I’m sorry...')
                    sleep(1)
                    print('''As the Ligma Lord vanishes, you pick up your school bag, and bow your head in silence, 
then take a deep breath, and slowly walk towards the brightening portal. 
You take one last look behind you, to see the platform and clouds turn into a stream of light, 
then step through the portal, awaiting your first day of school.''')
                    ending('Master of Fear', 7, 20, 'School', 'win')
                elif c == 3:
                    pass

    elif c == 1:
        print(f'You live a normal life {o}.')
        ending('Still Here...', 1, 20, 'School', 'win')
    
    cprint("\nTHE END", attrs=['bold'])

# ETHAN - TUTANKHAMUN'S TOMB
def story_tomb():
    print("""You are a tomb explorer that explores ancient tombs. You recently decided to explore Tutankhamun's tomb. You took a plane over to Egypt, but while flying over Tutankhamun’s tomb, the plane suddenly spluttered and crashed. You were flung out of the plane and landed near the tomb. You land without any food or water, but you have all the tools you need.""")
    x = choice("""Choices:
1. You can explore the tomb without any food or water
2. Leave exploring the tomb for later, and search for food and water in the plane’s wreckage""", ["You pick up all of your tools, and slowly walk towards the tomb’s entrance. You dust the sand away from the tomb entrance, and some of the sand gets blown into your face and up your nose, choking you. You have no water to clear your throat, so you suffocate.", "You walk towards the plane wreckage and discover that everyone inside the plane got burnt alive from the fire. You carefully walk into the plane’s storage unit from a side door and haul out a box of food and water. After walking out the plane, you discover the captain of the plane is still alive, but badly injured. He asks for food and water."], ["1", "2"])
    if x == 0:
        ending("Bad Choices", 1, 15, "tomb")
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
1. You grab onto the captain’s hand and run from the mummy, but the captain slows you down.
2. You choose to save yourself, so you push the captain towards the mummy, and you run.""", ["As you run, you hear the mummy slowly gaining on you. The captain is slowing you down and there is no hope for you and the captain, you are both doomed.", "You push the captain towards the mummy and run. The captain screams at you, but that is suddenly cut short. You run quickly out of the tomb. You feel bad, and that you are going to be haunted about what happened for the rest of your life, but at least you stayed alive."], ["1", "2"])
                if x == 0:
                    ending("Infinitely Doomed", 3, 15, "tomb")
                else:
                    ending("Sacrifices must be made", 4, 15, "tomb")
            else:
                x = choice("""Choices:
1. Stay and fight the mummy with the metal rod at the bottom of your backpack.
2. Run.""", ["You reach inside your bag, and you fumble for the metal rod, but it is hooked on something. The mummy jumps on top of you, and the bag tumbles out of your reach. You close your eyes for the inevitable.", "You turn around and run, and you hear the mummy’s footsteps slowly fading away. You make it out alive, but you are traumatized forever."], ["1", "2"])
                if x == 0:
                    ending("R.I.P", 5, 15, "tomb")
                else:
                    ending("Mentally unstable... womp womp", 6, 15, "tomb")
        elif x == 1:
            print("\nAfter entering the tomb, you slowly walk down the corridor, wary of any traps or ambushes from the undead. You reach inside your bag to get a flashlight, but you hear a footstep coming from ahead.")
            x = choice("""Choices:
1. You pull out your metal rod and wait for whatever it is ahead to show itself.
2. You pull out your metal rod and hide in a gap in the wall and wait for whatever it is to go away.
3. Run.""", ["You hold your weapon in one hand, and you prepare for whatever is coming towards you. The mummy appears much closer than you expected, but you still whack it on its head multiple times until it finally falls at your feet.", "You take out your metal rod and hide in the gap in the wall. The mummy walks right past you, and you let out the breath you were holding. You sneak behind the mummy and knock its head off.", "You turn around and run, and you hear the mummy’s footsteps slowly fading away. You make it out alive, but you are traumatized forever."], ["1", "2", "3"])
            if x == 0:
                story_tomb_passageway()
            elif x == 1:
                story_tomb_passageway()
            else:
                ending("Mentally unstable... womp womp", 6, 15, "tomb")
        else:
            ending("A Good Citizen", 2, 15, "tomb", "win")

def story_tomb_passageway():
    x = choice("""Choices:
1. Continue down the passageway into the antechamber as fast as possible, before any other mummies appear.
2. Advance slowly, checking for any traps.""", ["You sprint down the passageway, but you catch your foot on a tripwire, and you fall flat on your face. You land on a mound of sand, and a mummy jumps right on top of you. It pushes you further into the sand, and you choke on the sand that gets in your mouth and down your throat.", "You get out your flashlight, and you slowly walk forward, scanning the wall and floor for any traps. You avoid a tripwire, and with some luck you step over the pressure plate. You make it to the door of the antechamber."], ["1", "2"])
    if x == 0:
        ending("5-Star Meal", 7, 15, "tomb")
    else: 
        x = choice("""Choices:
1. Go into the antechamber and eat some of the food inside your bag, so you can restore some energy.
2. Walk through the antechamber without stopping, because there might be traps""", ["You open the door of the antechamber, and you sit on the closest spiritual animal couch. This angers the God of Tutankhamun, Anubis, but you are not aware of that, so you open a pack of beans, and you eat them. While you eat, a voice inside your head tells you to get off the couch...", "You walk swiftly through the antechamber, although you stop to admire one of the spiritual animal couches, the one which belonged to Anubis. This makes Anubis happy. Maybe he will help you later..."], ["1", "2"])
        if x == 0:
            inventory("Food", 1, "lose", True)
            x = choice("""Choices:
1. Ignore the voice and keep on eating, thinking it must be a random thought inside your head.
2. You get off the couch, realizing a God just spoke to you...""", ["You ignore the voice inside your head, and angers Anubis even more. He fires a beam of energy at your supplies, destroying all your tools and food, and he grants the beans that you just ate with powers. The beans burst out of your belly, causing many holes inside you.", "You get off the couch, but this doesn’t make Anubis any happier. He decides to let you go for now, until you do something else to anger him."], ["1", "2"])
            if x == 0:
                ending("The turns have tabled", 8, 15, "tomb")
            else:
                x = choice("""Choices:
1. You abandon your food, having lost your appetite, and you make for the burial chamber.							
2. You decide to go to the Annexe to find some utensils to finish your meal, as you are still hungry.""", ["When you enter the burial chamber, you notice that the coffin is sealed with magical markings, but you fail to notice the mummy behind the tomb staring at you, until it slashes your neck with an ancient weapon.", "You go into the annexe, and you spot some utensils with Anubis’s marking on them. Without thinking, you scoop up some more of your beans and eat them. This angers Anubis even more, so he sends a blast of energy right at your face."], ["1", "2"])
                if x == 0:
                    ending("So close but so far...", 9, 15, "tomb")
                else:
                    ending("Deep Fried", 10, 15, "tomb")
        else:
            x = choice("""Choices:
1. Continue into the annexe.
2. Go straight to the Burial Chamber, because anything inside the annexe won’t be useful.""", ["You go to the annexe, and you spot utensils with Anubis’s marking on them. You pick these up to admire.", "You go straight to the burial chamber of Tutankhamun and find the coffin tightly sealed with magical markings. You then spot another mummy standing behind the coffin, looking at you without its malicious eyes."], ["1", "2"])
            if x == 0:
                x = choice("""Choices:
1. Knowing these will be valuable, you pick them up and put them in your bag
2. You think that if you keep these, Anubis might get mad at you, so you put them safely on a stand.""", ["You put the utensils carefully into your bag, and you cross over to the burial chamber. The coffin is sealed with magical markings, so you ask Anubis how to open it. All this time you fail to notice the mummy behind you. It taps you on the shoulder, and you spin around with your metal rod in hand, but this time the mummy dodges your attack and slashes your neck.", "9d. You carefully set the utensils on the stand, making Anubis twice as happy with you! You cross over to the burial chamber, and you see the coffin sealed with magic. You also notice the mummy standing behind it."], ["1", "2"])
                if x == 0:
                    ending("Beheaded", 11, 15, "tomb")
                else:
                    x = choice("""Choices:
1. You ask Anubis to open the coffin while you take care of the mummy.
2. You ask Anubis to take care of the mummy while you try to open the coffin.
3. ??? (mystery)""", ["Anubis slowly works undoing the magical binding on the coffin’s lid, while you pull out your weapon and kill the mummy. But this time the mummy knows how to beat you. It dodges your first attack and slashes your neck.", "Anubis sends a beam of energy at the mummy, sending it flying, and it stops moving. You get to work on figuring out the magical binding, but you accidentally say the wrong hieroglyph and the coffin fires a magic bolt at your face.", "You remember that Anubis now owes you two favours, so you ask him to kill the mummy and unlock the coffin. Hearing your request, Anubis zaps the mummy and unlocks the coffin, revealing the mummified Tutankhamun and countless valuables."], ["1", "2", "3"]) # continue
                    if x == 0:
                        ending("At least you tried...", 12, 15, "tomb")
                    elif x == 1:
                        ending("Should've Studied Harder", 13, 15, "tomb")
                    else:
                        x = choice("""Choices:
1. You take all the valuables inside Tutankhamun’s coffin and escape from the tomb.
2. Not satisfied, you want to explore the last room inside Tutankhamun’s tomb, the treasury.""", ["You pick up all the gold bracelets, masks and other valuables inside Tutankhamun’s coffin, admiring each and every carving on them. You quickly put them in your bag and retrace your steps out of the tomb. You reach daylight again, and you heave a sigh of relief, having completed your most dangerous heist yet.", "You turn to your right to face the treasury of Tutankhamun’s tomb, which must contain a huge amount of treasure. Excited, you enter the treasury, imagining all the riches that should be inside. But when you open your eyes, instead of treasure, 4 mummies stood there staring at you..."], ["1", "2"])
                        if x == 0:
                            ending("The rich", 14, 15, "tomb", "win")
                        else:
                            ending("Got too Greedy", 15, 15, "tomb")
            else:
                x = choice("""Choices:
1. Ask Anubis to tell you how to open Tutankhamun’s coffin, and deal with the mummy yourself.
2. Ask Anubis to kill the mummy, while you try to open Tutankhamun’s coffin.""", ["Anubis slowly works undoing the magical binding on the coffin’s lid, while you pull out your weapon and kill the mummy. But this time the mummy knows how to beat you. It dodges your first attack and slashes your neck.", "Anubis sends a beam of energy at the mummy, sending it flying, and it stops moving. You get to work on figuring out the magical binding, but you accidentally say the wrong hieroglyph and the coffin fires a magic bolt at your face."], ["1", "2"])
                if x == 0:
                    ending("At least you tried...", 12, 15, "tomb")
                else:
                    ending("Should've Studied Harder", 13, 15, "tomb")

# GAME LOOP
while True:
    user = user_system()
    if user != "":
        endings, userach, fails, wins = grab_stats(user)
    running_commands = True
    while running_commands:
        print("")
        checkcommand(input("Enter a command ('Help' for options) > "))
        if not user == "":
            userach = updateachievements(userach, achievements)
            update_stats(user)