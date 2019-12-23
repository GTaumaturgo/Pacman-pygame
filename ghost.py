from game_object import GameObject
from queue import Queue
from collections import defaultdict
class Ghost(GameObject):
    def __init__(self, sprite_path, x, y):
        super().__init__(sprite_path, x, y)
        Ghost.__MOVING = 1
        Ghost.__NOT_MOVING = 0
        Ghost.__MOVES = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.__state = Ghost.__NOT_MOVING
        self.__count = 0
        self.__dir = (0,0)
        self.__speed = 3

    def valid(self, position):
        from engine import Engine
        return (position[0] >= 0 
                    and position[0] < 24
                    and position[1] >= 0
                    and position[1] < 32
                    and Engine.instance.map[position[0]][position[1]] != 'Wall')

    def contains_pacman(self, position):
        from engine import Engine
        for go in Engine.instance.get_state().go_list:
            block_pos = (go.y // Engine.instance.block_size, go.x // Engine.instance.block_size)
            if(block_pos == position and go.id() == 'Pacman'):
                return True
        return False
    
    def bfs_closest_pacman(self, start):
        from engine import Engine
        start = (self.y // Engine.instance.block_size, self.x // Engine.instance.block_size)
        q = Queue()
        q.put(start)
        par = defaultdict(lambda : None)
        par[start] = start
        while not q.empty():
            front = q.get()
            if self.contains_pacman(front):
                return (front, par)
            for move in Ghost.__MOVES:
                position = (move[0] + front[0], move[1] + front[1])
                if self.valid(position) and par[position] == None :
                    par[position] = front
                    q.put(position)
        raise PacmanNotFoundException     
    
    def get_optimal_dir(self, start, res, parents):
        if res == start:
            return (0,0)
        while(parents[res] != start):
            res = parents[res]
        return (res[0] - start[0], res[1] - start[1])     

    def update(self):
        from engine import Engine
        if self.__state == Ghost.__MOVING:
            self.y += self.__speed * self.__dir[0]
            self.x += self.__speed * self.__dir[1]
            self.__count -= 1
            if self.__count == 0:
                self.__state = Ghost.__NOT_MOVING
        else:
            start = (self.y // Engine.instance.block_size, self.x // Engine.instance.block_size)
            res, parents = self.bfs_closest_pacman(start)
            self.__dir = self.get_optimal_dir(start, res, parents)
            print(self.__dir)
            self.__state = Ghost.__MOVING
            self.__count = 8

    def draw(self):
        from engine import Engine
        Engine.instance.win.blit(self.sprite.sp, (self.x, self.y))
    
    def id(self):
        return 'Ghost'
    
    