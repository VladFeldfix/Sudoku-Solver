class main:
    def __init__(self):
        # global vars
        self.board = []
        
        # actions
        self.setup()
        self.read()
        self.current_state = ""
        for x in range(10):
            self.solve()
            self.display()
    
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
        
        #self.display()
    
    def solve(self):
        # clear what is not allowed
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
        
        
    
    def display(self):
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
        print(lines)
        if self.current_state != lines:
            self.current_state = lines
            print("state update")
        print("*"*150)

class node:
    def __init__(self, x, y, sec):
        self.x = x
        self.y = y
        self.sec = sec
        self.allowed = ["1","2","3","4","5","6","7","8","9"]
main()