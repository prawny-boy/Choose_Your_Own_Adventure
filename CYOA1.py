# VERSION 1.0
# - 1st Story
# - Functions
# - Quitting
# - Endings
# - Inventory

# imports
import sys
from termcolor import cprint, colored
import pygame
import random

# introduction
print("""Choose your own adventure
 ____    ____
/ ___|  / __ \    Corporation
\___ \ | /  \ |   Inc.
 ___) || \__/ |
|____/  \____/""")

# variables & lists
running = True
answer = False
inventoryList = []
autovillage = False
foundpilot = False
end = False

# definitions

def readanswer(answer1, answer2, answer3="\n"):
    global answer
    answer1 = answer1.lower()
    answer2 = answer2.lower()
    answer3 = answer3.lower()
    print("Enter", (answer1 + " or " + answer2) if answer3 == "\n" else (answer1 + ", " + answer2+" or "+answer3))
    answer = input(" > ").lower().strip()
    while (answer != answer1 and answer != answer2 and answer != answer3):
        print("\033[A"+(" "*(len(answer)+15))+"\033[A")
        # print("Invalid. Input either", answer1, "or", answer2 + ".")
        answer = input((" > ")).lower().strip()
        if answer == "quit":
            sys.exit()
        if answer == "i" or answer == "inventory":
            cprint("Inventory:", "green")
            if len(inventoryList) == 0:
                print("Nothing. Get some stuff to see them here.")
            for item in range(len(inventoryList)):
                cprint("  1 " + str(inventoryList[item]), "green")
            print("\n") #hi levi  # hi sean
    print("")

def inventory(addItem, amount=1, type="add"):
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

# STORY

def story_pilot():
    global autovillage
    if not autovillage:
        readanswer('village', 'search', 'stay')
    if answer == 'village' or autovillage:
        print("""You and John both leave the crashed plane and after hours of searching you find a village. As you approach the alarm sounds,
and you are both captured by the native tribe. You are going to be hanged in 2 hours, unless you have something to give.""", end="\n")
        if "Gem" in inventoryList:
            print("""Luckily, you have that gem that you found in the river, so you offer them it. The tribe accepts you and the pilot as a member,
letting you live with them forever. """ + colored("(Ending 1/20 'Accepted into tribe')", "red"))
            inventory("Gem", 1, "lose")
        else:
            print("""Well obviously you didn't have anything because you just crashed in a plane. 
After 2 hours of dread, you and John are hanged. """ + colored("(Ending 2/20 'Hanged')", "red"))
    elif answer == 'stay':
        story_stay()
    else:
        story_search()

def story_search():
    global autovillage, foundpilot
    if foundpilot:
        print("""'Do you know about anything else in the plane?' You ask John. 'Yes there is a wrench and a instruction manual in the glove box'
John replies, taking the things out. He gives them to you. These could be helpful for fixing the plane... Do you want to try fix the plane?""")
    else:
        print("""You continue searching the plane and find a toolbox and a instruction manual for the plane in the glovebox. This may be helpful for fixing the plane...
Do you want to try to fix the plane?""")
    inventory("Toolbox")
    inventory("Instruction Manual")
    readanswer('yes', 'no')
    if answer == 'yes':
        story_fix()
    else:
        print("""You decide against trying to fix the plane. It would be too difficult anyway. Do you want to go to find a village,
or stay?""")
        readanswer("village", "stay")
        if foundpilot:
            if answer == "village":
                autovillage = True
                story_pilot()
            else:
                story_stay()
        else:
            if answer == "village":
                story_town()
            else:
                print("""You get hungry, and have run out of food, so decide to go out to look for some. You stumble in the forest and fall down a cliff.
Maybe look where you step? """ + colored("(Ending 17/20 'Clumsy')", "red"))

def story_stay():
    global autovillage
    print("""You stay at the plane crash site, making a shelter for you and John for the next month. After you run out of food,
you face the options of adventuring into the dangerous forest for food, staying at the shelter to starve, or going to a village.
Which do you choose?""")
    readanswer('forest', 'stay', 'village')
    if answer == 'forest':
        print("""You go into the forest and venture for food. You find mushrooms, but you don't know if they are poisonous. 
After bringing them back to the crash site, you have the following options: go to a village to ask, eat the mushroom, 
or don't eat the mushroom and continue looking for food. Which will you choose?""")
        readanswer('village', 'eat', 'continue')
        if answer == 'village':
            autovillage = True
            story_pilot()
        elif answer == 'eat':
            print("""You decide to eat the mushroom but it ends up being poisonous. Oops! """ + colored("(Ending 4/20 'Poisoned')", "red"))
        else:
            print("""You continue looking but it soon turns night. A flash of bright red fur and a scream from John. Before you can react,
you fall victim to the night creature.""" + colored("(Ending 5/20 'The creature of the night')", "red"))
    elif answer == 'stay':
        print("""You stay at the plane crash without food, but don't last long. """ + colored("(Ending 3/20 'Starved to death')", "red"))
    else:
        autovillage = True
        story_pilot()

def story_fix():
    global end
    if "Toolbox" in inventoryList:
        if not foundpilot:
            print("""Luckily you have a toolbox, which helps you quickly fix the plane in a week. When you are finished, you jump into the pilot seat,
getting ready to escape the forest. Looking at the forest gives you nightmares, so you hurridly start the engine.
But right before you can go a dark animal jumps onto the front window, smashing the glass. Do you want to defend yourself or go and hide?""")
            readanswer("defend", "hide")
            if answer == "defend":
                print("""You collect a pole standing not far off and hit the monster with it. 3 whacks and the monster is gone. Finally, 
you start the engine and go off in the plane, using the instruction manual as a guide. """ + colored("(Ending 14/20 'Defeated a Monster')", "red"))
                end = True
            else:
                print("""Go run to the back of the plane, but the creature follows you, breaking down the door and destroying all your hard work in fixing the plane.
Before you can blink, you are devoured. """ + colored("(Ending 15/20 'So Close, But so devoured')", "red"))
                end = True
        else:
            input("""Luckily you have a toolbox, which helps you quickly fix the plane. Halfway through your engineering process, a high-pitched scream pierces the air.
You run out to see that John has his instruction manual in his hands, but a feral animal is trying to grab it away. (Enter to continue)""")
            if (not "Gem" in inventoryList):
                print("""He stumbles and falls onto the ground, and the animal now procceds to jump on John and tear his flesh. He is long gone.
You go and hide in the plane for several hours, but the dog doesn't do away. You are out of food supplies so you face an option.
Would you go and face the monster or stay and starve?""")
                inventory("Instruction Manual", 1, "lose")
                readanswer('face', 'stay')
                if answer == 'face':
                    print("""You go out to face the monster. You would die anyway, so beter die gloriously. Before you can even glimpse the monster,
you are devoured. I don't think that was so glorious... """ + colored("(Ending 10/20 'A Glorious Death')", "red"))
                    end = True
                else:
                    if random.randint(1,2) == 1:
                        print("""You decide against fighting the monster, which stays there for a very long time, leading you into a slow and painful death. Starvation. """ + colored("(Ending 9/20 'Starvation')", "red"))
                        end = True
                    else:
                        print("""You decide to not fight the monster, and after awhile it wonders away. You sit in the passengers seat and admire your hard work in fixing the plane. 
You start the engine and take off successfully. But suddenly, your plane dips and when you realise you never knew how to drive a plane, you crash. """ + colored("\n(Ending 13/20 'Crashed Again')", "red"))
            else:
                print("""You think fast. Getting the Gem that you found earlier, you wave it in the air, distracing the animal. This successfully distracts the animal,
making it run away, pulling the book away from John's hands and stealing it. At least you saved John...""")
                inventory("Instruction Manual", 1, "lose")
        if not end:
            if foundpilot:
                print("""You sit in the passengers seat and admire your hard work in fixing the plane. John drives the plane away from the forest,
flying back home. """ + colored("(Ending 11/20 'Passenger Escape')", "red"))
            elif "Instruction Manual" in inventoryList:
                print("You read the manual on how to drive the plane"+", letting you fly away safely" if not foundpilot else " remembering John and how he died. You fly away safely. " + colored("\n(Ending 12/20 'Becoming A Pilot')", "red"))
    else:
        print("""You start to try to fix it but you need tools to do it. That's quite sad. I've never heard of someone who has died of boredom,
so I think your're the first one. Good Night. """ + colored("(Ending 16/20 'Died of Boredom')", "red"))

def story_town():
  print("""You go searching for a village, but instead find a very developed town. A nice citizen invites you to stay with him, and you accept.
The citizen hands you a glass of green liquid. Do you want to drink it?""")
  readanswer('yes', 'no')
  if answer == 'yes':
    print("""When you drink the liquid, you pass out and wake up in a jail like cell. You are told that you will be used in an great experiment,
if that is great or not. """ + colored("(Ending 6/20 'Great Experiments')", "red"))
  else:
    print("""You put down the drink and hurridly leave the hut. There's something suspicious about the drink. You decide to start a new life,
by yourself. The town leader sees your intelligence and offers you a job: a town advisor. 
On the other hand, a independent company offers you another path: a secret spy. Which will you take?""")
    readanswer('advisor', 'spy')
    if answer == 'advisor':
      print("""You become an advisor for the town, and earn a lot of money, soon becoming rich. You live a happy life in the town.
""" + colored("(Ending 7/20 'Rich boi')", "red"))
    else:
      print("""You become a spy against the town, but you are not too good at it. After a week, you are caught and sent to jail. 
""" + colored("(Ending 8/20 'Jail Time')", "red"))

def story():
    global foundpilot
    print("")
    print("""You are a passenger heading to Africa on a plane with the name of GT_7. You remember that your mom abandoned you. 
Your life is falling around you, so you decide to move to africa to start a new life. While you are thinking about the latest happenings,
the plane suddenly dips and crashes into the trees. You go unconcious.
  
When you wake up, you remember what happened and wish that you never went to Africa. Do you want to walk to the nearest village?""")
    readanswer('yes', 'no')
    if answer == 'yes':
        story_town()
    else:
        print("""You stand there, aimlessly looking around for something to do. You see your plane a few feet away. 
Do you want to see what is inside?""")
        readanswer('yes', 'no')
        if answer == 'yes':
            print("""You walk towards the plane, opening the door to see the body of your pilot on the seats.
Do you want to check out his body or search the plane further?""")
            readanswer('search', 'check')
            if answer == 'check':
                print("""You climb up to the pilot, over the rubble. You hear hoarse, shallow breaths! He is still alive! 
He opens his eyes and struggles up. 'Wat...er..' he mumbles. Do you want to get him water?""")
                readanswer('yes', 'no')
                if answer == 'yes':
                    print("""You quickly dash out of the plane, looking for any water source. You see a water spring under a rock, 
and a fast flowing river in the distance. Which one do you want to get water from?""")
                    readanswer('spring', 'river')
                    if answer == 'spring':
                        print("""You get water from the spring, rushing back to give it to your pilot. He drinks it and stands up.
'Thanks. By the way my name is John. Where are we?' he questions. 'We are in the amazons', you reply. John then goes into the plane's stores, 
unlocking them to get food. 'There is enough to last for about a month. We can stay here or go to find a village of some sort.' John tells you.
Do you want to go find a village, continue searching in the plane, or stay and build a shelter next to the plane crash?""")
                        foundpilot = True
                        story_pilot()
                    else:
                        print("""You get water from the river, but right as you are about to go you find a cool looking gem in the water.
You pick it up, before rushing back to give it to your pilot. He drinks it and stands up. 'Thanks. By the way my name is John. 
Where are we?' he questions. 'We are in the amazons', you reply. John then goes into the plane's stores, unlocking them to get food. 
'There is enough to last for about a month. We can stay here or go to find a village of some sort.' John tells you.
Do you want to go find a village, continue searching in the plane, or stay and build a shelter next to the plane crash?""")
                        foundpilot = True
                        inventory("Gem")
                        story_pilot()
                else:
                    print("""You decide that you can't be bothered to get water for him. It is his fault that you are in this place anyways.
'Pleas...' the pilot says before coughing harshly then going silent. Now you are alone. Do you want to stay at the plane crash site,
to continue searching the plane, or try to find a village?""")
                    readanswer('search', 'village')
                    if answer == 'search':
                        story_search()
                    else:
                        print("""You go to a village, a big village with... FLOATING ISLANDS? What?! Apparantly this village is very technologically advanced,
so you enter happily. At the gates, a laser (Non-fatal) scans your face and suddenly raises an alarm. The people shout angrily at you, but you don't know what they are saying.
It's only when you are about to be killed by lasers (fatal) that they scold you for not saving an innocent life, the pilot's.
You wish you had saved the pilot and wonder how the people knew as you are burned by the light, over and over again. """ + colored("(Ending 18/20 'Sins Discovered')", "red"))
            else:
                print("""You keep searching, ignoring the pilots body. He's probably dead anyways. You find a locked storing shelf,
but you don't have the key. Do you want to search for the key or give up?""")
                readanswer('search', 'give up')
                if answer == 'search':
                    print("""You go and check in the pilot's pockets and find the key, unlocking the storage. 
Inside the storage is enough food for 2 months. You know that it won't last forever, but finding a village might be very helpful.
What do you want to do?""")
                    readanswer('village', 'stay')
                    if answer == 'village':
                        print("""""")
                    else:
                        print("""You stay at the plane crash site for a month, and start getting bored. Looking at the remains of the plane,
you realise that it is easy to fix, just need to fit the plane wing on. Do you want to fix it?""")
                        readanswer('yes', 'no')
                        if answer == 'yes':
                            story_fix()
                        else:
                            print("""You start getting hungry once your food supply is used up so go searching for food. While wondering you find some conveniently placed food.
"Someone must have left their lunch behind!" you think. Taking the food, you turn back and... SNAP!!! A bear trap catches you. You scream for help,
But after awhile your shouts die down as you lose too much blood. """ + colored("(Ending 19/20 'Tomato Sauce Everywhere')", "red"))
                else:
                    print("""You decide that it will be impossible to find the key. It probably fell off when the plane crashed.
You can either keep searching the plane or go to find a village. Which?""")
                    readanswer('search', 'village')
                    if answer == 'search':
                        story_search()
                    else:
                        story_town()
        else:
            print("""I don't know why you would not want to see what has inside a plane, but ok. You can't survive with nothing so you died. """ + colored("(Ending 20/20 'Bad Choices')", "red"))
    cprint("\nTHE END", attrs=["bold"])

# GAME LOOP (Commands)
def reset():
    global answer, inventoryList, autovillage, foundpilot, end
    answer = False
    inventoryList = []
    autovillage = False
    foundpilot = False
    end = False

def checkcommand():
    global running
    if command == "help":
        print("""List of commands:
  help - brings up this list
  info - shows project info
  start - starts the story
  i - In the story, to see your inventory
  quit - quits the story when in the story, if out of story quits program""")
    elif command == "start":
        reset()
        story()
    elif command == "quit":
        running = False
    elif command == "info":
        print("""Version: 1.0
Made by Sean Chan & Oliver Liu
Written in: Python, VS Code""")
    else: 
        print("That is an invalid command. Try Again.")

#script
while running != False:
    command = input("""\nEnter a command or enter 'help' for a list of available commands.
 > """)
    checkcommand()

sys.exit()
  