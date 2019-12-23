import pygame
from state import State
from pacman import Pacman
from wall import Wall
from ghost import Ghost

class Engine:
    class __Engine():
        def __init__(self, win):
            self.win = win
            self.block_size = 24
            self.win = win
            self.state_stack = []
            self.quit_requested = False

        def get_state(self):
            return self.state_stack[-1]

        def check_quit(self):
            for event in pygame.event.get() :
                if event.type == pygame.QUIT : 
                    self.quit_requested = True

        def load_map(self, game_state):
            self.map = [['' for _ in range(32)] for _ in range(32)]
            with open('mapa.txt') as f:
                first_line = f.readline()
                self.rows, self.cols = map(int, first_line.split())
                for row in range(self.rows):
                    line = f.readline()
                    for col in range(self.cols):
                        if line[col] == 'W':
                            game_state.add_go(Wall('parede.png', col*self.block_size, row*self.block_size))
                            self.map[row][col] = 'Wall'
                        else :
                            self.map[row][col] = 'Empty'
                            
        def loop(self):
            game_state = State()
            self.load_map(game_state)
            game_state.add_go(Ghost('azul.png',11*self.block_size, 11*self.block_size))
            game_state.add_go(Ghost('verde.png',12*self.block_size, 11*self.block_size))
            game_state.add_go(Ghost('vermelho.png',19*self.block_size, 11*self.block_size))
            game_state.add_go(Ghost('rosa.png',20*self.block_size, 11*self.block_size))
            game_state.add_go(Pacman('pacman.png', 1*self.block_size, 1*self.block_size))
            self.state_stack.append(game_state)
            while not self.quit_requested : 
                self.win.fill((0, 0, 0))
                self.check_quit()
                self.get_state().update()
                self.get_state().draw()
                pygame.display.update()
                pygame.time.delay(20)

    instance = None
    def __init__(self, win):
        if not Engine.instance:
            Engine.instance = Engine.__Engine(win)
        else:
            Engine.instance.win = win
        print(type(Engine.instance))
    def __getattr__(self, name):
        return getattr(self.instance, name)