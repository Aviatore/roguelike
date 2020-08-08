import curses
import engine
import ui
import time
import boards


def main(screen):
    screen.clear()
    curses.curs_set(False)
    curses.use_default_colors()
    curses.init_pair(1, 39, 21) # WATER_COLOR_PAIR
    curses.init_pair(2, 76, -1) # TREE_COLOR_PAIR
    curses.init_pair(3, 247, 15) # ROCK_COLOR_PAIR
    color_pairs = [
        ['~', 1],
        ['Y', 2],
        ['T', 2],
        ['#', 3],
        ['[', 3],
        [']', 3]
    ]
    
    all_boards = engine.Boards()
    
    board1 = engine.Board('b1', screen, 20, 40)
    board1.create_board(b2=[0, 6], b3=[12,39], b4=[19,10])
    
    board2 = engine.Board('b2', screen, 10, 50)
    board2.create_board(b1=[9,4], b3=[5,49])
    
    board3 = engine.Board('b3', screen, 30, 10)
    board3.create_board(b1=[25,0], b2=[5,0])
    
    board4 = engine.Board('b4', screen)
    board4.create_board_template(boards.board_5, ['b1'])
    
    all_boards.add_board(board1)
    all_boards.add_board(board2)
    all_boards.add_board(board3)
    all_boards.add_board(board4)
    
    all_boards.set_current_board('b1')
    
    printer = ui.Printer(all_boards, curses)
    printer.add_colors(color_pairs)
    
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
    objects4 = engine.Objects('b4', board4, printer)
    
    all_objects.add_objects('b1', objects1)
    all_objects.add_objects('b2', objects2)
    all_objects.add_objects('b3', objects3)
    all_objects.add_objects('b4', objects4)
    
    all_objects.set_current_objects('b1')
    
    hero = engine.Hero('fighter', all_boards, all_objects, printer)
    sword = engine.Weapon('sword', dmg=30)
    hero.Inventory.put_on_weapon(sword)
    hero.set_hp(100)
    hero.object_random_position()
    hero.put_on_board()
    printer.print_board()
    screen.refresh()
    
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
    

if __name__ == "__main__":
    curses.wrapper(main)