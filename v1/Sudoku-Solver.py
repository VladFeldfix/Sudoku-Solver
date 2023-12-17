class main:
    def __init__(self):
        # set up board
        self.board = []
        for row in range(1,10):
            for col in range(1,10):
                self.board.append(node(row,col,sec))
class node:
    def __init__(self, x, y, sec):
        self.x = x
        self.y = y
        self.sec = sec
        self.allowed = [1,2,3,4,5,6,7,8,9]
main()