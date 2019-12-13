import pygame
pygame.init()

win = pygame.display.set_mode((500,500))

pygame.display.set_caption("My First Game!!")
x = 50
y = 50
width = 40
height = 60
vel = 5
pac = pygame.image.load('pacman.bmp')
run = True

def draw():
    win.fill((0, 0, 0))
    win.blit(pac, (x, y))
    pygame.display.update()

def consume_input():
    global x
    global y
    global run
    for event in pygame.event.get() :
        if event.type == pygame.QUIT : 
            run = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] :
        x -= vel
    if keys[pygame.K_RIGHT] :
        x += vel
    if keys[pygame.K_UP] :
        y -= vel
    if keys[pygame.K_DOWN] :
        y += vel




while run :
    pygame.time.delay(40)
    consume_input()
    draw()
  

pygame.quit()