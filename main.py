import curses
import engine
import ui
import time


def main(stdscr):
    stdscr.clear()
    
    curses.curs_set(False)
    
    msgbox = [0]
    objects = []
    objects_persons = []
    
    board = engine.create_board(20, 40)
    
    objects.append(engine.object_food_create(board))
    objects.append(engine.object_person_create(board))
    
    hero = engine.object_hero_create(board)

    loop = True
    
    while loop:
        user_input = stdscr.getch()
        
        if user_input == curses.KEY_UP:
            engine.move_hero(board, hero, "up", objects, stdscr, msgbox)
        elif user_input == curses.KEY_DOWN:
            engine.move_hero(board, hero, "down", objects, stdscr, msgbox)
        elif user_input == curses.KEY_LEFT:
            engine.move_hero(board, hero, "left", objects, stdscr, msgbox)
        elif user_input == curses.KEY_RIGHT:
            engine.move_hero(board, hero, "right", objects, stdscr, msgbox)

        engine.move_objects(board, objects, hero, stdscr, msgbox)
        
        if msgbox[0] > 1:
            msgbox[0] -= 1
        elif msgbox[0] == 1:
            stdscr.clear()
            msgbox[0] -= 1
        
        ui.print_board(board, stdscr)
        
        stdscr.refresh()
        
        curses.flushinp()
        
        time.sleep(0.1)
        
    
if __name__ == "__main__":
    curses.wrapper(main)