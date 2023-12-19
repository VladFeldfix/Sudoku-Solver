
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