class Printer:
    def __init__(self, screen, Board):
        self.screen = screen
        self.Board = Board
        self.__OFFSET = 2
    
    def clear_screen(self):
        self.screen.clear()
        self.print_board()
        self.screen.refresh()
        
    def print_board(self):        
        for row_index in range(self.Board.height):
            for col_index in range(self.Board.width):
                self.screen.addch(row_index + self.__OFFSET, col_index + self.__OFFSET, self.Board.board[row_index][col_index])
        
        self.screen.refresh()
    
    def print_line(self, row, col, msg):
        self.screen.addstr(row, col, msg)
        self.screen.refresh()
        


def print_hero_stats():
    """The function prints the hero statistics, e.g. HP, Mana, Stamina, on the board right-hand-side."""
    pass