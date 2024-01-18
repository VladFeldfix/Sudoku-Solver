import functions
import tkinter
from tkinter import *
from tkinter import font as tkfont
import tkinter.messagebox
import tkinter.filedialog
import os
import time
import threading
import re

class SudokuSolver:
    def __init__(self):
        self.fun = functions.functions()
        self.numbers = {}
        self.working = False
        self.original_numbers = []
        self.steps = 0
        self.thread = None
        self.setup_gui()
        #self.start()
    
    def setup_gui(self):
        # setup data
        self.fun.setup()

        # setup main window
        self.root = tkinter.Tk()
        self.root.geometry("363x399")
        self.root.minsize(363,399)
        self.root.title("Sudoku Solver v1.0")
        self.root.protocol("WM_DELETE_WINDOW", self.exit)
        self.root.iconbitmap("favicon.ico")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
        self.root.resizable(False, False)

        # draw menu
        menuFrame = Frame(self.root)
        menuFrame.grid(column=0, row=0, sticky="news")
        self.loadButton = Button(menuFrame, text="Load", command=lambda: self.load())
        self.loadButton.grid(column=0, row=0, padx=5, pady=5, sticky="nw")
        self.loadButton.config(width = 10)
        self.startButton = Button(menuFrame, text="Start", command=lambda: self.start())
        self.startButton.grid(column=1, row=0, padx=5, pady=5, sticky="nw")
        self.startButton.config(width = 10)
        self.startButton.config(state=DISABLED)
        speedBarLBL = Label(menuFrame, text="Speed:")
        speedBarLBL.grid(column=2, row=0, padx=5, pady=5, sticky="nw")
        self.speedBar = Scale(menuFrame, orient = HORIZONTAL, showvalue=0, from_=1, to=0, resolution=0.01)
        self.speedBar.set(0)
        self.speedBar.grid(column=3, row=0, padx=5, pady=5, sticky="nw")

        # draw board
        self.board = Canvas(self.root,bg='white')
        self.board.grid(column=0, row=1, padx=5, pady=5, columnspan=4, sticky="news")
        # HOR lines
        self.grid = 32
        for x in range(10):
            if x % 3 == 0:
                w = 3
            else:
                w = 1 
            self.board.create_line(self.grid,self.grid+x*self.grid,self.grid+self.grid*9,self.grid+x*self.grid, width=w)
        
        # VER lines
        for y in range(10):
            if y % 3 == 0:
                w = 3
            else:
                w = 1
            self.board.create_line(self.grid+y*self.grid,self.grid,self.grid+y*self.grid,self.grid+self.grid*9, width=w)

        self.board.create_text(46,335,text = "Steps:")
        self.number_of_steps = self.board.create_text(65,335,text = str(self.steps), anchor='w')

        # draw board
        self.draw_board()
        
        # run main loop
        self.root.mainloop()
    
    def draw_board(self):
        data = self.fun.BOARD
        
        #for k,v, in self.numbers.items():
        #    if k in self.current_board:
        #        print(self.numbers[k][1],self.current_board[k][1])
        #        if self.numbers[k][1] != self.current_board[k][1]:
        #           self.board.delete(v[0])
        #self.numbers = {}
        
        Font_Helvetica12Bold = tkfont.Font(family="Helvetica", size=12, weight="bold")
        #self.current_board = self.numbers.copy()
        self.board.delete(self.number_of_steps)
        self.number_of_steps = self.board.create_text(65,335,text = str(self.steps), anchor='w')
        for cell in data:
            x = cell.x
            y = cell.y
            allowed = cell.allowed
            if len(allowed) == 1:
                n = allowed[0]
            else:
                n = 0
            n = str(n)
            if n == "0":
                n = ""
            else:
                if not self.working:
                    self.original_numbers.append(str(x)+str(y))
            
            if str(x)+str(y) in self.original_numbers:
                color = "Black"
            else:
                color = "Red"
            #draw = True
            #if str(x)+str(y) in self.numbers:
            #    if n != self.numbers[str(x)+str(y)][1]:
            #        self.board.delete(self.numbers[str(x)+str(y)][0])
            #        draw = True
            #    else:
            #        draw = False
            #if draw:
            if str(x)+str(y) in self.numbers:
                self.board.delete(self.numbers[str(x)+str(y)])
            text = self.board.create_text(self.grid*x+self.grid/2,self.grid*y+self.grid/2, text=n, fill=color, font=Font_Helvetica12Bold)
            #else:
            #    text = None
            self.numbers[str(x)+str(y)] = text

    def exit(self):
        self.root.destroy()
        os._exit(1)
        #sys.exit()

    def load(self):
        try:
            self.thread._stop()
        except:
            pass
        file = tkinter.filedialog.askopenfile(mode ='r', filetypes =[('Text Files', '*.txt')])
        self.fun.file_location = file.name
        test = self.evaluate(file.name)
        if test:
            self.original_numbers = []
            self.working = False
            self.fun.setup()
            self.fun.load()
            self.steps = 0
            self.draw_board()
            self.startButton.config(state=NORMAL)
            #self.loadButton.config(state=DISABLED)
            #self.display_board_console()
        else:
            tkinter.messagebox.showerror("Error", "Invalid board format")
            self.loadButton.config(state=NORMAL)
            return

    def start(self):
        self.thread = threading.Thread(target=self.process)
        self.thread.daemon = True 
        self.steps = 0
        self.thread.start()
    
    def process(self):
        self.working = True
        self.startButton.config(state=DISABLED)
        self.loadButton.config(state=DISABLED)
        #self.display_board_console()
        win = False

        while not win:
            self.steps += 1
            #self.root.update_idletasks()
            sleep_for = self.speedBar.get()
            time.sleep(sleep_for)
            self.draw_board()
            #input(">")
            #self.display_board_console()
            self.fun.clear()
            result = self.fun.evaluate()
            if result == "BAD":
                #print(" - BAD")
                self.fun.goback()
                if self.fun.dead:
                    tkinter.messagebox.showerror("Error", "This Sudoku is impossible")
                    self.loadButton.config(state=NORMAL)
                    return
                while self.fun.move() == "GOBACK":
                    self.fun.goback()
            elif result == "OK":
                #print(" - OK")
                self.fun.N = 0
                self.fun.move()
            elif result == "WIN":
                #print(" - WIN")
                win = True
        self.win()
 
    
    def evaluate(self, file):
        result = True
        data = open(file, 'r')
        lines = data.readlines()
        data.close()

        data = []
        for line in lines:
            line = re.sub("[^0-9]", "", line)
            if line != "":
                data.append(line)
        if len(data) != 9:
            result = False
        allzeros = True
        for line in data:
            if len(line) != 9:
                result = False
            for x in line:
                if x != "0":
                    allzeros = False
        if allzeros:
            result = False
        return result

    def win(self):
        #self.display_board_console()
        self.draw_board()
        self.loadButton.config(state=NORMAL)

    def display_board_console(self):
        result = "---1-----------2-----------3-----------|-4-----------5-----------6-----------|-7-----------8-----------9------------ \n1. "
        row = 0
        l = 2
        for cell in self.fun.BOARD:
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
        print(result)
    
    def display_allowed_list(self, cell):
            display_cell = "["
            for i in range(1,10):
                if i in cell.allowed:
                    display_cell += str(i)
                else:
                    display_cell += "_"
            display_cell += "] "
            return display_cell


SudokuSolver()