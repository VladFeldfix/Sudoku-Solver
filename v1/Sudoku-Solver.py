class Sudoku_Solver:
    def __init__(self):
        # global variables
        self.board = [] # this is a list of nodes objects where each node is a cell with x, y, sec, list of allowed numbers

        # take actions
        self.read_from_file()
        self.setup()
        self.start()

    def read_from_file():
        # load a map file
        pass

    def setup(self):
        # setup the playing board
        pass

    def start(self):
        # start solving the sudoku
        # step 1: remove all imposible numbers
        # step 2: evaluate if game over, if yes goto finish, else goto step 3
        # step 3: evaluate if there is an empty allowed list, if yes goto step 4
        # step 4: evaluate if no change has been made to the board before and after step 1, if no change has been 
        # step 4: go back to last saved game state before the error
        # step 5: set the next value of n [0 and up]
        # step 6: find the smallest allowed list and select the n'th element to try see if that is the right element
        # step 7: save the current state of the board
        # step 8: goto step 1
        pass
    
    def finish(self):
        # display the result
        pass

class node:
    def __init__(self, x, y, sec):
        self.x = x
        self.y = y
        self.sec = sec
        self.allowed = ["1","2","3","4","5","6","7","8","9"]





class main:
    def __init__(self):
        # global vars
        self.board = []
        self.current_state = ""
        self.saved_states = []
        
        # actions
        self.setup()
        self.read()
        self.start()
    
    def setup(self):
        # set up board
        sec = 0
        i = 1
        j = 0
        for row in range(1,10):
            for col in range(1,10):
                sec = i+j
                self.board.append(node(row,col,sec))
                if col % 3 == 0:
                    i += 1
            i = 1
            if row % 3 == 0:
                j += 3
    
    def read(self):
        # get data from file
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
    
    def start(self):
        print(self.create_visual_table())
        print("*****************************************************")
        # clear what is not allowed
        while self.go_again():
            for node in self.board:
                if len(node.allowed) == 1:
                    # hor
                    for n in self.board:
                        if n.x == node.x and n.y != node.y:
                            if node.allowed[0] in n.allowed:
                                n.allowed.remove(node.allowed[0])
                        if n.y == node.y and n.x != node.x:
                            if node.allowed[0] in n.allowed:
                                n.allowed.remove(node.allowed[0])
                        if n.sec == node.sec and n.x != node.x and n.y != node.y:
                            if node.allowed[0] in n.allowed:
                                n.allowed.remove(node.allowed[0])
        if self.complete():
            self.finish()
        else:
            # if i am here it means that I can't continue so i should start guessing
            # save the game state as it is to be able to returned
            # find the smallest allowed list and remove one elemnt (remember removed element )
            # 
            """
            # save the game state as it is to be able to return
            tmp = self.board.copy()
            self.saved_states.append(tmp)

            # find the smallest allowed list
            smallest = 9
            smallest_node = ""
            for n in self.board:
                if len(n.allowed) > 1:
                    if len(n.allowed) < smallest:
                        smallest = len(n.allowed)
                        smallest_node = n

            # from the smallest node remove one of the options
            smallest_node = [smallest_node.allowed.pop()]
            # test for errors
            for n in self.board:
                if len(n.allowed) == 0:
                    self.board = self.saved_states.pop()
            # go again
            self.start()
            """

    def go_again(self):
        # determine if the sudoku is solved, if not, solve again
        for n in self.board:
            if len(n.allowed) > 1:
                current_state = self.create_visual_table()
                if self.current_state != current_state:
                    self.current_state = current_state
                    return True
        return False
    
    def create_visual_table(self):
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
    
    def complete(self):
        for n in self.board:
            if len(n.allowed) > 1:
                return False
        return True

    def finish(self):
        current_state = self.create_visual_table()
        current_state = current_state.replace("_", "")
        print(current_state)

class node:
    def __init__(self, x, y, sec):
        self.x = x
        self.y = y
        self.sec = sec
        self.allowed = ["1","2","3","4","5","6","7","8","9"]
main()