import sys
import pygame


def getkey():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # pygame.image.save(window, "game-over.bmp")
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                sys.exit()
            if event.key in controls:
                key = controls[event.key]
                return key


def ferry(who, step):
    done = False
    for actor in who:
        actor["rect"] = actor["rect"].move((step, 0))
        if not arena.contains(actor["rect"]):
            actor["rect"] = actor["rect"].move((-step, 0))
            actor["surf"] = pygame.transform.flip(actor["surf"], True, False)
            done = True
    return done


def failure():
    myfont = pygame.font.Font('freesansbold.ttf', 48)
    msg = myfont.render("Failure", True, (255, 0, 0))
    msg_box = msg.get_rect()
    msg_box.center = arena.center
    window.blit(msg, msg_box)
    pygame.display.flip()
    pygame.time.wait(1000)

def success():
    myfont = pygame.font.Font('freesansbold.ttf', 48)
    msg = myfont.render("Success", True, (255, 255, 255))
    msg_box = msg.get_rect()
    msg_box.center = arena.center
    window.blit(msg, msg_box)
    pygame.display.flip()
    pygame.time.wait(1000)

pygame.init()
window = pygame.display.set_mode((640, 480))
arena = window.get_rect()

wolf = {"file": "wolf.png"}
goat = {"file": "goat.png"}
cabb = {"file": "cabb.png"}
farm = {"file": "farm.png"}

actors = [wolf, goat, cabb, farm]

for i, actor in enumerate(actors):
    actor["surf"] = pygame.image.load(actor["file"])
    actor["rect"] = actor["surf"].get_rect()
    actor["rect"].midleft = (0, (i+1)*arena.height/5)

gamegraph = {
            "wgcf-": {"f": "wgc-f", "w": "gc-wf", "g": "wc-gf", "c": "wg-cf"},
            "wc-gf": {"f": "wcf-g", "g": "wgcf-"},
            "wcf-g": {"f": "wc-gf", "c": "w-gcf", "w": "c-wgf"},
            "w-gcf": {"g": "wgf-c", "c": "wcf-g"},
            "c-wgf": {"g": "gcf-w", "w": "wcf-g"},
            "wgf-c": {"w": "g-wcf", "g": "w-gcf"},
            "gcf-w": {"c": "g-wcf", "g": "c-wgf"},
            "g-wcf": {"f": "gf-wc", "c": "gcf-w", "w": "wgf-c"},
            "gf-wc": {"g": "-wgcf", "f": "g-wcf"},
            "wgc-f": "failure",
            "cf-wg": "failure",
            "gc-wf": "failure",
            "wf-gc": "failure",
            "wg-cf": "failure",
            "f-wgc": "failure",
            "-wgcf": "success"
            }

gamestate = "wgcf-"
controls = {pygame.K_f: "f", 
            pygame.K_g: "g",
            pygame.K_w: "w",
            pygame.K_c: "c"}
passengers = {"f": [farm],
                "g": [farm, goat],
                "w": [farm, wolf],
                "c": [farm, cabb]}
ferry_step = -5
action = "listen"

fpsClock = pygame.time.Clock()
while True:
    if action == "listen":
        key = getkey()
        if key in gamegraph[gamestate]:
            gamestate = gamegraph[gamestate][key]
            ferry_who = passengers[key]
            ferry_step = -ferry_step
            action = "ferry"

    if action == "ferry":
        done = ferry(ferry_who, ferry_step)
        if done:
            if gamegraph[gamestate] == "failure":
                action = "failure"
                
            elif gamegraph[gamestate] == "success":
                print("does it work LOLOL")
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
    for actor in actors:
        window.blit(actor["surf"], actor["rect"])

    pygame.display.flip()
    fpsClock.tick(120)
