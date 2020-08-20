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
        self.ver_offset = 4
        self.row = self.Board.height + self.ver_offset
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
        self.row = self.Board.height + self.ver_offset
    
    def hp_stat_calc(self, ver_offset, hor_offset):
        hp_green = 7
        hp_orange = 4
        
        hp_percent = int((self.hero.hp * 10) // self.hero.max_hp)
        hp_percent_txt = "|" * hp_percent
        
        hp_remain = 10 - hp_percent
        
        
        if hp_percent <= 4:
            self.screen.addstr(ver_offset, hor_offset, hp_percent_txt, self.curses.color_pair(6))
            return hp_percent, hp_remain
        elif hp_percent <= 7:
            self.screen.addstr(ver_offset, hor_offset, hp_percent_txt, self.curses.color_pair(7))
            return hp_percent, hp_remain
        else:
            self.screen.addstr(ver_offset, hor_offset, hp_percent_txt, self.curses.color_pair(5))
            return hp_percent, hp_remain
    
    def print_hero_stats(self):
        """The function prints the hero statistics, e.g. HP, Mana, Stamina, on the board's right-hand-side."""
        HOR_OFFSET = 2
        VER_OFFSET = 0
        hp_label = "HP: "
        
        self.screen.addstr(VER_OFFSET, HOR_OFFSET, " "*self.Board.width)
        money_stat = f"Money: {self.hero.Backpack.money} coins"
        
        self.screen.addstr(VER_OFFSET, HOR_OFFSET, hp_label)
        hp_percent, hp_remain = self.hp_stat_calc(VER_OFFSET, HOR_OFFSET + len(hp_label))
        hp_remain_txt = "|" * hp_remain
        
        offset_sum = HOR_OFFSET + len(hp_label) + hp_percent
        self.screen.addstr(VER_OFFSET, offset_sum, hp_remain_txt)
        
        offset_sum += hp_remain + 4
        
        msg = f"Lvl: {self.hero.lvl}  Drunk: {self.hero.drunk}%  Map: m   Inventory: i   Stats: s"
        self.screen.addstr(VER_OFFSET, offset_sum, msg)
        
        self.lower_stat_printer()
        
        # msg = f"Coins: {self.hero.Backpack.money}   Cans: {self.hero.Backpack.recycles['Can']}   Bottles: {self.hero.Backpack.recycles['Bottle']}"
        # self.screen.addstr(0, 2, msg)
        
    def lower_stat_printer(self):
        self.update_board()
        
        row = self.Board.height + 2
        col = 2
        
        msg = f"Coins: {self.hero.Backpack.money}   Cans: {self.hero.Backpack.recycles['Can']}   Bottles: {self.hero.Backpack.recycles['Bottle']}"
        self.screen.addstr(row, col, msg)
        
    
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
        self.update_board()
        self.clear_screen()
        self.print_hero_stats()