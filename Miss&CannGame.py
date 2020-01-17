import random
import sys

import pygame

import Resources

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
boat = {"file": "Boat.png"}

# CONSTANTS
ACTORS = [cann1, cann2, cann3, miss1, miss2, miss3, boat]
CANNIBALS = [cann1, cann2, cann3]
MISSIONARIES = [miss1, miss2, miss3]
BOAT_LEFT = (200, 50)
BOAT_RIGHT = (50, 50)

# COLOUR AND TEXT FOR WELCOME SCREEN
WHITE = (255, 255, 255)
WELCOME_TEXT_POSITION = (320, 100)
WELCOME_TEXT = getattr(Resources, "WELCOME_TEXT")
FONT = pygame.font.Font('freesansbold.ttf', 18)

# GAME CONTROLS FOR ACTORS AND BOAT
CONTROLS = {pygame.K_e: "e",  # empty boat
            pygame.K_SPACE: " ",  # ferry boat
            pygame.K_m: "m",  # add missionary
            pygame.K_c: "c"}  # add cannibal

# PIXEL MOVEMENT OF BOAT WITH PASSENGERS
FERRY_STEP = -5

# INITIAL ACTOR STATE; ALL 6 ACTORS ON THE LEFT SIDE OF THE RIVER
startLineup = [[cann1, cann2, cann3], [miss1, miss2, miss3, boat]]
otherSide = [[], []]

# HAHA OVER-THINKING LEADS TO FUNNY THINGS
ferry = [boat]

# GAME GRAPH TREE WITH ALL PLAYABLE POSSIBILITIES
# NOT VERY READABLE AND NOT IN ORDER,
gameGraph = getattr(Resources, "graph")

# INITIAL GAME STATE, ALL ACTORS ON THE LEFT SIDE OF THE RIVER
gameState = "3, 3, 0, 0, 0"


def getKey():
    """Fetch pressed keys from pygame events and either
        close the game or return a key value to be used."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # pygame.image.save(window, "game-over.bmp")
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()
            if event.key in CONTROLS:
                key = CONTROLS[event.key]
                return key


def handleKeys(key):
    """Executes an action according to each keypress:
        Ferry, empty, or fill the boat."""

    global gameState
    global ferry

    if key in gameGraph[gameState]:
        if key == "c" or key == "m":
            if len(ferry) < 3:
                fillBoat(key)
            else:
                return
        elif key == " ":
            if len(ferry) > 1:
                moveBoat(ferry)
        elif key == "e":
            emptyBoat()

        gameState = gameGraph[gameState][key]
        print(gameState)

    if gameGraph[gameState] == "failure":
        action = "failure"
    elif gameGraph[gameState] == "success":
        action = "success"
    else:
        action = "listen"

    return action


def fillBoat(key):
    """Add either a cannibal or missionary to the boat
        for a maximum of 2 passengers"""
    global ferry

    if key == "c":
        if boat in startLineup:
            if any(cannibal in startLineup[0] for cannibal in CANNIBALS):
                cann = random.choice(startLineup[0])
                startLineup[0].remove(cann)
                ferry.append(cann)
        elif boat in otherSide:
            if any(cannibal not in startLineup[0]
                   and cannibal not in ferry
                   for cannibal in CANNIBALS):
                cann = random.choice(otherSide[0])
                otherSide[0].remove(cann)
                ferry.append(cann)

    elif key == "m":
        if boat in startLineup:
            if any(missionary in startLineup[1] for missionary in MISSIONARIES):
                miss = random.choice(startLineup[1])
                startLineup[1].remove(miss)
                ferry.append(miss)
        elif boat in otherSide:
            if any(missionary not in startLineup[1]
                   and missionary not in ferry
                   for missionary in MISSIONARIES):
                miss = random.choice(otherSide[1])
                otherSide[1].remove(miss)
                ferry.append(miss)


def emptyBoat():
    """Unloads all passengers from the boat
        onto either of the two sides."""
    if boat in startLineup:
        for actor in ferry:
            if actor is not boat:
                if actor in CANNIBALS:
                    startLineup[0].append(actor)
                elif actor in MISSIONARIES:
                    startLineup[1].append(actor)

                ferry.remove(actor)
    else:
        for actor in ferry:
            if actor is not boat:
                if actor in CANNIBALS:
                    otherSide[0].append(actor)
                elif actor in MISSIONARIES:
                    otherSide[0].append(actor)

                ferry.remove(actor)


def drawWelcomeScreen():
    """Displays welcome text and instructions"""
    welcomeText = FONT.render(WELCOME_TEXT, True, WHITE)
    welcomeBox = welcomeText.get_rect()
    welcomeBox.center = WELCOME_TEXT_POSITION
    window.blit(welcomeText, welcomeBox)


def moveBoat(passengers):
    """Moves the boat across the river
        containing between one or two passengers."""
    for actor in passengers:
        if boat in startLineup:
            while actor["rect"].center is not BOAT_RIGHT[0]:
                actor["rect"] = actor["rect"].move((FERRY_STEP, 0))

            startLineup[1].remove(boat)
            otherSide[1].append(boat)
            actor["surf"] = pygame.transform.flip(actor["surf"], True, False)
        else:
            while actor["rect"].center is not BOAT_LEFT[0]:
                actor["rect"] = actor["rect"].move((-FERRY_STEP, 0))

            otherSide[1].remove(boat)
            startLineup[1].append(boat)
            actor["surf"] = pygame.transform.flip(actor["surf"], True, False)

        window.blit(actor["surf"], actor["rect"])
        pygame.display.flip()


def failure():
    """Displays a screen for when you lose the game:
        Cannibals successfully eat missionary/ies."""
    myfont = pygame.font.Font('freesansbold.ttf', 48)
    msg = myfont.render("Failure", True, (255, 0, 0))
    msg_box = msg.get_rect()
    msg_box.center = arena.center
    window.blit(msg, msg_box)
    pygame.display.flip()
    pygame.time.wait(2000)


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
    pygame.time.wait(2000)


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

    # CONTROLLER VARIABLE FOR GAME
    action = "listen"

    # INITIALISE ACTORS WITH IMAGES
    drawactors()

    while True:
        if action == "listen":
            key = getKey()
            action = handleKeys(key)

        if action == "failure":
            failure()
            sys.exit()

        if action == "success":
            success()
            sys.exit()

        window.fill(pygame.Color("green"))

        for actor in ACTORS:
            window.blit(actor["surf"], actor["rect"])

        # drawWelcomeScreen()
        pygame.display.flip()
        fpsClock.tick(120)


if __name__ == "__main__":
    main()
