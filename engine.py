import pygame
from state import State
from pacman import Pacman
from wall import Wall

class Engine():
    block_size = 24
    win = None
    state_stack = []
    quit_requested = False
    def __init__(self, win):
        Engine.win = win
        Engine.state_stack = []
        Engine.quit_requested = False
        self.loop()

    def check_quit(self):
        for event in pygame.event.get() :
            if event.type == pygame.QUIT : 
                self.quit_requested = True

    def load_map(self, game_state):
        Engine.map = [['' for _ in range(32)] for _ in range(32)]
        row = -1
        with open('mapa.txt') as f:
            first_line = f.readline()
            rows, cols = map(int, first_line.split())
            print(rows, cols)
            for row in range(rows):
                line = f.readline()
                for col in range(cols):
                    if line[col] == 'W':
                        game_state.add_go(Wall('parede.png', col*Engine.block_size, row*Engine.block_size))
                        Engine.map[row][col] = 'Wall'
                    else :
                        Engine.map[row][col] = 'Empty'
                        
                

    def loop(self):
        game_state = State()
        self.load_map(game_state)
        game_state.add_go(Pacman('pacman.bmp', 1*Engine.block_size, 1*Engine.block_size))
        Engine.state_stack.append(game_state)
        while not self.quit_requested : 
            Engine.win.fill((0, 0, 0))
            self.check_quit()
            self.state_stack[-1].update()
            self.state_stack[-1].draw()
            pygame.display.update()
            pygame.time.delay(20)
