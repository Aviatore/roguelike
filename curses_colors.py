import curses

def main(screen):
    # curses.start_color()
    curses.use_default_colors()
    screen.addstr("Curses' default colors:\n\n")
    
    
    for i in range(1, curses.COLORS):
        curses.init_pair(i, i, -1) # -1 means no background
    try:
        for i in range(1, curses.COLORS):
            screen.addstr(str(f"{i} "), curses.color_pair(i))
    except curses.ERR:
        pass
    
    screen.getch()

curses.wrapper(main)