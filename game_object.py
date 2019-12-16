import pygame
from sprite import Sprite

class GameObject():
    
    def __init__(self, sprite_path, x, y):
        self.sprite = Sprite(sprite_path)
        self.x = x
        self.y = y

    def id(self):
        raise MethodNotImplementedException
    
    def update(self):
        raise MethodNotImplementedException

    def draw(self):
        raise MethodNotImplementedException