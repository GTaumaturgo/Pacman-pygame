from game_object import GameObject
from queue import Queue
from collections import defaultdict


class Ghost(GameObject):
    calculated = None
    best_moves = None
    __MOVING = 1
    __NOT_MOVING = 0
    __MOVES = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    def __init__(self, sprite_path, x, y):
        super().__init__(sprite_path, x, y)
        if not Ghost.calculated: 
            self.calculate_routes_for_all_positions()
            Ghost.calculated = True
        self.__state = Ghost.__NOT_MOVING
        self.__count = 0
        self.__dir = (0, 0)
        self.__speed = 3
    

    def calculate_routes(self, row, col):
        from engine import Engine

        start = (row, col)
        Ghost.best_moves[start] = defaultdict(lambda: None)
        Ghost.distances[start] = defaultdict(lambda: 1000000)
        q = Queue()
        q.put(start)
        dist = Ghost.distances[start]
        par = Ghost.best_moves[start]
        par[start] = start
        dist[start] = 0
        while not q.empty():
            front = q.get()
            for move in Ghost.__MOVES:
                position = (move[0] + front[0], move[1] + front[1])
                if self.valid(position) and par[position] is None:
                    par[position] = front
                    dist[position] = dist[front] + 1
                    q.put(position)

    def calculate_routes_for_all_positions(self):
        Ghost.best_moves = defaultdict(lambda: None)
        Ghost.distances = defaultdict(lambda: None)
        from engine import Engine
        for row in range(Engine.instance.rows):
            for col in range(Engine.instance.cols):
                self.calculate_routes(row, col)

    def valid(self, position):
        from engine import Engine
        return (position[0] >= 0
                and position[0] < Engine.instance.rows
                and position[1] >= 0
                and position[1] < Engine.instance.cols
                and Engine.instance.map[position[0]][position[1]] != 'Wall')

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
                if self.valid(position) and par[position] is None:
                    par[position] = front
                    q.put(position)
        raise PacmanNotFoundException     
    
    def get_optimal_dir(self, start, res, parents):
        if res == start:
            return (0, 0)
        while(parents[res] != start):
            res = parents[res]
        return (res[0] - start[0], res[1] - start[1])     

    def get_pacman_positions(self):
        from engine import Engine

        result = []
        for go in Engine.instance.get_state().go_list:
            block_pos = (go.y // Engine.instance.block_size, go.x // Engine.instance.block_size)
            if go.id() == 'Pacman':
                result.append(block_pos)
        return result

    def get_optimal_move(self, position):
        pacman_positions = self.get_pacman_positions()
        min_dist = 1000000
        min_elem = None
        for pac_pos in pacman_positions:
            if Ghost.distances[position][pac_pos] < min_dist:
                min_dist = Ghost.distances[position][pac_pos]
                min_elem = Ghost.best_moves[pac_pos][position]
        return min_elem

    def update(self):
        from engine import Engine
        if self.__state == Ghost.__MOVING:
            self.y += self.__speed * self.__dir[0]
            self.x += self.__speed * self.__dir[1]
            self.__count -= 1
            if self.__count == 0:
                self.__state = Ghost.__NOT_MOVING
        else:
            block_pos = (self.y // Engine.instance.block_size, self.x // Engine.instance.block_size)
            must_move_to = self.get_optimal_move(block_pos)
            self.__dir = (must_move_to[0] - block_pos[0], must_move_to[1] - block_pos[1])
            self.__state = Ghost.__MOVING
            self.__count = 8

    def draw(self):
        from engine import Engine
        Engine.instance.win.blit(self.sprite.sp, (self.x, self.y))
    
    def id(self):
        return 'Ghost'
    
    