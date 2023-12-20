class Sudoku_Solver:
    def __init__(self):
        # global variables
        self.board = [] # a list of node objects

        # go
        self.set_board()
    
    def set_board(self):
        # setup an empty board
        sec = 0
        i = 1
        j = 0
        for row in range(1,10):
            for col in range(1,10):
                sec = i+j
                self.board.append(Node(row,col,sec))
                if col % 3 == 0:
                    i += 1
            i = 1
            if row % 3 == 0:
                j += 3
        
        # load
        self.load_from_file()

    def load_from_file(self):
        self.clear()

    def clear(self):
        result = None

        if result == "OK":
            self.save()
        
        if result == "BAD":
            self.go_back()
        
        if result == "WIN":
            self.win()

    def save(self):
        self.move()

    def move(self):
        can_move = True

        if can_move:
            self.clear()
        else:
            self.go_back()

    def go_back(self):
        self.move()

    def win(self):
        print(self.draw_board())
    
    def draw_board(self):
        board = ""
        return board