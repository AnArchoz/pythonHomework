import pygame

# Define constants and colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
SIZE = (600, 350)
CENTER_RESET = (300, 250)
LEFT_PLAYER_POSITION = (75, 175)
RIGHT_PLAYER_POSITION = (525, 175)
LEFT_TEXT_POSITION = (125, 50)
RIGHT_TEXT_POSITION = (475, 50)
WELCOME_POSITION = (300, 100)

# Initialise Pygame, set up the window and running conditions
pygame.init()
screen = pygame.display.set_mode(SIZE)
win = screen.get_rect()
pygame.display.set_caption("Pong")
pygame.key.set_repeat(10, 60)
fps = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 18)

# Create ball and player objects.
ball = pygame.Rect(0, 0, 10, 10)
player1 = pygame.Rect(0, 0, 10, 50)
player2 = pygame.Rect.copy(player1)

# Movement vector for the ball.
# Vertical and horizontal movement, and pixels per tick.
VEC = [3, 3]

# Initialise position of ball and player objects
player2.center = RIGHT_PLAYER_POSITION
player1.center = LEFT_PLAYER_POSITION
ball.center = CENTER_RESET


def resetPositions():
    """Resets position of all game objects after a goal is scored"""
    player2.center = RIGHT_PLAYER_POSITION
    player1.center = LEFT_PLAYER_POSITION
    ball.center = CENTER_RESET
    pygame.time.delay(500)


def drawObjects(p1score, p2score):
    """Draws all game objects on a black screen, and fixes FPS to 60"""
    # Clear the screen to black
    screen.fill(BLACK)

    # Initialise text and update player scores
    welcomeText = font.render("Best of 3 wins the game. Good luck!", True, WHITE)
    p1ScoreText = font.render("W+S KEYS. Score: " + str(p1score), True, RED)
    p2ScoreText = font.render("UP-DOWN KEYS. Score: " + str(p2score), True, RED)
    welcomeBox = welcomeText.get_rect()
    p1Box = p1ScoreText.get_rect()
    p2Box = p2ScoreText.get_rect()
    welcomeBox.center = WELCOME_POSITION
    p1Box.center = LEFT_TEXT_POSITION
    p2Box.center = RIGHT_TEXT_POSITION

    # Draw player, ball, and text objects onto the screen
    pygame.draw.rect(screen, WHITE, player1)
    pygame.draw.rect(screen, WHITE, player2)
    pygame.draw.rect(screen, WHITE, ball)
    screen.blit(p1ScoreText, p1Box)
    screen.blit(p2ScoreText, p2Box)
    screen.blit(welcomeText, welcomeBox)
    pygame.display.flip()
    fps.tick(60)


def handleKeyEvents(event):
    global player1
    global player2

    # Amount of pixels the players move every tick
    step = 2

    if event.type == pygame.KEYDOWN:
        # Key events for player 2
        if event.key == pygame.K_UP:
            player2 = player2.move(0, -step)
        if event.key == pygame.K_DOWN:
            player2 = player2.move(0, +step)
        # Key events for player 1
        if event.key == pygame.K_w:
            player1 = player1.move(0, -step)
        if event.key == pygame.K_s:
            player1 = player1.move(0, +step)
        if event.key == pygame.K_ESCAPE:
            exit()


def main():
    """Main game loop. Controls movement of all objects and game logic."""

    global ball

    # Loop condition - will continue running until either a player
    # scores 3 total goals, or exits by pressing ESC-key
    continueRunning = True

    # Initialise player score to 0
    p1score = 0
    p2score = 0

    # Start of game loop
    while continueRunning:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or p1score == 3 or p2score == 3:
                continueRunning = False

        handleKeyEvents(event)

        # Movement of the ball using the vector
        ball = ball.move(VEC)

        # Increment score after goal and change direction on kickoff after reset
        if ball.left < 0:
            p2score = p2score - -1
            VEC[0] = -VEC[0]
            resetPositions()

        if ball.right > win.right:
            p1score = p1score - -1
            VEC[0] = -VEC[0]
            resetPositions()

        # Ball bouncing mechanics
        if ball.top < 0 or ball.bottom > win.bottom:
            VEC[1] = -VEC[1]
        if player2.colliderect(ball) or player1.colliderect(ball):
            VEC[0] = -VEC[0]

        drawObjects(p1score, p2score)


if __name__ == "__main__":
    main()