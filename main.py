import curses
import engine
import ui
import time


def main(screen):
    screen.clear()
    curses.curs_set(False)
    
    all_boards = engine.Boards()
    
    board1 = engine.Board('b1', 20, 40, screen)
    board1.create_board(b2=[0, 6], b3=[12,39])
    
    board2 = engine.Board('b2', 10, 80, screen)
    board2.create_board(b1=[9,4], b3=[5,79])
    
    board3 = engine.Board('b3', 30, 10, screen)
    board3.create_board(b1=[25,0], b2=[5,0])
    
    all_boards.add_board(board1)
    all_boards.add_board(board2)
    all_boards.add_board(board3)
    
    all_boards.set_current_board('b1')
    
    printer = ui.Printer(all_boards)
    
    all_objects = engine.AllObjects()
    
    objects1 = engine.Objects('b1', board1, printer)

    food = engine.Food(all_boards, printer)
    food.create_random()
    food.object_random_position()
    food.put_on_board()
    objects1.add_object(food)
    
    orc = engine.Orc(all_boards, printer)
    orc.create_random()
    orc.object_random_position()
    orc.put_on_board()
    objects1.add_object(orc)
    
    objects2 = engine.Objects('b2', board2, printer)
    objects3 = engine.Objects('b3', board3, printer)
    
    all_objects.add_objects('b1', objects1)
    all_objects.add_objects('b2', objects2)
    all_objects.add_objects('b3', objects3)
    
    all_objects.set_current_objects('b1')
    
    hero = engine.Hero('fighter', all_boards, all_objects, printer)
    sword = engine.Weapon('sword', dmg=30)
    hero.Inventory.put_on_weapon(sword)
    hero.set_hp(100)
    hero.object_random_position()
    hero.put_on_board()
    
    loop = True
    
    while loop:
        user_input = screen.getch()
        
        if user_input == curses.KEY_UP:
            hero.move("up")
        elif user_input == curses.KEY_DOWN:
            hero.move("down")
        elif user_input == curses.KEY_LEFT:
            hero.move("left")
        elif user_input == curses.KEY_RIGHT:
            hero.move("right")
    
        printer.print_board()
        
        screen.refresh()
        
        curses.flushinp()
        
        time.sleep(0.1)
    

def main3(screen):
    screen.clear()
    curses.curs_set(False)
    
    board = engine.Board(20, 40, screen)
    board.create_board([[0, 6], [12, 39]])
    
    printer = ui.Printer(board)
    
    objects = engine.Objects(board, printer)
    
    food = engine.Food(board)
    food.create_random()
    food.object_random_position()
    food.put_on_board()
    objects.add_object(food)
    
    orc = engine.Orc(board)
    orc.create_random()
    orc.object_random_position()
    orc.put_on_board()
    objects.add_object(orc)
    
    hero = engine.Hero('fighter', board, objects)
    sword = engine.Weapon('sword', dmg=30)
    hero.Inventory.put_on_weapon(sword)
    hero.set_hp(100)
    hero.object_random_position()
    hero.put_on_board()
    
    
    
    loop = True
    
    while loop:
        user_input = screen.getch()
        
        if user_input == curses.KEY_UP:
            hero.move("up")
        elif user_input == curses.KEY_DOWN:
            hero.move("down")
        elif user_input == curses.KEY_LEFT:
            hero.move("left")
        elif user_input == curses.KEY_RIGHT:
            hero.move("right")
    
        printer.print_board()
        
        screen.refresh()
        
        curses.flushinp()
        
        time.sleep(0.1)

def main2(stdscr):
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