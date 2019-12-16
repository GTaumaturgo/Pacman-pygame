class State():
    def __init__(self):
        self.go_list = []

    def add_go(self, go):
        self.go_list.append(go)
    
    def update(self):
        for go in self.go_list :
            go.update()
    def draw(self):
        for go in self.go_list:
            go.draw()