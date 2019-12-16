import game_object

class Ghost(GameObject):
    
    def update(self):
        pass

    def draw(self):
        from engine import Engine
        Engine.win.blit(self.sprite.sp, (self.x, self.y))
    
    
    