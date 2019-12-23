import pygame
from game_object import GameObject
class Wall(GameObject) : 
    def update(self):
        pass
    
    def draw(self):
        from engine import Engine
        Engine.instance.win.blit(self.sprite.sp, (self.x, self.y))

    def id(self):
        return 'Wall'