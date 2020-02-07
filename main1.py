import pygame
import random
from os import path

"""Created by Antoine Rebelo in February 2020.
    Python mutation of Space Invaders
    ___________Version 1.0____________"""

# Create paths to image and soundfolders for easy access
imgDir = path.join(path.dirname(__file__), 'img')
soundDir = path.join(path.dirname(__file__), 'sounds')

# Define constants and colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
SIZE = (800, 500)
CENTER_RESET = (400, 450)
ALIEN_CENTER = (400, 75)
SCORE_POSITION = (125, 450)
LEVEL_POSITION = (675, 450)
LIVES_POSITION = (400, 425)

# Initialise Pygame, set up the window and running conditions
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode(SIZE)
window = screen.get_rect()
pygame.display.set_caption("Space invaders")
fps = pygame.time.Clock()
FONT = pygame.font.Font('freesansbold.ttf', 18)
background = pygame.image.load(path.join(imgDir, 'space.jpg'))

# Load Image files for player and aliens
playerImage = pygame.image.load(path.join(imgDir, "player.png"))
alienImage = pygame.image.load(path.join(imgDir, "alien.png"))

# Create data structures for small and large
# explosion animations and loads them
explosionAnimation = {}
explosionAnimation['large'] = []
explosionAnimation['small'] = []
for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(imgDir, filename)).convert()
    img.set_colorkey(BLACK)
    imgLarge = pygame.transform.scale(img, (75, 75))
    explosionAnimation['large'].append(imgLarge)
    imgSmall = pygame.transform.scale(img, (32, 32))
    explosionAnimation['small'].append(imgSmall)

# Load sound files
shootSound = pygame.mixer.Sound(path.join(soundDir, "bulletSound.wav"))
deathSound = pygame.mixer.Sound(path.join(soundDir, "Explosion.wav"))

# Win/Lose conditions, score counter and level counter
level = 1
score = 0
bounty = 15
running = False
victory = False
failure = False


# Classes representing all actor- and projectile objects
class Player(pygame.sprite.Sprite):
    """Class representing the player object
        used to shoot down the awful aliens."""

    # Constructor for Player object
    def __init__(self):
        # Call superclass from Sprite
        pygame.sprite.Sprite.__init__(self)
        # Scales the image down
        self.image = pygame.transform.scale(playerImage, (45, 35))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = CENTER_RESET
        self.speedx = 0
        # Delay for autofire so you can't laserbeam-spam
        self.delay = 300
        self.lastShot = pygame.time.get_ticks()
        # Timer and check for hiding yourself when you lose a life
        self.hidden = False
        self.hideTimer = pygame.time.get_ticks()
        self.lives = 3

    def update(self):
        # If you lost a life, you hide out of bounds for 1 second
        if self.hidden and pygame.time.get_ticks() - self.hideTimer > 1000:
            self.hidden = False
            self.rect.center = CENTER_RESET
        self.speedx = 0
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.speedx = -4
        if key[pygame.K_RIGHT]:
            self.speedx = 4
        if key[pygame.K_SPACE]:
            self.shoot()
        self.rect.x += self.speedx

        # Going out of bounds is cheating
        if self.rect.right > SIZE[0]:
            self.rect.right = SIZE[0]
        elif self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        """Method for shooting a small bullet
            that travels upwards 5 pixels per frame"""

        # Autofire check
        now = pygame.time.get_ticks()
        if now - self.lastShot > self.delay:
            self.lastShot = now
            bullet = Bullet(self.rect.centerx, self.rect.top, -5)
            allSprites.add(bullet)
            bullets.add(bullet)
            # Pew pew
            shootSound.play()

    def hide(self):
        # Hide player during explosion, respawn in the middle
        self.hidden = True
        self.hideTimer = pygame.time.get_ticks()
        self.rect.center = (SIZE[0] / 2, SIZE[1] + 200)


class Alien(pygame.sprite.Sprite):
    """Class representing the alien objects
        that will spawn in a group of invaders"""

    # Constructor for alien class
    def __init__(self, x, y, level):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(alienImage, (30, 25))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        # Randomise speed so all aliens move differently
        speed = random.choice([(-2, -1), (1, 2)])
        # Have to skip 0 so they don't stand still
        self.speedVector = [random.randint(*speed) * level, 35]
        self.rect.centerx = x
        self.rect.centery = y
        # Randomised autofire delay so all shoot differently
        # and also so no one has laserbeams
        self.delay = random.randint(500, 2000) + random.randint(500, 7000)
        self.lastShot = pygame.time.get_ticks()

    def shoot(self):
        """Identical shooting method as the player"""

        # Autofire check
        now = pygame.time.get_ticks()
        if now - self.lastShot > self.delay:
            self.lastShot = now
            bullet = alienBullet(self.rect.centerx, self.rect.bottom + 5, 5)
            allSprites.add(bullet)
            alienBullets.add(bullet)
            # PEW PEW
            shootSound.play()

    def update(self):
        # Move downwards a few pixels when they
        # reach either side of the window
        if self.rect.left < 20 or self.rect.right > 780:
            self.speedVector[0] = -self.speedVector[0]
            self.rect.y += self.speedVector[1]

        self.rect.x += self.speedVector[0]
        self.shoot()


class Bullet(pygame.sprite.Sprite):
    """Bullet class used by the player when firing weapons."""

    # Constructor
    def __init__(self, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((5, 5))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        # Spawn at the top of the player ship
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = speed

    def update(self):
        self.rect.y += self.speedy

        # Destroy the sprite if it goes out of bounds
        if self.rect.bottom < 0:
            self.kill()
        if self.rect.top > 500:
            self.kill()


class alienBullet(pygame.sprite.Sprite):
    """Bullet class used by aliens, almost identical"""

    # Constructor
    def __init__(self, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((5, 5))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        # Spawn at bottom of alien ship
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = speed

    def update(self):
        self.rect.y += self.speedy

        # Die if goes off screen
        if self.rect.bottom < 0:
            self.kill()
        if self.rect.top > 500:
            self.kill()


class Explosion(pygame.sprite.Sprite):
    """Explosion class instantiated everytime
        an actor dies from a bullet, animated
            from a dictionary using 9 images"""

    # Constructor
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        # Access the dictionary
        self.image = explosionAnimation[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        # Speed of animation check
        self.frame = 0
        self.lastUpdate = pygame.time.get_ticks()
        self.frameRate = 50

    def update(self):
        """Checks the frame if it can still animate,
            kills itself if final image is used"""
        now = pygame.time.get_ticks()
        if now - self.lastUpdate > self.frameRate:
            self.lastUpdate = now
            self.frame += 1
            if self.frame == len(explosionAnimation[self.size]):
                # Boom
                self.kill()
            else:
                center = self.rect.center
                self.image = explosionAnimation[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


# Create sprite groups for my actors for easier manipulation
allSprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
playerGroup = pygame.sprite.Group()
alienBullets = pygame.sprite.Group()

# Add player to sprite group
player = Player()
playerGroup.add(player)
allSprites.add(player)


def resetGame():
    """Method for adding all actors to
        their relevant Sprite group and
            populating the screen with aliens"""

    global player

    allSprites.empty()
    enemies.empty()
    playerGroup.add(player)
    allSprites.add(player)
    repopulate()


def repopulate():
    """adds 6*6 aliens on the screen at random
        locations on the X axis and toggles the
            correct difficulty based on the current level."""

    global level
    for i in range(6):
        for j in range(6):
            x = random.randint(60, window.width-60)
            y = (j + 1) * window.height/2/7
            n = Alien(x, y, level)
            allSprites.add(n)
            enemies.add(n)


def showFailure():
    """Text to show when you lose."""
    FONT = pygame.font.Font('freesansbold.ttf', 35)
    screen.blit(background, (0, 0))
    failureText = FONT.render("FAILURE!! Final score: " + str(score), True, RED)
    failureBox = failureText.get_rect()
    failureBox.center = (window.width/2, window.height/2)
    screen.blit(failureText, failureBox)


def showVictory():
    """Text to show when you win."""
    FONT = pygame.font.Font('freesansbold.ttf', 35)
    screen.blit(background, (0, 0))
    victoryText = FONT.render("You have VICTORY! \
                            Final score: " + str(score), True, GREEN)
    victoryBox = victoryText.get_rect()
    victoryBox.center = (window.width/2, window.height/2)
    screen.blit(victoryText, victoryBox)


def showWelcome():
    """Text to show as welcome screen,
        contains rules and instructions"""

    FONT = pygame.font.Font('freesansbold.ttf', 20)
    screen.blit(background, (0, 0))
    welcomeText = FONT.render("Welcome to Space Invaders!", True, WHITE)
    controlText = FONT.render("Control your spaceship with left \
                        & right keys, shoot with Spacebar.", True, WHITE)
    levelText = FONT.render("There are 3 waves of dangerous aliens to beat.\
                                        Good luck!", True, WHITE)
    continueText = FONT.render("Press SPACE to begin the game!", True, WHITE)

    welcomeBox = welcomeText.get_rect()
    continueBox = continueText.get_rect()
    levelBox = levelText.get_rect()
    controlBox = controlText.get_rect()

    welcomeBox.center = (window.width/2, window.height/2)
    levelBox.center = (window.width/2, window.height/2 + 50)
    controlBox.center = (window.width/2, window.height/2 + 25)
    continueBox.center = (window.width/2, window.height/2 + 75)
    screen.blit(welcomeText, welcomeBox)
    screen.blit(controlText, controlBox)
    screen.blit(levelText, levelBox)
    screen.blit(continueText, continueBox)


def updateScore(points):
    """Just updates the score"""
    global score

    if points == 0:
        score = 0
    else:
        score += points


def drawScore(points, level, playerLives):
    """Displays the score, level number and
        amount of lives player has left,
            at the bottom of the window"""

    levelText = FONT.render("LEVEL: " + str(level), True, WHITE)
    levelRect = levelText.get_rect()
    levelRect.center = LEVEL_POSITION
    scoreText = FONT.render("SCORE: " + str(points), True, WHITE)
    scoreRect = scoreText.get_rect()
    scoreRect.center = SCORE_POSITION
    livesText = FONT.render("LIVES LEFT: " + str(playerLives), True, WHITE)
    livesRect = livesText.get_rect()
    livesRect.center = LIVES_POSITION

    screen.blit(livesText, livesRect)
    screen.blit(levelText, levelRect)
    screen.blit(scoreText, scoreRect)


def victoryScreen():
    """Displays the victory screen and
        awaits input before closing"""
    global running
    global victory

    showVictory()
    while victory:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()
                if event.key == pygame.K_SPACE:
                    victory = False
        pygame.display.flip()


def failureScreen():
    """Displays the losing screen and
        awaits input before closing"""
    global running
    global failure

    showFailure()
    while failure:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()
                if event.key == pygame.K_SPACE:
                    failure = False
        pygame.display.flip()


def welcomeScreen():
    """Displays the welcome screen
        and awaits input before closing"""
    global running

    welcome = True
    screen.blit(background, (0, 0))
    showWelcome()
    while welcome:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()
                if event.key == pygame.K_SPACE:
                    running = True
                    welcome = False
        pygame.display.flip()


def main():
    """Main game loop. Controls the game states
        and acts accordingly, controls and checks for collisions between
        actors and objects, and updates all sprites and animations """
    global running
    global victory
    global failure
    global level

    resetGame()
    welcomeScreen()
    while running:
        # Keep game at 60 fps
        fps.tick(60)
        # Background Image
        screen.blit(background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()

        # Enemies hit with a bullet explode beautifully
        hits = pygame.sprite.groupcollide(bullets, enemies, True, True)
        for hit in hits:
            deathSound.play()
            # 15 points per alien, times the current level
            updateScore(bounty * level)
            expl = Explosion(hit.rect.center, 'small')
            allSprites.add(expl)
            if not enemies:
                # If all enemies are killed on level 3
                # You have won the game. Congratulations
                if level == 3:
                    running = False
                    victory = True
                # If all enemies are killed, to go next level
                level += 1
                resetGame()

        # If enemies reach the player, you instantly lose
        collision = pygame.sprite.groupcollide(
                                        playerGroup,
                                        enemies,
                                        True, True,
                                        pygame.sprite.collide_circle)
        if collision:
            deathSound.play()
            expl = Explosion(hit.rect.center, 'large')
            allSprites.add(expl)
            player.kill()

        # If player is hit by enemy bullets your HP is decreased
        # starting from 3 to 0, then you explode and lose
        shotDown = pygame.sprite.groupcollide(playerGroup, alienBullets,
                                              False,
                                              True,
                                              pygame.sprite.collide_circle
                                              )
        for hit in shotDown:
            deathSound.play()
            expl = Explosion(hit.rect.center, 'large')
            player.lives -= 1
            player.hide()
            allSprites.add(expl)

        # To make sure the explosion animation
        # fully finishes when you die
        if player.lives == 0 and not expl.alive():
            running = False
            failure = True

        # Update all the graphics and sprites on the screen
        drawScore(score, level, player.lives)
        allSprites.update()
        allSprites.draw(screen)
        pygame.display.flip()

    while victory:
        victoryScreen()
    while failure:
        failureScreen()


if __name__ == "__main__":
    main()
