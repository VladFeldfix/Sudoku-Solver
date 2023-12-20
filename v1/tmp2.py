class Sudoku_Solver:
    def __init__(self):
        # global variables
        self.board = [] # a list of node objects
        self.states = [] # a list of copies of self.board in various states
        self.current_state = None # the current state of the board
        self.selelcted_node = None # the currently selected node for testing
        self.N = -1 # the currently selected element of the allowed list for the currently selected node

        # start
        self.set_stone_numbers()

    def set_stone_numbers(self):
        """
        Stone numbers are the numbers who cannot be changed because they are given
        Along side stone numbers, we get stone allowed lists
        So for example if the coordinates [x,y] has a stone number n -> all allowed lists effected by that cannot be changed
        """
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

        # load data from file
        file = open("board.txt")
        lines = file.readlines()
        file.close()

        # insert data to board
        i = 0
        for line in lines:
            line = line.replace("\n", "")
            line = line.replace("\t", "")
            line = line.replace(" ", "")
            line = line.split(",")
            for ch in line:
                if ch != "0":
                    self.board[i].allowed = [ch]
                i += 1
        
        # setup stone allowed lists
        self.clear()

        # save the current state
        self.save_state()
    
    def clear(self):
        go_again = True
        while go_again:
            for node in self.board:
                if len(node.allowed) == 1:
                    for n in self.board:
                        # eliminate all non allowed HOR
                        if n.x == node.x and n.y != node.y:
                            if node.allowed[0] in n.allowed:
                                n.allowed.remove(node.allowed[0])
                        
                        # eliminate all non allowed VER
                        if n.y == node.y and n.x != node.x:
                            if node.allowed[0] in n.allowed:
                                n.allowed.remove(node.allowed[0])
                        
                        # eliminate all non allowed SEC
                        if n.sec == node.sec and n.x != node.x and n.y != node.y:
                            if node.allowed[0] in n.allowed:
                                n.allowed.remove(node.allowed[0])
            go_again = False
            for n in self.board:
                if len(n.allowed) > 1:
                    current_state = self.draw_table()
                    if self.current_state != current_state:
                        self.current_state = current_state
                        go_again = True

    def save_state(self):
        """
        Save the current satate of the board to be able to go back to it later
        """
        tmp = self.board.copy()
        self.states.append(tmp)

        # now go take the first step
        self.can_a_move_be_made()

    def can_a_move_be_made(self):
        """
        Eavluate if a move can be made or not based on how many options have been tried
        """
        can = True
        self.N += 1
        if self.selelcted_node != None:
            if self.N > len(self.selelcted_node.allowed):
                can = False
        
        if can:
            self.make_a_move()
        else:
            self.go_back_a_state()

    def make_a_move(self):
        """
        Make a possible move
        """

        if self.selelcted_node == None:
            # select the smallest node
            smallest_allowed_list = 9
            for node in self.board:
                if len(node.allowed) < smallest_allowed_list and len(node.allowed) > 1:
                    smallest_allowed_list = len(node.allowed)
                    self.selected_node = node
        else:
            # select the next node
            self.selelcted_node.allowed = [self.selelcted_node.allowed[self.N]]

        self.evaluate_a_move()
    
    def evaluate_a_move(self):
        # Evaluate the state of the board after the move
        # OK move means that there are no empty allowed lists after the move
        # BAD move means that there is at least one empty allowed list so the move should
        self.clear()
        print(self.draw_table())

        move = "WIN"
        for node in self.board:
            if len(node.allowed) > 1:
                move = "OK"
            if len(node.allowed) == 0:
                move = "BAD"

        if move == "OK":
            input(">")
            self.save_state()
        elif move == "BAD":
            input(">")
            self.go_back_a_state()
        elif move == "WIN":
            self.win()

    def go_back_a_state(self):
        self.selelcted_node = None
        self.N = -1
        
        self.can_a_move_be_made()
    
    def win(self):
        print(self.draw_table())

    def draw_table(self):
        lines = ""
        col = 1
        row = 1
        delimiter = False
        for n in self.board:
            #lines += str(n.sec)+"."
            for i in range(1,10):
                i = str(i)
                if i in n.allowed:
                    lines += i
                else:
                    lines += "_"
            col += 1
            lines += "  "
            if col == 10:
                lines += "\n"
                col = 1
                row += 1
                delimiter = False
            if col == 4 or col == 7:
                lines += "|  "
            if not delimiter:
                if row == 4 or row == 7:
                    lines += "-"*103+"\n"
                    delimiter = True
        return lines

class Node:
    def __init__(self, x, y, sec):
        self.x = x
        self.y = y
        self.sec = sec
        self.allowed = ["1","2","3","4","5","6","7","8","9"]

Sudoku_Solver()