# Amazon Jungle
amazon = {
    'Keep the Gem': ['Finish the story still with a gem in your inventory'], # not added
    'Pilot Buddy': ['Finish the story with the pilot still with you'], # not added
    'Die of Boredom': ['Get the ending: Died of Boredom'],
    'Bad Choices': ['Get the ending: Bad choices'],
    "Escape of the Jungle": ['Win Amazon Jungle'], # not added (Get the ending: Passenger Escape or Defeated a Monster)
    'Again?!': ['Get the ending: Crashed again'], # not added
    #Standard Achievements
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
    #Standard Achievements
    'Beginner space': ['Play this story 1 time', 'space story.play-1'],
    'Intermediate space': ['Play this story 10 times', 'space story.play-10'],
    'Advanced space': ['Play this story 50 times', 'space story.play-50'],
    'All Endings [Space Story]': ["Get all the endings in Space Story", 'space story.allendings-1'],
}

# Time Travel
time = {
    'Bonker': ["Use The Bonker"], # not added
    'Bonked': ["Get Bonked by the Bonker"], # not added
    "Back to reality": ["Win Time Travel"], # not added
    #Standard Achievements
    'Time Traveller': ['Play this story 1 time', 'time travel.play-1'],
    'Better Time Traveller': ['Play this story 10 times', 'time travel.play-10'],
    'Doctor Who': ['Play this story 50 times', 'time travel.play-50'],
    'All Endings [Time Travel]': ["Get all the endings in Time Travel", 'time travel.allendings-1'],
}

# School
school = {
    'LIGMA BALLS': ['Die to LIGMA'], # not added
    'Godslayer': ['Fight a god with your school bag.'], # not added
    'Ligma Master': ["Win School"], # not added
    #Standard Achievements
    'Year 7': ['Play this story 1 time', 'school.play-1'],
    'Year 9': ['Play this story 10 times', 'school.play-10'],
    'Year 11': ['Play this story 50 times', 'school.play-50'],
    'Graduated': ["Get all the endings in School", 'school.allendings-1'],
}

# Tombs
tomb = {
    'I Want My Mummy!': ['Die to a Mummy'], # not added
    'The Rich': ['Win Tutankhamun\'s Tomb'], # not added
    'Killed by [Anubis]': ['Die to Anubis'], # not added
    #Standard Achievements
    'Explorer': ['Play this story 1 time', 'tomb.play-1'],
    'Excavator': ['Play this story 10 times', 'tomb.play-10'],
    'Mummy Master': ['Play this story 50 times', 'tomb.play-50'],
    'All Endings [Tutankhamun\'s Tomb]': ["Get all the endings in Tutankhamun's Tomb", 'tomb.allendings-1'],
}

# Special
special = {
    # Easter Egg
    "The Long Egg": ["Find the longest Easter Egg in the game."],
    # Commands
    "Supporter": ["Use the credits command"],
    "Saved": ["Save your progress"],
    "Technician": ["Look at the updates"],
    # Others
}

achievements = { #name: [description, code (Only if neccesary)]
    "amazon jungle": amazon,
    "space story": space,
    "time travel": time,
    "school": school,
    "tomb": tomb,
    "special": special,
}
