#My first rpg game

import cmd
import textwrap
import sys
import os
import time
import random

screen_width = 200

##### Player setup #####
class player:
    def __init__(self):
        self.name = ''
        self.job = ''
        self.hp = 0
        self.mp = 0
        self.status_effects = []
        self.location = 'b2'
        self.game_over = False
myPlayer = player()

#### Title screen ####
def title_screen_selections():
    option = input("> ")
    if option.lower() == ("play"):
        setup_game() #placeholder
    elif option.lower() == ("help"):
        help_menu()
    elif option.lower() == ("quit"):
        sys.exit()
    while option.lower() not in ['play', 'help', 'quit']:
        print("Please enter a valid command")
        option = input("> ")
        if option.lower() == ("play"):
            setup_game() #placeholder
        elif option.lower() == ("help"):
            help_menu()
        elif option.lower() == ("quit"):
            sys.exit() 

def title_screen():
    os.system('cls')
    print('############################')
    print('# Welcome to the Text Rpg! #')
    print('############################')
    print('           -Play-           ')
    print('           -Help-           ')
    print('           -Quit-           ')
    title_screen_selections()

def help_menu():
    print('############################')
    print('# Welcome to the Text Rpg! #')
    print('############################')
    print('-Use up, down, left, right to move')
    print('-type commands to move')
    print('-use "look" to inspect something')
    print('Good luck new player!')
    title_screen_selections()


#### MAP ####
"""
('a1') ('a2') ('a3') #player starts at b2
-------------
|  |  |  |  | ('a4')
-------------
|  |  |  |  | ('b4') ...
-------------
|  |  |  |  |
-------------
|  |  |  |  |
-------------
"""


ZONENAME = ''
DESCRIPTION = 'description'
EXAMINATION = 'examine'
SOLVED = False
UP = 'up, north'
DOWN = 'down, south'
LEFT = 'left, west'
RIGHT = 'right, east'
INSPECT = 'inspect'
TALK = 'talk'
TALKING_TEXT = 'talking text'
TALKING_TEXT_TWO = 'merchanr text'
ACTION = 'actions the player can do'

solved_places = {'a1': False, 'a2': False, 'a3': False, 'a4': False,
                'b1': False, 'b2': True, 'b3': False, 'b4': False,
                'c1': False, 'c2': False, 'c3': False, 'c4': False,
                'd1': False, 'd2': False, 'd3': False, 'd4': False,
                }

talking_places = {'a1': False, 'a2': True, 'a3': True, 'a4': True,
                'b1': True, 'b2': False, 'b3': True, 'b4': True,
                'c1': True, 'c2': True, 'c3': False, 'c4': True,
                'd1': True, 'd2': True, 'd3': False, 'd4': True,
                }

action_places = {'a1': False, 'a2': True, 'a3': False, 'a4': False,
                'b1': False, 'b2': False, 'b3': True, 'b4': True,
                'c1': True, 'c2': True, 'c3': False, 'c4': True,
                'd1': True, 'd2': True, 'd3': False, 'd4': True,
                }

zonemap = {
        ('a1'): {
            ZONENAME: "The Town Hall",
            DESCRIPTION: 'A busy place filled with people.',
            EXAMINATION: 'There are job listings on the "Help Wanted!" board.\nMany people waiting to talk to clerks.',
            SOLVED: False,
            UP: 'Unknown??',
            DOWN: 'b1',
            LEFT: 'Unknown??',
            RIGHT: 'a2',
            INSPECT: 'On the "Help Wanted!" board, you find an interesting job listing.\nIt says to go to the town market place and look for an man named Steve who works at a tips stall. There is no other information about the quest.',
            TALK: False,
            TALKING_TEXT: '',
            ACTION: False,

        },
        ('a2'): {
            ZONENAME: "The Town Marketplace",
            DESCRIPTION: 'People are walking along the stalls and observing the items.',
            EXAMINATION: 'Potions, armor, and other merchandise is sold here.',
            SOLVED: False,
            UP: 'Unknown??',
            DOWN: 'b2',
            LEFT: 'a1',
            RIGHT: 'a3',
            INSPECT: 'On the right, there is a weapons stall and a armor stall.\nOn the left side, there is a potions stall and a tips stall.\nThe man in the tips stall looks eager for a conversation.', 
            TALK: True,
            TALKING_TEXT: "Yes, my name is Steve! Have you come for the quest?\nIt's a simple one! Go to the house in the woods and then report to me what you find there.\nYou'll be rewarded handsomely!",
            TALKING_TEXT_TWO:"Hello there traveler! Would you like to buy potions, armor, or weapons?",
            ACTION: False,

        },
        ('a3'): {
            ZONENAME: "The Town Sqaure",
            DESCRIPTION: 'A lively place filled with people.',
            EXAMINATION: 'Conversations can be heard all around.',
            SOLVED: False,
            UP: 'Unknown??',
            DOWN: 'b3',
            LEFT: 'a2',
            RIGHT: 'a4',
            INSPECT: '',
            TALK: True,
            TALKING_TEXT: '',
            ACTION: False,

        }, 
        ('a4'): {
            ZONENAME: "The Town Neighborhood",
            DESCRIPTION: 'This area is where most of the town people live.',
            EXAMINATION: 'The neighborhood is peaceful.',
            SOLVED: False,
            UP: 'Unknown??',
            DOWN: 'b4',
            LEFT: 'a3',
            RIGHT: 'Unknown??',
            INSPECT: '',
            TALK: True,
            TALKING_TEXT: '',
            ACTION: False,

        }, 
        ('b1'): {
            ZONENAME: "The Meadow",
            DESCRIPTION: 'This is a meadow.',
            EXAMINATION: 'Colorful flowers reside in the grass. There are stone paths that lead into town',
            SOLVED: False,
            UP: 'a1',
            DOWN: 'c1',
            LEFT: 'Unknown??',
            RIGHT: 'b2',
            INSPECT: '',
            TALK: True,
            TALKING_TEXT: '',
            ACTION: False,

        }, 
        ('b2'): {
            ZONENAME: "Home",
            DESCRIPTION: 'This is your home.',
            EXAMINATION: 'Your home looks the same. Not much to do here.',
            SOLVED: True,
            UP: 'a2',
            DOWN: 'c2',
            LEFT: 'b1',
            RIGHT: 'b3',
            INSPECT: '',
            TALK: False,
            TALKING_TEXT: '',
            ACTION: False,

        }, 
        ('b3'): {
            ZONENAME: "Forest area 1",
            DESCRIPTION: 'This is a forest.',
            EXAMINATION: 'It has trees. As expected of a forest.',
            SOLVED: False,
            UP: 'a3',
            DOWN: 'c3',
            LEFT: 'b2',
            RIGHT: 'b4',
            INSPECT: '',
            TALK: True,
            TALKING_TEXT: '',
            ACTION: True,            

        }, 
        ('b4'): {
            ZONENAME: "The Mysterious House in the Forest",
            DESCRIPTION: 'There is an old house deep within the forest.',
            EXAMINATION: 'The house seems to be falling apart. The house is covered in vines.',
            SOLVED: False,
            UP: 'a4',
            DOWN: 'c4',
            LEFT: 'b3',
            RIGHT: 'Unknown??',
            INSPECT: 'The doors and windows are boarded shut. The chimmey on the roof looks large enough for a person to climb into.',
            TALK: True,
            TALKING_TEXT: "I am you from the future! In my time, the demon king has taken over and has launched a series of bloody wars!\nYou must defeat the demon king while you still have the chance!\nHe lives in d4. Go and recruit people to fight him!\nOh and take this! It's a weapon that'll do for now!\nHead to Town Square and look for a man named Sal.\nMake haste!",
            ACTION: True,

        }, 
        ('c1'): {
            ZONENAME: "The City Town hall",
            DESCRIPTION: "Extremely loud and busy. This place is three times the size of the town's town hall.",
            EXAMINATION: 'The "Help Wanted" board is chock full of flyers.',
            SOLVED: False,
            UP: 'b1',
            DOWN: 'd1',
            LEFT: 'Unknown??',
            RIGHT: 'c2',
            INSPECT: '',
            TALK: True,
            TALKING_TEXT: '',
            ACTION: False,

        },
        ('c2'): {
            ZONENAME: "City Homes and Guild houses",
            DESCRIPTION: 'A great number of people live here. Guild houses are close by.',
            EXAMINATION: 'Guild houses are open for those looking to recruit.',
            SOLVED: False,
            UP: 'b2',
            DOWN: 'd2',
            LEFT: 'c1',
            RIGHT: 'c3',
            INSPECT: '',
            TALK: True,
            TALKING_TEXT: '',
            ACTION: False, 

        }, 
        ('c3'): {
            ZONENAME: "Forest area 2",
            DESCRIPTION: 'This is a forest.',
            EXAMINATION: 'It has trees. As expected of a forest.',
            SOLVED: False,
            UP: 'b3',
            DOWN: 'd3',
            LEFT: 'c2',
            RIGHT: 'c4',
            INSPECT: '',
            TALK: False,
            TALKING_TEXT: '',
            ACTION: True,

        }, 
        ('c4'): {
            ZONENAME: "The Ruins area 1",
            DESCRIPTION: 'Rubble, dust, and stone are all that have been left behind by a once great town.',
            EXAMINATION: 'Traveling merchants and travelers can be seen moving through the ruins.',
            SOLVED: False,
            UP: 'b4',
            DOWN: 'd4',
            LEFT: 'c3',
            RIGHT: 'Unknown??',
            INSPECT: '',
            TALK: True,
            TALKING_TEXT: '',
            ACTION: True, 

        }, 
        ('d1'): {
            ZONENAME: "The City Library",
            DESCRIPTION: 'This place is the city library.',
            EXAMINATION: 'The library contains books on the history of this world, special moves for each class, and some secrets and rumors about the surrouding cities, towns, and forests.',
            SOLVED: False,
            UP: 'c1',
            DOWN: 'Unknown??',
            LEFT: 'Unknown??',
            RIGHT: 'd2',
            INSPECT: '',
            TALK: True,
            TALKING_TEXT: '',
            ACTION: False,

        }, 
        ('d2'): {
            ZONENAME: "The City downtown area",
            DESCRIPTION: 'This area has is bustling with people entering and exiting stores. Some can be seen stumbling in and out of pubs.',
            EXAMINATION: 'There are general ware shops, weaponry shops, and black smith shops.',
            SOLVED: False,
            UP: 'c2',
            DOWN: 'Unknown??',
            LEFT: 'd1',
            RIGHT: 'd3',
            INSPECT: '',
            TALK: True,
            TALKING_TEXT: '',
            ACTION: False,

        }, 
        ('d3'): {
            ZONENAME: "The Ruins area 2",
            DESCRIPTION: 'Rubble, dust, and stone are all that have been left behind by a once great town.',
            EXAMINATION: 'At the heart of the ruins, a sword rests in a rock. There is a plaque beneath the rock. It reads "Only those who are worthy can claim the legendary sword as their own".',
            SOLVED: False,
            UP: 'c3',
            DOWN: 'Unknown??',
            LEFT: 'd2',
            RIGHT: 'd4',
            INSPECT: '',
            TALK: False,
            TALKING_TEXT: '',
            ACTION: True,

        },
        ('d4'): {
            ZONENAME: "The Demon King's castle",
            DESCRIPTION: "This place is the Demon King's castle. The ominous castle looms over you.",
            EXAMINATION: 'The main door of the castle is closed. On the door it reads: "All ye who dare enter will face a terrible fate".',
            SOLVED: False,
            UP: 'c4',
            DOWN: 'unknown??',
            LEFT: 'd3',
            RIGHT: '',
            INSPECT: '',
            TALK: True,
            TALKING_TEXT: '',
            ACTION: True,
        },
        ('Unknown??'): {
            ZONENAME: 'Area Unknown',
            DESCRIPTION: 'A thick fog lies ahead of you. You feel that you must turn back.',

        }
    }



##### GAME INTERACTIVITY #####

def prompt():
    print("\n" + "--------------------------")
    print("What would you like to do?\nmove? examine? inspect? talk? action?")
    action = input("> ")
    acceptable_actions = ['move', 'go', 'travel', 'walk', 'quit', 'examine', 'inspect', 'talk', 'action']
    while action.lower() not in acceptable_actions:
        print("Unknown action. Please type something else.\n")
        action = input("> ")
    if action.lower() == 'quit':
        sys.exit()
    elif action.lower() in ['move', 'go', 'travel', 'walk']:
        player_move(action.lower())
    elif action.lower() in ['examine']:
        player_examine(action.lower())
    elif action.lower() in ['inspect']:
        player_inspect(action.lower())
    elif action.lower() in ['talk']:
        player_talk(action.lower())
    elif action.lower() in ['action']:
        player_action(action.lower())


##### Player movements ####
def movement_handler(destination):
    print('\n' + 'You have arrived to your destination. (' + destination +').')
    myPlayer.location = destination
    print_location()
    prompt()


def print_location():
    print('You are in:')
    print(zonemap[myPlayer.location][ZONENAME])
    print(zonemap[myPlayer.location][DESCRIPTION])

def player_move(myAction):
    ask ='Where would you like to move?\n' + '> '
    dest = input(ask)
    if dest in ['up', 'north']:
        destination = zonemap[myPlayer.location][UP]
        movement_handler(destination)
    elif dest in ['down', 'south']:
        destination = zonemap[myPlayer.location][DOWN]
        movement_handler(destination)
    elif dest in ['left', 'west']:
        destination = zonemap[myPlayer.location][LEFT]
        movement_handler(destination)
    elif dest in ['right', 'east']:
        destination = zonemap[myPlayer.location][RIGHT]
        movement_handler(destination)
    


##### Player examine and inspect####
def player_examine(action):
    print(zonemap[myPlayer.location][EXAMINATION])
    if zonemap[myPlayer.location][SOLVED]:
        print('You have already completed this area.')
    else:
        print('You can trigger something here!')
    prompt()

def player_inspect(myAction):
    print(zonemap[myPlayer.location][INSPECT])
    prompt()

#### Player Actions#####
def player_action(myAction):
    print('What action would you like to do?\nfight?, climb?')
    action = input("> ")
    acceptable_words = ['fight', 'climb', 'pull']
    while action.lower() not in acceptable_words:
        print("Unknown action. Please type something else.\n")
        action = input("> ")
    if action.lower() == 'quit':
        sys.exit()
    elif action.lower() in ['fight']:
        print('Who do you want to fight?')
        action = input("> ")
        acceptable_fighters = ['bandits', 'slimes', 'demon king']
        while action.lower() not in acceptable_fighters:
            print("Unknown action. Please type something else.\n")
            action = input("> ")
        if action.lower() == 'quit':
            sys.exit()
    elif action.lower() in ['climb']:
        print("You managed to climb onto the roof top and shimmy down the chimmey.\nIt's so dusty!\nWhen you finally make it down the chimmey, you see a bearded version of yourself.")
        print(zonemap[myPlayer.location][TALKING_TEXT])
        print('You have obtained a wooden sword')



#### Talking stuff ####
def player_talk(myAction):
    print('Who would you like to talk to?')
    action = input("> ")
    acceptable_people = ['steve', 'demon king', 'merchant']
    while action.lower() not in acceptable_people:
        print("Unknown action. Please type something else.\n")
        action = input("> ")
    if action.lower() == 'quit':
        sys.exit()
    elif action.lower() in ['steve']:
        print(zonemap[myPlayer.location][TALKING_TEXT])
    elif action.lower() in ['merchant']:
        print(zonemap[myPlayer.location][TALKING_TEXT_TWO])
    if zonemap[myPlayer.location][TALK] is False:
        print('You cannot talk here.')
    prompt()














##### GAME FUNCTIONALITY ####

def main_game_loop():
    while myPlayer.game_over == False:
        prompt()
    #Here handle if all puzzles have been solved, boss defeated, or all areas explored

def setup_game():
    os.system('cls')

### NAME COLLECTING 
    Question1 = 'What is your name?\n'
    for character in Question1:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.05)
    player_name = input('> ')
    myPlayer.name = player_name

### JOB COLLECTING
    Question2 = "What is your class?\n"
    Question2added = "You can play as a warrior, wizard, or a alchemist.\n"
    for character in Question2:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.05)
    for character in Question2added:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.05)
    player_job = input('> ')
    valid_jobs = ['warrior', 'wizard', 'alchemist']
    while player_job.lower() not in valid_jobs:
        player_job = input('> ')
    if player_job.lower() in valid_jobs:
        myPlayer.job = player_job
        print("You are now a " + player_job + "!\n")


### PlAYER STATS
    if myPlayer.job is "warrior":
        self.hp = 140
        self.mp = 20
    elif myPlayer.job is "wizard":
        self.hp = 100
        self.mp = 70
    elif myPlayer.job is "alchemist":
        self.hp = 120
        self.mp = 60

### INTRODUCTION
    Question3 = "Welcome, " + player_name + " the " + player_job + ".\n"
    for character in Question3:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.05)
    

os.system('cls')
speech1 = "Welcome to this fantasy world! \n"
speech2 =  "Please enjoy your visit. \n"
speech3 =  "Your destiny awaits! \n"


for character in speech1:
    sys.stdout.write(character)
    sys.stdout.flush()
    time.sleep(0.05)
for character in speech2:
    sys.stdout.write(character)
    sys.stdout.flush()
    time.sleep(0.07)
for character in speech3:
    sys.stdout.write(character)
    sys.stdout.flush()
    time.sleep(0.07)
os.system('cls')

title_screen()

print('------------------------------------------')
print("You wake up in your home. It's a nice day today.")
print('You feel like going on an adventure.')
print('You find a note on your table. It says:')
print('"There is a town up north, a forest to the east, and another town south west.')
print('"New players should head to the town up north first."')
 

prompt()

print_location()






