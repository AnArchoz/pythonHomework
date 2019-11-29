import pygame, sys
black = (0, 0, 0); white = (255, 255, 255); red = (255, 0, 0)
pygame.init()

scr = pygame.display.set_mode((360, 240))
win = scr.get_rect()

box2 = pygame.Rect( 0, 0, 30, 60)
box2.midleft = win.midleft

vec = [1,0]
pygame.key.set_repeat(50,50)
fps = pygame.time.Clock()

myfont = pygame.font.Font('freesansbold.ttf', 13)
msg = myfont.render("The Game !!!", True, red)

box1 = msg.get_rect()
box1.center = win.center

step = 1

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    scr.blit(msg, box1)
    box1 = box1.move(vec)
    
    if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                box2 = box2.move(-step,0)
            if event.key == pygame.K_RIGHT:
                box2 = box2.move(+step,0)
            if event.key == pygame.K_UP:
                box2 = box2.move(0, -step)
            if event.key == pygame.K_DOWN:
                box2 = box2.move(0, +step)
            if event.key == pygame.K_ESCAPE:
                sys.exit()
                
    if not win.contains(box1):
        vec[0] = -vec[0]

    if box1.colliderect(box2):
        vec[0] = -vec[0]

    scr.fill(black)
    scr.blit(msg, box1)
    pygame.draw.rect(scr,white,box2)
    pygame.display.flip()
    fps.tick(200)
