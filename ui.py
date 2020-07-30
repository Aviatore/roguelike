def print_board(board, stdscr):
    BOARD_HEIGHT = len(board)
    BOARD_WIDTH = len(board[0])
    OFFSET = 2
    
    for row_index in range(BOARD_HEIGHT):
        for col_index in range(BOARD_WIDTH):
            stdscr.addch(row_index + OFFSET, col_index + OFFSET, board[row_index][col_index])
            

def clear_msgbox(board, stdscr):
    stdscr.clear()
    print_board(board, stdscr)
    stdscr.refresh()


def print_hero_stats():
    """The function prints the hero statistics, e.g. HP, Mana, Stamina, on the board right-hand-side."""
    pass