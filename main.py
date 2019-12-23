import pygame
from engine import Engine
pygame.init()


win = pygame.display.set_mode((768, 768))

pygame.display.set_caption("My First Game!!")

eng = Engine(win)
eng.loop()
pygame.quit()