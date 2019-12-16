import pygame
from game_object import GameObject

class Pacman(GameObject):

    def __init__(self, sprite_path, x, y):
        super().__init__(sprite_path, x, y)
        self.__dir = (0, 0)
        self.__wdir = (0, 0)
        self.__speed = 4

    def draw(self):
        from engine import Engine
        Engine.win.blit(self.sprite.sp, (self.x, self.y))

    def get_collider_candidates(self, newy, newx, dir):
        from engine import Engine
        upper_left = (newy, newx)
        upper_right = (newy, newx + Engine.block_size - 1)
        lower_left = (newy + Engine.block_size - 1, newx)
        lower_right = (newy + Engine.block_size - 1, newx + Engine.block_size - 1)
        if dir == (0,1):
            return (upper_right, lower_right) 
        elif dir == (1,0):
            return(lower_left, lower_right)
        elif dir == (0, -1):
            return (upper_left, lower_left)
        elif dir == (-1,0):
            return (upper_left, upper_right)
        return None
            
    def move_collides(self, newy, newx, dir):
        from engine import Engine
        if dir == (0,0):
            return False
        pointA, pointB = self.get_collider_candidates(newy, newx, dir)
        blockA = (pointA[0]//Engine.block_size, pointA[1]//Engine.block_size)
        blockB = (pointB[0]//Engine.block_size, pointB[1]//Engine.block_size)

        return (Engine.map[blockA[0]][blockA[1]] == 'Wall'
            or Engine.map[blockB[0]][blockB[1]] == 'Wall')

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] :
            self.__wdir = (0, -1)
        if keys[pygame.K_RIGHT] :
            self.__wdir = (0, 1)
        if keys[pygame.K_UP] :
            self.__wdir = (-1, 0)
        if keys[pygame.K_DOWN] :
            self.__wdir = (1, 0)
        
        newy = self.__dir[0] * self.__speed + self.y
        newx = self.__dir[1] * self.__speed + self.x
        wantedy = self.__wdir[0] * self.__speed + self.y
        wantedx = self.__wdir[1] * self.__speed + self.x
        if(not self.move_collides(wantedy, wantedx, self.__wdir)):
            self.y = wantedy
            self.x = wantedx
            self.__dir = self.__wdir
        elif(not self.move_collides(newy, newx, self.__dir)):
            self.y = newy
            self.x = newx



        


            