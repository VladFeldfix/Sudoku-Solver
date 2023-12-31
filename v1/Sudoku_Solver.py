class Sudoku_Solver:
    def __init__(self):
        # global variables
        self.board = [] # a list of node objects
        self.states = [] # a list of saved board states
        self.selected_node = None # the currently selected node
        self.N = -1 # the index of the allwed list of the 
        
        # go
        self.set_board()
    
    def set_board(self):
        print("Set board")
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
        print("Load from file")
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

        self.clear()

    def clear(self):
        print("Clear")
        go_again = True
        current_state = ""
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
                    tmp = self.draw_table()
                    if current_state != tmp:
                        current_state = tmp
                        go_again = True

        result = "WIN"
        for node in self.board:
            if len(node.allowed) > 1 :
                result = "OK"
            if len(node.allowed) == 0 :
                result = "BAD"
                break
        print(self.draw_table())
        print(" - "+result)
        if result == "OK":
            self.save()
        
        if result == "BAD":
            self.go_back()
        
        if result == "WIN":
            self.win()

    def save(self):
        if self.selected_node != None:
            print("Save: "+str(self.selected_node.x)+", "+str(self.selected_node.y)+", "+str(self.N))
        else:
            print("Save: No node selected, "+str(self.N))
        self.states.append([self.board.copy(), self.selected_node, self.N])
        self.N = -1
        self.selected_node = None
        self.move()

    def move(self):
        print("Move")
        # raise N
        self.N += 1
        
        # if there is no selected node
        if self.selected_node == None:
            # select the smallest allowed list
            smallest_allowed_list = 9
            self.selected_node = None
            for node in self.board:
                if len(node.allowed) < smallest_allowed_list and len(node.allowed) > 1:
                    smallest_allowed_list = len(node.allowed)
                    self.selected_node = node
                    print("Select node: ("+str(self.selected_node.x)+","+str(self.selected_node.y)+") "+str(self.selected_node.allowed)+"  N="+str(self.N))
        
        # set the number of the selected node
        if self.N < len(self.selected_node.allowed):
            self.selected_node.allowed = [self.selected_node.allowed[self.N]]
            can_move = True
        else:
            can_move = False

        if self.selected_node != None:
            print("Selected node: ("+str(self.selected_node.x)+","+str(self.selected_node.y)+") Number: "+str(self.selected_node.allowed)+"  N="+str(self.N))

        # determine if can move
        if can_move:
            print("Can move")
            input(">")
            self.clear()
        else:
            print("Can't move")
            input(">")
            self.go_back()

    def go_back(self):
        print("Go back to this")
        print(self.draw_table())
        self.board = self.states[-2][0]
        self.selected_node = self.states[-2][1]
        self.N = self.states[-2][2]
        self.states = self.states[:-2]
        self.move()

    def win(self):
        print(self.draw_board())

    def draw_table(self):
        lines = "   1          2          3          |  4          5          6          |  7          8          9\n"
        col = 1
        row = 1
        delimiter = False
        lines += str(row)+". "
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
                lines += "\n"+str(row+1)+". "
                col = 1
                row += 1
                delimiter = False
            if col == 4 or col == 7:
                lines += "|  "
            if not delimiter:
                if row == 4 or row == 7:
                    lines = lines[:-3]
                    lines += "-"*106+"\n"+str(row)+". "
                    delimiter = True
        lines = lines[:-4]
        return lines

class Node:
    def __init__(self, x, y, sec):
        self.x = x
        self.y = y
        self.sec = sec
        self.allowed = ["1","2","3","4","5","6","7","8","9"]

Sudoku_Solver()