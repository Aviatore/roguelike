class Printer:
    def __init__(self, all_boards, curses):
        self.all_boards = all_boards
        self.Board = self.all_boards.current_board
        self.screen = self.Board.screen
        self.__OFFSET = 2
        self.curses = curses
        self.colors = {}
        self.hero = None
    
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
        self.screen.addstr(0, 2, money_stat)
    
    def print_hero_inventory(self):
        pass