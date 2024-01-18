import re
class functions:
    def __init__(self):
        # global variables
        self.BOARD = []
        self.MEMORY = []
        self.N = 0
        self.dead = False
        self.file_location = None

        # start
        #self.start()

    def start(self):
        self.setup()
        self.load()
        win = False

        while not win:
            self.clear()
            result = self.evaluate()
            if result == "BAD":
                #print(" - BAD")
                self.goback()
                while self.move() == "GOBACK":
                    self.goback()
            elif result == "OK":
                #print(" - OK")
                self.N = 0
                self.move()
            elif result == "WIN":
                #print(" - WIN")
                win = True
        self.win()
    
    def setup(self):
        #print("SETUP")
        self.BOARD = []
        self.MEMORY = []
        self.N = 0
        self.dead = False
        sec = 1
        secc = 0
        x = 1
        y = 1
        for row in range(1,82):
            self.BOARD.append(node(x,y,sec+secc))
            x += 1
            if row % 9 == 0:
                y += 1
                x = 1
                sec = 0
            if row % 27 == 0:
                secc += 3
            if row % 3 == 0:
                sec += 1
        #self.display_board()
        #self.load()
    
    def load(self):
        #print("LOAD")      
        # load data from file
        file = open(self.file_location)
        lines = file.readlines()
        file.close()

        # load data onto board
        i = 0
        for line in lines:
            line = re.sub("[^0-9]", "", line)
            for number in line:
                number = int(number)
                if number != 0:
                    self.BOARD[i].allowed = [number]
                i += 1
        
        # display the board and call next function
        #self.display_board()
        #self.clear()

    def clear(self):
        #print("CLEAR")
        
        changed = True
        while changed:
            changed = False
            for cell in self.BOARD:
                if len(cell.allowed) == 1:
                    for other in self.BOARD:
                        if not cell is other:
                            if other.x == cell.x or other.y == cell.y or other.sec == cell.sec:
                                if cell.allowed[0] in other.allowed:
                                    other.allowed.remove(cell.allowed[0])
                                    changed = True

        # display the board and call next function
        #self.display_board()
        #self.evaluate()

    def evaluate(self):
        #print("EVALUATE")

        result = "WIN"
        for cell in self.BOARD:
            if len(cell.allowed) == 0:
                result = "BAD"
            if len(cell.allowed) > 1:
                if result != "BAD":
                    result = "OK"
        return result
        """
        if result == "BAD":
            #print(" - BAD")
            self.goback()
        elif result == "OK":
            #print(" - OK")
            self.N = 0
            self.move()
        elif result == "WIN":
            #print(" - WIN")
            self.win()
        """

    def goback(self):
        #print("GO BACK")
        # load saved board
        if len(self.MEMORY) > 0:
            loaded_data = self.MEMORY.pop()
            loaded_board_x = loaded_data[0]
            loaded_board_y = loaded_data[1]
            self.N = loaded_data[2]
            loaded_board_data = loaded_data[3]
        else:
            #print(" - ERROR! THIS SUDOKU IS NOT POSSIBLE")
            self.dead = True
            return
        # insert saved data
        i = 0
        for cell in self.BOARD:
            cell.allowed = loaded_board_data[i]
            i += 1
        
        #print(" - GO BACK TO: ("+str(loaded_board_x)+","+str(loaded_board_y)+") N = "+str(self.N))
        self.N += 1
        #print(" - DO N += 1")
        #self.display_board()
        #self.move()

    def move(self):
        #print("MOVE")
        #input("MOVE >")

        # select the cell with the smallest allowed list
        shortest_list = 9
        selected_cell = None
        for cell in self.BOARD:
            if len(cell.allowed) < shortest_list:
                if len(cell.allowed) > 1:
                    shortest_list = len(cell.allowed)
                    selected_cell = cell
        #display_cell = self.display_allowed_list(selected_cell)
        #print(" - SELECT CELL: ("+str(selected_cell.x)+","+str(selected_cell.y)+") "+display_cell+" N = "+str(self.N))
        
        # remove the n'th element
        if len(selected_cell.allowed) > self.N:
            # save
            self.save(selected_cell.x,selected_cell.y,self.N)
            # move
            selected_cell.allowed = [selected_cell.allowed[self.N]]
        else:
            #self.goback()
            return "GOBACK"
        #print(" - PLACE: "+str(selected_cell.allowed[0])+" (N = "+str(self.N)+")")
        #print(" - SAVE MOVE: ["+str(selected_cell.x)+","+str(selected_cell.y)+"] "+str(self.N))
        return "CLEAR"
        #self.clear()
    
    def save(self, x, y, n):
        board_before_the_move = []
        for cell in self.BOARD:
            board_before_the_move.append(cell.allowed.copy())
        self.MEMORY.append((x,y,n,board_before_the_move))

    def display_board(self):
        result = "---1-----------2-----------3-----------|-4-----------5-----------6-----------|-7-----------8-----------9------------ \n1. "
        row = 0
        l = 2
        for cell in self.BOARD:
            br = ""
            sp = ""
            line = ""
            row += 1
            if row % 3 == 0:
                sp = "| "
            if row % 9 == 0:
                br = "\n"+str(l)+". "
                l += 1
            if row % 27 == 0:
                l -= 1
                line = "-"*116+"\n"+str(l)+". "
                br = "\n"
                l += 1
            display_cell = self.display_allowed_list(cell)
            #result += "("+str(cell.x)+","+str(cell.y)+")"+str(cell.sec)+display_cell+sp+br+line
            result += display_cell+sp+br+line
        result = result[:-5]
        #print(result)
    
    def display_allowed_list(self, cell):
            display_cell = "["
            for i in range(1,10):
                if i in cell.allowed:
                    display_cell += str(i)
                else:
                    display_cell += "_"
            display_cell += "] "
            return display_cell

class node:
    def __init__(self,row,col,sec):    
        self.x = row
        self.y = col
        self.sec = sec
        self.allowed = [1,2,3,4,5,6,7,8,9]

