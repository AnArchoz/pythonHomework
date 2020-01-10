import random
import sys

import pygame

# INITIALISE GAME AND WINDOW
pygame.init()
window = pygame.display.set_mode((640, 480))
arena = window.get_rect()
fpsClock = pygame.time.Clock()

# DECLARE ACTORS AND ASSIGN IMAGE FILES
cann1 = {"file": "Cannibal.png"}
cann2 = {"file": "Cannibal.png"}
cann3 = {"file": "Cannibal.png"}
miss1 = {"file": "Missionary.png"}
miss2 = {"file": "Missionary.png"}
miss3 = {"file": "Missionary.png"}

# ADD AND SEPARATE ACTORS TO LISTS FOR EASY ACCESS
ACTORS = [cann1, cann2, cann3, miss1, miss2, miss3]
CANNIBALS = [cann1, cann2, cann3]
MISSIONARIES = [miss1, miss2, miss3]

# INITIAL ACTOR STATE; ALL 6 ACTORS ON THE LEFT SIDE OF THE RIVER
startLineup = [cann1, cann2, cann3, miss1, miss2, miss3]
boat = []

# GAME GRAPH TREE WITH ALL PLAYABLE POSSIBILITIES
# NOT READABLE AND NOT IN ORDER,
# PLEASE DON'T OPEN FOR LONG PERIODS OF TIME
gameGraph = {
    "3, 3, 0, 0, 0": {
        "c": "3, 2, 0, 0, 0",
        "m": "2, 3, 0, 0, 0",
        " ": "3, 3, 1, 0, 0"
    },
    "3, 3, 1, 0, 0": {
        " ": "3, 3, 0, 0, 0"
    },
    "3, 2, 0, 0, 0": {
        "c": "3, 1, 0, 0, 0",
        "m": "2, 2, 0, 0, 0",
        "e": "3, 3, 0, 0, 0",
        " ": "3, 2, 1, 0, 0"
    },
    "3, 2, 1, 0, 0": {
        "e": "3, 2, 1, 0, 1",
        " ": "3, 2, 0, 0, 0"
    },
    "3, 2, 1, 0, 1": {
        "c": "3, 2, 1, 0, 0",
        " ": "3, 2, 0, 0, 1",
    },
    "3, 2, 0, 0, 1": {
        "c": "3, 1, 0, 0, 1",
        "m": "2, 2, 0, 0, 1",
        " ": "3, 2, 1, 0, 1",
    },
    "3, 1, 0, 0, 1": {
        "c": "3, 0, 0, 0, 1",
        "m": "2, 1, 0, 0, 1",
        "e": "3, 2, 0, 0, 1",
        " ": "3, 1, 1, 0, 1"
    },

    "3, 1, 1, 0, 1": {
        "c": "3, 1, 1, 0, 0",
        " ": "3, 1, 0, 0, 1"
    },

    "3, 1, 1, 0, 0": {
        "e": "3, 1, 1, 0, 2",
        " ": "3, 1, 0, 0, 0"
    },

    "3, 1, 1, 0, 2": {
        "c": "3, 1, 1, 0, 1",
        " ": "3, 1, 0, 0, 2"
    },

    "3, 1, 0, 0, 2": {
        "c": "3, 0, 0, 0, 2",
        "m": "2, 1, 0, 0, 2",
        " ": "3, 1, 1, 0, 2"
    },

    "3, 1, 0, 0, 0": {
        "e": "3, 3, 0, 0, 0",
        " ": "3, 1, 1, 0, 0"
    },

    "3, 0, 0, 0, 2": {
        "m": "2, 0, 0, 0, 2",
        "e": "3, 1, 0, 0, 2",
        " ": "3, 0, 1, 0, 2"
    },

    "3, 0, 1, 0, 2": {
        "c": "3, 0, 1, 0, 1",
        "e": "3, 0, 1, 0, 3",
        " ": "3, 0, 0, 0, 2"
    },

    "3, 0, 1, 0, 1": {
        "e": "3, 0, 1, 0, 3",
        " ": "3, 0, 0, 0, 1"
    },

    "3, 0, 1, 0, 3": {
        "c": "3, 0, 1, 0, 2",
        " ": "3, 0, 0, 0, 3"
    },

    "3, 0, 0, 0, 3": {
        "m": "2, 0, 0, 0, 3",
        " ": "3, 0, 1, 0, 3"
    },

    "3, 0, 0, 0, 1": {
        "e": "3, 2, 0, 0, 1",
        " ": "3, 0, 1, 0, 1"
    },
    "2, 3, 0, 0, 0": {
        "m": "1, 3, 0, 0, 0",
        "c": "2, 2, 0, 0, 0",
        "e": "3, 3, 0, 0, 0",
        " ": "2, 3, 1, 0, 0"  # FAILURE
    },
    "2, 2, 0, 0, 0": {
        "e": "3, 3, 0, 0, 0",
        " ": "2, 2, 1, 0, 0"
    },

    "2, 2, 1, 0, 0": {
        "e": "2, 2, 1, 1, 1",
        " ": "2, 2, 0, 0, 0"
    },

    "2, 2, 1, 1, 1": {
        "c": "2, 2, 1, 1, 0",
        "m": "2, 2, 1, 0, 1",
        " ": "2, 2, 0, 1, 1"
    },

    "2, 2, 0, 1, 1": {
        "c": "2, 1, 0, 1, 1",
        "m": "1, 2, 0, 1, 1",
        " ": "2, 2, 1, 1, 1"
    },

    "2, 2, 1, 0, 1": {
        "c": "2, 2, 1, 0, 0",
        "e": "2, 2, 1, 1, 1",
        " ": "2, 2, 0, 0, 1"
    },

    "2, 2, 1, 1, 0": {
        "m": "2, 2, 1, 0, 0",
        "e": "2, 2, 1, 1, 1"
    },

    "2, 2, 0, 0, 1": {
        "c": "2, 1, 0, 0, 1",
        "m": "1, 2, 0, 0, 1",
        "e": "3, 2, 0, 0, 1",
        " ": "2, 2, 1, 0, 1"
    },

    "2, 1, 0, 1, 1": {
        "c": "2, 0, 0, 1, 1",
        "m": "1, 1, 0, 1, 1",
        "e": "2, 2, 0, 1, 1",
        " ": "2, 1, 1, 1, 1"
    },

    "2, 1, 0, 0, 1": {
        "e": "3, 2, 0, 0, 1",
        " ": "2, 1, 1, 0, 1"
    },

    "2, 1, 0, 0, 2": {
        "c": "2, 0, 0, 0, 2",
        "m": "1, 1, 0, 0, 2",
        "e": "3, 1, 0, 0, 2",
        " ": "2, 1, 1, 0, 2"
    },

    "2, 1, 1, 0, 2": {
        "c": "2, 1, 1, 0, 1",
        "e": "2, 1, 1, 1, 2",  # FAILURE
        " ": "2, 1, 0, 0, 2"
    },

    "2, 1, 1, 0, 1": {
        "e": "2, 1, 1, 1, 2",  # FAILURE
        " ": "2, 1, 0, 0, 1"
    },

    "2, 1, 1, 1, 1": {
        "c": "2, 1, 1, 1, 0",
        "m": "2, 1, 1, 0, 1",
        "e": "2, 1, 1, 1, 2",  # FAILURE
        " ": "2, 1, 0, 1, 1"
    },

    "2, 1, 1, 1, 0": {
        "e": "2, 1, 1, 1, 2",  # FAILURE,
        " ": "2, 1, 0, 1, 0"
    },

    "2, 1, 0, 1, 0": {
        "e": "2, 3, 0, 1, 0",  # FAILURE
        " ": "2, 1, 1, 1, 0"
    },

    "2, 0, 0, 1, 1": {
        "e": "2, 2, 0, 1, 1",
        " ": "2, 0, 1, 1, 1"
    },

    "2, 0, 1, 1, 1": {
        "e": "2, 0, 1, 1, 3",  # FAILURE
        " ": "2, 0, 0, 1, 1"
    },

    "2, 0, 0, 0, 3": {
        "m": "1, 0, 0, 0, 3",
        "e": "3, 0, 0, 0, 3",
        " ": "2, 0, 1, 0, 3"
    },

    "2, 0, 1, 0, 3": {
        "c": "2, 0, 1, 0, 2",
        "e": "2, 0, 1, 1, 3",  # FAILURE
        " ": "2, 0, 0, 0, 3"
    },

    "2, 0, 1, 0, 2": {
        "e": "2, 0, 1, 1, 3",  # FAILURE
        " ": "2, 0, 0, 0, 2"
    },

    "2, 0, 0, 0, 2": {
        "e": "3, 1, 0, 0, 2",
        " ": "2, 0, 1, 0, 2"
    },

    "1, 3, 0, 0, 0": {
        "e": "3, 3, 0, 0, 0",
        " ": "1, 3, 1, 0, 0"  # FAILURE
    },

    "1, 2, 0, 1, 1": {
        "m": "0, 2, 0, 1, 1",
        "c": "1, 1, 0, 1, 1",
        "e": "2, 2, 0, 1, 1",
        " ": "1, 2, 1, 1, 1",  # FAILURE
    },

    "1, 2, 0, 0, 1": {
        "e": "3, 2, 0, 0, 1",
        " ": "1, 2, 1, 0, 1"  # FAILURE
    },

    "1, 1, 0, 1, 1": {
        "e": "2, 2, 0, 1, 1",
        " ": "1, 1, 1, 1, 1"
    },

    "1, 1, 1, 1, 1": {
        "e": "1, 1, 1, 2, 2",
        " ": "1, 1, 0, 1, 1"
    },

    "1, 1, 0, 2, 0": {
        "e": "1, 3, 0, 2, 0",  # FAILURE
        " ": "1, 1, 1, 2, 0"
    },

    "1, 1, 0, 2, 1": {
        "c": "1, 0, 0, 2, 1",
        "m": "0, 1, 0, 2, 1",
        "e": "1, 2, 0, 2, 1"  # FAILURE
    },

    "1, 1, 1, 2, 0": {
        "e": "1, 1, 1, 2, 2",
        " ": "1, 1, 0, 2, 0"
    },

    "1, 1, 1, 2, 1": {
        "c": "1, 1, 1, 2, 0",
        "m": "1, 1, 1, 1, 1",
        "e": "1, 1, 1, 2, 2",
        " ": "1, 1, 0, 2, 1"
    },

    "1, 1, 0, 2, 2": {
        "c": "1, 0, 0, 2, 2",
        "m": "0, 1, 0, 2, 2",
        " ": "1, 1, 1, 2, 2"
    },

    "1, 1, 0, 0, 2": {
        "e": "3, 1, 0, 0, 2",
        " ": "1, 1, 1, 0, 2"
    },

    "1, 1, 1, 0, 2": {
        "e": "1, 1, 1, 2, 2",
        " ": "1, 1, 0, 0, 2"
    },

    "1, 1, 1, 1, 2": {
        "c": "1, 1, 1, 1, 1",
        "m": "1, 1, 1, 0, 2",
        "e": "1, 1, 1, 2, 2",
        " ": "1, 1, 0, 1, 2"  # FAILURE

    },

    "1, 1, 1, 2, 2": {
        "c": "1, 1, 1, 2, 1",
        "m": "1, 1, 1, 1, 2",
        " ": "1, 1, 0, 2, 2"
    },

    "1, 0, 1, 2, 1": {
        "e": "1, 0, 1, 2, 3",  # FAILURE
        " ": "1, 0, 0, 2, 1"
    },

    "1, 0, 1, 1, 2": {
        "e": "1, 0, 1, 2, 3",  # FAILURE
        " ": "1, 0, 0, 1, 2"
    },

    "1, 0, 1, 2, 2": {
        "c": "1, 0, 1, 2, 1",
        "m": "1, 0, 1, 1, 2",
        "e": "1, 0, 1, 2, 3",  # FAILURE
        " ": "1, 0, 0, 2, 2"
    },

    "1, 0, 0, 2, 1": {
        "e": "1, 2, 0, 2, 1",  # FAILURE,
        " ": "1, 0, 1, 2, 1"
    },

    "1, 0, 0, 2, 2": {
        "m": "0, 0, 0, 2, 2",
        "e": "1, 1, 0, 2, 2",
        " ": "1, 0, 1, 2, 2"
    },

    "1, 0, 0, 0, 3": {
        "e": "3, 0, 0, 0, 3",
        " ": "1, 0, 1, 0, 3"
    },

    "1, 0, 1, 0, 3": {
        "e": "1, 0, 1, 2, 3",  # FAILURE
        " ": "1, 0, 0, 2, 1"
    },

    "0, 0, 0, 2, 2": {
        "e": "1, 1, 0, 2, 2",
        " ": "0, 0, 1, 2, 2"
    },

    "0, 0, 1, 2, 2": {
        "e": "0, 0, 1, 3, 3",  # SUCCESS SUCCESS SUCCESS
        " ": "0, 0, 0, 2, 2"
    },

    "0, 1, 0, 2, 1": {
        "e": "1, 2, 0, 2, 1",  # FAILURE
        " ": "0, 1, 1, 2, 1"
    },

    "0, 1, 1, 2, 1": {
        "e": "0, 1, 1, 3, 2",
        " ": "0, 1, 0, 2, 1"
    },

    "0, 1, 0, 2, 2": {
        "c": "0, 0, 0, 2, 2",
        "e": "1, 1, 0, 2, 2",
        " ": "0, 1, 1, 2, 2"
    },

    "0, 1, 1, 1, 2": {
        "e": "0, 1, 1, 3, 2",
        " ": "0, 1, 0, 1, 2"  # FAILURE
    },

    "0, 1, 1, 2, 2": {
        "c": "0, 1, 1, 2, 1",
        "m": "0, 1, 1, 1, 2",
        "e": "0, 1, 1, 3, 2",
        " ": "0, 1, 0, 2, 2"
    },

    "0, 1, 1, 3, 0": {
        "e": "0, 1, 1, 3, 2",
        " ": "0, 1, 0, 3, 0"
    },

    "0, 1, 1, 3, 1": {
        "c": "0, 1, 1, 3, 0",
        "m": "0, 1, 1, 2, 1",
        "e": "0, 1, 1, 3, 2",
        " ": "0, 1, 0, 3, 1"
    },

    "0, 1, 1, 3, 2": {
        "c": "0, 1, 1, 3, 1",
        "m": "0, 1, 1, 2, 2",
        " ": "0, 1, 0, 3, 2"
    },

    "0, 1, 0, 3, 0": {
        "e": "0, 3, 0, 3, 0",
        " ": "0, 1, 1, 3, 0"
    },

    "0, 1, 0, 3, 1": {
        "c": "0, 0, 0, 3, 1",
        "e": "0, 2, 0, 3, 1",
        " ": "0, 1, 1, 3, 1"
    },

    "0, 1, 0, 3, 2": {
        "c": "0, 0, 0, 3, 2",
        " ": "0, 1, 1, 3, 2"
    },

    "0, 0, 1, 3, 2": {
        "e": "0, 0, 1, 3, 3",  # SUCCESS SUCCESS SUCCESS
        " ": "0, 0, 0, 3, 2"

    },

    "0, 0, 0, 3, 2": {
        "e": "0, 1, 0, 3, 2",
        " ": "0, 0, 1, 3, 2"
    },

    "0, 0, 0, 3, 1": {
        "e": "0, 2, 0, 3, 1",
        " ": "0, 0, 1, 3, 1"
    },

    "0, 0, 1, 3, 1": {
        "e": "0, 0, 1, 3, 3",  # SUCCESS SUCCESS SUCCESS
        " ": "0, 0, 0, 3, 1"
    },

    "0, 2, 0, 3, 0": {
        "c": "0, 1, 0, 3, 0",
        "e": "0, 3, 0, 3, 0",
        " ": "0, 2, 1, 3, 0"
    },

    "0, 2, 0, 1, 1": {
        "e": "2, 2, 0, 1, 1",
        " ": "0, 2, 1, 1, 1"
    },

    "0, 2, 0, 2, 0": {
        "e": "1, 3, 0, 2, 0",  # FAILURE
        " ": "0, 2, 1, 2, 0"
    },

    "0, 2, 0, 2, 1": {
        "c": "0, 1, 0, 2, 1",
        "e": "1, 2, 0, 2, 1",  # FAILURE
        " ": "0, 2, 1, 2, 1"
    },

    "0, 2, 1, 2, 0": {
        "e": "0, 2, 1, 3, 1",
        " ": "0, 2, 0, 2, 0"
    },

    "0, 2, 1, 2, 1": {
        "c": "0, 2, 1, 2, 0",
        "m": "0, 2, 1, 1, 1",
        "e": "0, 2, 1, 3, 1",
        " ": "0, 2, 0, 2, 1"
    },

    "0, 2, 1, 1, 1": {
        "e": "0, 2, 1, 3, 1",
        " ": "0, 2, 0, 1, 1"
    },

    "0, 2, 0, 3, 1": {
        "c": "0, 1, 0, 3, 1",
        " ": "0, 2, 1, 3, 1"
    },

    "0, 2, 1, 3, 0": {
        "m": "0, 2, 1, 2, 0",
        "e": "0, 2, 1, 3, 1",
        " ": "0, 2, 0, 3, 0"
    },

    "0, 2, 1, 3, 1": {
        "c": "0, 2, 1, 3, 0",
        "m": "0, 2, 1, 2, 1",
        " ": "0, 2, 0, 3, 1"
    },

    "0, 3, 0, 3, 0": {
        "c": "0, 2, 0, 3, 0",
        " ": "0, 3, 1, 3, 0"
    },

    "0, 3, 0, 1, 0": {
        "e": "2, 3, 0, 1, 0",  # FAILURE
        " ": "0, 3, 0, 1, 0"
    },

    "0, 3, 0, 2, 0": {
        "c": "0, 2, 0, 2, 0",
        "e": "1, 3, 0, 2, 0",  # FAILURE
        " ": "0, 3, 1, 2, 0"
    },

    "0, 3, 1, 1, 0": {
        "e": "0, 3, 1, 3, 0",
        " ": "0, 3, 0, 1, 0"
    },

    "0, 3, 1, 2, 0": {
        "m": "0, 3, 1, 1, 0",
        "e": "0, 3, 1, 3, 0",
        " ": "0, 3, 0, 2, 0"
    },

    "0, 3, 1, 3, 0": {
        "m": "0, 3, 1, 2, 0",
        " ": "0, 3, 0, 3, 0"
    },

    "1, 3, 0, 2, 0": "failure",
    "1, 3, 1, 0, 0": "failure",
    "1, 3, 1, 2, 0": "failure",
    "1, 2, 0, 2, 1": "failure",
    "1, 2, 1, 0, 0": "failure",
    "1, 2, 1, 1, 1": "failure",
    "1, 2, 1, 0, 1": "failure",
    "1, 2, 1, 2, 1": "failure",
    "1, 1, 0, 1, 2": "failure",
    "1, 0, 1, 2, 3": "failure",
    "2, 3, 0, 1, 0": "failure",
    "2, 3, 1, 1, 0": "failure",
    "2, 3, 1, 0, 0": "failure",
    "2, 1, 0, 1, 2": "failure",
    "2, 1, 1, 1, 2": "failure",
    "2, 0, 0, 1, 3": "failure",
    "2, 0, 1, 1, 3": "failure",
    "1, 0, 0, 2, 3": "failure",
    "0, 1, 0, 1, 2": "failure",

    "0, 0, 1, 3, 3": "success"
}

# INITIAL GAME STATE, ALL ACTORS ON THE LEFT SIDE OF THE RIVER
gameState = "3, 3, 0, 0, 0"

# GAME CONTROLS FOR ACTORS AND BOAT
CONTROLS = {pygame.K_e: "e",  # empty boat
            pygame.K_SPACE: " ",  # ferry boat
            pygame.K_m: "m",  # add missionary
            pygame.K_c: "c"}  # add cannibal

# ~~~~~~~ UNSURE IF I WILL USE, KEEP FOR NOW ~~~~~~~~
passenger = {"c": [random.choice(CANNIBALS)],
             "m": [random.choice(MISSIONARIES)],
             "e": [],
             " ": []}

# PIXEL MOVEMENT OF BOAT WITH PASSENGERS
FERRY_STEP = -5


def getKey():
    """Fetch pressed keys from pygame events and either
        close the game or return a key value to be used."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # pygame.image.save(window, "game-over.bmp")
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                sys.exit()
            if event.key in CONTROLS:
                key = CONTROLS[event.key]
                return key


# TODO: WRITE FUNCTION
def handleKeys(key):
    """Executes an action according to each keypress:
        Ferry, empty, or fill the boat."""
    pass


# TODO: WRITE FUNCTION
def drawWelcomeScreen():
    """Displays welcome text and instructions"""
    pass


def ferry(who, step):
    """Moves the boat across the river
        containing between one or two passengers."""
    # TODO: REMAKE FUNCTION
    done = False
    for actor in who:
        actor["rect"] = actor["rect"].move((step, 0))
        if not arena.contains(actor["rect"]):
            actor["rect"] = actor["rect"].move((-step, 0))
            actor["surf"] = pygame.transform.flip(actor["surf"], True, False)
            done = True
    return done


def failure():
    """Displays a screen for when you lose the game:
        Cannibals successfully eat missionary/ies."""
    myfont = pygame.font.Font('freesansbold.ttf', 48)
    msg = myfont.render("Failure", True, (255, 0, 0))
    msg_box = msg.get_rect()
    msg_box.center = arena.center
    window.blit(msg, msg_box)
    pygame.display.flip()
    pygame.time.wait(1000)


def success():
    """Displays a screen for when you win the game:
        All cannibals and missionaries have been ferried
            To the right side of the river."""
    myfont = pygame.font.Font('freesansbold.ttf', 48)
    msg = myfont.render("Success", True, (255, 255, 255))
    msg_box = msg.get_rect()
    msg_box.center = arena.center
    window.blit(msg, msg_box)
    pygame.display.flip()
    pygame.time.wait(1000)


def drawactors():
    """Loops through the list of Actors and draw them on
        the screen with their assigned images"""
    for i, actor in enumerate(ACTORS):
        actor["surf"] = pygame.image.load(actor["file"])
        actor["rect"] = actor["surf"].get_rect()
        actor["rect"].midleft = (0, (i + 1) * arena.height / 8)


def main():
    """Main game function, contains initialisations, game loop and logic."""
    global gameState
    global FERRY_STEP

    # CONTROLLER VARIABLE FOR GAME
    action = "listen"

    # INITIALISE ACTORS WITH IMAGES
    drawactors()

    # TODO REBUILD LOOP WITH NEW ACTION SYSTEM
    while True:
        if action == "listen":
            key = getKey()
            if key in gameGraph[gameState]:
                handleKeys(key)
                gameState = gameGraph[gameState][key]

            if gameGraph[gameState] == "failure":
                action = "failure"
            elif gameGraph[gameState] == "success":
                action = "success"
            else:
                action = "listen"

        if action == "failure":
            failure()
            sys.exit()

        if action == "success":
            success()
            sys.exit()

        window.fill(pygame.Color("green"))
        for actor in ACTORS:
            window.blit(actor["surf"], actor["rect"])

        pygame.display.flip()
        fpsClock.tick(120)


if __name__ == "__main__":
    main()
