import pygame
import random
import pygame, os 

os.environ['SDL_VIDEO_WINDOW_POS'] = str(40) + "," + str(40)

#display
display_x = 500
display_y = 750

#colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (220,20,60)
green = (124, 252, 0)
blue = (0, 191, 255)
pipecolor = (34, 139,34)

#score
score = 0

#ball
pos_x = 190
pos_y = 275

#values for obsacles
x1 = 750
x2 = 920
y1 = random.choice([180, 200, 250, 320, 400, 460])
y2 = 500
#set display 
gameDisplay = pygame.display.set_mode((display_x,display_y))
pygame.display.set_caption("FappyChafita")
clock = pygame.time.Clock()

pygame.init()
font = pygame.font.SysFont(None, 20)

def end():
    pygame.display.update()
    clock.tick(10)


def ball(pos_x, pos_y):
    pygame.draw.circle(gameDisplay, ((red)), [pos_x, pos_y], 20)



def barrierCreator(x1):
    pygame.draw.rect(gameDisplay, ((pipecolor)), pygame.Rect(x1,0,40,800))
    
def gapCreator(x1,y1):
    pygame.draw.rect(gameDisplay, ((blue)), pygame.Rect(x1, y1, 40, 100))


def drawSky():
    pygame.draw.rect(gameDisplay, ((blue)), pygame.Rect(0,0, 500, 900))
    #pygame.draw.rect(gameDisplay, ((blue)), pygame.Rect(0, 0, 1750, 900))

def drawGround():
    pygame.draw.rect(gameDisplay,((green)), pygame.Rect(0, 650, 500, 100))

done = False
checker = True

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    
    #Collision Detection
    ball_rect = pygame.Rect(pos_x,pos_y, 35, 35)
    barrier_rect = pygame.Rect(x1, 0, 100, 650)
    hole_rect = pygame.Rect(x1, y1, 40, 100)
    topBarrier_rect = pygame.Rect(x1,  0, 100, y1)
    bottomBarrier_rect = pygame.Rect(x1, y1+200, 100, 800)
    invisibleBarrier_rect = pygame.Rect(0, 0, 5, 650)
    ground_rect = pygame.Rect(0, 650, 500, 100)

    text1 = font.render(str(score/10),True, ((white)))

    if ball_rect.colliderect(bottomBarrier_rect) or ball_rect.colliderect(topBarrier_rect):
        break
    if ball_rect.colliderect(ground_rect):
        break

    if ball_rect.colliderect(hole_rect):
        while checker:
            #sound.play()
            checker = False
        score = score + 1.6666666666666667 
    if not ball_rect.colliderect(hole_rect):
        checker = True

    pressed = pygame.key.get_pressed()

    y_change = 5

    if pressed[pygame.K_UP]:
        y_change = -20
    
    pos_y = y_change + pos_y

    gameDisplay.fill((white))
    drawSky()
    barrierCreator(x1)
    gapCreator(x1, y1)

    x1 = x1 - 13

    if (invisibleBarrier_rect.colliderect(bottomBarrier_rect) or invisibleBarrier_rect.colliderect(topBarrier_rect)):
        x1 = 950
        y1 = random.choice([140, 200, 250, 320, 400, 420])
        barrierCreator(x1)
        gapCreator(x1, y1)
    drawGround()
    ball(pos_x, pos_y)

    gameDisplay.blit(text1, (200 - text1.get_width() // 2, 50 - text1.get_height()// 2))

    pygame.display.flip()
    end()

text = font.render("GG! Score: " + str(score/10), True, ((black)))

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    gameDisplay.fill((white))    
    gameDisplay.blit(text,(200 - text.get_width() // 2 , 500 - text.get_height() // 2))
    pygame.display.flip()
    end()
pygame.quit()
