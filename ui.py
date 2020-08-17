class Printer:
    def __init__(self, all_boards, curses):
        self.all_boards = all_boards
        self.Board = self.all_boards.current_board
        self.screen = self.Board.screen
        self.__OFFSET = 2
        self.curses = curses
        self.colors = {}
        self.hero = None
        self.msg = ""
        self.row = self.Board.height + 3
        self.current_row = self.row
        self.col = 5
        self.current_col = self.col
        
    
    def add_hero(self, hero):
        self.hero = hero

    def add_colors(self, colors): # np. [['~',1],['Y',2],['T',2]]
        for color_pair in colors:
            self.colors[color_pair[0]] = color_pair[1]
    
    def clear_screen(self):
        self.screen.clear()
            
        self.print_board()
        self.screen.refresh()
        
    def print_board(self):        
        for row_index in range(self.Board.height):
            for col_index in range(self.Board.width):
                mark = self.Board.board[row_index][col_index]
                
                if mark in self.colors.keys():
                    self.screen.addstr(row_index + self.__OFFSET, col_index + self.__OFFSET, mark, self.curses.color_pair(self.colors[mark]))
                else:
                    self.screen.addch(row_index + self.__OFFSET, col_index + self.__OFFSET, mark)
        
        self.screen.refresh()
    
    def print_line(self, row, col, msg):
        self.screen.addstr(row, col, msg)
        self.screen.refresh()
    
    def update_board(self):
        self.Board = self.all_boards.current_board
        
    def print_hero_stats(self):
        """The function prints the hero statistics, e.g. HP, Mana, Stamina, on the board's right-hand-side."""
        money_stat = f"Money: {self.hero.Backpack.money} coins"
        msg = f"Coins: {self.hero.Backpack.money}   Cans: {self.hero.Backpack.recycles['Can']}   Bottles: {self.hero.Backpack.recycles['Bottle']}"
        self.screen.addstr(0, 2, msg)
    
    def print_hero_inventory(self):
        pass
    
    def msgBox_print_line(self, msg):
        self.screen.addstr(self.current_row, self.current_col, msg)
        self.current_row += 1
    
    def msgBox_print_line_cached(self):
        self.screen.addstr(self.current_row, self.current_col, self.msg)
        self.msgBox_reset_line()
        self.msg = ""
        
    
    def msgBox_reset_line(self):
        self.current_row = self.row
        self.current_col = self.col
    
    def refresh(self):
        self.screen.refresh()
    
    def msgBox_clear(self):
        self.clear_screen()
        self.print_hero_stats()