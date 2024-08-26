# Amazon Jungle
amazon = {
    'Keep the Gem': ['Finish the story still with a gem in your inventory'],
    'Pilot Buddy': ['Win the story with the pilot still with you'],
    'Die of Boredom': ['Get the ending: Died of Boredom'],
    'Bad Choices': ['Get the ending: Bad choices'],
    "Escape of the Jungle": ['Win Amazon Jungle'],
    'Again?!': ['Get the ending: Crashed again'],
    # Standard Achievements
    'Beginner Jungle': ['Play this story 1 time', 'amazon jungle.play-1'],
    'Intermediate Jungle': ['Play this story 10 times', 'amazon jungle.play-10'],
    'Advanced Jungle': ['Play this story 50 times', 'amazon jungle.play-50'],
    'All Endings [Amazon Jungle]': ["Get all the endings in Amazon Jungle", 'amazon jungle.allendings-1'],
}

# Space Story
space = {
    "Bob the Alien": ['Die to Bob the Alien'],
    "How did we get back?": ["Win Space Story"],
    "Hubble Space Skill Issue": ['Die to the Hubble Space Telescope'], 
    "Flamed": ['Die to Fire'],
    # Standard Achievements
    'Beginner space': ['Play this story 1 time', 'space story.play-1'],
    'Intermediate space': ['Play this story 10 times', 'space story.play-10'],
    'Advanced space': ['Play this story 50 times', 'space story.play-50'],
    'All Endings [Space Story]': ["Get all the endings in Space Story", 'space story.allendings-1'],
}

# Time Travel
time = {
    "Lumberjacked": ["Get your head chopped off by an axe."],
    'Bonker': ["Use The Bonker"], # not added
    'Bonked': ["Get Bonked by the Bonker"], # not added
    'Bad Choices': ["Get the ending: bad choices"],
    "Back to reality": ["Win Time Travel"],
    "Finding Gold": ["Find gold"],
    "The Future is Bright": ["Save the future and win"],
    # Standard Achievements
    'Time Traveller': ['Play this story 1 time', 'time travel.play-1'],
    'Better Time Traveller': ['Play this story 10 times', 'time travel.play-10'],
    'Doctor Who': ['Play this story 50 times', 'time travel.play-50'],
    'All Endings [Time Travel]': ["Get all the endings in Time Travel", 'time travel.allendings-1'],
}

# School
school = {
    'LIGMA BALLS': ['Die to LIGMA'],
    'Godslayer': ['Fight a god with your school bag'],
    'Ligma Master': ["Win School"],
    'With Great Power Comes Great Responsibility - Confucius (I think)': ["Get Power in school"],
    'Luffy, that\'s not the real One Piece… that\'s Wingsley\'s pocket money.': ['Find the One Piece'],
    # Standard Achievements
    'Year 7': ['Play this story 1 time', 'school.play-1'],
    'Year 9': ['Play this story 10 times', 'school.play-10'],
    'Year 11': ['Play this story 50 times', 'school.play-50'],
    'Graduated': ["Get all the endings in School", 'school.allendings-1'],
}

# Tombs
tomb = {
    'I Want My Mummy!': ['Die to a Mummy'],
    'The Rich': ['Win Tutankhamun\'s Tomb'],
    'Killed by [Anubis]': ['Die to Anubis'],
    # Standard Achievements
    'Explorer': ['Play this story 1 time', 'tomb.play-1'],
    'Excavator': ['Play this story 10 times', 'tomb.play-10'],
    'Mummy Master': ['Play this story 50 times', 'tomb.play-50'],
    'All Endings [Tutankhamun\'s Tomb]': ["Get all the endings in Tutankhamun's Tomb", 'tomb.allendings-1'],
}

mountain = {
    'Yeti Man': ['Find the Abominable Snowman'], # not added
    # Standard Achievements
    'Rock Climber': ['Play this story 1 time', 'mountain.play-1'],
    'Hiker': ['Play this story 10 times', 'mountain.play-10'],
    'Alpinist': ['Play this story 50 times', 'mountain.play-50'],
    'All Endings [Mountain]': ['Get all endings in Mountain', 'mountain.allendings-1'],
}

allstories = {
    "Oliver's Collection": ['Play all stories written by Oliver', 'stories.oliver-1'],
    "Sean's Collection": ['Play all stories written by Sean', 'stories.sean-1'],
    "Levi's Collection": ['Play all stories written by Levi', 'stories.levi-1'],
    "Newbie": ["Play 1 time", "stories.totalplays-1"],
    "Good": ["Play 10 times", "stories.totalplays-10"],
    "Pro": ["Play 100 times", "stories.totalplays-100"],
    "Hacker": ["Play 1000 times", "stories.totalplays-1000"],
    "Taster": ["Play all the stories at least once.", "stories.allplays-1"],
}

# Special
special = {
    # Easter Egg
    "The Long Egg": ["Find the longest Easter Egg in the game."],
    # Commands
    "Supporter": ["Use the credits command"],
    "Saved": ["Save your progress"],
    "Technician": ["Look at the updates"],
    "Inspired": ["See the inspirational story"],
    "First Command": ["Use 1 Command", "commands.amount-1"],
    "Command User": ["Use 10 Commands", "commands.amount-10"],
    "God of Commands": ["Use 100 Commands", "commands.amount-100"],
    "Command Master": ["Use all types of commands", "commands.allcommands-1"],
    # Others
}

achievements = { #name: [description, code (Only if neccesary)]
    "amazon jungle": amazon,
    "space story": space,
    "time travel": time,
    "school": school,
    "tomb": tomb,
    "mountain": mountain,
    "all stories": allstories,
    "special": special,
}
